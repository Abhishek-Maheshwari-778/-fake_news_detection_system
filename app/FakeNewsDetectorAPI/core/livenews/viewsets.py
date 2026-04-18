from rest_framework.response import Response
from rest_framework import viewsets, generics
from rest_framework import status

import requests

from bs4 import BeautifulSoup

from .models import LiveNews
from .serializers import LiveNewsSerializer, LiveNewsDetailedSerializer
from core.model import load_models

import threading
import time

def get_new_news_from_api_and_update():
    """Gets news from the guardian news using it's API"""
    try:
        # Using NewsAPI.org for primary Indian headlines (User should replace YOUR_API_KEY)
        # Fallback to a query that targets Indian news if the key is default
        api_url = "https://newsapi.org/v2/top-headlines?country=in&apiKey=YOUR_API_KEY_HERE"
        # Since I don't have a key, I'll simulate or use a more open source if possible.
        # For now, I'll update the Guardian query to target 'India' results as a workaround 
        # OR better: use an Indian news specific RSS feed
        response = requests.get("https://content.guardianapis.com/search?q=India&api-key=e705adff-ca49-414e-89e2-7edede919e2e", timeout=10)
        if response.status_code != 200:
            print(f"Error fetching news: Received status code {response.status_code}")
            return
        
        news_data = response.json()
        
        if "response" not in news_data or "results" not in news_data["response"]:
            print("Error: 'response' or 'results' not found in API response")
            return

        results = news_data["response"]["results"]
        if not results:
            print("No new news found in API response")
            return

        news_titles = [article.get("webTitle", "No Title") for article in results]
        news_publication_dates = [article.get("webPublicationDate", "") for article in results]
        news_categories = []

        for article in results:
            try:
                news_categories.append(article.get("pillarName", "Undefined"))
            except KeyError:
                news_categories.append("Undefined")
        
        section_id = [article.get("sectionId", "unknown") for article in results]
        section_name = [article.get("sectionName", "General") for article in results]
        type_list = [article.get("type", "article") for article in results]
        web_url = [article.get("webUrl", "#") for article in results]
    except Exception as e:
        print(f"Exception during news fetch: {e}")
        return

    nb_model, vect_model = load_models()

    def scrap_img_from_web(url):
        print(url)
        r = requests.get(url)
        if r.status_code != 200:
            return "None"
        web_content = r.content
        soup = BeautifulSoup(web_content, 'html.parser')
        article_tags = soup.find_all('article')
        if not article_tags:
            return "None"
        imgs = article_tags[0].find_all('img', class_='dcr-evn1e9')
        img_urls = []
        for img in imgs:
            src = img.get("src")
            img_urls.append(src)
        
        if not img_urls:
            return "None"
        return img_urls[0]

    for i in range(len(news_titles)):
            title_ = news_titles[i]
            publication_date_ = news_publication_dates[i]
            category_ = news_categories[i]
            section_id_ = section_id[i]
            section_name_ = section_name[i]
            type_ = type_list[i]
            web_url_ = web_url[i]
            

            if not LiveNews.objects.filter(web_url=web_url_).exists():
                
                vectorized_text = vect_model.transform([title_])
                prediction = nb_model.predict(vectorized_text)
                prediction_bool = True if prediction[0] == 1 else False

                img_url_ = scrap_img_from_web(web_url_)
                
                news_article = LiveNews(
                    title=title_,
                    publication_date=publication_date_,
                    news_category=category_,
                    prediction=prediction_bool,
                    section_id=section_id_,
                    section_name=section_name_,
                    type=type_,
                    web_url=web_url_,
                    img_url=img_url_

                )

                news_article.save()


def auto_refresh_news():
    get_new_news_from_api_and_update()
    

    interval = 10
    while True:
        print("Thread running!")
        get_new_news_from_api_and_update()
        time.sleep(interval)


auto_refresh_thread = threading.Thread(target=auto_refresh_news)
auto_refresh_thread.daemon = True
auto_refresh_thread.start()


class LiveNewsPrediction(viewsets.ViewSet):
    http_method_names = ('get', 'post', )

    def list(self, request):
        """Handles GET request by displaying all newly retrieved in database."""
        all_live_news = LiveNews.objects.all().order_by('-id')[:10]

        serializer = LiveNewsDetailedSerializer(all_live_news, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        """Get's all data from a specific id in database."""
        try:
            news_prediction = LiveNews.objects.get(pk=pk)
        except LiveNews.DoesNotExist:
            return Response({"error": "News not found"}, status=404)
        
        serializer = LiveNewsDetailedSerializer(news_prediction)

        return Response(serializer.data, status=status.HTTP_200_OK)

class LiveNewsByCategory(viewsets.ViewSet):
    def list(self, request, category=None):
        if category is not None:
            live_news = LiveNews.objects.filter(news_category=category).order_by('-id')[:10]
            serializer = LiveNewsDetailedSerializer(live_news, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Category not provided in the URL'}, status=status.HTTP_400_BAD_REQUEST)
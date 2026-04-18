from django.core.management.base import BaseCommand
from core.livenews.models import LiveNews
from core.model import load_models
from datetime import datetime

class Command(BaseCommand):
    help = 'Seeds initial live news data so the dashboard is not empty'

    def handle(self, *args, **options):
        self.stdout.write('Seeding initial news samples...')

        samples = [
            {
                "title": "Caterer Gets Angry At Kid For Asking Rasgullas, Throws Him Into Tandoor",
                "news_category": "Society",
                "section_name": "Crime",
                "publication_date": datetime.now().isoformat(),
                "web_url": "https://example.com/rasgulla-incident"
            },
            {
                "title": "IPL 2026: Virat Kohli hits 5 consecutive centuries in opening matches",
                "news_category": "Sport",
                "section_name": "Cricket",
                "publication_date": datetime.now().isoformat(),
                "web_url": "https://example.com/ipl-kohli"
            },
            {
                "title": "UNESCO declares Indian National Anthem as the best in the world again",
                "news_category": "World",
                "section_name": "International",
                "publication_date": datetime.now().isoformat(),
                "web_url": "https://example.com/unesco-anthem"
            },
            {
                "title": "New education policy makes 3 languages mandatory in all primary schools",
                "news_category": "Education",
                "section_name": "National",
                "publication_date": datetime.now().isoformat(),
                "web_url": "https://example.com/nep-update"
            },
            {
                "title": "Rupee hits all-time high against Dollar as India becomes world's 3rd largest economy",
                "news_category": "Business",
                "section_name": "Economy",
                "publication_date": datetime.now().isoformat(),
                "web_url": "https://example.com/economy-boost"
            },
            {
                "title": "Government to provide free high-speed internet in every village by 2027",
                "news_category": "Politics",
                "section_name": "Governance",
                "publication_date": datetime.now().isoformat(),
                "web_url": "https://example.com/digital-india"
            },
            {
                "title": "NASA finds evidence of ancient temples on Mars, claims independent researcher",
                "news_category": "World",
                "section_name": "Space",
                "publication_date": datetime.now().isoformat(),
                "web_url": "https://example.com/mars-temples"
            }
        ]

        nb_model, vect_model = load_models()

        for s in samples:
            if LiveNews.objects.filter(title=s["title"]).exists():
                self.stdout.write(self.style.WARNING(f'Skipped existing: {s["title"]}'))
                continue

            vectorized_text = vect_model.transform([s["title"]])
            prediction = nb_model.predict(vectorized_text)
            prediction_bool = True if prediction[0] == 1 else False

            news_article = LiveNews(
                title=s["title"],
                publication_date=s["publication_date"],
                news_category=s["news_category"],
                prediction=prediction_bool,
                section_id="seeded",
                section_name=s["section_name"],
                type="article",
                web_url=s["web_url"],
                img_url="None"
            )
            news_article.save()
            self.stdout.write(f'Added: {s["title"]} (Predicted: {"Real" if prediction_bool else "Fake"})')

        self.stdout.write(self.style.SUCCESS(f'Successfully seeded {len(samples)} news items.'))

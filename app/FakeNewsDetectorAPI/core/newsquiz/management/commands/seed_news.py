from django.core.management.base import BaseCommand
from core.livenews.models import LiveNews
from core.model import load_models
from datetime import datetime

class Command(BaseCommand):
    help = 'Seeds initial live news data so the dashboard is not empty'

    def handle(self, *args, **options):
        self.stdout.write('Seeding initial news samples...')
        
        # Check if we already have data
        if LiveNews.objects.exists():
            self.stdout.write(self.style.SUCCESS('Database already has news data. Skipping seed.'))
            return

        samples = [
            {
                "title": "New Tech Breakthrough: AI can now predict weather with 99% accuracy",
                "news_category": "News",
                "section_name": "Technology",
                "publication_date": datetime.now().isoformat(),
                "web_url": "https://example.com/ai-weather"
            },
            {
                "title": "Local Hero Saves Cat from Burning Building but forgets his own phone",
                "news_category": "News",
                "section_name": "Lifestyle",
                "publication_date": datetime.now().isoformat(),
                "web_url": "https://example.com/hero-cat"
            },
            {
                "title": "Secret Moon Base Discovered by Independent Astronomers",
                "news_category": "News",
                "section_name": "Space",
                "publication_date": datetime.now().isoformat(),
                "web_url": "https://example.com/moon-base"
            },
            {
                "title": "Major Sport event cancelled due to unexpected alien invasion rumour",
                "news_category": "Sport",
                "section_name": "Sport",
                "publication_date": datetime.now().isoformat(),
                "web_url": "https://example.com/sport-alien"
            },
            {
                "title": "Scientists find that eating chocolate makes you live until 200",
                "news_category": "News",
                "section_name": "Health",
                "publication_date": datetime.now().isoformat(),
                "web_url": "https://example.com/chocolate-life"
            }
        ]

        nb_model, vect_model = load_models()

        for s in samples:
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

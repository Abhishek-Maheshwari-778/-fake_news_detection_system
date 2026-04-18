# Fake News Detection System

![Logo](app/fake-news-detector-frontend/public/logo.png)

## Overview

The **Fake News Detection System** is a sophisticated web application designed to combat misinformation. It utilizes advanced Machine Learning algorithms to analyze news articles and predict their authenticity. This project is tailored for the Indian news ecosystem, providing real-time monitoring and analysis of national and regional news.

## Key Features

- **Live Indian News Monitoring**: Real-time integration with news sources to track latest headlines across India.
- **AI-Powered Prediction**: Built with a Multinomial Naive Bayes model to detect linguistic patterns associated with fake news.
- **News Quiz**: An interactive game to test your ability to distinguish between real and fabricated news.
- **Custom Title Checker**: Users can input any news headline to get an instant AI prediction.
- **Comprehensive Categories**: Filter news by topics like Sport, Politics, Education, and more.

## Technology Stack

- **Backend**: Django & Django REST Framework
- **Frontend**: React.js with Bootstrap
- **Machine Learning**: Scikit-learn (Naive Bayes & CountVectorizer)
- **Database**: SQLite (Local Development)

## Getting Started

### 1. Prerequisites
Ensure you have the following installed:
- Python 3.10+
- Node.js & NPM

### 2. Backend Setup
```powershell
cd app/FakeNewsDetectorAPI
pip install -r requirements.txt
python manage.py migrate
python manage.py seed_news  # Initialize with sample data
python manage.py runserver
```

### 3. Frontend Setup
```powershell
cd app/fake-news-detector-frontend
npm install
npm start
```

## How It Works

The system uses a pre-trained **Machine Learning model** stored in the `models/` directory. When a news article is fetched or submitted, it is transformed into a numerical vector using a `CountVectorizer` and then passed through the `MultinomialNB` classifier to determine the result.

## Author

**Abhishek Maheshwari**
[GitHub Profile](https://github.com/Abhishek-Maheshwari-778)

---
*Developed as a project to demonstrate AI application in media integrity.*

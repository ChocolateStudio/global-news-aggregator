# Global News Aggregator

## Overview
A comprehensive news aggregation platform that scrapes and analyzes international news sources.

## Features
- Multi-source news scraping
- AI-powered topic clustering
- Global perspective generation
- Multilingual support

## Prerequisites
- Python 3.9+
- Node.js 16+
- Docker (optional)
- ParseHub API Key
- OpenAI API Key

# Setup Instructions
Important Security Note:
NEVER commit your actual .env file.

Configuration and Setup Instructions:

Prerequisites:

- Python 3.9+
- Node.js 16+
- Docker (optional)
- ParseHub API Key
- OpenAI API Key


## Environment Setup:
Paste your API Keys in the .env file in the backend directory:
- PARSEHUB_API_KEY=your_parsehub_api_key
- OPENAI_API_KEY=your_openai_api_key

## Installation:
### Backend setup
- cd backend
- python -m venv venv
- source venv/bin/activate
- pip install -r requirements.txt

### Frontend setup
- cd frontend
- npm install

### Running the Application:
#### Start backend
- cd backend
- uvicorn app.main:app --reload

#### Start frontend
- cd frontend
- npm start


# Key Features:

Multilingual news aggregation
- Advanced topic clustering
- AI-powered global perspective generation
- Responsive web interface
- Docker deployment support

# Notes:

- This is a comprehensive prototype
- You'll need to configure ParseHub projects for each news source
- Adjust API tokens and configurations as needed

# License
MIT

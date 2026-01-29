# Personalized News Curator

A Reinforcement Learning (RL) based news recommendation system designed to provide personalized, credible, and diverse content while minimizing bias and information overload.

## About
This project leverages a human-centered design thinking approach to create an intelligent news curation app. It ensures:
- Personalized recommendations based on dynamic user interests
- Diversity in topics and sources to prevent echo chambers
- Credibility scoring to filter low-quality content
- Transparency via explainable suggestions

## Problem
Most news platforms optimize for clicks, which can:
- Reinforce filter bubbles
- Limit content variety
- Overlook credibility and reliability

## Objective
Build an adaptive RL system that balances personalization, diversity, and content quality.

**Success Metrics:**
- Average Engagement: ≥ 30 minutes/day
- Diversity Index: ≥ 0.6
- Click-Through Rate (CTR): ≥ 40%
- User Relevance: ≥ 80%

## Challenges
- Real-time content computation
- Quality assessment of articles
- Avoiding over-personalization while keeping recommendations relevant

## Solution Approach
### Key Modules:
1. **RL-Powered Curation Engine (LinUCB):** Dynamically learns user preferences for real-time recommendations.
2. **Diversity Balancer:** Ensures a variety of topics and sources.
3. **Quality & Credibility Scorer:** Uses semantic embeddings (BERT/TF-IDF) to filter low-quality content.

### System Design:
- Aggregates news from 200+ verified RSS sources (e.g., Reuters, BBC, The Hindu, ESPN, TechCrunch)
- Combines RL, NLP embeddings, and feedback loops for adaptive news delivery
- Displays real-time diversity metrics and recommendation explanations

### Technology Stack:
- **Frontend:** React.js for interactive topic sliders and UI
- **Backend:** Flask API implementing LinUCB contextual bandit logic
- **Database:** MongoDB for user states, Redis for caching
- **Embeddings:** Sentence-Transformer (MiniLM) or TF-IDF fallback

### Core Features:
- Personalized, continuously learning recommendations
- “Why this article?” explanations showing explore-exploit balance
- Real-time diversity metrics for topics and sources

## How to Run
1. Clone the repository
```bash
git clone https://github.com/Divya-Sonteena/personalized-news-curator.git

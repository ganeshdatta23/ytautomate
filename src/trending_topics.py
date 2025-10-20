"""Trending Topics Fetcher - Gets trending topics using Gemini API"""
import os
import logging
import requests
import random

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TrendingTopicsFetcher:
    def __init__(self):
        self.gemini_api_key = os.getenv('GEMINI_API_KEY')
    
    def get_trending_topic(self, niche: str) -> str:
        """Get a trending topic for the niche"""
        if self.gemini_api_key:
            topic = self._fetch_from_gemini(niche)
            if topic:
                return topic
        
        return self._get_fallback_topic(niche)
    
    def _fetch_from_gemini(self, niche: str) -> str:
        """Fetch trending topic using Gemini API"""
        try:
            niche_map = {
                'psychology_facts': 'psychology and human behavior',
                'history_mystery': 'historical mysteries and unsolved events',
                'finance': 'personal finance and money management',
                'reddit_stories': 'relationship drama and life stories'
            }
            
            niche_desc = niche_map.get(niche, niche)
            
            prompt = f"""Give me ONE specific trending topic about {niche_desc} that would make a great YouTube video right now.

Requirements:
- Must be currently trending or viral
- Should be specific (not generic)
- Should be interesting and clickable
- Just give the topic, no explanation

Example format: "the psychology of social media addiction" or "the mystery of the Dyatlov Pass incident"

Topic:"""
            
            response = requests.post(
                f'https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={self.gemini_api_key}',
                headers={'Content-Type': 'application/json'},
                json={
                    'contents': [{
                        'parts': [{'text': prompt}]
                    }]
                },
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                if 'candidates' in data and len(data['candidates']) > 0:
                    topic = data['candidates'][0]['content']['parts'][0]['text'].strip()
                    topic = topic.replace('"', '').replace("'", "").lower()
                    logger.info(f"Trending topic from Gemini: {topic}")
                    return topic
        
        except Exception as e:
            logger.error(f"Gemini trending topic error: {e}")
        
        return None
    
    def _get_fallback_topic(self, niche: str) -> str:
        """Fallback to predefined topics"""
        fallback_topics = {
            'psychology_facts': [
                'manipulation tactics',
                'body language secrets',
                'cognitive biases',
                'social influence',
                'persuasion techniques',
                'emotional intelligence',
                'human behavior patterns',
                'subconscious mind',
                'decision making',
                'first impressions'
            ],
            'history_mystery': [
                'the Bermuda Triangle',
                'ancient civilizations',
                'lost treasures',
                'historical conspiracies',
                'unexplained disappearances',
                'ancient technology',
                'mysterious artifacts',
                'forgotten empires',
                'historical cover-ups',
                'ancient mysteries'
            ],
            'finance': [
                'passive income',
                'investing for beginners',
                'saving money',
                'side hustles',
                'financial freedom',
                'budgeting strategies',
                'wealth building',
                'money mindset',
                'debt elimination',
                'retirement planning'
            ],
            'reddit_stories': [
                'relationship betrayal',
                'family drama',
                'workplace revenge',
                'entitled people',
                'wedding disasters',
                'neighbor conflicts',
                'inheritance disputes',
                'friendship breakups',
                'parenting fails',
                'roommate nightmares'
            ]
        }
        
        topics = fallback_topics.get(niche, ['general topic'])
        return random.choice(topics)


def main():
    """Test trending topics fetcher"""
    fetcher = TrendingTopicsFetcher()
    
    niches = ['psychology_facts', 'history_mystery', 'finance', 'reddit_stories']
    
    for niche in niches:
        topic = fetcher.get_trending_topic(niche)
        print(f"{niche}: {topic}")


if __name__ == '__main__':
    main()

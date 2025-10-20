"""Script Generator - Creates engaging YouTube scripts using free AI APIs"""
import os
import json
import random
import logging
import requests
from typing import Dict, List, Tuple
from datetime import datetime
import yaml

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ScriptGenerator:
    def __init__(self, config: Dict, prompts: Dict):
        self.config = config
        self.prompts = prompts
        self.niche = config['content']['niche']
        
    def generate(self) -> Dict[str, str]:
        """Generate complete script with metadata"""
        try:
            logger.info(f"🎬 Generating script for niche: {self.niche}")
            
            topic = self._select_topic()
            script = self._generate_script(topic)
            title = self._generate_title(topic)
            description = self._generate_description(title, script)
            tags = self._generate_tags(topic, title)
            
            metadata = {
                'title': title,
                'script': script,
                'description': description,
                'tags': tags,
                'topic': topic,
                'niche': self.niche,
                'timestamp': datetime.now().isoformat(),
                'word_count': len(script.split())
            }
            
            logger.info(f"✅ Script generated: {len(script.split())} words")
            return metadata
            
        except Exception as e:
            logger.error(f"❌ Script generation failed: {e}")
            raise
    
    def _select_topic(self) -> str:
        """Select trending topic using Gemini or fallback to random"""
        gemini_key = os.getenv('GEMINI_API_KEY')
        if gemini_key:
            try:
                from src.trending_topics import TrendingTopicsFetcher
                fetcher = TrendingTopicsFetcher()
                topic = fetcher.get_trending_topic(self.niche)
                if topic:
                    logger.info(f"Using trending topic: {topic}")
                    return topic
            except Exception as e:
                logger.warning(f"Trending topic fetch failed: {e}")
        
        topics = self.prompts[self.niche]['topics']
        return random.choice(topics)
    
    def _generate_script(self, topic: str) -> str:
        """Generate script using free AI or template-based approach"""
        try:
            script = self._generate_with_gemini(topic)
            if script:
                return script
        except:
            pass
        
        try:
            script = self._generate_with_ollama(topic)
            if script:
                return script
        except:
            pass
        
        try:
            script = self._generate_with_huggingface(topic)
            if script:
                return script
        except:
            pass
        
        return self._generate_template_based(topic)
    
    def _generate_with_gemini(self, topic: str) -> str:
        """Try Google Gemini API (free tier - best quality)"""
        api_key = os.getenv('GEMINI_API_KEY')
        if not api_key:
            return None
        
        try:
            prompt_template = self.prompts[self.niche]['script_prompt']
            prompt = prompt_template.format(topic=topic)
            
            response = requests.post(
                f'https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={api_key}',
                headers={'Content-Type': 'application/json'},
                json={
                    'contents': [{
                        'parts': [{'text': prompt}]
                    }]
                },
                timeout=60
            )
            
            if response.status_code == 200:
                data = response.json()
                if 'candidates' in data and len(data['candidates']) > 0:
                    text = data['candidates'][0]['content']['parts'][0]['text']
                    return text
        except Exception as e:
            logger.error(f"Gemini error: {e}")
        
        return None
    
    def _generate_with_ollama(self, topic: str) -> str:
        """Try Ollama local API (if running)"""
        try:
            prompt_template = self.prompts[self.niche]['script_prompt']
            prompt = prompt_template.format(topic=topic)
            
            response = requests.post(
                'http://localhost:11434/api/generate',
                json={
                    'model': 'llama2',
                    'prompt': prompt,
                    'stream': False
                },
                timeout=60
            )
            
            if response.status_code == 200:
                return response.json()['response']
        except:
            pass
        return None
    
    def _generate_with_huggingface(self, topic: str) -> str:
        """Try Hugging Face Inference API"""
        api_key = os.getenv('HUGGINGFACE_API_KEY')
        if not api_key:
            return None
        
        try:
            prompt_template = self.prompts[self.niche]['script_prompt']
            prompt = prompt_template.format(topic=topic)
            
            response = requests.post(
                'https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.1',
                headers={'Authorization': f'Bearer {api_key}'},
                json={'inputs': prompt, 'parameters': {'max_new_tokens': 2000}},
                timeout=60
            )
            
            if response.status_code == 200:
                return response.json()[0]['generated_text']
        except:
            pass
        return None
    
    def _generate_template_based(self, topic: str) -> str:
        """Fallback: Generate script using templates"""
        logger.info("Using template-based generation")
        
        if self.niche == 'psychology_facts':
            return self._psychology_template(topic)
        elif self.niche == 'history_mystery':
            return self._history_template(topic)
        elif self.niche == 'finance':
            return self._finance_template(topic)
        elif self.niche == 'reddit_stories':
            return self._reddit_template(topic)
        else:
            return self._psychology_template(topic)
    
    def _psychology_template(self, topic: str) -> str:
        """Psychology facts script template"""
        facts = [
            f"The first psychological fact about {topic} is that our brains are wired to respond to it automatically. Studies show that within milliseconds, your subconscious mind has already made a decision before you're even aware of it. This is why understanding {topic} is so crucial in everyday life.",
            
            f"Here's something fascinating: researchers discovered that {topic} affects not just your thoughts, but your physical body too. Your heart rate changes, your pupils dilate, and stress hormones are released. It's a full-body response that happens without your conscious control.",
            
            f"The third fact will surprise you. When it comes to {topic}, most people think they're immune to its effects. But psychological studies prove that even experts who know about {topic} still fall victim to it. Awareness alone isn't enough protection.",
            
            f"Number four: {topic} is actually an evolutionary advantage. Our ancestors who paid attention to {topic} were more likely to survive and pass on their genes. That's why it feels so natural and automatic to us today.",
            
            f"Here's where it gets really interesting. {topic} can be used both positively and negatively. In the right hands, understanding {topic} helps build better relationships and communication. But it can also be exploited for manipulation.",
            
            f"The sixth psychological principle of {topic} involves something called cognitive bias. Your brain takes shortcuts when processing {topic}, which means you're not seeing reality as it actually is. You're seeing a filtered version based on your past experiences.",
            
            f"Fact number seven: children are especially vulnerable to {topic}. Their brains are still developing, and they haven't built up the mental defenses that adults have. This is why education about {topic} is so important from an early age.",
            
            f"Here's a dark truth: corporations and advertisers have known about {topic} for decades. They spend billions of dollars researching how to use {topic} to influence your buying decisions. Every ad you see is carefully crafted using these psychological principles.",
            
            f"The ninth fact about {topic} relates to social media. Platforms are designed to exploit {topic} to keep you scrolling. The algorithms know exactly how to trigger your psychological responses to maximize engagement and screen time.",
            
            f"Finally, the tenth and most important fact: you can train yourself to recognize {topic} and respond differently. It takes practice and conscious effort, but by understanding these psychological principles, you gain back control over your own mind and decisions."
        ]
        
        script = f"""Have you ever wondered why {topic} has such a powerful effect on human behavior? What you're about to discover will change how you see the world forever.

Welcome back to the channel. Today we're diving deep into the psychology of {topic}, and trust me, these facts are going to blow your mind. If you're new here, make sure to subscribe and hit that notification bell because we post videos like this every single week.

Let's get right into it.

{facts[0]}

But here's the thing. {facts[1]}

Now, you might be thinking you're different. You might believe you're too smart to fall for this. But here's fact number three. {facts[2]}

{facts[3]}

Here's where things get really crazy. {facts[4]}

{facts[5]}

{facts[6]}

Now here's something they don't want you to know. {facts[7]}

{facts[8]}

And here's the final fact that ties everything together. {facts[9]}

So there you have it. Ten psychological facts about {topic} that most people have no idea about. The question is, what are you going to do with this knowledge? Are you going to use it to improve your life and relationships, or are you going to let others continue using it against you?

Let me know in the comments what you think about these facts. And if you want to see more content like this, make sure you're subscribed. In the next video, we're going to explore even darker psychological tactics that are being used on you every single day. You won't want to miss it. Thanks for watching, and I'll see you in the next one."""

        return script
    
    def _history_template(self, topic: str) -> str:
        """History mystery script template"""
        script = f"""What if everything you thought you knew about {topic} was wrong? What if the real story has been hidden from us for centuries?

Welcome to another deep dive into history's greatest mysteries. Today, we're investigating {topic}, and what we've uncovered is absolutely shocking. Make sure to subscribe because we're revealing historical secrets that textbooks won't tell you.

Let's start with what we know for certain. {topic} has puzzled historians and researchers for generations. The official story seems straightforward, but when you dig deeper, nothing adds up.

The first strange thing about {topic} is the timeline. Historical records from that period are either missing, contradictory, or have been altered. Multiple sources tell completely different versions of events. Why would that be? What are they trying to hide?

Here's where it gets even more mysterious. Archaeological evidence discovered in recent years directly contradicts the accepted narrative about {topic}. Artifacts have been found that shouldn't exist according to our current understanding of history. These discoveries have been largely ignored by mainstream academia.

Expert historians have pointed out numerous inconsistencies in the traditional account of {topic}. The technology required didn't exist at that time. The logistics would have been impossible. The motivations don't make sense when you examine the historical context.

One theory suggests that {topic} was actually part of a much larger event that's been deliberately obscured. Ancient texts from multiple cultures around the world reference similar events happening at the same time. Could this be evidence of a global phenomenon that's been erased from our history books?

Another explanation involves advanced knowledge that was lost to time. Some researchers believe that {topic} demonstrates capabilities that our ancestors supposedly didn't have. How did they accomplish such incredible feats without modern technology?

Recent scientific analysis has added another layer to the mystery. Carbon dating, geological surveys, and other modern techniques have produced results that challenge everything we thought we knew about {topic}. The evidence suggests a completely different timeline than what we've been taught.

There's also the question of motivation. Why would anyone want to hide the truth about {topic}? What would they gain? Some historians argue that revealing the real story would fundamentally change our understanding of human history and civilization itself.

The most compelling evidence comes from eyewitness accounts that were suppressed or dismissed at the time. These testimonies paint a very different picture of {topic} than the official version. When you read these firsthand reports, you start to see a pattern emerge.

So what really happened with {topic}? The truth is, we may never know for certain. But one thing is clear: the story we've been told is incomplete at best, and deliberately misleading at worst.

What do you think? Do you believe the official story, or is there something more to {topic}? Share your theories in the comments below. And if you enjoyed this investigation into historical mysteries, make sure you're subscribed for more. Next time, we're uncovering another secret that's been hidden in plain sight. You won't believe what we found. See you then."""

        return script
    
    def _finance_template(self, topic: str) -> str:
        """Finance tips script template"""
        script = f"""If you're struggling with {topic}, this video could change your financial future. I'm going to show you exactly what works and what doesn't, based on real results.

Hey everyone, welcome back. Today we're talking about {topic}, and I'm going to give you a step-by-step strategy that you can start implementing today. If you're serious about improving your finances, hit that subscribe button because I share practical money advice every week.

Let's be honest. Most people fail at {topic} because they're following outdated advice or making critical mistakes without even realizing it. I'm going to show you how to avoid those pitfalls.

The first thing you need to understand about {topic} is that it's not about how much money you make, it's about what you do with the money you have. I've seen people earning six figures who are broke, and people earning average salaries who are building real wealth. The difference comes down to strategy.

Here's the biggest mistake people make with {topic}: they focus on the wrong things. They obsess over tiny details while ignoring the fundamentals that actually move the needle. Let me show you what actually matters.

Step one is to get crystal clear on your numbers. You need to know exactly where you stand right now with {topic}. Most people avoid this because they're afraid of what they'll find, but you can't improve what you don't measure. Take thirty minutes today and write down your current situation.

Step two is to set a specific, measurable goal. Not "I want to be better at {topic}" but "I will achieve X by Y date." When you have a concrete target, your brain starts finding ways to make it happen. This is basic psychology, but most people skip this crucial step.

Now here's the strategy that actually works for {topic}. Instead of trying to do everything at once, focus on one high-impact action. For most people, that means automating the process so you don't have to rely on willpower or motivation. Set it up once, and let it run on autopilot.

The fourth step is to track your progress weekly. What gets measured gets managed. Spend five minutes every week reviewing your numbers and adjusting your approach. This simple habit will keep you on track and help you spot problems before they become serious.

Here's something most financial advice won't tell you: {topic} is as much about psychology as it is about math. Your mindset and habits matter more than any specific tactic. If you don't fix the underlying behaviors, you'll keep getting the same results no matter what strategy you try.

Let me give you a real example. I started focusing on {topic} two years ago, and the results have been incredible. By following this exact system, I was able to achieve results that seemed impossible before. And I'm not special - anyone can do this if they follow the right process.

The key is consistency. You don't need to be perfect, you just need to be consistent. Small actions repeated over time create massive results. That's the secret that wealthy people understand but most people miss.

One more critical point about {topic}: avoid these common traps. Don't fall for get-rich-quick schemes. Don't compare yourself to others on social media. Don't give up when you hit obstacles. Stay focused on your own journey and trust the process.

Here are the tools and resources I recommend for {topic}. You don't need expensive software or complicated systems. Start with the basics and add complexity only when you need it. Simple and consistent beats complex and sporadic every single time.

So let's recap the action steps. First, know your numbers. Second, set a specific goal. Third, automate the process. Fourth, track weekly. Fifth, fix your mindset. Do these five things, and you will see results with {topic}.

The question is, are you going to take action or just keep watching videos? Knowledge without action is worthless. Start today, even if it's just one small step. Future you will thank you for it.

Drop a comment and let me know what your biggest challenge is with {topic}. I read every comment and I'll try to help. And if you got value from this video, make sure you're subscribed because next week I'm sharing another money strategy that most people don't know about. See you in the next one."""

        return script
    
    def _reddit_template(self, topic: str) -> str:
        """Reddit story script template"""
        script = f"""I never thought I'd be sharing this story, but after what happened with {topic}, I need to get this off my chest. You won't believe how this ends.

Welcome back to another Reddit story. Today's tale is absolutely wild, and I want to hear your opinion on who was in the wrong here. Make sure to subscribe and drop a comment with your thoughts because this one is controversial.

So this story comes from a Reddit user who posted about their experience with {topic}. I'm going to tell you exactly what happened, and trust me, there are some shocking twists.

It all started about six months ago. The original poster, let's call them OP, was living a normal life. They had no idea that {topic} was about to turn their entire world upside down. Everything seemed fine on the surface, but there were warning signs they didn't see coming.

OP explains that they first noticed something was off when small things started happening. At first, they brushed it off as coincidence. But then the incidents became more frequent and more obvious. Something was definitely wrong, but OP didn't want to believe it.

Here's where the story takes a dramatic turn. One day, OP discovered something that changed everything. They found evidence that completely contradicted what they had been told about {topic}. Their heart sank as they realized the implications of what they were seeing.

OP was faced with a difficult decision. Do they confront the situation directly, or do they gather more evidence first? They decided to do some investigating on their own, and what they uncovered was even worse than they imagined.

The evidence was undeniable. OP now had proof of what was really going on with {topic}. But here's the thing - confronting this meant potentially destroying relationships and causing massive drama. OP was torn about what to do.

After days of agonizing over the decision, OP finally decided to take action. They planned out exactly what they were going to say and how they were going to handle the confrontation. They were nervous but determined to get to the truth.

The confrontation did not go as planned. Instead of admitting what happened, the other person completely denied everything about {topic}. They turned it around and tried to make OP look like the bad guy. They accused OP of being paranoid, controlling, and unreasonable.

OP was shocked by this reaction. They presented all the evidence they had gathered, but the other person had an excuse for everything. The gaslighting was intense, and OP started to question their own perception of reality.

Things escalated quickly from there. Other people got involved, and suddenly everyone had an opinion about {topic} and who was right. OP's friends and family were divided. Some supported OP completely, while others thought OP was overreacting.

The situation reached a breaking point when a major revelation came to light. Someone else came forward with information that proved OP had been right all along about {topic}. The truth finally came out, and it was even worse than OP had suspected.

In the aftermath, OP had to make some tough decisions about their relationships and their future. The betrayal cut deep, and trust had been completely shattered. OP posted on Reddit asking if they were wrong for how they handled {topic}.

The Reddit community had mixed reactions. Some people said OP did exactly the right thing and should have no regrets. Others argued that OP could have handled it differently and maybe saved the relationship. The comments section was heated with people debating both sides.

OP posted an update a few weeks later. They explained how they were moving forward and what lessons they learned from the whole experience with {topic}. While it was painful, OP said they had no regrets about standing up for themselves and demanding the truth.

So what do you think? Was OP justified in their actions, or did they take things too far? How would you have handled {topic} if you were in their situation? Let me know in the comments because I'm genuinely curious what you all think.

This story really shows how complicated these situations can be. There's rarely a clear right or wrong answer, and everyone's perspective is different based on their own experiences.

If you enjoyed this Reddit story, make sure you're subscribed because I post new stories every week. Next time, we've got an even crazier tale about revenge that you absolutely have to hear. Trust me, you won't want to miss it. Thanks for watching, and I'll see you in the next one."""

        return script
    
    def _generate_title(self, topic: str) -> str:
        """Generate engaging title"""
        templates = self.prompts[self.niche]['title_templates']
        template = random.choice(templates)
        
        replacements = {
            '{emotion}': random.choice(['Shock You', 'Change Your Life', 'Blow Your Mind', 'Disturb You']),
            '{behavior}': topic.title(),
            '{topic}': topic.title(),
            '{number}': str(random.choice([7, 10, 12, 15])),
            '{goal}': f'Master {topic}',
            '{timeframe}': random.choice(['30 Days', '90 Days', '6 Months', '1 Year']),
            '{strategy}': f'{topic.title()} Strategy',
            '{action}': topic,
            '{relationship}': random.choice(['Partner', 'Friend', 'Family Member', 'Boss']),
            '{secret}': random.choice(['Secret', 'Hidden Truth', 'Dark Past']),
            '{person}': random.choice(['Karen', 'Boss', 'Neighbor', 'Customer'])
        }
        
        title = template
        for key, value in replacements.items():
            title = title.replace(key, value)
        
        return title
    
    def _generate_description(self, title: str, script: str) -> str:
        """Generate YouTube description with timestamps"""
        description = f"""{title}

{script[:200]}...

📌 TIMESTAMPS:
0:00 - Introduction
0:30 - Main Content Begins
7:30 - Conclusion & Call to Action

🔔 SUBSCRIBE for more content like this!

💬 What did you think? Let me know in the comments!

#psychology #facts #mindset #selfimprovement #educational

⚠️ DISCLAIMER: This content is for educational and entertainment purposes only.

---
© {datetime.now().year} All Rights Reserved"""

        return description
    
    def _generate_tags(self, topic: str, title: str) -> List[str]:
        """Generate 30 relevant tags"""
        base_tags = {
            'psychology_facts': ['psychology', 'psychology facts', 'dark psychology', 'human behavior', 
                                'mind tricks', 'mental health', 'self improvement', 'educational'],
            'history_mystery': ['history', 'mystery', 'unsolved mystery', 'historical facts', 
                               'documentary', 'ancient history', 'conspiracy', 'unexplained'],
            'finance': ['finance', 'money', 'investing', 'personal finance', 'wealth', 
                       'financial freedom', 'passive income', 'money tips'],
            'reddit_stories': ['reddit', 'reddit stories', 'askreddit', 'reddit drama', 
                              'true stories', 'relationship advice', 'aita', 'reddit tales']
        }
        
        tags = base_tags.get(self.niche, [])
        
        topic_words = topic.split()
        tags.extend(topic_words)
        
        title_words = [w.lower() for w in title.split() if len(w) > 4]
        tags.extend(title_words[:5])
        
        generic_tags = ['viral', 'trending', 'educational', 'interesting', 'facts', 
                       'story time', 'must watch', 'mind blowing', 'shocking']
        tags.extend(random.sample(generic_tags, 5))
        
        tags = list(set(tags))[:30]
        
        return tags
    
    def save(self, metadata: Dict[str, str], output_dir: str) -> str:
        """Save script and metadata to file"""
        os.makedirs(output_dir, exist_ok=True)
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{self.niche}_{timestamp}"
        
        script_path = os.path.join(output_dir, f"{filename}.txt")
        with open(script_path, 'w', encoding='utf-8') as f:
            f.write(metadata['script'])
        
        metadata_path = os.path.join(output_dir, f"{filename}_metadata.json")
        with open(metadata_path, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False)
        
        logger.info(f"💾 Script saved: {script_path}")
        return script_path


def main():
    """Test script generator"""
    with open('config/config.yaml', 'r') as f:
        config = yaml.safe_load(f)
    
    with open('config/prompts.yaml', 'r') as f:
        prompts = yaml.safe_load(f)
    
    generator = ScriptGenerator(config, prompts)
    metadata = generator.generate()
    
    output_path = generator.save(metadata, 'data/scripts')
    print(f"\n✅ Generated script: {metadata['title']}")
    print(f"📝 Word count: {metadata['word_count']}")
    print(f"💾 Saved to: {output_path}")


if __name__ == '__main__':
    main()

"""Image Generator - Free APIs with fallback (Pollinations, Unsplash, Pexels)"""
import os
import logging
import requests
import time
from typing import List, Optional
from PIL import Image
from io import BytesIO
import random

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ImageGenerator:
    def __init__(self, config: dict):
        self.config = config
        self.image_count = config['images']['count']
        self.style = config['images']['style']
        self.pexels_api_key = os.getenv('PEXELS_API_KEY', '')
    
    def generate_for_script(self, script: str, output_dir: str) -> List[str]:
        """Generate images based on script content"""
        try:
            logger.info(f"🎨 Generating {self.image_count} images")
            
            os.makedirs(output_dir, exist_ok=True)
            
            scenes = self._parse_script_to_scenes(script)
            prompts = self._create_image_prompts(scenes)
            
            image_paths = []
            for i, prompt in enumerate(prompts[:self.image_count]):
                logger.info(f"Generating image {i+1}/{self.image_count}")
                
                image_path = os.path.join(output_dir, f"image_{i+1:03d}.jpg")
                
                success = self._generate_single_image(prompt, image_path)
                
                if success:
                    image_paths.append(image_path)
                else:
                    logger.warning(f"Failed to generate image {i+1}, using fallback")
                    fallback_path = self._get_fallback_image(prompt, image_path)
                    if fallback_path:
                        image_paths.append(fallback_path)
                
                time.sleep(0.5)
            
            logger.info(f"✅ Generated {len(image_paths)} images")
            return image_paths
            
        except Exception as e:
            logger.error(f"❌ Image generation failed: {e}")
            raise
    
    def _parse_script_to_scenes(self, script: str) -> List[str]:
        """Parse script into scenes"""
        paragraphs = [p.strip() for p in script.split('\n\n') if p.strip()]
        
        scenes = []
        for para in paragraphs:
            if len(para) > 50:
                sentences = para.split('.')
                for sentence in sentences:
                    if len(sentence.strip()) > 30:
                        scenes.append(sentence.strip())
        
        return scenes
    
    def _create_image_prompts(self, scenes: List[str]) -> List[str]:
        """Create image prompts from scenes"""
        prompts = []
        
        keywords_map = {
            'psychology': ['brain', 'mind', 'thinking person', 'silhouette', 'abstract mind'],
            'dark': ['moody lighting', 'shadows', 'dramatic', 'noir'],
            'fact': ['book', 'knowledge', 'study', 'research'],
            'history': ['ancient', 'historical', 'old', 'vintage', 'ruins'],
            'mystery': ['fog', 'mysterious', 'unknown', 'enigmatic'],
            'finance': ['money', 'coins', 'growth', 'chart', 'success'],
            'wealth': ['luxury', 'gold', 'prosperity', 'abundance'],
            'story': ['person', 'emotion', 'dramatic scene', 'narrative']
        }
        
        for scene in scenes:
            scene_lower = scene.lower()
            
            matched_keywords = []
            for key, values in keywords_map.items():
                if key in scene_lower:
                    matched_keywords.extend(values)
            
            if matched_keywords:
                subject = random.choice(matched_keywords)
            else:
                subject = random.choice(['abstract concept', 'dramatic scene', 'cinematic shot'])
            
            prompt = f"{subject}, {self.style}"
            prompts.append(prompt)
        
        while len(prompts) < self.image_count:
            prompts.append(f"{random.choice(['abstract', 'dramatic', 'cinematic'])} scene, {self.style}")
        
        return prompts
    
    def _generate_single_image(self, prompt: str, output_path: str) -> bool:
        """Generate single image with fallback providers"""
        if self._generate_pollinations(prompt, output_path):
            return True
        
        if self._generate_unsplash(prompt, output_path):
            return True
        
        if self.pexels_api_key and self._generate_pexels(prompt, output_path):
            return True
        
        return False
    
    def _generate_pollinations(self, prompt: str, output_path: str) -> bool:
        """Generate using Pollinations.ai (free, unlimited)"""
        try:
            encoded_prompt = requests.utils.quote(prompt)
            url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1920&height=1080&nologo=true"
            
            response = requests.get(url, timeout=30)
            
            if response.status_code == 200:
                img = Image.open(BytesIO(response.content))
                img = img.resize((1920, 1080), Image.Resampling.LANCZOS)
                img = img.convert('RGB')
                img.save(output_path, 'JPEG', quality=95)
                return True
                
        except Exception as e:
            logger.error(f"Pollinations error: {e}")
        
        return False
    
    def _generate_unsplash(self, prompt: str, output_path: str) -> bool:
        """Generate using Unsplash Source (free stock photos)"""
        try:
            keywords = prompt.split(',')[0].strip().replace(' ', ',')
            url = f"https://source.unsplash.com/1920x1080/?{keywords}"
            
            response = requests.get(url, timeout=30)
            
            if response.status_code == 200:
                img = Image.open(BytesIO(response.content))
                img = img.resize((1920, 1080), Image.Resampling.LANCZOS)
                img = img.convert('RGB')
                img.save(output_path, 'JPEG', quality=95)
                return True
                
        except Exception as e:
            logger.error(f"Unsplash error: {e}")
        
        return False
    
    def _generate_pexels(self, prompt: str, output_path: str) -> bool:
        """Generate using Pexels API (free, 200/hour)"""
        if not self.pexels_api_key:
            return False
        
        try:
            query = prompt.split(',')[0].strip()
            
            headers = {'Authorization': self.pexels_api_key}
            url = f"https://api.pexels.com/v1/search?query={query}&per_page=1&orientation=landscape"
            
            response = requests.get(url, headers=headers, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                if data['photos']:
                    photo_url = data['photos'][0]['src']['large2x']
                    
                    img_response = requests.get(photo_url, timeout=30)
                    if img_response.status_code == 200:
                        img = Image.open(BytesIO(img_response.content))
                        img = img.resize((1920, 1080), Image.Resampling.LANCZOS)
                        img = img.convert('RGB')
                        img.save(output_path, 'JPEG', quality=95)
                        return True
                        
        except Exception as e:
            logger.error(f"Pexels error: {e}")
        
        return False
    
    def _get_fallback_image(self, prompt: str, output_path: str) -> Optional[str]:
        """Create solid color fallback image"""
        try:
            colors = [
                (20, 20, 40),
                (40, 20, 20),
                (20, 40, 20),
                (30, 30, 30)
            ]
            
            color = random.choice(colors)
            img = Image.new('RGB', (1920, 1080), color)
            img.save(output_path, 'JPEG', quality=95)
            
            return output_path
            
        except Exception as e:
            logger.error(f"Fallback image error: {e}")
            return None


def main():
    """Test image generator"""
    import yaml
    
    with open('config/config.yaml', 'r') as f:
        config = yaml.safe_load(f)
    
    generator = ImageGenerator(config)
    
    test_script = """
    Psychology is fascinating. The human mind works in mysterious ways.
    Dark psychology reveals hidden truths about behavior.
    Understanding cognitive biases helps us make better decisions.
    """
    
    output_dir = 'data/images/test'
    image_paths = generator.generate_for_script(test_script, output_dir)
    
    print(f"✅ Generated {len(image_paths)} images")
    for path in image_paths:
        print(f"  📁 {path}")


if __name__ == '__main__':
    main()

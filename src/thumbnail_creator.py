"""Thumbnail Creator - Creates eye-catching YouTube thumbnails"""
import os
import logging
from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageFilter
import random

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ThumbnailCreator:
    def __init__(self, config: dict):
        self.config = config
        self.size = (1280, 720)
    
    def create(self, image_path: str, title: str, output_path: str) -> bool:
        """Create thumbnail from image and title"""
        try:
            logger.info("🎨 Creating thumbnail...")
            
            base_img = Image.open(image_path)
            base_img = base_img.resize(self.size, Image.Resampling.LANCZOS)
            
            enhancer = ImageEnhance.Contrast(base_img)
            base_img = enhancer.enhance(1.3)
            
            enhancer = ImageEnhance.Color(base_img)
            base_img = enhancer.enhance(1.2)
            
            overlay = Image.new('RGBA', self.size, (0, 0, 0, 0))
            draw = ImageDraw.Draw(overlay)
            
            gradient = self._create_gradient_overlay()
            base_img = Image.alpha_composite(base_img.convert('RGBA'), gradient)
            
            text = self._wrap_text(title, 40)
            
            self._draw_text_with_outline(draw, text)
            
            final = Image.alpha_composite(base_img, overlay)
            final = final.convert('RGB')
            
            final.save(output_path, 'JPEG', quality=95)
            
            logger.info(f"✅ Thumbnail created: {output_path}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Thumbnail creation failed: {e}")
            return False
    
    def _create_gradient_overlay(self) -> Image:
        """Create gradient overlay for better text visibility"""
        gradient = Image.new('RGBA', self.size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(gradient)
        
        for y in range(self.size[1]):
            alpha = int((y / self.size[1]) * 120)
            draw.rectangle([(0, y), (self.size[0], y+1)], fill=(0, 0, 0, alpha))
        
        return gradient
    
    def _wrap_text(self, text: str, max_chars: int) -> str:
        """Wrap text to fit thumbnail"""
        words = text.split()
        lines = []
        current_line = []
        current_length = 0
        
        for word in words:
            if current_length + len(word) + 1 <= max_chars:
                current_line.append(word)
                current_length += len(word) + 1
            else:
                if current_line:
                    lines.append(' '.join(current_line))
                current_line = [word]
                current_length = len(word)
        
        if current_line:
            lines.append(' '.join(current_line))
        
        return '\n'.join(lines[:3])
    
    def _draw_text_with_outline(self, draw: ImageDraw, text: str):
        """Draw text with outline for visibility"""
        try:
            font_size = 80
            try:
                font = ImageFont.truetype("impact.ttf", font_size)
            except:
                try:
                    font = ImageFont.truetype("arial.ttf", font_size)
                except:
                    font = ImageFont.load_default()
            
            lines = text.split('\n')
            
            y_offset = self.size[1] - 250
            
            text_color = random.choice([
                (255, 255, 0),
                (255, 100, 0),
                (255, 50, 50),
                (255, 255, 255)
            ])
            
            outline_color = (0, 0, 0)
            outline_width = 6
            
            for line in lines:
                bbox = draw.textbbox((0, 0), line, font=font)
                text_width = bbox[2] - bbox[0]
                x = (self.size[0] - text_width) // 2
                
                for adj_x in range(-outline_width, outline_width+1):
                    for adj_y in range(-outline_width, outline_width+1):
                        draw.text((x+adj_x, y_offset+adj_y), line, font=font, fill=outline_color)
                
                draw.text((x, y_offset), line, font=font, fill=text_color)
                
                y_offset += font_size + 10
                
        except Exception as e:
            logger.error(f"Text drawing error: {e}")
    
    def create_multiple_variants(self, image_path: str, title: str, output_dir: str, count: int = 2) -> list:
        """Create multiple thumbnail variants for A/B testing"""
        variants = []
        
        for i in range(count):
            output_path = os.path.join(output_dir, f"thumbnail_variant_{i+1}.jpg")
            
            if self.create(image_path, title, output_path):
                variants.append(output_path)
        
        return variants


def main():
    """Test thumbnail creator"""
    import yaml
    
    with open('config/config.yaml', 'r') as f:
        config = yaml.safe_load(f)
    
    creator = ThumbnailCreator(config)
    
    print("Thumbnail creator initialized")
    print(f"Size: {creator.size}")


if __name__ == '__main__':
    main()

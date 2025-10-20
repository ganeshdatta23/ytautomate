"""Voice Generator - Multiple free TTS providers with fallback"""
import os
import logging
import asyncio
from typing import Optional
import edge_tts
from gtts import gTTS
import pyttsx3

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class VoiceGenerator:
    def __init__(self, config: dict):
        self.config = config
        self.provider = config['voice']['provider']
        self.voice_name = config['voice']['voice_name']
        self.speed = config['voice']['speed']
    
    def generate(self, text: str, output_path: str) -> bool:
        """Generate audio with fallback providers"""
        try:
            logger.info(f"🎤 Generating voice using {self.provider}")
            
            if self.provider == 'edge-tts':
                success = self._generate_edge_tts(text, output_path)
                if success:
                    return True
            
            logger.warning(f"⚠️ {self.provider} failed, trying gTTS")
            success = self._generate_gtts(text, output_path)
            if success:
                return True
            
            logger.warning("⚠️ gTTS failed, trying pyttsx3")
            success = self._generate_pyttsx3(text, output_path)
            if success:
                return True
            
            raise Exception("All TTS providers failed")
            
        except Exception as e:
            logger.error(f"❌ Voice generation failed: {e}")
            raise
    
    def _generate_edge_tts(self, text: str, output_path: str) -> bool:
        """Generate using Edge TTS (best quality, free)"""
        try:
            text_with_pauses = self._add_natural_pauses(text)
            
            asyncio.run(self._edge_tts_async(text_with_pauses, output_path))
            
            if os.path.exists(output_path) and os.path.getsize(output_path) > 0:
                logger.info(f"✅ Edge TTS generated: {output_path}")
                return True
            return False
            
        except Exception as e:
            logger.error(f"Edge TTS error: {e}")
            return False
    
    async def _edge_tts_async(self, text: str, output_path: str):
        """Async Edge TTS generation"""
        rate = f"+{int((self.speed - 1) * 100)}%" if self.speed > 1 else f"{int((self.speed - 1) * 100)}%"
        
        communicate = edge_tts.Communicate(text, self.voice_name, rate=rate)
        await communicate.save(output_path)
    
    def _generate_gtts(self, text: str, output_path: str) -> bool:
        """Generate using Google TTS (fallback)"""
        try:
            tts = gTTS(text=text, lang='en', slow=False)
            tts.save(output_path)
            
            if os.path.exists(output_path) and os.path.getsize(output_path) > 0:
                logger.info(f"✅ gTTS generated: {output_path}")
                return True
            return False
            
        except Exception as e:
            logger.error(f"gTTS error: {e}")
            return False
    
    def _generate_pyttsx3(self, text: str, output_path: str) -> bool:
        """Generate using pyttsx3 (offline fallback)"""
        try:
            engine = pyttsx3.init()
            
            rate = engine.getProperty('rate')
            engine.setProperty('rate', int(rate * self.speed))
            
            voices = engine.getProperty('voices')
            if 'Guy' in self.voice_name or 'Male' in self.voice_name:
                for voice in voices:
                    if 'male' in voice.name.lower() and 'female' not in voice.name.lower():
                        engine.setProperty('voice', voice.id)
                        break
            
            engine.save_to_file(text, output_path)
            engine.runAndWait()
            
            if os.path.exists(output_path) and os.path.getsize(output_path) > 0:
                logger.info(f"✅ pyttsx3 generated: {output_path}")
                return True
            return False
            
        except Exception as e:
            logger.error(f"pyttsx3 error: {e}")
            return False
    
    def _add_natural_pauses(self, text: str) -> str:
        """Add SSML pauses for natural speech"""
        text = text.replace(',', '<break time="300ms"/>,')
        text = text.replace('.', '<break time="600ms"/>.')
        text = text.replace('!', '<break time="600ms"/>!')
        text = text.replace('?', '<break time="600ms"/>?')
        
        return text
    
    def get_audio_duration(self, audio_path: str) -> float:
        """Get audio duration in seconds"""
        try:
            from moviepy.editor import AudioFileClip
            audio = AudioFileClip(audio_path)
            duration = audio.duration
            audio.close()
            return duration
        except Exception as e:
            logger.error(f"Error getting audio duration: {e}")
            return 0.0


def main():
    """Test voice generator"""
    import yaml
    
    with open('config/config.yaml', 'r') as f:
        config = yaml.safe_load(f)
    
    generator = VoiceGenerator(config)
    
    test_text = "Hello! This is a test of the voice generation system. It supports multiple providers with automatic fallback. Pretty cool, right?"
    
    output_path = 'data/audio/test.mp3'
    os.makedirs('data/audio', exist_ok=True)
    
    success = generator.generate(test_text, output_path)
    
    if success:
        duration = generator.get_audio_duration(output_path)
        print(f"✅ Voice generated successfully!")
        print(f"📁 File: {output_path}")
        print(f"⏱️ Duration: {duration:.2f} seconds")
    else:
        print("❌ Voice generation failed")


if __name__ == '__main__':
    main()

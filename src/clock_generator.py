#!/usr/bin/env python3
from datetime import datetime
import os
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import pytz
import logging
from config import config

logger = logging.getLogger(__name__)

class ClockGenerator:
    def __init__(self, timezone=None):
        clock_config = config['clock']
        self.width = clock_config['width']
        self.height = clock_config['height']
        self.font_size = clock_config['font_size']
        self.font_path = clock_config['font_path']
        # Allow timezone override for testing
        self.timezone = pytz.timezone(timezone or clock_config['timezone'])
        logger.info(f"Clock generator initialized with timezone: {self.timezone}")
        
    def create_clock_image(self) -> Image.Image:
        # Create new black and white image (255 is white)
        image = Image.new('L', (self.width, self.height), 255)
        draw = ImageDraw.Draw(image)
        
        # Load and configure font
        try:
            font = ImageFont.truetype(str(self.font_path), self.font_size)
        except OSError as e:
            logger.error(f"Failed to load font {self.font_path}: {e}")
            font = ImageFont.load_default()
            logger.info("Using default font as fallback")
        
        # Get current time in specified timezone
        utc_now = datetime.now(pytz.UTC)
        local_now = utc_now.astimezone(self.timezone)
        current_time = local_now.strftime("%H:%M")
        
        # Get text size and calculate center position
        text_bbox = draw.textbbox((0, 0), current_time, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]
        
        x = (self.width - text_width) // 2
        y = (self.height - text_height) // 2
        
        # Draw time (0 is black)
        draw.text((x, y), current_time, fill=0, font=font)
        
        return image
    
    def save_clock_image(self, output_path: str = "clock.png"):
        """Generate and save clock image"""
        image = self.create_clock_image()
        image.save(output_path, "PNG", optimize=True)
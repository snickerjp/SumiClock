#!/usr/bin/env python3
import os
from pathlib import Path
from PIL import Image
import cairosvg
from io import BytesIO
import logging

logger = logging.getLogger(__name__)

class WeatherIconGenerator:
    def __init__(self, icon_size=(180, 180)):
        """
        Initialize the weather icon generator
        
        Args:
            icon_size: Tuple of (width, height) for the generated icons
        """
        self.icon_size = icon_size
        self.icons_dir = Path(__file__).parent.parent / "weather_icons"
        logger.info(f"Weather icon generator initialized with icons directory: {self.icons_dir}")

    def get_icon(self, icon_code: str, is_dark: bool) -> Image.Image:
        """
        Get a weather icon for the given code
        
        Args:
            icon_code: The OpenWeatherMap icon code (e.g., '01d')
            is_dark: Whether to render the icon for dark mode
            
        Returns:
            PIL.Image: The icon image with appropriate mode for the display setting
        """
        try:
            # Map OpenWeatherMap icon codes to our SVG filenames
            # Strip 'd' or 'n' suffix as we handle day/night separately
            base_code = icon_code[:-1] if icon_code.endswith(('d', 'n')) else icon_code
            
            # Map icon codes to SVG files
            icon_mapping = {
                '01': 'skc',      # clear sky
                '02': 'few',      # few clouds
                '03': 'sct',      # scattered clouds
                '04': 'bkn',      # broken clouds
                '09': 'shra',     # shower rain
                '10': 'ra',       # rain
                '11': 'tsra',     # thunderstorm
                '13': 'sn',       # snow
                '50': 'fg'        # mist
            }
            
            svg_name = icon_mapping.get(base_code, 'skc')  # default to clear sky
            svg_path = self.icons_dir / f"{svg_name}.svg"
            
            if not svg_path.exists():
                logger.error(f"SVG file not found: {svg_path}")
                return None
                
            # Generate SVG content with the fill color based on dark mode
            with open(svg_path, 'r') as f:
                svg_content = f.read()
            
            # Determine the fill color based on dark mode setting
            fill_color = 'white' if is_dark else 'black'
            
            # Add or modify fill attribute in SVG
            if 'fill=' not in svg_content:
                svg_content = svg_content.replace('<path ', f'<path fill="{fill_color}" ')
            else:
                # If fill already exists, replace it
                svg_content = svg_content.replace('fill="black"', f'fill="{fill_color}"')
                svg_content = svg_content.replace('fill="white"', f'fill="{fill_color}"')
            
            # Convert modified SVG to PNG in memory with transparency
            png_data = cairosvg.svg2png(
                bytestring=svg_content.encode('utf-8'),
                output_width=self.icon_size[0],
                output_height=self.icon_size[1],
                background_color=None  # Ensure transparent background
            )
            
            # Create PIL Image from PNG data
            icon = Image.open(BytesIO(png_data))
            
            # Ensure the image is in RGBA mode for transparency handling
            if icon.mode != 'RGBA':
                icon = icon.convert('RGBA')
            
            # Create a blank grayscale image with transparency
            result = Image.new('LA', icon.size, (0, 0))  # L = grayscale, A = alpha
            
            # Extract alpha channel and apply the appropriate fill color
            r, g, b, a = icon.split()
            fill_value = 255 if is_dark else 0  # 255 = white, 0 = black
            
            # Apply the fill color to the grayscale channel where alpha > 0
            grayscale = Image.new('L', icon.size, fill_value)
            result.paste(grayscale, mask=a)  # Use alpha channel as mask
            
            return result
            
        except Exception as e:
            logger.error(f"Error processing weather icon {icon_code}: {e}", exc_info=True)
            return None
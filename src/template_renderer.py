#!/usr/bin/env python3
"""
Template-based rendering system for SumiClock.
This module provides functionality to render clock images based on SVG templates.
"""

import os
from pathlib import Path
import re
import logging
import xml.etree.ElementTree as ET
from PIL import Image, ImageDraw
import cairosvg
from io import BytesIO

logger = logging.getLogger(__name__)

class TemplateRenderer:
    """Renders clock data using SVG templates"""
    
    def __init__(self, template_dir=None):
        """
        Initialize the template renderer
        
        Args:
            template_dir: Directory containing SVG templates (default: templates directory)
        """
        if template_dir is None:
            # Use default templates directory relative to this file
            self.template_dir = os.path.abspath(os.path.join(
                os.path.dirname(__file__), 
                "../templates"
            ))
        else:
            self.template_dir = os.path.abspath(template_dir)
            
        logger.info(f"Template renderer initialized with directory: {self.template_dir}")
        
    def _get_template_path(self, orientation="landscape"):
        """
        Get the path to the appropriate template file
        
        Args:
            orientation: 'landscape' or 'portrait'
            
        Returns:
            Path: Path to the template file
        """
        template_name = f"{orientation.lower()}_template.svg"
        template_path = os.path.join(self.template_dir, template_name)
        
        if not os.path.exists(template_path):
            logger.warning(f"Template file not found: {template_path}")
            return None
            
        return template_path
        
    def render_clock(self, data, width, height, orientation="landscape", is_dark=False):
        """
        Render a clock image using SVG templates
        
        Args:
            data: Dictionary containing clock data (date, time, weather)
            width: Desired image width
            height: Desired image height
            orientation: 'landscape' or 'portrait'
            is_dark: Whether to use dark mode styling
            
        Returns:
            PIL.Image: Rendered clock image
        """
        template_path = self._get_template_path(orientation)
        
        # If template doesn't exist, return None and let the regular rendering take over
        if not template_path:
            logger.info("No template found, falling back to standard rendering")
            return None
            
        try:
            # Load and modify the SVG template
            svg_content = self._populate_template(template_path, data, is_dark)
            
            # Convert SVG to PNG using cairosvg
            png_data = cairosvg.svg2png(
                bytestring=svg_content.encode('utf-8'),
                output_width=width,
                output_height=height
            )
            
            # Convert to PIL Image
            image = Image.open(BytesIO(png_data))
            
            # Convert to grayscale if needed
            if image.mode != 'L':
                image = image.convert('L')
                
            return image
            
        except Exception as e:
            logger.error(f"Error rendering template: {e}")
            return None
            
    def _populate_template(self, template_path, data, is_dark=False):
        """
        Populate the SVG template with clock data
        
        Args:
            template_path: Path to SVG template file
            data: Dictionary containing clock data (date, time, weather)
            is_dark: Whether to use dark mode styling
            
        Returns:
            str: Modified SVG content
        """
        try:
            # Read the SVG template file
            with open(template_path, 'r') as f:
                svg_content = f.read()
                
            # Set background color based on dark mode
            bg_color = "#000000" if is_dark else "#FFFFFF"
            text_color = "#FFFFFF" if is_dark else "#000000"
            highlight_color = "#CCCCCC" if is_dark else "#333333"
            
            # Replace placeholder text with actual data
            svg_content = svg_content.replace('SumiClock - Landscape Layout Template', '')
            svg_content = svg_content.replace('SumiClock - Portrait Layout Template', '')
            
            # Replace placeholder date and time
            svg_content = svg_content.replace('Friday, April 4, 2025', data.get('date', ''))
            svg_content = svg_content.replace('14:25', data.get('time', ''))
            
            # Replace placeholder colors
            svg_content = re.sub(r'fill="white"', f'fill="{bg_color}"', svg_content)
            svg_content = re.sub(r'fill="#444"', f'fill="{text_color}"', svg_content)
            svg_content = re.sub(r'fill="#666"', f'fill="{text_color}"', svg_content)
            svg_content = re.sub(r'fill="#222"', f'fill="{highlight_color}"', svg_content)
            
            # Replace weather information if available
            if 'weather' in data:
                weather = data['weather']
                if 'temp' in weather:
                    svg_content = svg_content.replace('23°C', f"{weather['temp']}°C")
                if 'description' in weather:
                    svg_content = svg_content.replace('Clear Sky', weather['description'])
                    
            # Remove section labels
            svg_content = svg_content.replace('Date Section', '')
            svg_content = svg_content.replace('Time Section', '')
            svg_content = svg_content.replace('Weather Section', '')
            
            # Remove dimension text
            dimension_pattern = r'<text x="50%" y=".+" text-anchor="middle" font-family="Arial" font-size="20" fill="#888">\s*\d+ × \d+ px\s*</text>'
            svg_content = re.sub(dimension_pattern, '', svg_content)
            
            return svg_content
            
        except Exception as e:
            logger.error(f"Error populating template: {e}")
            raise
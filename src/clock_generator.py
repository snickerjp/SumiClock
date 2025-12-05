#!/usr/bin/env python3
from datetime import datetime
import os
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import pytz
import logging
from config import config
import requests
from io import BytesIO
from weather_icon_generator import WeatherIconGenerator
from template_renderer import TemplateRenderer

logger = logging.getLogger(__name__)

class ClockGenerator:
    def __init__(self, timezone=None):
        clock_config = config['clock']
        self.width = clock_config['width']
        self.height = clock_config['height']
        self.font_size = int(clock_config.get('font_size', 200) * 1.4)
        self.font_path = clock_config['font_path']
        self.date_font_size = clock_config.get('date_font_size', int(self.font_size * 0.3))
        self.weather_font_size = clock_config.get('weather_font_size', int(self.font_size * 0.25))
        self.timezone = pytz.timezone(timezone or clock_config['timezone'])
        self.dark_mode_start = clock_config.get('dark_mode_start', 18)
        self.dark_mode_end = clock_config.get('dark_mode_end', 6)
        
        # Weather configuration
        self.display_weather = clock_config.get('display_weather', False)
        self.weather_api_key = clock_config.get('weather_api_key', '')
        self.weather_city = clock_config.get('weather_city', 'Tokyo')
        self.weather_units = clock_config.get('weather_units', 'metric')
        self.weather_icon_size = clock_config.get('weather_icon_size', (180, 180))
        
        # Portrait mode configuration
        self.portrait_mode = clock_config.get('portrait_mode', False)
        
        # Template-based rendering configuration
        self.use_templates = clock_config.get('use_templates', True)
        self.template_dir = clock_config.get('template_dir', None)
        
        # Initialize renderers
        self.weather_icon_generator = WeatherIconGenerator(icon_size=self.weather_icon_size)
        self.template_renderer = TemplateRenderer(template_dir=self.template_dir)
        
        logger.info(f"Clock generator initialized with timezone: {self.timezone}, portrait mode: {self.portrait_mode}, templates: {self.use_templates}")

    def _is_dark_mode(self, hour):
        """
        Determine if dark mode should be active based on hour
        
        Args:
            hour: Current hour (0-23)
            
        Returns:
            bool: True if dark mode should be active, False otherwise
        """
        if self.dark_mode_start < self.dark_mode_end:
            # Simple case: dark from start to end (e.g., 22 to 6)
            return self.dark_mode_start <= hour < self.dark_mode_end
        else:
            # Complex case: dark mode spans midnight (e.g., 18 to 6)
            return hour >= self.dark_mode_start or hour < self.dark_mode_end

    def _get_weather_data(self):
        """Get weather data from OpenWeatherMap API"""
        if not self.display_weather:
            return None
            
        # Mock weather data for development without API key
        if not self.weather_api_key:
            logger.info("No API key provided, using mock weather data for development")
            return {
                "weather": [{"description": "clear sky", "icon": "01d"}],
                "main": {"temp": 18}
            }
            
        try:
            url = f"https://api.openweathermap.org/data/2.5/weather?q={self.weather_city}&units={self.weather_units}&appid={self.weather_api_key}"
            response = requests.get(url, timeout=5)
            
            if response.status_code == 200:
                return response.json()
            else:
                logger.error(f"Weather API error: {response.status_code} - {response.text}")
                return None
        except Exception as e:
            logger.error(f"Error fetching weather data: {e}")
            return None

    def _get_weather_icon(self, icon_code, is_dark=None):
        """
        Get a weather icon for the given code
        
        Args:
            icon_code: The OpenWeatherMap icon code (e.g., '01d')
            is_dark: Whether dark mode is active, defaults to current hour setting if None
            
        Returns:
            PIL.Image: The icon image in grayscale format
        """
        try:
            # Use provided is_dark value or determine from current time if not provided
            if is_dark is None:
                is_dark = self._is_dark_mode(datetime.now(self.timezone).hour)
                
            return self.weather_icon_generator.get_icon(icon_code, is_dark)
        except Exception as e:
            logger.error(f"Error getting weather icon: {e}")
            return None
    
    def _create_template_data(self, local_now, weather_data):
        """
        Create data dictionary for template rendering
        
        Args:
            local_now: Current datetime in local timezone
            weather_data: Weather data from API
            
        Returns:
            dict: Data for template rendering
        """
        # Format time and date
        current_time = local_now.strftime("%H:%M")
        current_date = local_now.strftime("%A, %B %d, %Y")
        
        # Create basic data dictionary
        data = {
            'time': current_time,
            'date': current_date
        }
        
        # Add weather data if available
        if weather_data:
            try:
                weather_desc = weather_data["weather"][0]["description"].capitalize()
                temp = round(weather_data["main"]["temp"])
                weather_icon_code = weather_data["weather"][0]["icon"]
                
                data['weather'] = {
                    'temp': temp,
                    'description': weather_desc,
                    'icon_code': weather_icon_code
                }
            except Exception as e:
                logger.error(f"Error processing weather data for template: {e}")
                
        return data

    def create_clock_image(self) -> Image.Image:
        # Get current time in specified timezone
        utc_now = datetime.now(pytz.UTC)
        local_now = utc_now.astimezone(self.timezone)
        
        # Determine if dark mode should be active
        is_dark = self._is_dark_mode(local_now.hour)
        
        # Get weather data if enabled
        weather_data = self._get_weather_data() if self.display_weather else None
        
        # Try template-based rendering first if enabled
        if self.use_templates:
            # Create data for template
            template_data = self._create_template_data(local_now, weather_data)
            
            # Determine orientation
            orientation = "portrait" if self.portrait_mode else "landscape"
            
            # Try to render using template
            image = self.template_renderer.render_clock(
                template_data, 
                self.width, 
                self.height, 
                orientation, 
                is_dark
            )
            
            # If template rendering succeeded, return the image
            if image:
                logger.info(f"Generated clock image using {orientation} template")
                return image
            
            # Otherwise, fall back to standard rendering
            logger.info("Template rendering failed, falling back to standard rendering")
        
        # Standard rendering (fallback)
        bg_color = 0 if is_dark else 255  # 0 = black, 255 = white
        text_color = 255 if is_dark else 0  # 255 = white, 0 = black
        
        # Create new image with appropriate background color
        image = Image.new('L', (self.width, self.height), bg_color)
        draw = ImageDraw.Draw(image)
        
        # Load fonts
        try:
            time_font = ImageFont.truetype(str(self.font_path), self.font_size)
            date_font = ImageFont.truetype(str(self.font_path), self.date_font_size)
            weather_font = ImageFont.truetype(str(self.font_path), self.weather_font_size)
            weather_desc_font = ImageFont.truetype(str(self.font_path), int(self.weather_font_size * 0.8))
        except OSError as e:
            logger.error(f"Failed to load font {self.font_path}: {e}")
            time_font = ImageFont.load_default()
            date_font = ImageFont.load_default()
            weather_font = ImageFont.load_default()
            weather_desc_font = ImageFont.load_default()
            logger.info("Using default font as fallback")
        
        # Format time and date
        current_time = local_now.strftime("%H:%M")
        current_date = local_now.strftime("%A, %B %d, %Y")
        
        # Calculate text positions for layout
        time_bbox = draw.textbbox((0, 0), current_time, font=time_font)
        time_width = time_bbox[2] - time_bbox[0]
        time_height = time_bbox[3] - time_bbox[1]
        
        date_bbox = draw.textbbox((0, 0), current_date, font=date_font)
        date_width = date_bbox[2] - date_bbox[0]
        date_height = date_bbox[3] - date_bbox[1]
        
        if self.portrait_mode:
            # Portrait mode layout
            # Center time horizontally and position it in the middle area
            time_x = (self.width - time_width) // 2
            time_y = (self.height // 2) - time_height  # Position time in the middle, accounting for its height
            
            # Position date centered above time with padding
            date_x = (self.width - date_width) // 2
            date_y = time_y - date_height - 40  # Place date above time with sufficient padding
            
            # Draw date and time
            draw.text((date_x, date_y), current_date, fill=text_color, font=date_font)
            draw.text((time_x, time_y), current_time, fill=text_color, font=time_font)
            
            # Add weather information if enabled (positioned at the bottom of the screen)
            if self.display_weather and weather_data:
                try:
                    # Extract weather information
                    weather_desc = weather_data["weather"][0]["description"].capitalize()
                    temp = round(weather_data["main"]["temp"])
                    weather_icon_code = weather_data["weather"][0]["icon"]
                    
                    # Format temperature text and calculate sizes
                    temp_text = f"{temp}°C"
                    
                    # Calculate text sizes
                    temp_bbox = draw.textbbox((0, 0), temp_text, font=weather_font)
                    temp_width = temp_bbox[2] - temp_bbox[0]
                    temp_height = temp_bbox[3] - temp_bbox[1]
                    
                    desc_bbox = draw.textbbox((0, 0), weather_desc, font=weather_desc_font)
                    desc_width = desc_bbox[2] - desc_bbox[0]
                    desc_height = desc_bbox[3] - desc_bbox[1]
                    
                    # Get weather icon
                    weather_icon = self._get_weather_icon(weather_icon_code, is_dark)
                    
                    # Position weather information at the bottom area of the screen
                    # Ensure enough space between time display and weather section
                    weather_section_y = int(self.height * 0.65)  # Adjusted to ensure clear separation from time
                    
                    if weather_icon:
                        # In portrait mode, stack elements vertically
                        icon_size = self.weather_icon_size[0]  # Assume square icon
                        
                        # Center icon horizontally
                        icon_x = (self.width - icon_size) // 2
                        icon_y = weather_section_y
                        
                        # Position temperature text centered below icon
                        temp_x = (self.width - temp_width) // 2
                        temp_y = icon_y + icon_size + 30  # Add padding below icon
                        
                        # Position description centered below temperature
                        desc_x = (self.width - desc_width) // 2
                        desc_y = temp_y + temp_height + 15  # Add padding below temperature
                        
                        # Paste icon
                        image.paste(weather_icon, (icon_x, icon_y), weather_icon.split()[-1])
                        
                        # Draw text elements
                        draw.text((temp_x, temp_y), temp_text, fill=text_color, font=weather_font)
                        draw.text((desc_x, desc_y), weather_desc, fill=text_color, font=weather_desc_font)
                    else:
                        # Fallback if no icon: display combined text
                        combined_text = f"{temp}°C ({weather_desc})"
                        combined_bbox = draw.textbbox((0, 0), combined_text, font=weather_font)
                        combined_width = combined_bbox[2] - combined_bbox[0]
                        
                        weather_x = (self.width - combined_width) // 2
                        weather_y = weather_section_y + 50  # Center in the weather section
                        draw.text((weather_x, weather_y), combined_text, fill=text_color, font=weather_font)
                except Exception as e:
                    logger.error(f"Error processing weather data: {e}")
        else:
            # Landscape mode (original layout)
            # Position time in center of the screen
            time_x = (self.width - time_width) // 2
            time_y = (self.height - time_height) // 2
            
            # Position date centered above time with padding
            date_x = (self.width - date_width) // 2
            date_y = time_y - date_height - 60  # increased padding for larger time display
            
            # Draw date and time
            draw.text((date_x, date_y), current_date, fill=text_color, font=date_font)
            draw.text((time_x, time_y), current_time, fill=text_color, font=time_font)
            
            # Add weather information if enabled
            if self.display_weather and weather_data:
                try:
                    # Extract weather information
                    weather_desc = weather_data["weather"][0]["description"].capitalize()
                    temp = round(weather_data["main"]["temp"])
                    weather_icon_code = weather_data["weather"][0]["icon"]
                    
                    # Format temperature text (larger) and description text (smaller)
                    temp_text = f"{temp}°C"
                    
                    # Calculate text sizes
                    temp_bbox = draw.textbbox((0, 0), temp_text, font=weather_font)
                    temp_width = temp_bbox[2] - temp_bbox[0]
                    temp_height = temp_bbox[3] - temp_bbox[1]
                    
                    desc_bbox = draw.textbbox((0, 0), weather_desc, font=weather_desc_font)
                    desc_width = desc_bbox[2] - desc_bbox[0]
                    desc_height = desc_bbox[3] - desc_bbox[1]
                    
                    # Make weather section appear at bottom of screen with adequate spacing
                    weather_y = time_y + time_height + 120  # Increased vertical spacing
                    
                    # Get weather icon with current dark mode setting to ensure consistency
                    weather_icon = self._get_weather_icon(weather_icon_code, is_dark)
                    if weather_icon:
                        # Use the configured icon size
                        icon_size = self.weather_icon_size[0]  # Assume square icon
                        
                        # Calculate total width with proper spacing
                        total_width = icon_size + 20 + temp_width + 15 + desc_width
                        
                        # Center the entire weather block
                        start_x = (self.width - total_width) // 2
                        
                        # Position each element
                        icon_x = start_x
                        temp_x = icon_x + icon_size + 20  # 20px after icon
                        desc_x = temp_x + temp_width + 15  # 15px after temperature
                        
                        # Align icon vertically with text
                        icon_y = weather_y - (icon_size - temp_height) // 2
                        
                        # Paste icon onto the main image with transparency
                        image.paste(weather_icon, (icon_x, icon_y), weather_icon.split()[-1])  # Use alpha channel as mask
                        
                        # Draw temperature text (larger) and description (smaller)
                        draw.text((temp_x, weather_y), temp_text, fill=text_color, font=weather_font)
                        draw.text((desc_x, weather_y + (temp_height - desc_height) // 2), 
                                weather_desc, fill=text_color, font=weather_desc_font)
                    else:
                        # Fallback if no icon available: center text only
                        combined_text = f"{temp}°C ({weather_desc})"
                        combined_bbox = draw.textbbox((0, 0), combined_text, font=weather_font)
                        combined_width = combined_bbox[2] - combined_bbox[0]
                        
                        weather_x = (self.width - combined_width) // 2
                        draw.text((weather_x, weather_y), combined_text, fill=text_color, font=weather_font)
                        
                except Exception as e:
                    logger.error(f"Error processing weather data: {e}")
        
        return image
    
    def save_clock_image(self, output_path: str = "clock.png"):
        """Generate and save clock image"""
        image = self.create_clock_image()
        image.save(output_path, "PNG", optimize=True)
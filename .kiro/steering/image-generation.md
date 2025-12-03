# Image Generation Guidelines for SumiClock

## E-Paper Display Characteristics

### Understanding E-Paper
- **Refresh Rate**: Slow (typically 1-2 seconds for full refresh)
- **Color Depth**: Usually 1-bit (black/white) or 4-bit (16 grayscales)
- **Persistence**: Images remain visible without power
- **Viewing Angle**: Excellent, similar to paper
- **Contrast**: High contrast in good lighting

### Design Implications
- Minimize unnecessary updates (use caching)
- Use pure black and white for best contrast
- Avoid complex gradients
- Keep designs simple and clear
- Consider ambient light conditions

## PIL/Pillow Best Practices

### Image Mode Selection
```python
# For E-paper displays, use grayscale mode
image = Image.new('L', (width, height), 255)  # 'L' = 8-bit grayscale
```

### Color Values
- `0`: Pure black (best for E-paper)
- `255`: Pure white (background)
- Avoid intermediate values unless necessary

### Font Rendering

#### Font Loading
```python
# Try to load custom font with fallback
try:
    font = ImageFont.truetype(font_path, font_size)
except OSError:
    logger.error(f"Failed to load font {font_path}")
    font = ImageFont.load_default()
```

#### Text Positioning
```python
# Get accurate text dimensions
text_bbox = draw.textbbox((0, 0), text, font=font)
text_width = text_bbox[2] - text_bbox[0]
text_height = text_bbox[3] - text_bbox[1]

# Center text
x = (image_width - text_width) // 2
y = (image_height - text_height) // 2
```

#### Anti-aliasing Considerations
- For E-paper: Consider disabling anti-aliasing for sharper text
- For high-DPI displays: Anti-aliasing improves readability
- Test on target device to determine best approach

## Timezone Handling

### Using pytz
```python
import pytz
from datetime import datetime

# Always work with UTC internally
utc_now = datetime.now(pytz.UTC)

# Convert to target timezone
timezone = pytz.timezone('Asia/Tokyo')
local_time = utc_now.astimezone(timezone)
```

### Common Timezones
- `UTC`: Coordinated Universal Time
- `Asia/Tokyo`: Japan Standard Time (JST)
- `America/New_York`: Eastern Time (ET)
- `Europe/London`: British Time (GMT/BST)
- `Australia/Sydney`: Australian Eastern Time (AET)

### Time Format
- Use 24-hour format for clarity: `%H:%M`
- Consider adding date for context: `%Y-%m-%d %H:%M`
- Respect locale preferences when possible

## Image Optimization

### PNG Optimization
```python
image.save(output_path, 'PNG', optimize=True)
```

### File Size Considerations
- E-paper devices often have limited bandwidth
- Smaller files = faster transfers
- PNG is ideal for high-contrast images
- Consider compression level vs quality trade-off

### Memory Management
- Generate images on-demand
- Use caching to avoid regeneration
- Clean up PIL Image objects when done
- Monitor memory usage in production

## Device-Specific Considerations

### Kindle
- Common resolutions: 1448x1072, 1680x1264, 1860x1440
- Supports PNG format
- Prefers high-contrast images
- Browser-based display via experimental browser

### Kobo
- Common resolutions: 1440x1920, 1404x1872, 1264x1680
- Supports PNG format
- Similar characteristics to Kindle
- Browser-based display

### Testing
- Test on actual devices when possible
- Use device simulators for initial testing
- Verify image dimensions match device resolution
- Check contrast and readability

## Performance Optimization

### Image Generation
- Cache generated images (30-60 seconds)
- Pre-calculate common values
- Minimize PIL operations
- Use efficient font loading

### Caching Strategy
- Cache by minute (not second) for clock displays
- Invalidate cache on configuration changes
- Monitor cache hit rate
- Adjust TTL based on usage patterns

## Future Enhancements

### Potential Features
- Date display alongside time
- Multiple timezone support in single image
- Weather information integration
- Battery-friendly update intervals
- Customizable layouts and themes
- Support for different E-paper resolutions

### Extensibility
- Modular design for easy feature addition
- Configuration-driven customization
- Plugin system for custom renderers
- Template-based layouts

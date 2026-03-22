"""Create Umbrella Corporation icon"""
from PIL import Image, ImageDraw

# Create 256x256 image
size = 256
img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
draw = ImageDraw.Draw(img)

# Background - red circle
center = size // 2
radius = 120
draw.ellipse([center-radius, center-radius, center+radius, center+radius], 
             fill=(220, 20, 20, 255))

# White border
draw.ellipse([center-radius+5, center-radius+5, center+radius-5, center+radius-5], 
             outline=(255, 255, 255, 255), width=8)

# Umbrella shape - white
# Top arc
draw.arc([center-80, center-60, center+80, center+60], 
         start=0, end=180, fill=(255, 255, 255, 255), width=12)

# Handle
draw.rectangle([center-6, center+20, center+6, center+80], 
               fill=(255, 255, 255, 255))

# Handle curve
draw.arc([center-20, center+65, center+20, center+95], 
         start=0, end=180, fill=(255, 255, 255, 255), width=12)

# Umbrella ribs (8 lines from center)
for angle in range(0, 180, 22):
    import math
    rad = math.radians(angle)
    x1 = center
    y1 = center - 10
    x2 = center + int(75 * math.sin(rad))
    y2 = center - 10 - int(75 * math.cos(rad))
    draw.line([x1, y1, x2, y2], fill=(255, 255, 255, 255), width=4)

# Save as ICO
img.save('umbrella.ico', format='ICO', sizes=[(256, 256), (128, 128), (64, 64), (32, 32), (16, 16)])
print("✓ Icon created: umbrella.ico")

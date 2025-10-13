#!/usr/bin/env python3
"""
Image Optimization Script
Converts PNG/JPG images to WebP format for better performance
Maintains original images as fallback
"""
from PIL import Image
import os

def convert_to_webp(image_path, quality=85):
    """Convert image to WebP format"""
    try:
        # Open image
        img = Image.open(image_path)

        # Convert RGBA to RGB if needed
        if img.mode in ('RGBA', 'LA'):
            background = Image.new('RGB', img.size, (255, 255, 255))
            background.paste(img, mask=img.split()[-1])
            img = background

        # Generate WebP path
        webp_path = os.path.splitext(image_path)[0] + '.webp'

        # Save as WebP
        img.save(webp_path, 'WebP', quality=quality, method=6)

        # Get file sizes
        original_size = os.path.getsize(image_path)
        webp_size = os.path.getsize(webp_path)
        savings = ((original_size - webp_size) / original_size) * 100

        print(f"✓ Converted: {image_path}")
        print(f"  Original: {original_size/1024:.2f} KB → WebP: {webp_size/1024:.2f} KB (Saved {savings:.1f}%)")

        return True
    except Exception as e:
        print(f"✗ Error converting {image_path}: {e}")
        return False

def optimize_images(static_dir='static'):
    """Optimize all images in static directory"""
    image_extensions = ('.png', '.jpg', '.jpeg')
    converted_count = 0

    # Walk through static directory
    for root, dirs, files in os.walk(static_dir):
        for file in files:
            if file.lower().endswith(image_extensions):
                image_path = os.path.join(root, file)
                webp_path = os.path.splitext(image_path)[0] + '.webp'

                # Skip if WebP already exists
                if os.path.exists(webp_path):
                    print(f"⊘ Skipped (already exists): {image_path}")
                    continue

                if convert_to_webp(image_path):
                    converted_count += 1

    print(f"\n{'='*60}")
    print(f"Optimization Complete: {converted_count} images converted to WebP")
    print(f"{'='*60}")

if __name__ == '__main__':
    optimize_images()

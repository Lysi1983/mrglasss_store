#!/usr/bin/env python3
"""
CSS Minification Script
Minifies CSS files to reduce file size
"""
import re
import os

def minify_css(css_content):
    """Minify CSS content"""
    # Remove comments
    css_content = re.sub(r'/\*.*?\*/', '', css_content, flags=re.DOTALL)

    # Remove whitespace
    css_content = re.sub(r'\s+', ' ', css_content)

    # Remove spaces around certain characters
    css_content = re.sub(r'\s*{\s*', '{', css_content)
    css_content = re.sub(r'\s*}\s*', '}', css_content)
    css_content = re.sub(r'\s*:\s*', ':', css_content)
    css_content = re.sub(r'\s*;\s*', ';', css_content)
    css_content = re.sub(r'\s*,\s*', ',', css_content)

    # Remove last semicolon in blocks
    css_content = re.sub(r';}', '}', css_content)

    return css_content.strip()

def minify_css_files(css_dir='static/css'):
    """Minify all CSS files"""
    minified_count = 0

    for filename in os.listdir(css_dir):
        if filename.endswith('.css') and not filename.endswith('.min.css'):
            css_path = os.path.join(css_dir, filename)
            min_path = os.path.join(css_dir, filename.replace('.css', '.min.css'))

            with open(css_path, 'r', encoding='utf-8') as f:
                css_content = f.read()

            minified = minify_css(css_content)

            with open(min_path, 'w', encoding='utf-8') as f:
                f.write(minified)

            original_size = os.path.getsize(css_path)
            minified_size = os.path.getsize(min_path)
            savings = ((original_size - minified_size) / original_size) * 100

            print(f"✓ Minified: {filename}")
            print(f"  Original: {original_size/1024:.2f} KB → Minified: {minified_size/1024:.2f} KB (Saved {savings:.1f}%)")
            minified_count += 1

    print(f"\n{'='*60}")
    print(f"CSS Minification Complete: {minified_count} files processed")
    print(f"{'='*60}")

if __name__ == '__main__':
    minify_css_files()

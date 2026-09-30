import os
import re

dir_path = r'c:\Users\Sudarsanan\Desktop\MWUS\itiz'
html_files = []

for root, dirs, files in os.walk(dir_path):
    for f in files:
        if f.endswith('.html') or f.endswith('.htm'):
            html_files.append(os.path.join(root, f))
print(f"Total HTML files: {len(html_files)}")

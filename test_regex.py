import os
import re

dir_path = r'c:\Users\Sudarsanan\Desktop\MWUS\itiz'
html_files = []

for root, dirs, files in os.walk(dir_path):
    for f in files:
        if f.endswith('.html') or f.endswith('.htm'):
            html_files.append(os.path.join(root, f))

pattern_to_remove = re.compile(
    r'<div[^>]*class="button-with-tooltip"[^>]*>.*?<img[^>]*class="icon-figma"[^>]*></a>\s*</div>\s*<a[^>]*href="[^"]*byq\.studio/template/itiz[^"]*"[^>]*class="cta-sales light w-inline-block"[^>]*>\s*<div>Buy</div>\s*</a>',
    re.DOTALL | re.IGNORECASE
)

count = 0
for file_path in html_files:
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    new_content, num_subs = pattern_to_remove.subn('', content)
    if num_subs > 0:
        count += 1
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)

print(f"Modified {count} files.")

from bs4 import BeautifulSoup
import os
from urllib.parse import urlparse

dir_path = r'c:\Users\Sudarsanan\Desktop\MWUS\itiz'
external_links = set()

for root, dirs, files in os.walk(dir_path):
    for f in files:
        if f.endswith('.html') or f.endswith('.htm'):
            filepath = os.path.join(root, f)
            with open(filepath, 'r', encoding='utf-8') as file:
                content = file.read()
            
            soup = BeautifulSoup(content, 'html.parser')
            
            for tag in soup.find_all(['a', 'img', 'script', 'link']):
                url = tag.get('href') or tag.get('src')
                if url:
                    parsed = urlparse(url)
                    if parsed.scheme in ['http', 'https']:
                        external_links.add(url)

print("List of third-party links:")
for link in sorted(external_links):
    print(link)

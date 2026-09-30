from bs4 import BeautifulSoup
import os

dir_path = r'c:\Users\Sudarsanan\Desktop\MWUS\itiz'
filepath = os.path.join(dir_path, 'index.htm')

with open(filepath, 'r', encoding='utf-8') as file:
    content = file.read()

soup = BeautifulSoup(content, 'html.parser')
for a in soup.find_all('a'):
    if 'figma' in str(a).lower():
        print(a)

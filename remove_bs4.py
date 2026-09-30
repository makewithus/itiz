from bs4 import BeautifulSoup
import os

dir_path = r'c:\Users\Sudarsanan\Desktop\MWUS\itiz'
count = 0

for root, dirs, files in os.walk(dir_path):
    for f in files:
        if f.endswith('.html') or f.endswith('.htm'):
            filepath = os.path.join(root, f)
            with open(filepath, 'r', encoding='utf-8') as file:
                content = file.read()
            
            soup = BeautifulSoup(content, 'html.parser')
            changed = False
            
            # Find the Figma button
            figma_buttons = soup.find_all('a', class_=lambda x: x and 'figma' in x.split())
            for btn in figma_buttons:
                parent = btn.parent
                if parent and 'button-with-tooltip' in parent.get('class', []):
                    parent.decompose()
                    changed = True
                else:
                    btn.decompose()
                    changed = True
            
            # Find the Buy button
            buy_buttons = soup.find_all('a', class_=lambda x: x and 'cta-sales' in x.split() and 'light' in x.split())
            for btn in buy_buttons:
                if 'Buy' in btn.get_text():
                    btn.decompose()
                    changed = True

            if changed:
                with open(filepath, 'w', encoding='utf-8') as file:
                    file.write(str(soup))
                count += 1

print(f'Modified {count} files.')

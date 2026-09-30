import os
import re

dir_path = r'c:\Users\Sudarsanan\Desktop\MWUS\itiz'

# =========================================================================
# TASK 1: Replace "Modulabs" (case-insensitive) with "Itiz" in all HTML files
# =========================================================================

# =========================================================================
# TASK 2: The "Pages" section (sales-cta-master block) needs to be in ALL pages.
# We extract it from index.htm and insert it into pages that are missing it.
# The insertion point is right before </section> that wraps the footer,
# actually right before <section class="footer"> 
# =========================================================================

# =========================================================================
# TASK 3: Remove https://webflow.com/ redirecting links in buttons
# (replace href="https://webflow.com/" with href="#")
# =========================================================================

# =========================================================================
# TASK 4: Make team names Indian in about.html
# =========================================================================

# =========================================================================
# TASK 5: Replace "Get Template" button text with "About Us" and update link
# The hero button with "Get Template" text (in button-wrap-hero) -> "About Us" + link to about page
# The CTA section "Get Template" (in button-wrap-cta section) -> "About Us" + link to about page  
# =========================================================================

# =========================================================================
# TASK 6: Make footer-legal-link hrefs all "#"
# =========================================================================

# --- Extract sales-cta-master block from index.htm ---
with open(os.path.join(dir_path, 'index.htm'), 'r', encoding='utf-8') as f:
    index_content = f.read()

sales_start = index_content.find('<div class="sales-cta-master">')
# Find matching closing tag
depth = 0
pos = sales_start
end = -1
while pos < len(index_content):
    if index_content[pos:pos+4] == '<div':
        depth += 1
    elif index_content[pos:pos+6] == '</div>':
        depth -= 1
        if depth == 0:
            end = pos + 6
            break
    pos += 1

sales_block_from_index = index_content[sales_start:end]
print(f"Extracted sales block length: {len(sales_block_from_index)}")

# Also extract the JS that goes with it (the Pages popup toggle script)
# Find the inline <script> that contains "Pages popup toggle"
js_start = index_content.find('<script type="text/javascript">\n      (function ()')
if js_start == -1:
    js_start = index_content.find('<script type="text/javascript">\r\n      (function ()')
js_end = index_content.find('</script>', js_start) + len('</script>')
sales_js_from_index = index_content[js_start:js_end]
print(f"Extracted JS length: {len(sales_js_from_index)}")

# --- Walk all HTML files ---
html_files = []
for root, dirs, files in os.walk(dir_path):
    for f in files:
        if f.endswith('.html') or f.endswith('.htm'):
            html_files.append(os.path.join(root, f))

print(f"Total HTML files: {len(html_files)}")

task_counts = {1:0, 2:0, 3:0, 4:0, 5:0, 6:0}

# Indian names map
name_map = {
    'John Kowalski': 'Arjun Nair',
    'Emily Carter': 'Priya Menon',
    'Jessica Mercedes': 'Deepa Krishnan',
    'Alex Thompson': 'Rahul Sharma',
    'Hannah Becker': 'Ananya Pillai',
    'David Lee': 'Kiran Raj'
}

def get_relative_about_path(filepath):
    """Get the relative path to about.html from a given file"""
    file_dir = os.path.dirname(filepath)
    rel = os.path.relpath(os.path.join(dir_path, 'about.html'), file_dir)
    return rel.replace('\\', '/')

def adapt_sales_block(block, filepath):
    """Adapt the sales block links to be relative to the target file"""
    file_dir = os.path.dirname(filepath)
    index_dir = dir_path
    
    # For files in subdirectories, paths need "../" prefix
    depth = len(os.path.relpath(file_dir, dir_path).split(os.sep))
    if os.path.relpath(file_dir, dir_path) == '.':
        depth = 0
    prefix = '../' * depth
    
    # Replace absolute paths in the block
    adapted = block
    if depth > 0:
        # Replace relative links (non-http) by adding prefix
        # These are hrefs like href="index.htm", href="about.html", href="service/..."
        def fix_href(m):
            href = m.group(1)
            if href.startswith('http') or href.startswith('#') or href.startswith('../'):
                return m.group(0)
            return f'href="{prefix}{href}"'
        adapted = re.sub(r'href="([^"]*)"', fix_href, adapted)
        
        # Fix src attributes for images
        def fix_src(m):
            src = m.group(1)
            if src.startswith('http') or src.startswith('../') or src.startswith('data:'):
                return m.group(0)
            return f'src="{prefix}{src}"'
        adapted = re.sub(r'src="([^"]*)"', fix_src, adapted)
    
    return adapted

for filepath in html_files:
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    changed = False
    
    # --- TASK 1: Replace Modulabs with Itiz ---
    new_content, n = re.subn(r'Modulabs', 'Itiz', content, flags=re.IGNORECASE)
    if n > 0:
        content = new_content
        task_counts[1] += n
        changed = True
    
    # --- TASK 2: Add Pages section if missing ---
    if 'sales-cta-master' not in content:
        # Find insertion point: right before <section class="footer">
        footer_pattern = re.search(r'<section class="footer">', content)
        if footer_pattern:
            insert_pos = footer_pattern.start()
            adapted_block = adapt_sales_block(sales_block_from_index, filepath)
            adapted_js = sales_js_from_index
            content = content[:insert_pos] + adapted_block + '\n' + content[insert_pos:]
            # Also insert the JS: find <script src=...jquery...> and insert before it
            jquery_pos = content.find('<script src=')
            if jquery_pos != -1:
                # Find the last script src to insert after
                last_script_src = content.rfind('<script src=')
                # Actually insert the JS right after </section> for footer
                # Better: insert before </body>
                body_end = content.rfind('</body>')
                if body_end != -1 and adapted_js not in content:
                    content = content[:body_end] + '\n' + adapted_js + '\n' + content[body_end:]
            task_counts[2] += 1
            changed = True
    
    # --- TASK 3: Replace webflow.com links in button hrefs with # ---
    # Match href="https://webflow.com/" in <a> tags
    new_content, n = re.subn(
        r'href="https://webflow\.com/"(\s+button="")',
        r'href="#"\1',
        content
    )
    if n > 0:
        content = new_content
        task_counts[3] += n
        changed = True
    # Also match without button="" following
    new_content, n = re.subn(
        r'href="https://webflow\.com/"',
        'href="#"',
        content
    )
    if n > 0:
        content = new_content
        task_counts[3] += n
        changed = True
    
    # --- TASK 4: Make team names Indian (only in about.html) ---
    if os.path.basename(filepath) == 'about.html':
        for old_name, new_name in name_map.items():
            new_content, n = re.subn(re.escape(old_name), new_name, content)
            if n > 0:
                content = new_content
                task_counts[4] += n
                changed = True
    
    # --- TASK 5: Replace "Get Template" with "About Us" + update link ---
    # Pattern: button in button-wrap-hero or button-wrap-cta containing "Get Template"
    # The text "Get Template" inside <div button-text="" class="button-text">Get Template</div>
    # Update the href of the parent <a> tag 
    
    about_rel = get_relative_about_path(filepath)
    
    # Replace href + text for hero "Get Template" button (in button-wrap-hero section linked to figma)
    # Pattern: <a href="...figma..." ... class="cta-main w-inline-block">...Get Template...</a>
    def replace_get_template_button(m):
        btn_html = m.group(0)
        if 'Get Template' in btn_html:
            # Replace href
            btn_html = re.sub(r'href="[^"]*"', f'href="{about_rel}"', btn_html, count=1)
            # Remove target="_blank" if present
            btn_html = btn_html.replace(' target="_blank"', '')
            # Replace button text
            btn_html = btn_html.replace('>Get Template<', '>About Us<')
            return btn_html
        return m.group(0)
    
    # Match <a ...>...</a> blocks that contain "Get Template"
    new_content = re.sub(
        r'<a\s[^>]*class="cta-main[^"]*"[^>]*>.*?Get Template.*?</a>',
        replace_get_template_button,
        content,
        flags=re.DOTALL
    )
    if new_content != content:
        task_counts[5] += 1
        content = new_content
        changed = True
    
    # --- TASK 6: Make footer-legal-link hrefs all "#" ---
    new_content, n = re.subn(
        r'(<a\s+href=")[^"]*("(?:\s+class="footer-legal-link"|[^>]*class="footer-legal-link")[^>]*>)',
        r'\1#\2',
        content
    )
    if n > 0:
        content = new_content
        task_counts[6] += n
        changed = True
    
    if changed:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)

print("\nResults:")
print(f"Task 1 - 'Modulabs' replaced: {task_counts[1]} occurrences")
print(f"Task 2 - Pages section added to: {task_counts[2]} files")
print(f"Task 3 - webflow.com links replaced: {task_counts[3]} occurrences")
print(f"Task 4 - Indian names replaced: {task_counts[4]} occurrences")
print(f"Task 5 - 'Get Template' replaced with 'About Us': {task_counts[5]} files")
print(f"Task 6 - footer-legal-links set to #: {task_counts[6]} occurrences")

# Webflow Template Editing Rules (Strict)

## Purpose
This document defines **strict limitations** for editing the Webflow HTML template.  
The AI must **only modify textual content** and **must not change any layout or structural code**.

---

# Absolute Restrictions

The following actions are **NOT ALLOWED**:

## HTML Structure
- Do NOT add new HTML elements
- Do NOT remove existing HTML elements
- Do NOT move elements
- Do NOT wrap elements in new divs
- Do NOT modify section hierarchy

## CSS
- Do NOT edit CSS files
- Do NOT add CSS
- Do NOT rename classes
- Do NOT remove classes
- Do NOT change styling

CSS Path:


68c9c39b88fdc718ad27d553/css/itiz-template.webflow.shared.4659d4835.css


## JavaScript
- Do NOT modify JS
- Do NOT add JS
- Do NOT remove JS
- Do NOT edit script tags

## Images
- Do NOT change image paths
- Do NOT remove images
- Do NOT replace images
- Do NOT add new images

## Layout
- Do NOT change spacing
- Do NOT change container sizes
- Do NOT redesign sections

---

# Allowed Actions

The AI is only allowed to modify **text content inside existing elements**.

Allowed modifications:

- Heading text
- Paragraph text
- Service descriptions
- Navbar labels
- Footer text
- Contact information

Example:

Original

```html
<h1>Service A</h1>
<p>Lorem ipsum</p>

Modified

<h1>Application Services</h1>
<p>Enterprise-grade application development including SaaS and ERP systems.</p>
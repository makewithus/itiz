# Project Structure

This document defines the **allowed pages and file structure** for editing.

The AI must ignore all files outside this list.

---

# CSS Location


68c9c39b88fdc718ad27d553/css/itiz-template.webflow.shared.4659d4835.css


---

# Pages Allowed For Editing


index.htm
about.html
404.html
401.html
privacy-policy.html
service/service-a.html
service/service-b.html
service/service-c.html
contact/contact.html


All other files must be ignored.

---

# Service Folder

Service pages are located inside:


service/


The base layout for all service pages is:


service/service-a.html


This file must be used as the **template for all service pages**.

---

# Service Pages To Create

The following service pages must exist:


service/application-services.html
service/marketing-services.html
service/3d-print.html
service/web-services.html
service/business-services.html
service/networking-hardware.html


---

# Cloning Rule

Each service page must be created by **cloning the structure of `service-a.html`**.

The following must remain identical:

- layout
- HTML structure
- class names
- images
- sections
- scripts

Only text content should change.

---

# Shared Components

## Navbar

Always replicate navbar from:


index.htm


## Footer

Always replicate footer from:


index.htm


These components must appear on all pages.
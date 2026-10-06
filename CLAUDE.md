# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

This is a personal portfolio website for Edmund Arvin De Leon, a Data Scientist. It's a static website built with vanilla HTML, CSS, and JavaScript, served via a simple Python HTTP server.

## Development Commands

### Running the Development Server

```bash
python server.py
```

The site runs on `http://0.0.0.0:8080` (configurable via PORT in server.py). The server includes CORS headers and cache-control headers for development.

### Project Structure

```
/
├── index.html          # Landing page with hero section
├── projects.html       # Projects showcase with filtering
├── about.html          # About page with skills and experience
├── server.py           # Python HTTP server with CORS support
├── styles/
│   └── main.css        # Single CSS file with all styles
├── js/
│   └── main.js         # Single JS file with all functionality
└── images/             # Project images and profile photo
```

## Architecture

### Single-Page Application Style

While technically multi-page, the site uses a cohesive design system:
- CSS Variables defined in `:root` for consistent theming (colors, shadows, transitions)
- Shared header/nav across all pages
- Common component patterns (cards, buttons, sections)

### Key Components

**Header (Fixed Navigation)**
- Fixed position header with blur effect
- Active page indication with underline
- Logo links to home

**Landing Page (index.html)**
- Full-height hero section with gradient background
- Social links (GitHub, LinkedIn, Kaggle)
- CTA buttons to projects and about pages

**Projects Page (projects.html)**
- Filter tabs for categorizing projects (all/ml/app/article)
- Grid layout with responsive project cards
- Each card has: image, title, description, tags, and CTA button
- Filtering logic in main.js uses `data-category` and `data-filter` attributes

**About Page (about.html)**
- Two-column layout: profile image (sticky) + content
- Skills organized in grid by category
- Contact section with social links

### JavaScript Functionality (js/main.js)

All interactivity is in a single file:
1. **Project filtering**: Shows/hides cards based on category
2. **Smooth scrolling**: For anchor links
3. **Header scroll effect**: Shadow appears on scroll
4. **Scroll animations**: Fade-in and slide-up effects for elements

The JS waits for `DOMContentLoaded` and checks for element existence before attaching listeners, making it safe to include on all pages.

### CSS Architecture (styles/main.css)

Organized in sections:
1. Base styles + CSS variables
2. Header styles
3. Landing page styles
4. Projects page styles
5. About page styles
6. Responsive breakpoints (992px, 768px, 576px)

Uses modern CSS features:
- CSS Grid for layouts (projects grid, skills grid, about container)
- Flexbox for alignment
- CSS Variables for theming
- Gradient text with `-webkit-background-clip`
- Smooth transitions and hover effects

## Design System

**Colors** (from CSS variables):
- Primary: `#6c5ce7` (purple)
- Secondary: `#a29bfe` (light purple)
- Accent: `#fd79a8` (pink)
- Text: `#2d3436` (dark gray)
- Light text: `#636e72` (medium gray)

**Typography**:
- Font: 'Poppins' from Google Fonts
- Weights: 300, 400, 500, 600, 700

**Spacing Pattern**:
- Page padding: `120px 5%` (top accounts for fixed header)
- Card padding: `1.5rem`
- Section gaps: `2-3rem`

**Button Pattern**:
- Two variants: `.btn.primary` (filled) and `.btn.secondary` (outline)
- Border radius: `50px`
- Hover: transform translateY and shadow changes

## Adding New Projects

To add a project to projects.html:

1. Add a new `.project-card` div in the `.projects-grid`
2. Set `data-category` attribute to: `ml`, `app`, or `article`
3. Include: image, title, description, tags, and link
4. Place project image in `/images/` directory

## Static Deployment

This site is deployment-ready for static hosting (GitHub Pages, Netlify, Vercel, etc.). The Python server is only for local development. For production, any static file server will work since there are no build steps or dependencies.

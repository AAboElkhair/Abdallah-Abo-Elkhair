# Adding an article

1. Create `_content/articles/<slug>.md` (English) and optionally `<slug>.ar.md` (Arabic). `<slug>` is the URL part, lowercase with dashes.
2. Start each file with this header, then write the article in Markdown (## headings, lists, > quotes, tables, links, images):

```
---
title: Article title
date: 2026-11-18
description: One or two sentences for Google and social previews (about 150 characters).
tags: Medical equipment planning, BIM
linkedin: https://www.linkedin.com/pulse/... (optional, original post; hides the matching LinkedIn card)
image: images/my-cover.jpg (optional, 1200x630, social preview)
updated: 2026-12-01 (optional)
---
```

3. Run `python3 _build/build_articles.py`. It writes the article pages, both listing pages, `feed.xml`, `ar/feed.xml` and the sitemap entries.
4. Commit and push. Folders starting with `_` are not published by GitHub Pages.

`_content/legacy-links.json` holds the LinkedIn-only cards shown until each one has a full article.

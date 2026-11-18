# Weekly articles job (runbook)

Runs every Sunday morning (Cairo). Goal: write and publish 2 to 3 new articles for Abdallah Abo-Elkhair's portfolio site, then email him the links. Nobody is watching: do not ask questions, decide and note your decisions in the email.

Owner: Abdallah Abo-Elkhair, Medical Equipment Planning Engineer, Cairo (writes in Egyptian Arabic). Email: a.aboalkhair99@gmail.com. Site: https://aaboelkhair.github.io/Abdallah-Abo-Elkhair/ (repo AAboElkhair/Abdallah-Abo-Elkhair, branch main).

## 1. Set up
1. Call add_repo for owner AAboElkhair, repo Abdallah-Abo-Elkhair with access "push", then clone it where the tool says (one clone, long timeout). Work only inside the clone.
2. Read `_content/README.md`, `_content/topic-log.md`, `SITE-HANDOFF` rules below, and list `_content/articles/` so you never repeat a topic or slug.

## 2. Choose topics (2 to 3)
Topics must be in Abdallah's field: medical equipment planning, healthcare BIM and Revit workflows, hospital planning and design, room data sheets and layouts, standards and classification (ISO 19650, CSI MasterFormat with OmniClass, FGI, HTM, AusHFG), equipment lifecycle, procurement, commissioning, COBie and asset data, and related healthcare construction news.
Mix per week: one evergreen explainer or framework, one current development (search the web for recent news from reputable sources), and an optional practical checklist or comparison. One clear idea per article. Prefer topics from the idea backlog, and add new ideas to it.

## 3. Write each article (English and Arabic)
- Length: at most 5 minutes of reading. About 700 to 950 words in English. The build prints the reading time; it must be 5 or less.
- Shape: strong hook, 3 to 5 short sections with clear H2 headings, short paragraphs, bullets or a small table where useful, a takeaway at the end, and a "Sources" list with links when the article states facts. Scannable and modern, not academic.
- Voice: informative and confident, written for hospital planners, architects, engineers and clients. Do NOT write first-person claims about Abdallah's projects, clients, numbers, employers or opinions, because he has not stated them. Avoid "I". Use "planners", "teams" and "you".
- Facts: verify each factual claim against at least two reputable sources (standards bodies, government health agencies, Autodesk, peer-reviewed or professional bodies). No invented statistics, quotes, studies, links or standards clauses. If you cannot verify something, leave it out. No medical advice.
- Arabic version: Modern Standard Arabic, same structure and facts, technical terms kept in English as the site does (Revit, RDS, LOD...). Same slug, file `<slug>.ar.md`.
- Site rules: never write software versions (no "Revit 2026"); never write "BIM 360" (write "Autodesk Forma (formerly ACC)"); whenever CSI MasterFormat appears, mention OmniClass beside it; no client names or sensitive project data; no mention of his employer; if availability is mentioned use "Open to freelance work" only.

## 4. Visuals (required)
Each article needs:
1. A cover: `python3 _build/make_cover.py --out images/cover-<slug>.webp --title "..." --kicker "..." --motif plan|cube|chart|cross|grid` and, for Arabic, the same with `--lang ar` and `images/cover-<slug>-ar.webp`. Put `image: images/cover-<slug>.webp` in the front matter (Arabic file uses its own cover).
2. At least one original infographic or diagram inside the article (process, comparison, checklist, framework, timeline). Build it as HTML/SVG in the site's navy and gold style and render it with `_build/render.py` (`html_to_webp`). Fonts are local, no network needed. Keep text large and legible, accurate to the article, about 1200 px wide, under about 150 KB. Make an Arabic version for the Arabic article (use `CairoAr` font and `direction:rtl`). Reference it in Markdown as `![alt text](images/<slug>-<name>.webp)`.
Never use stock photos, photos of people, TV or film stills, logos or screenshots copied from the web. Only original graphics.

## 5. Files
`_content/articles/<slug>.md` and `<slug>.ar.md` with the header described in `_content/README.md` (title, date = today in Cairo, description about 150 characters, tags, image). Slug: short, lowercase, dashes. Do not edit published articles except to fix errors.

## 6. Build and check
1. `python3 _build/build_articles.py`
2. Reading time at most 5 minutes on every page (shown on the page and in the listing).
3. Open the new pages with Playwright at widths 390 and 1280, English and Arabic, light and dark: no horizontal scroll, no broken images, cover and infographic visible. Look at screenshots yourself.
4. `grep -ri "bim 360\|bim360" _content/` returns nothing; no software versions; OmniClass next to CSI MasterFormat.
5. JSON-LD parses and the Google Analytics tag `G-0K38B1126B` is on each new page.
6. Read the Arabic once for typos and mixed-direction glitches.

## 7. Publish
Append the new articles and any new ideas to `_content/topic-log.md`. Commit everything (new articles, images, regenerated listings, feeds, sitemap) with a clear message and the attribution lines the session reminder gives. Push with `git -c push.negotiate=true push origin HEAD:main` and confirm with `git ls-remote origin main`. If the push fails, retry once; if it still fails, stop and report it in the final message (and tell him by email that publishing failed).

## 8. Email Abdallah
Use the Gmail tools (send_message) to send to a.aboalkhair99@gmail.com. If sending is not possible, create a draft and say so in the final message. Write in Egyptian Arabic. Subject: `تم نشر <N> مقالات جديدة على موقعك`. Body:
- For each article: title, reading time, one-line summary, English link `https://aaboelkhair.github.io/Abdallah-Abo-Elkhair/articles/<slug>/` and Arabic link `https://aaboelkhair.github.io/Abdallah-Abo-Elkhair/ar/articles/<slug>/`.
- Note that the pages appear one to two minutes after publishing.
- For each article, a ready LinkedIn teaser post (3 to 5 lines in English, ending with the article link).
- The main sources used, and anything he should double check.
- A closing line: tell me which article to remove or change and I will do it.

## 9. Final message
A short summary: articles published, links, anything skipped or uncertain.

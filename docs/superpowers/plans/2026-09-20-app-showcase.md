# App Showcase Implementation Plan

**Goal:** Help visitors understand and install Yoonique Labs apps.
**Architecture:** Static, crawlable pages generated from versioned app and guide data. A standalone script enhances the app directory without hiding content on load.
**Tech Stack:** Python standard library, HTML, CSS, vanilla JavaScript, GitHub Pages.

- [x] Create `scripts/build_showcase.py` using `data/apps.json`, `data/guides.json`, `data/blog-posts.json`. Generate homepage hero, nine cards, game feature, six guide links and six blog links. Preserve head verification and business footer.
- [x] Create `assets/showcase.css`: responsive navy/lime visual system, screenshot frames, app grid, readable sections and visible focus. Scope home styles and use explicit detail classes.
- [x] Create `assets/showcase.js`: search names and descriptions, combine category filter, announce result count and provide reset. Use textContent and hidden; no dependencies.
- [x] Enhance nine existing `apps/*/index.html` pages with shared navigation, visual hero, feature cards and guide/blog links. Preserve existing facts and privacy links.
- [x] Run `python scripts/build_showcase.py`; validate all local links, metadata, JSON-LD and image paths. Preview using `python -m http.server 8765 --bind 127.0.0.1`.
- [x] Browser-check desktop/mobile home, keyboard filtering, no-result reset, and game detail. Fix any overflow or failed interaction.
- [x] Commit reviewed files, merge approved branch to main, push and verify GitHub Pages build plus live homepage and changed detail pages.


## Validation — 2026-09-20

- 17 crawlable HTML pages passed local metadata, H1, JSON-LD, canonical, asset, internal-link and fragment checks.
- Desktop hero and game detail visually reviewed; actual screenshots displayed.
- 390px viewport: home and game detail had no horizontal overflow. App cards use one column.
- Game category shows 2 apps; search for 주차 shows 여기주차; no-results reset restores all 9 and focuses search; keyboard activation of 기록 shows 3 apps after clearing search.
- Homepage generation is repeatable. Existing site verification and ads/privacy files unchanged.
- Deployment status is recorded in the workspace release report after live checks.

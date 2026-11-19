# yooniquelabs-site
Yoonique Labs official website

## Showcase maintenance

- App facts: `data/apps.json`. Storefront extras (filter group, one-line promise, fact chips, card order, Play update date, screenshot count): `data/store.json`. Both files must list the same slugs.
- Images: `assets/icons/<slug>.webp` (Google Play icon) and `assets/shots/<slug>-N.webp` (Google Play screenshots, 640px tall).
- Guide titles: `data/guides.json`; verified Naver posts: `data/blog-posts.json`.
- Run `python scripts/build_showcase.py` to regenerate the homepage, create detail pages for new apps, refresh every detail page (icon, chips, screenshot gallery, related apps) and the sitemap.
- Validate with `python scripts/check_site.py` (requires BeautifulSoup 4 for this development-only checker).
- Preview: `python -m http.server 8765 --bind 127.0.0.1`.
- Directory controls progressively enhance static app cards; every app remains accessible without JavaScript.
- The Windows pages (`apps/pdf-reader`, `apps/unique-excel`) are produced by their own builders; the showcase build only refreshes their shared header. If those or the older growth/guide generators are used, run the showcase generator last.
- GitHub Pages publishes the root of `main`. Keep CNAME, verification files, app-ads.txt and existing public paths intact.

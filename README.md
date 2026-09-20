# yooniquelabs-site
Yoonique Labs official website

## Showcase maintenance

- App facts: `data/apps.json`; guide titles: `data/guides.json`; verified Naver posts: `data/blog-posts.json`.
- Run `python scripts/build_showcase.py` to regenerate the homepage and apply the shared detail/guide presentation.
- Validate with `python scripts/check_site.py` (requires BeautifulSoup 4 for this development-only checker).
- Preview: `python -m http.server 8765 --bind 127.0.0.1`.
- Directory controls progressively enhance static app cards; all nine apps remain accessible without JavaScript.
- If the older growth/guide generators outside this repository are used, run the showcase generator last to restore the current homepage and shared navigation.
- GitHub Pages publishes the root of `main`. Keep CNAME, verification files, app-ads.txt and existing public paths intact.

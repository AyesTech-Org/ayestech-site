# ayestech.com

Static corporate site of AyesTech, served by GitHub Pages at `https://ayestech.com` (custom domain in `CNAME`, DNS on Cloudflare).

## Editing

All pages are generated from one template so navigation, header and footer never drift:

```
python3 tools/build.py
```

Content lives in `tools/build.py` (one function per page). Commit the generated HTML together with the script; Pages serves the repository root as-is (`.nojekyll`).

## Paths that must stay stable

- `/pdf-reader/privacy/`, `/pdf-reader/support/`, `/pdf-reader/terms/` – linked from the ListenFly App Store listing.
- `/ads.txt` – Google AdSense / Ad Manager authorisation.
- `/app-ads.txt` – AdMob app-ads authorisation (also served on `listenfly.ayestech.com`).

The ListenFly product site is a separate repository (`AyesTech-Org/listenfly-site`, `listenfly.ayestech.com`); this site links to it.

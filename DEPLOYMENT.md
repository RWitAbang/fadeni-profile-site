# Deployment Instructions — Dr. Fadeni Executive Profile

## What you have
A static site (`index.html`, `styles.css`, `script.js`, `assets/`) driven by a single content file (`content.json`), plus a PDF generator (`generate_pdf.py`) that reads the same `content.json` so the site and PDF stay in sync — both content and, as closely as the two mediums allow, design.

## Updating content (no rebuild needed)
1. Edit `content.json` — change any text, add/remove a leadership entry, update an award, etc.
2. Re-upload `content.json` to your host (the site reads it live — no other files need to change).
3. Re-run `python3 generate_pdf.py` to regenerate the matching PDF, then upload the new `fadeni-executive-profile.pdf` alongside it.

No layout code needs to be touched for a content-only change.

## Adding the confirmed portrait
The Executive Profile section (Section 01) currently shows a labeled placeholder box instead of a photo — no confirmed headshot was available at build time. To add one:
1. Save the final approved headshot into `assets/` (e.g. `assets/portrait.jpg`).
2. In `content.json`, add a `"url"` field under `"photo"`, e.g. `"photo": { "url": "assets/portrait.jpg", ... }`.
3. The site will pick it up automatically (`script.js` already checks for `photo.url`); re-run `generate_pdf.py` afterward so the PDF matches.

## Hosting options (domain decision still pending — see brief)

**Option A — Subdomain of seindefadeni.com (recommended in the brief)**
1. Choose a static host (Netlify, Vercel, Cloudflare Pages, or GitHub Pages all work and are free at this scale).
2. Deploy the site files (`index.html`, `styles.css`, `script.js`, `content.json`, `assets/`) plus the PDF to that host.
3. In whoever manages the seindefadeni.com DNS, add a CNAME record for the chosen subdomain (e.g. `profile`) pointing to the host's provided address (e.g. `your-site.netlify.app`).
4. In the hosting provider's dashboard, add the custom subdomain (e.g. `profile.seindefadeni.com`) and enable HTTPS (most providers do this automatically once the CNAME resolves).

**Option B — Standalone domain**
1. Purchase the domain through any registrar.
2. Point its DNS to the same static host as above (the host will give you the exact records).
3. Add the domain in the hosting dashboard and enable HTTPS.

**Option C — Temporary GitHub Pages for internal preview (before client sign-off)**
If you want a quick, private-first way to show this to others before it's client-ready:
1. Push this folder to a **private** GitHub repository.
2. In the repo's Settings → Pages, enable GitHub Pages (branch: main, folder: root, or `/docs` if you move files there).
3. GitHub will give you a temporary `https://<username>.github.io/<repo>/` URL.
4. Keep the repo private until you're ready to share more broadly — GitHub Pages sites served from private repos are only visible to people with repo access (on paid GitHub plans) or you can keep the repo private and only share the built site with specific collaborators added to the repo.

## Important: this must be served, not opened as a local file
The site loads `content.json` via `fetch()`, which requires an actual web server (any of the hosts above, or a simple local server for testing — e.g. `python3 -m http.server`). Opening `index.html` directly by double-clicking it will not load the content, due to browser security restrictions on local file access.

## Fonts
The site uses Georgia (serif headlines) and Arial/Helvetica (body/nav text) — both are system fonts available by default on essentially every device, so there's nothing to load from Google Fonts and no external font dependency to break. If you'd prefer a different serif/sans pairing later, update the `font-family` declarations in `styles.css`.

## PDF font note
`generate_pdf.py` currently uses reportlab's built-in Times-Roman/Helvetica as close substitutes for the site's Georgia/Arial, since this build environment couldn't download real font files. For a pixel-perfect match, register the actual Georgia/Arial (or licensed equivalents) TTF files with reportlab and update the `fontName` values in `generate_pdf.py` — see the FONT NOTE at the bottom of that file.

## After deployment
- Add the confirmed portrait (see above) before this goes external — a placeholder box is not launch-ready.
- Add the schema.org cross-link: once the profile's final URL is known, confirm it's included in the `sameAs` field the page already generates, and add a matching link from www.seindefadeni.com back to the profile (see the brief's SEO section).
- Test on an actual mobile device, not just a resized browser window, before sharing the link externally.
- Confirm the `office@seindefadeni.com` contact address is real/monitored, or replace it with the client's preferred address, before this goes external.

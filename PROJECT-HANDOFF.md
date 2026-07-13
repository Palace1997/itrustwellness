# iTrust Wellness — Project Handoff & Context

A complete handoff for continuing this website on a new Claude account (or with any developer).
**Read this first.** The website files live in this folder on disk — any account that opens this
folder can edit them. This doc carries the *context* a new account won't have automatically:
decisions, preferences, structure, and how to build/run.

---

## 1. What this is
A redesigned marketing website for **iTrust Wellness**, a psychiatry / mental-health practice in
Upstate South Carolina (Greenville, Anderson, Spartanburg + telehealth). Tone: welcoming,
hopeful, "mental health is the priority, you belong here." Content was sourced from the live
itrustwellness.com. Design blends three references the client gave: SimplePractice, Talkspace,
and Mental Health America.

Static HTML/CSS/JS — **no framework, no build dependencies beyond `python3`** (which macOS has).

---

## 2. How to open / preview
- **Quick view:** double-click any `.html` in this folder (e.g. `index.html`) — opens in the browser.
- **Local server (recommended):** `python3 .claude/server.py` then visit `http://127.0.0.1:4173`.

## 3. How to edit (IMPORTANT — there's a build step)
The root `*.html` files are **GENERATED**. Do **not** edit them directly — your changes get
overwritten. Edit the sources in `src/`, then run the build:

```bash
python3 build.py
```

Sources:
- `src/templates/base.html` — the page shell (`<head>`, favicon, OG tags, header/footer slots).
- `src/templates/condition.html` — layout for the 11 condition pages.
- `src/partials/header.html` — nav + Treatments mega-menu (shared by every page).
- `src/partials/footer.html` — footer (shared by every page).
- `src/pages/*.html` — the body of each normal page, with a metadata comment on top
  (`title`, `desc`, `nav`).

`build.py` also holds the **CONDITIONS data** (name, tagline, intro copy, "Our Approach" points)
that generates all 11 `condition-*.html` pages. To edit a condition's copy or add a condition,
change the data in `build.py` and rebuild — the sidebar, mega-menu, and landing grid update
automatically.

CSS (`assets/styles.css`) and JS (`assets/script.js`) are linked directly — edits apply on
browser refresh, no rebuild needed. (Hard-refresh with Cmd+Shift+R; the browser caches CSS.)

---

## 4. Pages (19 total)
- `index.html` — Home: hero, feature tabs, "Conditions we treat", Insurance & payment (rotating
  3D logo ring + "View payment options & pricing" popup), testimonials, CTA.
- `about.html`, `treatments.html`, `patients.html`, `partners.html`, `locations.html`, `contact.html`
- `condition-*.html` ×11 (adhd, anxiety, bipolar-disorder, depression, ocd, ptsd,
  womens-mental-health, perinatal-mental-health, sleep-disorders, schizophrenia,
  substance-use-disorders) — full-bleed photo hero + sticky sidebar + "Understanding…" +
  "Our Approach" checklist.

---

## 5. Design system
**Fonts**
- Headings/titles: **GT Super Display** (licensed — Grilli Type), self-hosted in `assets/fonts/`
  (bold + medium, woff2/woff). ⚠️ Confirm the web/self-host license covers your deploy domain.
- Body: **Plus Jakarta Sans** (Google Fonts).
- Set via `--font-display` variable; Fraunces/serif are the fallback.

**Color palette** (all in `:root` of `assets/styles.css` — retarget the whole site from there):
| Variable | Value | Role |
|----------|-------|------|
| `--evergreen` | `#17281e` | darkest green — headings, footer, dark buttons |
| `--forest` | `#223a2a` | deep green — secondary accents/hovers |
| `--sage` | `#5f7a4a` | readable olive — links, eyebrows, icons (darkened for contrast) |
| `--amber` | `#94a276` | **accent** — CTAs, highlights, bands (this replaced the old yellow) |
| `--amber-deep` | `#7E8E62` | accent hover |
| `--mint` / `--mint-deep` | `#E7EDDF` / `#CFDCC0` | pale sage backgrounds / cards |
| `--cream` | `#F5F7F1` | neutral off-white page background |
| `--white` | `#fff` | |

> Note: the palette is intentionally all-green + white — **the yellow/amber was removed** per the
> client's brand sheet. `--amber` is kept as a variable name but now holds sage green.

---

## 6. Standing preferences / working style (carry these forward)
These were saved to memory during the build. A NEW account won't have them unless you keep them
here — so they're embedded:

1. **Unique image per section.** Never reuse a photo that's already placed anywhere on the site;
   every section gets its own fresh image. Photos are CC0 (StockSnap via the Openverse API);
   the API rate-limits in bursts, so a self-retrying background fetch script is the reliable way.
2. **Always provide sliders for visual tuning.** Whenever adjusting a visual value (image size,
   opacity, text size, animation speed), build a small `preview-*.html` with sticky range sliders
   driving CSS variables so the client can dial it in, then bake the chosen value into the real
   page. Sliders are a tuning tool only — never shipped on the live site.
3. **Titles in Title Case** (every word capitalized) — done via `text-transform:capitalize` on
   h1/h2, with `.nocaps` protecting "iTrust".
4. **No em dashes in headings** — use commas instead.

The full memory files are also bundled in **`project-memory/`** inside this folder
(`MEMORY.md`, `unique-images-per-section.md`, `slider-tuning-preference.md`) so they travel with
the project. On the new account, ask Claude to read `project-memory/` and re-save those facts to
its own memory. (The originals live in the old account's local
`~/.claude/projects/.../memory/`, which is why copies are kept here — memory is per-account.)

---

## 7. Assets
- `assets/styles.css` — all styling. `assets/script.js` — tabs, mobile menu, payment modal, newsletter/contact stubs.
- `assets/fonts/` — GT Super Display (4 files).
- `assets/photos/` — page hero photos (home, patients, partners, locations, contact, care-portrait, treatments-hero) + `photos/conditions/` (11 condition photos).
- `assets/insurers/` — 11 insurance logos (from itrustwellness.com) used in the ring + payment popup.
- `assets/itrust-logo.svg` (dark) + `assets/itrust-logo-light.svg` (white) — real iTrust logos.
- `assets/favicon.png`, `assets/og-image.svg` (social share card).

---

## 8. Placeholders to replace before launch
- **Forms** (contact, newsletter) are front-end stubs — connect to a real handler/email service.
- **Booking / Patient Portal** links point to `#` — wire to the real scheduling/EHR system.
- **Privacy / Terms / BAA** footer links point to `#`.
- **Testimonials** on the home page are illustrative — replace with real, consented client stories.
- **Free-assessment card** (patients page) and the **payment popup** are content mockups — confirm
  the real self-pay rates (the source site showed $259 vs $229 for the 60-min visit; $259 is used).
- **Condition photos** are calming stock — swap for licensed clinical photography if desired.

---

## 9. Going live (when ready)
It's a static site, so hosting is easy: Netlify, Vercel, GitHub Pages, Cloudflare Pages, or any
web host — just upload the folder (the root `*.html` + `assets/`). No server code required.
(You asked about sharing without those — see the chat's note: locally it's `python3 .claude/server.py`;
for others to reach it over the internet you do need a host or a tunnel like `ngrok`/`cloudflared`.)

---

## 10. To continue on your new account
1. Open this folder in Claude on the new account.
2. Say: "Read PROJECT-HANDOFF.md and README.md to get up to speed on this project."
3. Ask Claude to re-save the section 6 preferences into its memory so they stick going forward.

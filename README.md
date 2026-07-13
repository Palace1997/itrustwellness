# iTrust Wellness — New Website

A redesigned, welcoming single-page site for iTrust Wellness, built to feel like
*mental health is the priority* and every visitor belongs.

## Pages
- `index.html` — Home (hero, feature tabs, conditions preview, CTA)
- `about.html` — About Us (mission, what makes us different, values)
- `treatments.html` — Treatments (all conditions + treatment methods)
- `patients.html` — Patients (journey, new/current, free assessment, insurance, FAQ)
- `partners.html` — Partners (refer, employer programs, careers)
- `locations.html` — Locations (Greenville, Anderson, Spartanburg + telehealth)
- `contact.html` — Contact (message form, phone/fax/hours, location quick-links)

> **The `.html` files in the project root are GENERATED — do not edit them directly.**
> They are built from the `src/` folder by `build.py` (see below).

## Shared files
- `assets/styles.css` — design system + responsive layout
- `assets/script.js` — feature tabs, mobile menu, newsletter + contact form
- `assets/og-image.svg` — social-share preview image (referenced by Open Graph tags)

## Before you publish (placeholders to replace)
- **Testimonials** on the home page are illustrative examples — swap in real, consented
  client stories (the page already notes this in small print).
- **Photos** — hero/feature blocks use gradient placeholders (see "Replacing the
  placeholder images" below).
- **Forms** (contact + newsletter) are front-end stubs — connect them to a real handler.
- **Booking / Patient Portal / Privacy / Terms / BAA** links currently point to `#`.
- **Social image** is an SVG (`assets/og-image.svg`). Some networks (Facebook, X) don't
  render SVG previews — export a 1200×630 PNG and update the `og:image` / `twitter:image`
  paths in `src/templates/base.html` if you want guaranteed previews.

## Editing the site (static-site generator)
The header, footer, and crisis bar now live in **one place** each, so you never have to
update them in six files again. The site is assembled by a tiny zero-dependency Python
script (`build.py`, stdlib only — no Node/npm needed).

```
src/
  templates/base.html     ← the page shell (<head>, body wrapper, script tag)
  partials/header.html    ← crisis bar + nav  (shared by every page)
  partials/footer.html    ← footer            (shared by every page)
  pages/
    index.html            ← body content for the home page
    about.html            ← body content for About, etc.
    treatments.html
    patients.html
    partners.html
    locations.html
    contact.html
build.py                  ← run this to regenerate the root *.html files
```

### To make a change
1. Edit a file under `src/` (e.g. change a nav link once in `src/partials/header.html`,
   or edit page copy in `src/pages/about.html`).
2. Run the build:
   ```bash
   python3 build.py
   ```
3. The root `index.html`, `about.html`, … are regenerated. Refresh your browser.

### Page metadata
Each `src/pages/*.html` starts with a small comment block the build reads:
```html
<!--
title: About Us — iTrust Wellness
desc: A more personal approach to mental health...
nav: about
-->
```
- `title` → the browser tab title / `<title>`
- `desc` → the SEO meta description
- `nav` → which top-nav link gets highlighted (`about`, `treatments`, `patients`,
  `partners`, `locations`, or `home` for no highlight)

### Adding a new page
1. Create `src/pages/contact.html` with a metadata comment + body sections.
2. Add a `<a href="contact.html" data-nav="contact">Contact</a>` link to
   `src/partials/header.html` (and footer if desired).
3. Run `python3 build.py`. Done.

## Preview locally
```bash
python3 .claude/server.py
# then open http://127.0.0.1:4173 in your browser
```
(Or just double-click `index.html` to open it directly in a browser.)

## Design notes
The look blends the three reference sites you shared into one iTrust identity:
- **SimplePractice** → deep evergreen headlines, warm amber call-to-action, mint cards,
  the 3-card hero row, the feature-tab section, and the yellow footer.
- **Talkspace** → soft sage/calming greens and cream warmth.
- **Mental Health America** → a hopeful sky-blue trust accent.

### Color palette
| Token | Hex | Use |
|------|------|-----|
| Evergreen | `#143A2B` | Headlines, footer text |
| Forest | `#1F5C44` | Buttons, accents |
| Sage | `#3E8E6E` | Links, icons |
| Mint | `#DDF1E4` | Section backgrounds |
| Mint deep | `#BFE6CC` | Cards |
| Amber | `#FFC94B` | CTAs, highlights |
| Sky | `#5B9BB5` | Trust accent |
| Cream | `#FBF8F1` | Page background |

## Replacing the placeholder images
The three reference layouts (hero cards, feature visuals) currently use tasteful
CSS gradient placeholders so no copyrighted stock photos are used. To drop in real
iTrust photography, replace each `.photo-ph` / `.visual-ph` block's `background`
in `assets/styles.css` with `background: url('your-image.jpg') center/cover;`.

## Content sourced from
All copy (conditions, treatments, values, locations, hours, phone/fax, crisis lines,
insurance) was pulled from the live itrustwellness.com so nothing was lost in the move.

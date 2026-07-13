---
name: slider-tuning-preference
description: "Always give the user interactive sliders to tune visual values (image size, opacity, text size, etc.) for the iTrust site"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: b7b76f47-4830-49cc-a6d9-a2551aba68df
---

Whenever the user asks to adjust a visual property — image size/height, opacity, text size, spacing, blend, etc. — always build an interactive slider preview so they can dial in the value themselves live, then bake the chosen value into the real page. Do this proactively for every task of this kind, without being reminded.

**Why:** The user explicitly wants to control these values themselves rather than have me guess; they said "I want you to always have the slider every time I have this kind of task."

**How to apply:** Create a standalone `preview-*.html` (linking `assets/styles.css`) with sticky range sliders at the top that drive CSS variables (e.g. `--banner-h`, `--img-opacity`, `--h1-size`) via JS. Open it for the user. Sliders are a tuning tool only — never ship them on the live site. Once the user gives the value(s), set them on the real page (a CSS variable or value) and rebuild. Relates to [[unique-images-per-section]].

---
name: unique-images-per-section
description: Every website section must get its own unique image; never reuse an image already placed elsewhere on the site
metadata: 
  node_type: memory
  type: feedback
  originSessionId: b7b76f47-4830-49cc-a6d9-a2551aba68df
---

When adding an image to any part of the iTrust Wellness website, always source a NEW, unique photo. If an image is already used anywhere on the site, it must not be reused in another section.

**Why:** The user wants visual variety across the site; repeated photos look unpolished and lazy.

**How to apply:** Before placing any image, check what's already in use (home-hero, care-portrait, the 11 condition photos in `assets/photos/conditions/`, etc.). Fetch a fresh one (Openverse → StockSnap CC0, via the self-retrying background fetcher since the API rate-limits). When the user asks for "samples to choose from," provide that many distinct, unused options. Track which images are placed where so none repeat.

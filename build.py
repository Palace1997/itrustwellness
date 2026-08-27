#!/usr/bin/env python3
"""
iTrust Wellness, static site generator (zero dependencies, stdlib only).

Assembles each page from shared parts so the header/footer live in ONE place, AND
generates a detailed page for every condition from the CONDITIONS data below.

    src/templates/base.html       the HTML shell ({{TITLE}} {{DESC}} {{HEADER}} {{MAIN}} {{FOOTER}})
    src/templates/condition.html  the detailed condition-page body (sidebar + content)
    src/partials/header.html      crisis bar + nav + Treatments mega-menu
    src/partials/footer.html      footer
    src/pages/<name>.html         body of a normal page, with a metadata comment on top

Run:    python3 build.py
Output: <name>.html  +  condition-<slug>.html  written to the project root.
"""

import os
import re
import sys
import hashlib

ROOT = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(ROOT, "src")
PAGES_DIR = os.path.join(SRC, "pages")

# Canonical origin for <link rel="canonical">, og:url, and sitemap.xml.
# ---> CHANGE THIS ONE LINE when the custom domain goes live, i.e. to
#      "https://itrustwellness.com/". Everything else follows from it.
SITE_URL = "https://palace1997.github.io/itrustwellness/"

# ---------------------------------------------------------------------------
# CONDITIONS, the single source of truth for the treatments section.
# Each condition generates condition-<slug>.html and appears in the sidebar,
# the Treatments mega-menu, and the treatments landing grid.
# ---------------------------------------------------------------------------
CONDITIONS = [
    {
        "slug": "adhd", "name": "ADHD", "label": "Attention & Focus", "cat": "ADHD",
        "tagline": "Sharper focus, calmer days, care that works with how your brain works.",
        "intro": [
            "ADHD (Attention-Deficit/Hyperactivity Disorder) is a neurodevelopmental condition that affects <strong>focus, impulse control, and energy regulation</strong>. It can make everyday tasks, staying organized, following through, sitting still, feel harder than they should, for both children and adults.",
            "While ADHD can be frustrating, it is <strong>highly treatable</strong>. With the right support, the same mind that struggles to focus can also bring creativity, energy, and big-picture thinking. You are not lazy or broken, you simply need tools and care designed for you.",
        ],
        "lead": "ADHD shows up differently in everyone, so we never use a one-size-fits-all plan. We focus on understanding how your attention actually works.",
        "custom_title": "Skills & Lifestyle Strategies",
        "custom_desc": "Beyond medication, we help you build the routines, environments, and coping strategies that make focus feel natural.",
    },
    {
        "slug": "anxiety", "name": "Anxiety", "label": "Anxiety Disorders", "cat": "Anxiety",
        "tagline": "Quiet the noise and find steady ground again.",
        "intro": [
            "Anxiety is more than everyday worry, it's a persistent sense of <strong>fear, dread, or unease</strong> that can affect your thoughts, body, and daily life. It may show up as racing thoughts, a pounding heart, trouble sleeping, or avoiding the things you care about.",
            "Anxiety is one of the most common, and most treatable, mental health conditions. With the right care, the constant 'what ifs' can quiet down, and you can feel present, calm, and in control again.",
        ],
        "lead": "We help you understand what's driving your anxiety and give you practical, lasting ways to manage it.",
        "custom_title": "Calming, Evidence-Based Techniques",
        "custom_desc": "We pair medical care with proven strategies to help you regulate your nervous system and face triggers with confidence.",
    },
    {
        "slug": "bipolar-disorder", "name": "Bipolar Disorder", "label": "Mood Disorders", "cat": "Mood Disorders",
        "tagline": "Find balance and stability, and prevent the cycles from controlling your life.",
        "intro": [
            "Bipolar Disorder is a mental health condition characterized by <strong>significant mood swings</strong> that include emotional highs (mania or hypomania) and lows (depression). These shifts can affect sleep, energy, activity, judgment, behavior, and the ability to think clearly.",
            "While these symptoms can feel isolating, you are not alone. Bipolar Disorder is a <strong>manageable condition</strong>. With the right combination of medication, therapy, and lifestyle adjustments, you can achieve emotional stability and prevent the cycles from controlling your life.",
        ],
        "lead": "We know that Bipolar Disorder affects everyone differently. That is why we reject a 'one-size-fits-all' mentality, our approach treats the whole person to ensure long-term wellness.",
        "custom_title": "Mood Stabilization & Monitoring",
        "custom_desc": "We track patterns over time and fine-tune your plan to smooth out the highs and lows before they take hold.",
    },
    {
        "slug": "depression", "name": "Depression", "label": "Mood Disorders", "cat": "Mood Disorders",
        "tagline": "When everything feels heavy, you don't have to carry it alone.",
        "intro": [
            "Depression is more than sadness, it's a <strong>persistent low mood, loss of interest, and heaviness</strong> that can drain your energy, focus, and hope. It can affect how you sleep, eat, work, and connect with the people you love.",
            "Depression is real, common, and treatable. With compassionate, consistent care, the fog can lift, and the things that once felt impossible can start to feel possible again.",
        ],
        "lead": "We treat the whole person, not just the symptoms, to help you feel like yourself again.",
        "custom_title": "Therapy & Holistic Support",
        "custom_desc": "We connect you with therapeutic and lifestyle support that addresses the roots of depression, not only the surface.",
    },
    {
        "slug": "ocd", "name": "OCD", "label": "Anxiety & OCD", "cat": "OCD",
        "tagline": "Break the cycle of obsessions and compulsions, and reclaim your time.",
        "intro": [
            "Obsessive-Compulsive Disorder (OCD) involves <strong>unwanted, intrusive thoughts</strong> (obsessions) and <strong>repetitive behaviors or rituals</strong> (compulsions) done to ease the distress those thoughts cause. It can be time-consuming, exhausting, and deeply misunderstood.",
            "OCD is not a personality quirk, it's a treatable medical condition. With specialized, compassionate care, you can loosen the grip of these cycles and get your time and peace of mind back.",
        ],
        "lead": "We help you understand the OCD cycle and treat it with proven, specialized methods.",
        "custom_title": "Specialized OCD Care",
        "custom_desc": "We use evidence-based approaches designed specifically for OCD, rather than generic anxiety treatment.",
    },
    {
        "slug": "ptsd", "name": "PTSD", "label": "Trauma & PTSD", "cat": "Trauma",
        "tagline": "Healing from the past, at your pace, in a place that feels safe.",
        "intro": [
            "Post-Traumatic Stress Disorder (PTSD) can develop after experiencing or witnessing a traumatic event. It may bring <strong>flashbacks, nightmares, hypervigilance, or emotional numbness</strong> that make it hard to feel safe in the present.",
            "Trauma is not a weakness, and healing is possible. With trauma-informed, judgment-free care, you can process the past and build a sense of safety and stability again.",
        ],
        "lead": "We provide trauma-informed care that puts your safety and comfort first, always at your pace.",
        "custom_title": "Trauma-Informed, Safe Environment",
        "custom_desc": "Every step is built on safety, choice, and trust. You stay in control of your care from start to finish.",
    },
    {
        "slug": "womens-mental-health", "name": "Women's Mental Health", "label": "Women's Mental Health", "cat": "Women's Mental Health",
        "tagline": "Care that understands the whole of a woman's life.",
        "intro": [
            "Women face unique mental health experiences shaped by <strong>hormones, life transitions, relationships, and daily pressures</strong>. From PMS and PMDD to the changes of perimenopause and beyond, these shifts can affect mood, energy, and wellbeing.",
            "You deserve care that listens and understands. We provide thoughtful, affirming support tailored to the realities of women's lives at every stage.",
        ],
        "lead": "We tailor care to the hormonal, emotional, and life factors that uniquely affect women.",
        "custom_title": "Care Across Every Life Stage",
        "custom_desc": "From early adulthood through menopause and beyond, your plan evolves right along with you.",
    },
    {
        "slug": "perinatal-mental-health", "name": "Perinatal Mental Health", "label": "Women's Mental Health", "cat": "Perinatal Mental Health",
        "tagline": "Support for the journey into parenthood, for your mind, too.",
        "intro": [
            "The perinatal period, pregnancy and the first year after birth, is a time of <strong>enormous change</strong>. It's also when many parents experience anxiety, depression, or mood changes that can feel overwhelming and isolating.",
            "Perinatal mental health struggles are common and treatable, and seeking help is a sign of strength. We offer gentle, specialized care so you can care for your little one while feeling supported yourself.",
        ],
        "lead": "We provide specialized, compassionate care for the emotional health of new and expecting parents.",
        "custom_title": "Safe, Family-Centered Care",
        "custom_desc": "We carefully consider pregnancy and breastfeeding in every treatment decision, with you and your baby in mind.",
    },
    {
        "slug": "sleep-disorders", "name": "Psychological Sleep Disorders", "label": "Sleep Health", "cat": "Sleep Disorders",
        "tagline": "Rest that restores you, and a mind that can finally switch off.",
        "intro": [
            "Psychological sleep disorders, like insomnia tied to <strong>stress, anxiety, or depression</strong>, can leave you exhausted, foggy, and on edge. Poor sleep and mental health are deeply connected, each affecting the other.",
            "Better sleep is within reach. By treating the mind and the sleep cycle together, we help you fall asleep, stay asleep, and wake up feeling more like yourself.",
        ],
        "lead": "We address the mental and behavioral roots of sleep problems, not just the symptoms.",
        "custom_title": "Sleep & Mental Health Together",
        "custom_desc": "We treat the conditions that disrupt your sleep and the habits that keep it disrupted, as one connected plan.",
    },
    {
        "slug": "schizophrenia", "name": "Schizophrenia", "label": "Psychotic Disorders", "cat": "Schizophrenia",
        "tagline": "Steady, respectful care that supports a full and meaningful life.",
        "intro": [
            "Schizophrenia is a complex condition that can affect <strong>how a person thinks, feels, and perceives the world</strong>, sometimes including changes in thinking, hallucinations, or delusions. It is widely misunderstood and surrounded by stigma.",
            "With consistent, compassionate treatment, people living with schizophrenia can manage symptoms and lead stable, meaningful lives. We're here to support that journey with respect and expertise.",
        ],
        "lead": "We provide consistent, long-term care focused on stability, dignity, and quality of life.",
        "custom_title": "Long-Acting Treatment Options",
        "custom_desc": "When helpful, we offer Long-Acting Injectables (LAIs) that simplify treatment and support consistency.",
    },
    {
        "slug": "substance-use-disorders", "name": "Substance Use Disorders", "label": "Substance Use", "cat": "Substance Use",
        "tagline": "Recovery, without judgment, one supported step at a time.",
        "intro": [
            "Substance Use Disorder is a <strong>medical condition, not a moral failing</strong>. It affects the brain and behavior, making it hard to control the use of alcohol or other substances despite the harm it causes.",
            "Recovery is possible, and you don't have to do it alone. We offer supportive, non-judgmental care that meets you where you are and walks with you toward lasting change.",
        ],
        "lead": "We treat substance use as a health condition, with compassion and evidence-based care.",
        "custom_title": "Dual-Diagnosis Aware Care",
        "custom_desc": "We address substance use alongside any co-occurring mental health conditions, because they're often connected.",
    },
]

# Shared treatment methods (appear in the sidebar + mega-menu).
METHODS = [
    "Medication management",
    "Genetic testing",
    "Long-Acting Injectables (LAIs)",
    "Diagnostic assessments",
    "Substance use disorder care",
    "Personalized plans",
]

# The four standard "Our Approach" pillars (the custom item is inserted as #4).
PILLARS = [
    ("Thorough Mental Health Assessments",
     "Accurate diagnosis is the cornerstone of effective treatment. Our providers conduct comprehensive assessments to understand your specific symptoms, history, and triggers, so we can build a plan that truly fits you."),
    ("Expert Medication Management",
     "When medication is part of your care, our psychiatric specialists are highly trained in the latest options. We work closely with you to find the right regimen that eases symptoms while minimizing side effects."),
    ("Whole-Person, Personalized Care",
     "We treat the whole person, mind, body, and spirit, never a one-size-fits-all script. Your plan reflects your environment, lifestyle, and the goals that matter most to you."),
]
PILLAR_LAST = ("Ongoing Support & Frequent Check-ins",
               "Healing has a rhythm. We stay close with regular check-ins so your treatment keeps its momentum and you always know your next step.")


def read(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def write(path, text):
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)


def parse_front_matter(raw):
    m = re.match(r"\s*<!--(.*?)-->\s*", raw, re.DOTALL)
    meta = {}
    if not m:
        return meta, raw
    for line in m.group(1).strip().splitlines():
        if ":" in line:
            key, _, value = line.partition(":")
            meta[key.strip().lower()] = value.strip()
    return meta, raw[m.end():]


def activate_nav(header, nav_key):
    if not nav_key or nav_key == "home":
        return header
    return header.replace(
        f'<a href="{nav_key}.html" data-nav="{nav_key}"',
        f'<a href="{nav_key}.html" class="active" data-nav="{nav_key}"',
        1,
    )


def mega_conditions():
    return "\n".join(
        f'<a href="condition-{c["slug"]}.html">{c["name"]}</a>' for c in CONDITIONS
    )


def mega_methods():
    return "\n".join(f'<a href="treatments.html#methods">{m}</a>' for m in METHODS)


def sidebar(active_slug):
    links = []
    for c in CONDITIONS:
        cls = ' class="active"' if c["slug"] == active_slug else ""
        links.append(f'<a href="condition-{c["slug"]}.html"{cls}>{c["name"]}</a>')
    conds = "\n".join(links)
    meths = "\n".join(f'<a href="treatments.html#methods">{m}</a>' for m in METHODS)
    return (
        '<div class="side-group"><h4>What We Treat</h4>' + conds + "</div>"
        '<div class="side-group"><h4>Treatment Methods</h4>' + meths + "</div>"
    )


def approach_items(c):
    items = list(PILLARS)
    items.insert(3, (c["custom_title"], c["custom_desc"]))
    items.append(PILLAR_LAST)
    out = []
    for title, desc in items:
        out.append(
            '<li><span class="check" aria-hidden="true"></span>'
            f'<div><strong>{title}:</strong> {desc}</div></li>'
        )
    return "\n".join(out)


def canonical_for(name):
    """index.html canonicalises to the directory root, everything else to itself."""
    return SITE_URL if name == "index.html" else SITE_URL + name


# Patient portal is a demo we keep locally but not on the live/deploy build.
# Content wrapped in <!--PORTAL-->...<!--/PORTAL--> is kept only when building with
# the portal on; <!--NOPORTAL-->...<!--/NOPORTAL--> is the live-only alternate.
# Default is OFF (live-safe): plain `python3 build.py` omits the portal.
# Turn it on locally with:  WITH_PORTAL=1 python3 build.py
WITH_PORTAL = os.environ.get("WITH_PORTAL", "").strip().lower() in ("1", "true", "yes", "on")

def apply_portal(html):
    if WITH_PORTAL:
        html = re.sub(r"<!--NOPORTAL-->.*?<!--/NOPORTAL-->", "", html, flags=re.DOTALL)
        html = html.replace("<!--PORTAL-->", "").replace("<!--/PORTAL-->", "")
    else:
        html = re.sub(r"<!--PORTAL-->.*?<!--/PORTAL-->", "", html, flags=re.DOTALL)
        html = html.replace("<!--NOPORTAL-->", "").replace("<!--/NOPORTAL-->", "")
    return html


def build():
    base = read(os.path.join(SRC, "templates", "base.html"))
    # Cache-busting: append a short content hash to the CSS/JS so a deploy always
    # refreshes returning visitors, while unchanged files stay cached.
    def _ver(rel):
        try:
            h = hashlib.md5(open(os.path.join(ROOT, rel), "rb").read()).hexdigest()[:8]
            return rel + "?v=" + h
        except OSError:
            return rel
    base = base.replace("assets/styles.css", _ver("assets/styles.css"))
    base = base.replace("assets/script.js", _ver("assets/script.js"))
    cond_tpl = read(os.path.join(SRC, "templates", "condition.html"))
    footer = read(os.path.join(SRC, "partials", "footer.html"))
    header = read(os.path.join(SRC, "partials", "header.html"))
    # inject the mega-menu lists into the shared header once
    header = header.replace("{{NAV_CONDITIONS}}", mega_conditions()).replace("{{NAV_METHODS}}", mega_methods())

    built = []

    # --- normal pages ---
    for name in sorted(f for f in os.listdir(PAGES_DIR) if f.endswith(".html")):
        meta, body = parse_front_matter(read(os.path.join(PAGES_DIR, name)))
        html = (
            base
            .replace("{{CANONICAL}}", canonical_for(name))
            .replace("{{TITLE}}", meta.get("title", "iTrust Wellness"))
            .replace("{{DESC}}", meta.get("desc", ""))
            .replace("{{HEADER}}", activate_nav(header, meta.get("nav", "")))
            .replace("{{MAIN}}", body.strip())
            .replace("{{FOOTER}}", footer)
        )
        html = apply_portal(html)
        write(os.path.join(ROOT, name), html)
        built.append(name)

    # --- condition pages ---
    # hero image tuning per condition (framing, zoom, filters, overlay) — tuned via preview
    # slug: (posX%, posY%, zoom%, brightness%, contrast%, saturate%, blur_px, overlay%)
    HERO = {
        "adhd":                    (55, 14, 100,  93, 135, 148, 0,    89),
        "anxiety":                 (53, 61, 100, 107, 100, 115, 0,    87),
        "bipolar-disorder":        (50, 63, 100, 101, 119, 128, 0.2, 102),
        "depression":              (45, 81, 110,  88, 100,  95, 0,    61),
        "ocd":                     (52, 28, 100,  85, 105,  86, 0,    78),
        "ptsd":                    (50, 25, 100,  86, 100,  90, 0,    97),
        "womens-mental-health":    (50, 77, 100,  89, 100, 116, 0,   108),
        "perinatal-mental-health": (50, 26, 100,  84, 100, 116, 0,   100),
        "sleep-disorders":         (0,  97, 100,  99, 100, 115, 0,   103),
        "schizophrenia":           (50, 26, 100, 100, 100, 100, 0,   100),
        "substance-use-disorders": (50, 74, 100, 100, 100, 100, 0,   100),
    }

    def hero_style(slug):
        x, y, zoom, br, co, sa, bl, ov = HERO.get(slug, (50, 50, 100, 100, 100, 100, 0, 100))
        filt = f"brightness({br/100:g}) contrast({co/100:g}) saturate({sa/100:g})"
        if bl:
            filt += f" blur({bl:g}px)"
        return f"{x}% {y}%", f"{zoom/100:g}", filt, f"{ov/100:g}"

    for c in CONDITIONS:
        intro = "\n".join(f"<p>{p}</p>" for p in c["intro"])
        hpos, hzoom, hfilter, hov = hero_style(c["slug"])
        body = (
            cond_tpl
            .replace("{{NAME}}", c["name"])
            .replace("{{LABEL}}", c["label"])
            .replace("{{CAT}}", c["cat"])
            .replace("{{TAGLINE}}", c["tagline"])
            .replace("{{HEROPOS}}", hpos)
            .replace("{{HEROZOOM}}", hzoom)
            .replace("{{HEROFILTER}}", hfilter)
            .replace("{{HEROOV}}", hov)
            .replace("{{PHOTO}}", f'assets/photos/conditions/{c["slug"]}.jpg')
            .replace("{{INTRO}}", intro)
            .replace("{{LEAD}}", c["lead"])
            .replace("{{APPROACH_ITEMS}}", approach_items(c))
            .replace("{{SIDEBAR}}", sidebar(c["slug"]))
        )
        html = (
            base
            .replace("{{CANONICAL}}", canonical_for(f'condition-{c["slug"]}.html'))
            .replace("{{TITLE}}", f'{c["name"]} Treatment | iTrust Wellness')
            .replace("{{DESC}}", f'{c["name"]}: {c["tagline"]} Compassionate, personalized psychiatric care across South Carolina.')
            .replace("{{HEADER}}", activate_nav(header, "treatments"))
            .replace("{{MAIN}}", body.strip())
            .replace("{{FOOTER}}", footer)
        )
        html = apply_portal(html)
        write(os.path.join(ROOT, f'condition-{c["slug"]}.html'), html)
        built.append(f'condition-{c["slug"]}.html')

    # --- sitemap.xml + robots.txt (generated so they cannot drift from the pages) ---
    urls = [canonical_for(n) for n in built]
    sitemap = ['<?xml version="1.0" encoding="UTF-8"?>',
               '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for u in sorted(urls):
        # the homepage is the entry point, so it gets the higher priority
        priority = "1.0" if u == SITE_URL else "0.7"
        sitemap.append("  <url><loc>%s</loc><priority>%s</priority></url>" % (u, priority))
    sitemap.append("</urlset>")
    write(os.path.join(ROOT, "sitemap.xml"), "\n".join(sitemap) + "\n")

    write(os.path.join(ROOT, "robots.txt"),
          "User-agent: *\nAllow: /\n\nSitemap: %ssitemap.xml\n" % SITE_URL)

    print("Built %d page(s):" % len(built))
    for name in built:
        print("  ✓ %s" % name)


if __name__ == "__main__":
    build()

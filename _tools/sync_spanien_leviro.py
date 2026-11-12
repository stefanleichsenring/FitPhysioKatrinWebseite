#!/usr/bin/env python3
"""Erzeugt /spanien_leviro als 1:1-Kopie von /spanien im Leviro Corporate Design
und baut die eigenständige Datei für Manuel ("Fuer Manuel/kraft-mindset-leviro.html").

Ablauf: Inhalte nur in spanien/index.html ändern, dann
    python3 _tools/sync_spanien_leviro.py
ausführen. Jede Ersetzung muss treffen – sonst bricht das Skript mit Fehler ab,
damit nichts unbemerkt im FPK-Design durchrutscht.
"""
import base64, re, sys, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = ROOT / "spanien" / "index.html"
DST = ROOT / "spanien_leviro" / "index.html"
MANUEL = ROOT / "Fuer Manuel" / "kraft-mindset-leviro.html"


def rep(h, old, new, count=1, regex=False):
    n = len(re.findall(old, h, flags=re.S)) if regex else h.count(old)
    if n == 0:
        sys.exit(f"FEHLER: nicht gefunden:\n{old[:200]}")
    if count and n != count:
        sys.exit(f"FEHLER: {n}x statt {count}x gefunden:\n{old[:200]}")
    return re.sub(old, new, h, flags=re.S) if regex else h.replace(old, new)


def to_leviro(h):
    # ── Kopf ──
    h = rep(h, "| Fit.Physio.Katrin</title>", "| Leviro</title>")
    if 'name="robots"' not in h:  # Duplikat von /spanien → nicht indexieren
        h = rep(h, '  <link rel="canonical"',
                '  <!-- Kopie von /spanien – nicht indexieren (Duplicate Content) -->\n'
                '  <meta name="robots" content="noindex, nofollow">\n  <link rel="canonical"')
    h = rep(h, "https://fitphysiokatrin.com/spanien", "https://fitphysiokatrin.com/spanien_leviro", count=0)
    h = rep(h, '<link rel="icon" type="image/svg+xml" href="../favicon.svg">',
            '<link rel="icon" type="image/png" href="favicon.png">')
    h = rep(h, "family=Inter:wght@400;600;700;800&display=swap",
            "family=Raleway:wght@500;600;700;800&family=Source+Sans+3:wght@400;600;700&display=swap")
    h = rep(h, ":root { --sand: #b7792e; --sea: #2a8ea3; --text: #4a5a69; --line: #e3e8ee; --soft: #f5f7f9; }",
            ":root { --sand: #8B6F57; --sea: #9A7F66; --text: #5b5353; --line: #e5eadc; --soft: #f4f8ee; }")

    # ── Farben FPK → Leviro ──
    for a, b in [("rgba(210,35,78", "rgba(133,180,64"), ("rgba(44,59,73", "rgba(74,44,53"),
                 ("rgba(15,25,35", "rgba(52,30,37"), ("#D2234E", "#85B440"), ("#ff8fa8", "#9cc85a"),
                 ("#b01c3f", "#5f8a2a"), ("#8f1636", "#4f7524"), ("#2a8ea3", "#9A7F66"),
                 ("#4fb3c8", "#C9B49A"), ("#1f6f80", "#7A5E48"), ("#7a5cff", "#4A2C35"),
                 ("#f2c48d", "#D9C9B4"), ("#2C3B49", "#4A2C35"), ("#4a5a69", "#5b5353"),
                 ("#7b8894", "#8a8080"), ("#8a96a1", "#948a8a")]:
        h = h.replace(a, b)

    # ── Leviro-Design-Block ans Ende des Styles ──
    h = rep(h, "    .nav .nav__hamburger span { background: var(--navy); }\n  </style>",
            "    .nav .nav__hamburger span { background: var(--navy); }\n" + LEVIRO_CSS + "  </style>")

    # ── Logo, Footer ──
    h = rep(h, '<a href="../6am/" class="nav__logo">Fit<span>.</span>Physio<span>.</span>Katrin</a>',
            '<a href="https://leviro.ch" class="nav__logo nav__logo--img"><img src="images/leviro-logo.png" alt="Leviro – Dive deep, fly high"></a>')
    h = rep(h, '<div class="footer__logo">Fit<span>.</span>Physio<span>.</span>Katrin</div>',
            '<a href="https://leviro.ch" class="footer__logo"><img src="images/leviro-logo.png" alt="Leviro – Dive deep, fly high"></a>')
    h = rep(h, r'<nav class="footer__links" aria-label="Footer-Navigation">.*?</nav>',
            '<nav class="footer__links" aria-label="Footer-Navigation">\n'
            '        <a href="https://leviro.ch/index.php/impressum/">Impressum</a>\n'
            '        <a href="https://leviro.ch/index.php/datenschutz/">Datenschutz</a>\n'
            '        <a href="https://leviro.ch/agb/">AGB</a>\n'
            '        <a href="https://leviro.ch/kontakt/">Kontakt</a>\n'
            '      </nav>', regex=True)
    h = rep(h, "© 2026 Fit.Physio.Katrin · HL Geniusmind Ltd", "© 2026 Leviro · in Kooperation mit Fit.Physio.Katrin")
    h = rep(h, 'Ein Retreat von Fit.Physio.Katrin &amp; <a href="https://leviro.ch" target="_blank" rel="noopener">Leviro</a>',
            'Ein Retreat von Leviro &amp; <a href="https://fitphysiokatrin.com/6am/" target="_blank" rel="noopener">Fit.Physio.Katrin</a>')

    # ── Manuel zuerst: Venn-Grafik spiegeln ──
    m = re.search(r'<svg class="venn".*?</svg>', h, flags=re.S)
    if not m:
        sys.exit("FEHLER: Venn-Grafik nicht gefunden")
    v = m.group(0)
    v = v.replace("Kraft (Körper, mit Katrin) und Mindset (Geist, mit Manuel)",
                  "Mindset (Geist, mit Manuel) und Kraft (Körper, mit Katrin)")
    v = re.sub(r'(cx|x)="(165|295|105|355)"',
               lambda k: f'{k.group(1)}="{ {"165": "295", "295": "165", "105": "355", "355": "105"}[k.group(2)] }"', v)
    h = h.replace(m.group(0), v)

    # ── Manuel zuerst: Einleitung + Team-Karten ──
    h = rep(h, "Katrin setzt beim Körper an, Manuel bei den inneren Prozessen.",
            "Manuel setzt bei den inneren Prozessen an, Katrin beim Körper.")
    t = re.search(r'(<div class="team">\s*)(<article class="member fade-up">)(.*?</article>)(\s*)'
                  r'(<article class="member fade-up fade-up-delay-1">)(.*?</article>)', h, flags=re.S)
    if not t:
        sys.exit("FEHLER: Team-Karten nicht gefunden")
    h = h.replace(t.group(0), t.group(1) + t.group(2) + t.group(6) + t.group(4) + t.group(5) + t.group(3))

    # ── Kein WhatsApp-Button: nur die FPK-Community schreibt Katrin ──
    h = rep(h, r'<a class="wa-float".*?</a>\n\n', "", regex=True)
    h = rep(h, r'  // WhatsApp-Button:.*?\}\)\(\);\n', "", regex=True)
    if "wa.me" in h or 'id="waFloat"' in h:
        sys.exit("FEHLER: WhatsApp-Reste in der Leviro-Version")

    # ── Leviro-Hinweise aus Leviro-Sicht formulieren ──
    h = h.replace("Anmeldung &amp; Bezahlung laufen sicher über unseren Vertrauenspartner <strong>Leviro</strong>, mit dem wir das Retreat gemeinsam veranstalten.",
            "Anmeldung &amp; Bezahlung laufen sicher und direkt über <strong>Leviro</strong> – wir veranstalten das Retreat gemeinsam mit Fit.Physio.Katrin.")
    h = h.replace('Die Anmeldung und Bezahlung wickelt unser Vertrauenspartner <a href="https://leviro.ch" target="_blank" rel="noopener">Leviro</a> für uns ab.',
            'Die Anmeldung und Bezahlung läuft direkt über <a href="https://leviro.ch" target="_blank" rel="noopener">Leviro</a>.')
    h = h.replace("Leviro ist unser Partner, mit dem wir das Retreat gemeinsam veranstalten.",
            "Leviro veranstaltet das Retreat gemeinsam mit Fit.Physio.Katrin.")

    if re.search(r"#D2234E|rgba\(210,35,78|Fit<span>\.</span>Physio|unseren Vertrauenspartner|Leviro ist unser Partner", h):
        sys.exit("FEHLER: FPK-Reste in der Leviro-Version")
    return h


LEVIRO_CSS = """
    /* ── Leviro Corporate Design (muss zuletzt stehen) ── */
    :root { --navy: #4A2C35; --red: #85B440; --red-dark: #698E33; }
    body, p, a, button, input, li { font-family: 'Source Sans 3', 'Source Sans Pro', sans-serif; }
    h1, h2, h3, h4, blockquote, .eyebrow, .rt-badge, .btn-red, .btn-ghost, .btn-white, .nav__cta, .nav__links a,
    .pillar__tag, .rhythm__time, .tl__date, .member__role, .member__stat, .price-card__label,
    .price-card__num, .countdown__num, .countdown__label, .spots-bar__text, .faq-item__q { font-family: 'Raleway', sans-serif; }
    h1, h2 { font-weight: 800; letter-spacing: -0.01em; }
    p { font-size: 1.05rem; }
    .rt-hero h1 em, .grad { background: linear-gradient(135deg, #5f8a2a, #85B440); -webkit-background-clip: text; background-clip: text; }
    .eyebrow { color: #698E33; }
    .price-card { background: linear-gradient(160deg, #73A136 0%, #4f7524 100%); }
    .price-card .btn-white { color: #4f7524; }
    .btn-red:hover { background: #698E33; }
    .trust-item__icon { background: rgba(133,180,64,0.15); }
    .nav__logo--img img { height: 54px; width: auto; display: block; transition: height .3s; }
    .nav.scrolled .nav__logo--img img { height: 42px; }
    .footer { background: var(--soft); border-top: 1px solid var(--line); }
    .footer__logo img { height: 64px; width: auto; display: block; margin: 0 auto; }
    .footer__links a { color: var(--navy); }
    .footer__copy { color: #8a8080; }
"""


def standalone(h):
    """Alles in eine Datei: CSS, JS, Bilder eingebettet; ohne noindex; URLs auf leviro.ch."""
    d = DST.parent
    uri = lambda p, mime: f"data:{mime};base64," + base64.b64encode(p.read_bytes()).decode()
    h = re.sub(r'  <!--[^>]*nicht indexieren[^>]*-->\n  <meta name="robots"[^>]*>\n', "", h)
    h = re.sub(r'  <meta property="og:image"[^>]*>\n', "", h)
    h = h.replace("https://fitphysiokatrin.com/spanien_leviro", "https://leviro.ch/kraft-mindset/")
    h = rep(h, '<link rel="stylesheet" href="../assets/css/style.css">',
            "<style>\n" + (ROOT / "assets/css/style.css").read_text(encoding="utf-8") + "\n</style>")
    h = rep(h, '<script src="../assets/js/script.js" defer></script>',
            "<script>\n" + (ROOT / "assets/js/script.js").read_text(encoding="utf-8") + "\n</script>")
    h = rep(h, 'href="favicon.png"', 'href="' + uri(d / "favicon.png", "image/png") + '"')
    for name in ["terrasse.jpg", "bucht.jpg", "manuel.jpg", "katrin.jpg", "leviro-logo.png"]:
        h = h.replace("images/" + name, uri(d / "images" / name, "image/png" if name.endswith("png") else "image/jpeg"))
    left = re.findall(r'(?:src|href)="(?!https?:|data:|#|mailto:|tel:)[^"]+"|url\(\'(?!data:)[^\']+\'\)', h)
    if left:
        sys.exit(f"FEHLER: nicht eingebettete Pfade: {left}")
    return h


if __name__ == "__main__":
    src = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else SRC
    out = to_leviro(src.read_text(encoding="utf-8"))
    if len(sys.argv) > 2:  # Testmodus: nur in Datei schreiben
        pathlib.Path(sys.argv[2]).write_text(out, encoding="utf-8"); sys.exit()
    DST.write_text(out, encoding="utf-8")
    MANUEL.parent.mkdir(exist_ok=True)
    MANUEL.write_text(standalone(out), encoding="utf-8")
    print(f"ok: {DST.relative_to(ROOT)} und {MANUEL.relative_to(ROOT)} ({MANUEL.stat().st_size // 1024} KB)")

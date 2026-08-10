#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Générateur du dépliant « Appartements à louer ».

    python3 build.py            → régénère les 3 chartes (HTML + PDF)
    python3 build.py --no-pdf   → HTML seulement (plus rapide)

Format : A4 paysage (297 × 210 mm), 4 volets de 74,25 mm, pli accordéon.
Le contenu se modifie dans contenu.py, l'apparence dans chartes.py.
"""
import argparse
import base64
import json
import os
import re
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from contenu import CONTENU          # noqa: E402
from chartes import CHARTES          # noqa: E402

CACHE = os.path.join(HERE, ".fonts-cache")
UA = ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

# Familles Google Fonts utilisées par les chartes, embarquées en base64
# pour que chaque HTML soit autonome (impression hors ligne, envoi par mail).
FAMILLES = {
    "Fraunces":        "family=Fraunces:opsz,wght@9..144,400..900",
    "Inter":           "family=Inter:wght@300..800",
    "Marcellus":       "family=Marcellus:wght@400",
    "Montserrat":      "family=Montserrat:wght@400..800",
    "Outfit":          "family=Outfit:wght@300..800",
    "InstrumentSerif": "family=Instrument+Serif:ital@0;1",
}


# --------------------------------------------------------------------------
#  Polices
# --------------------------------------------------------------------------
def polices():
    """Renvoie {famille: css @font-face avec woff2 en base64}."""
    manifeste = os.path.join(CACHE, "polices.json")
    if os.path.exists(manifeste):
        return json.load(open(manifeste, encoding="utf-8"))

    os.makedirs(CACHE, exist_ok=True)
    out = {}
    for nom, requete in FAMILLES.items():
        url = "https://fonts.googleapis.com/css2?%s&display=swap" % requete
        css = subprocess.run(["curl", "-sS", "-m", "30", "-A", UA, url],
                             capture_output=True, text=True).stdout
        faces = []
        morceaux = re.split(r"/\*\s*([a-z\-]+)\s*\*/", css)
        for i in range(1, len(morceaux), 2):
            sous_ensemble, corps = morceaux[i], morceaux[i + 1]
            if sous_ensemble not in ("latin", "latin-ext"):
                continue                       # on jette cyrillique, grec, vietnamien…
            for m in re.finditer(r"@font-face\s*\{[^}]*\}", corps):
                face = m.group(0)
                lien = re.search(r"url\((https://[^)]+\.woff2)\)", face)
                if not lien:
                    continue
                fichier = os.path.join(CACHE, lien.group(1).split("/")[-1])
                if not os.path.exists(fichier):
                    subprocess.run(["curl", "-sS", "-m", "40", "-A", UA,
                                    lien.group(1), "-o", fichier], check=True)
                b64 = base64.b64encode(open(fichier, "rb").read()).decode()
                faces.append(face.replace(lien.group(1),
                                          "data:font/woff2;base64," + b64))
        out[nom] = "\n".join(faces)
        print("   police %-16s %4d Ko" % (nom, sum(map(len, faces)) // 1024))
    json.dump(out, open(manifeste, "w", encoding="utf-8"))
    return out


# --------------------------------------------------------------------------
#  QR code
# --------------------------------------------------------------------------
def qr_svg(cible, couleur):
    """QR code en image de fond : se met à l'échelle proprement à l'impression."""
    try:
        import segno
    except ImportError:
        return '<span class="qr-img"></span>'
    import io
    qr = segno.make(cible, error="m")
    buf = io.BytesIO()
    qr.save(buf, kind="svg", scale=10, dark=couleur, light=None, border=0,
            xmldecl=False, svgns=True, nl=False)
    uri = base64.b64encode(buf.getvalue()).decode()
    return ('<span class="qr-img" style="background-image:'
            'url(data:image/svg+xml;base64,%s)"></span>' % uri)


# --------------------------------------------------------------------------
#  Illustrations vectorielles (utilisées si aucune photo n'est fournie)
# --------------------------------------------------------------------------
def _uri(svg):
    return "url(\"data:image/svg+xml;base64,%s\")" % base64.b64encode(
        svg.encode("utf-8")).decode()


def art(nom, p):
    """p = palette de la charte : ciel, masse, clair, accent, trait."""
    ciel, masse, clair, accent, trait = (p["ciel"], p["masse"], p["clair"],
                                         p["accent"], p["trait"])

    # Les proportions des viewBox suivent celles des cadres CSS (≈ 0,62 pour la
    # couverture, ≈ 0,93 pour les fiches) afin qu'aucun sujet ne soit rogné.
    if nom == "couverture":
        fenetres = ""
        for i, x in enumerate((36, 82, 128, 174)):
            for j, y in enumerate((302, 340)):
                c = accent if (i + j) % 3 == 0 else clair
                fenetres += ('<rect x="%d" y="%d" width="22" height="24" rx="11" '
                             'fill="%s" opacity=".92"/>' % (x, y, c))
        return _uri(f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 240 384">
<rect width="240" height="384" fill="{ciel}"/>
<circle cx="152" cy="112" r="56" fill="{accent}"/>
<path d="M0 258 C 44 194 78 192 116 240 C 142 274 160 276 190 250 C 208 234 226 232 240 242 L240 384 L0 384 Z" fill="{masse}" opacity=".92"/>
<path d="M0 296 C 40 252 70 250 104 286 C 134 318 168 314 200 286 C 216 272 230 270 240 276 L240 384 L0 384 Z" fill="{trait}" opacity=".6"/>
<rect x="26" y="288" width="188" height="96" rx="5" fill="{masse}"/>
<rect x="26" y="288" width="188" height="6" fill="{clair}" opacity=".3"/>
{fenetres}
</svg>""")

    if nom == "facade":
        fenetres = ""
        for i, x in enumerate((56, 104, 152, 200)):
            for j, y in enumerate((122, 174, 226)):
                c = accent if (i * 3 + j) % 5 == 0 else clair
                fenetres += ('<rect x="%d" y="%d" width="26" height="34" rx="13" '
                             'fill="%s" opacity=".92"/>' % (x, y, c))
        return _uri(f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 280 300">
<rect width="280" height="300" fill="{ciel}"/>
<circle cx="230" cy="54" r="30" fill="{accent}" opacity=".85"/>
<rect x="40" y="90" width="204" height="210" rx="4" fill="{masse}"/>
<rect x="40" y="90" width="204" height="8" fill="{clair}" opacity=".3"/>
{fenetres}
<path d="M126 300 v-38 a16 16 0 0 1 32 0 v38 z" fill="{clair}" opacity=".9"/>
</svg>""")

    if nom == "interieur":
        return _uri(f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 280 300">
<rect width="280" height="300" fill="{ciel}"/>
<path d="M74 208 L110 40 L200 40 L238 208 Z" fill="{accent}" opacity=".2"/>
<path d="M80 44 h116 v150 h-116 z" fill="{clair}"/>
<path d="M80 44 h116 v150 h-116 z M138 44 v150 M80 119 h116" fill="none" stroke="{masse}" stroke-width="5"/>
<rect x="66" y="196" width="144" height="7" rx="3.5" fill="{masse}"/>
<path d="M192 300 v-44 h46 v44 z" fill="{masse}" opacity=".2"/>
<path d="M215 256 c-27 -6 -31 -35 -6 -45 c23 -10 39 10 31 31" fill="{accent}" opacity=".85"/>
<path d="M215 256 v-42" stroke="{masse}" stroke-width="4" fill="none"/>
<rect x="52" y="244" width="76" height="56" rx="8" fill="{trait}" opacity=".55"/>
</svg>""")

    if nom == "sejour":
        return _uri(f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 280 300">
<rect width="280" height="300" fill="{ciel}"/>
<circle cx="74" cy="64" r="34" fill="{accent}" opacity=".8"/>
<rect x="140" y="32" width="94" height="74" rx="6" fill="{clair}" opacity=".85"/>
<rect x="140" y="32" width="94" height="74" rx="6" fill="none" stroke="{masse}" stroke-width="4"/>
<ellipse cx="142" cy="266" rx="112" ry="20" fill="{trait}" opacity=".45"/>
<rect x="54" y="184" width="176" height="58" rx="20" fill="{masse}"/>
<rect x="44" y="198" width="26" height="48" rx="13" fill="{masse}"/>
<rect x="214" y="198" width="26" height="48" rx="13" fill="{masse}"/>
<rect x="72" y="167" width="62" height="30" rx="15" fill="{accent}" opacity=".9"/>
<rect x="146" y="167" width="62" height="30" rx="15" fill="{clair}" opacity=".9"/>
<path d="M244 176 v-76 h-36" fill="none" stroke="{masse}" stroke-width="4"/>
<circle cx="206" cy="100" r="15" fill="{accent}"/>
</svg>""")

    if nom == "bandeau":       # panorama continu sur les 4 volets du verso
        imm = ""
        blocs = [(60, 74, 46), (118, 96, 40), (172, 60, 52), (238, 88, 44),
                 (300, 70, 50), (366, 104, 42), (430, 62, 48), (492, 86, 54),
                 (560, 72, 40), (616, 98, 46), (678, 64, 50), (742, 88, 42),
                 (798, 74, 52), (864, 60, 44), (922, 92, 48), (984, 70, 40),
                 (1038, 86, 50), (1102, 66, 46)]
        for x, h, w in blocs:
            imm += ('<rect x="%d" y="%d" width="%d" height="%d" rx="3" fill="%s"/>'
                    % (x, 150 - h, w, h, masse))
            for k in range(2):
                for r in range(max(1, h // 26)):
                    imm += ('<rect x="%d" y="%d" width="7" height="9" rx="3.5" fill="%s" opacity=".55"/>'
                            % (x + 10 + k * 18, 150 - h + 14 + r * 24, clair))
        return _uri(f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1188 150" preserveAspectRatio="none">
<path d="M0 96 C 90 40 168 38 250 84 C 318 122 372 120 438 82 C 520 34 596 40 668 90 C 742 140 812 136 884 90 C 962 40 1044 42 1112 88 C 1144 110 1170 116 1188 112 L1188 150 L0 150 Z" fill="{trait}" opacity=".55"/>
<path d="M0 122 C 84 84 150 82 226 116 C 300 148 360 146 428 116 C 508 80 580 84 648 120 C 720 158 790 154 858 120 C 934 82 1014 84 1082 118 C 1120 136 1158 140 1188 134 L1188 150 L0 150 Z" fill="{accent}" opacity=".35"/>
{imm}
<path d="M0 149 H1188" stroke="{masse}" stroke-width="2" opacity=".35"/>
</svg>""")

    raise ValueError(nom)


# --------------------------------------------------------------------------
#  Fragments de mise en page
# --------------------------------------------------------------------------
def esc(t):
    return (str(t).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


def volet_couverture(c, th):
    return f"""
<section class="panel cover">
  <div class="cover-art" role="presentation"></div>
  <div class="cover-inner">
    <header class="brandline">
      <p class="brand">{esc(c['marque'])}</p>
      <p class="brand-sub">{esc(c['marque_sub'])}</p>
    </header>
    <div class="cover-main">
      <p class="pill">{esc(c['pastille'])}</p>
      <h1 class="cover-title"><span>{esc(c['titre_1'])}</span><em>{esc(c['titre_2'])}</em></h1>
      <p class="cover-place">{esc(c['ville'])}<br><span>{esc(c['quartier'])}</span></p>
      <p class="cover-lede">{esc(c['accroche'])}</p>
    </div>
    <footer class="cover-foot">
      <p class="count">{esc(c['compteur'])}</p>
      <p class="foot-note">{esc(c['cover_foot'])}</p>
    </footer>
  </div>
</section>"""


def volet_bien(bien, i, th, c=CONTENU):
    feats = "".join("<li>%s</li>" % esc(f) for f in bien["feats"])
    specs = "".join("<div><dt>%s</dt><dd>%s</dd></div>" % (esc(k), esc(v))
                    for k, v in bien["specs"])
    return f"""
<section class="panel fiche fiche--{i}">
  <figure class="shot shot--{i}"><figcaption class="tag">{esc(bien['dispo'])}</figcaption></figure>
  <div class="fiche-body">
    <p class="ref">{esc(bien['ref'])}</p>
    <h2 class="fiche-title">{esc(bien['type'])}</h2>
    <p class="fiche-surface">{esc(bien['surface'])}</p>
    <p class="phrase">{esc(bien.get('phrase', ''))}</p>
    <p class="price"><b>{esc(bien['loyer'])}</b><span>{esc(bien['loyer_note'])}</span></p>
    <ul class="feats">{feats}</ul>
    <dl class="specs">{specs}</dl>
    <p class="fiche-cta">Visite&nbsp;: <b>{esc(c['tel'])}</b></p>
  </div>
</section>"""


def volet_contact(c, th):
    qr = qr_svg(c["qr_cible"], th["qr_couleur"])
    return f"""
<section class="panel back">
  <header class="brandline">
    <p class="brand">{esc(c['marque'])}</p>
    <p class="brand-sub">{esc(c['marque_sub'])}</p>
  </header>
  <div class="back-main">
    <h2 class="h2">{esc(c['contact_titre'])}</h2>
    <p class="lede">{esc(c['contact_chapo'])}</p>
    <p class="tel">{esc(c['tel'])}</p>
    <p class="email">{esc(c['email'])}</p>
    <p class="zone">{esc(c['zone'])}</p>
    <div class="qr-block">
      <div class="qr">{qr}</div>
      <p class="qr-cap">{esc(c['qr_legende'])}</p>
    </div>
  </div>
  <p class="mentions">{esc(c['mentions'])}</p>
</section>"""


def volet_quartier(c, th):
    pts = "".join("<li><span>%s</span><b>%s</b></li>" % (esc(k), esc(v))
                  for k, v in c["quartier_points"])
    return f"""
<section class="panel quartier">
  <p class="eyebrow">À deux pas</p>
  <h2 class="h2">{esc(c['quartier_titre'])}</h2>
  <p class="lede">{esc(c['quartier_chapo'])}</p>
  <ul class="walk">{pts}</ul>
  <p class="note">{esc(c['quartier_note'])}</p>
</section>"""


def volet_etapes(c, th):
    et = "".join(
        '<li><span class="num">%02d</span><div><b>%s</b><p>%s</p></div></li>'
        % (i + 1, esc(t), esc(d)) for i, (t, d) in enumerate(c["etapes"]))
    doc = "".join("<li>%s</li>" % esc(d) for d in c["dossier"])
    return f"""
<section class="panel etapes">
  <p class="eyebrow">En 3 étapes</p>
  <h2 class="h2">{esc(c['etapes_titre'])}</h2>
  <ol class="steps">{et}</ol>
  <p class="note">{esc(c['etapes_note'])}</p>
  <div class="dossier">
    <p class="dossier-title">{esc(c['dossier_titre'])}</p>
    <ul class="check">{doc}</ul>
  </div>
</section>"""


def volet_infos(c, th):
    lignes = "".join("<div><dt>%s</dt><dd>%s</dd></div>" % (esc(k), esc(v))
                     for k, v in c["infos"])
    chips = "".join("<li>%s</li>" % esc(x) for x in c["infos_chips"])
    return f"""
<section class="panel infos">
  <p class="eyebrow">Pratique</p>
  <h2 class="h2">{esc(c['infos_titre'])}</h2>
  <div class="encart">
    <p class="encart-title">{esc(c['infos_encart_titre'])}</p>
    <p>{esc(c['infos_encart_texte'])}</p>
  </div>
  <dl class="infolist">{lignes}</dl>
  <ul class="chips">{chips}</ul>
</section>"""


REPERES = ('<div class="foldmarks" aria-hidden="true">'
           + "".join('<i class="t" style="left:%smm"></i><i class="b" style="left:%smm"></i>'
                     % (x, x) for x in ("74.25", "148.5", "222.75"))
           + "</div>")


# --------------------------------------------------------------------------
#  Feuille de style commune
# --------------------------------------------------------------------------
BASE_CSS = """
*,*::before,*::after{box-sizing:border-box}
html,body{margin:0;padding:0}
body{background:var(--paper);color:var(--ink);
     font-family:var(--font-text);font-size:8.2pt;line-height:1.45;
     -webkit-font-smoothing:antialiased;
     -webkit-print-color-adjust:exact;print-color-adjust:exact}
h1,h2,p,ul,ol,dl,dd,figure,figcaption{margin:0;padding:0}
ul,ol{list-style:none}

.sheet{width:297mm;height:210mm;position:relative;overflow:hidden;background:var(--paper);
       display:grid;grid-template-columns:repeat(4,74.25mm)}
.panel{position:relative;overflow:hidden;padding:11mm 6.6mm 9mm;
       display:flex;flex-direction:column}
.panel + .panel{box-shadow:inset 1px 0 0 var(--sep)}

/* repères de pliage — discrets, dans la marge non imprimable des bords */
.foldmarks{position:absolute;inset:0;pointer-events:none;z-index:60}
.foldmarks i{position:absolute;width:.25mm;height:3.6mm;background:#fff;
             mix-blend-mode:difference;opacity:.5;transform:translateX(-50%)}
.foldmarks i.t{top:0}.foldmarks i.b{bottom:0}

/* ---------- couverture ---------- */
.cover{padding:0;color:var(--cover-ink);background:var(--cover-bg)}
.cover-art{position:absolute;inset:0;background-color:var(--cover-bg);
           background-image:url("photos/couverture.jpg"),var(--art-cover);
           background-size:cover;background-position:center}
.cover-inner{position:relative;z-index:2;display:flex;flex-direction:column;
             height:100%;padding:11mm 6.6mm 9mm}
.brandline .brand{font-family:var(--font-display);font-size:11pt;line-height:1.05;
                  letter-spacing:-.01em}
.brandline .brand-sub{font-size:5.6pt;letter-spacing:.16em;text-transform:uppercase;
                      margin-top:1.6mm;opacity:.72}
.cover-main{margin-top:auto}
.pill{display:inline-block;font-size:5.8pt;letter-spacing:.14em;text-transform:uppercase;
      padding:1.5mm 3mm;border-radius:99px;background:var(--accent);color:var(--on-accent);
      font-weight:600}
.cover-title{font-family:var(--font-display);font-weight:var(--display-weight);
             font-size:26pt;line-height:.94;letter-spacing:-.025em;margin-top:4mm}
.cover-title span{display:block}
.cover-title em{display:block;font-style:italic;color:var(--accent-soft)}
.cover-place{margin-top:4mm;font-size:8.6pt;font-weight:600;line-height:1.25}
.cover-place span{font-weight:400;opacity:.75}
.cover-lede{margin-top:3mm;font-size:7.6pt;line-height:1.5;opacity:.85;
            max-width:52mm}
.cover-foot{margin-top:7mm;padding-top:3.5mm;border-top:.4mm solid var(--cover-rule)}
.cover-foot .count{font-family:var(--font-display);font-size:10pt;letter-spacing:-.01em}
.cover-foot .foot-note{font-size:6.4pt;letter-spacing:.08em;text-transform:uppercase;
                       opacity:.7;margin-top:1.2mm}

/* ---------- fiches logement ---------- */
.fiche{padding:0}
.shot{position:relative;height:82mm;background-color:var(--shot-bg);
      background-size:cover;background-position:center;flex:none}
.shot--1{background-image:url("photos/appart-1.jpg"),var(--art-1)}
.shot--2{background-image:url("photos/appart-2.jpg"),var(--art-2)}
.shot--3{background-image:url("photos/appart-3.jpg"),var(--art-3)}
.tag{position:absolute;left:5mm;bottom:5mm;font-size:5.8pt;font-weight:600;
     letter-spacing:.1em;text-transform:uppercase;padding:1.4mm 2.6mm;border-radius:99px;
     background:var(--tag-bg);color:var(--tag-ink)}
.fiche-body{flex:1;display:flex;flex-direction:column;padding:6mm 6.6mm 9mm}
.ref{font-size:5.8pt;letter-spacing:.18em;text-transform:uppercase;color:var(--muted)}
.fiche-title{font-family:var(--font-display);font-weight:var(--display-weight);
             font-size:15pt;line-height:1.02;letter-spacing:-.02em;margin-top:2mm}
.fiche-surface{font-family:var(--font-display);font-size:11pt;font-style:italic;
               color:var(--accent);line-height:1;margin-top:1mm}
.phrase{font-size:7.2pt;line-height:1.5;color:var(--muted);margin-top:3mm}
.price{margin-top:4mm;padding-top:3mm;border-top:.35mm solid var(--line);
       display:flex;flex-direction:column}
.price b{font-family:var(--font-display);font-weight:var(--display-weight);
         font-size:19pt;line-height:1;letter-spacing:-.03em}
.price span{font-size:6.2pt;letter-spacing:.06em;color:var(--muted);margin-top:1.4mm}
.feats{margin-top:5mm;display:flex;flex-direction:column;gap:3mm}
.feats li{position:relative;padding-left:4.6mm;font-size:7.5pt;line-height:1.35}
.feats li::before{content:"";position:absolute;left:0;top:1.5mm;width:2.2mm;height:2.2mm;
                  border-radius:50%;background:var(--accent)}
.specs{margin-top:auto;padding-top:4mm;display:grid;grid-template-columns:1fr 1fr;
       gap:2.6mm 3mm;border-top:.35mm solid var(--line)}
.specs dt{font-size:5.6pt;letter-spacing:.12em;text-transform:uppercase;color:var(--muted)}
.specs dd{font-size:7pt;font-weight:600;margin-top:.6mm;line-height:1.2}
.fiche-cta{margin-top:4mm;font-size:6.4pt;letter-spacing:.1em;text-transform:uppercase;
           color:var(--muted)}
.fiche-cta b{color:var(--accent);font-weight:700;letter-spacing:.04em}

/* ---------- verso : dos / contact ---------- */
.back{color:var(--back-ink);background:var(--back-bg)}
.back .brand-sub{opacity:.7}
.back-main{margin-top:auto;margin-bottom:auto;padding-bottom:4mm}
.h2{font-family:var(--font-display);font-weight:var(--display-weight);font-size:17pt;
    line-height:1.02;letter-spacing:-.025em}
.back .lede{font-size:7.4pt;line-height:1.5;opacity:.82;margin-top:2.5mm;max-width:52mm}
.tel{font-family:var(--font-display);font-weight:var(--display-weight);font-size:20pt;
     letter-spacing:-.03em;line-height:1;margin-top:6mm;color:var(--accent-soft)}
.email{font-size:7.2pt;margin-top:2.4mm;word-break:break-all;opacity:.9}
.zone{font-size:6.2pt;letter-spacing:.1em;text-transform:uppercase;opacity:.65;margin-top:1.6mm}
.qr-block{margin-top:6mm;display:flex;flex-direction:column;align-items:flex-start}
.qr{width:26mm;height:26mm;background:var(--qr-bg);border-radius:var(--qr-radius);
    padding:2.6mm;display:grid;place-items:center}
.qr-img{display:block;width:100%;height:100%;background-size:contain;
        background-repeat:no-repeat;background-position:center}
.qr-cap{font-size:5.8pt;line-height:1.35;margin-top:2mm;opacity:.75;max-width:38mm}
.mentions{font-size:4.9pt;line-height:1.4;opacity:.55;margin-top:auto}

/* ---------- verso : colonnes claires ---------- */
.eyebrow{font-size:5.8pt;letter-spacing:.18em;text-transform:uppercase;color:var(--accent);
         font-weight:600}
.quartier .h2,.etapes .h2,.infos .h2{margin-top:2.2mm}
.quartier .lede{font-size:7.4pt;line-height:1.5;color:var(--muted);margin-top:2.5mm}
.quartier .note{margin-top:auto}
.walk{margin-top:5mm;display:flex;flex-direction:column}
.walk li{display:flex;justify-content:space-between;align-items:baseline;gap:2mm;
         padding:2.6mm 0;border-bottom:.3mm solid var(--line)}
.walk span{font-size:7.4pt}
.walk b{font-size:6.6pt;white-space:nowrap;color:var(--accent);font-weight:600}

.steps{margin-top:5mm;display:flex;flex-direction:column;gap:4mm}
.steps li{display:flex;gap:3mm;align-items:flex-start}
.steps .num{font-family:var(--font-display);font-weight:var(--display-weight);
            font-size:13pt;line-height:1;color:var(--accent);flex:none;width:9mm}
.steps b{font-size:8pt;display:block;line-height:1.2}
.steps p{font-size:6.9pt;line-height:1.4;color:var(--muted);margin-top:1mm}
.dossier{margin-top:auto;padding:5mm;border-radius:var(--box-radius);background:var(--box-bg)}
.dossier-title{font-size:6pt;letter-spacing:.14em;text-transform:uppercase;font-weight:600}
.check{margin-top:3mm;display:flex;flex-direction:column;gap:1.8mm}
.check li{position:relative;padding-left:4.4mm;font-size:6.8pt;line-height:1.3}
.check li::before{content:"";position:absolute;left:0;top:1.1mm;width:2.6mm;height:1.4mm;
                  border-left:.5mm solid var(--accent);border-bottom:.5mm solid var(--accent);
                  transform:rotate(-45deg)}

.encart{margin-top:4.5mm;padding:4.5mm;border-radius:var(--box-radius);
        background:var(--accent);color:var(--on-accent)}
.encart-title{font-family:var(--font-display);font-weight:var(--display-weight);font-size:10pt;
              line-height:1.05;letter-spacing:-.02em}
.encart p{font-size:6.8pt;line-height:1.4;margin-top:1.8mm;opacity:.92}
.encart p.encart-title{margin-top:0;opacity:1;font-size:10.5pt}
.note{font-size:6.6pt;line-height:1.5;color:var(--muted);margin-top:5mm;
      padding-left:4.4mm;border-left:.5mm solid var(--accent)}
.infolist{margin-top:5mm;display:flex;flex-direction:column;gap:3.4mm}
.infolist dt{font-size:6pt;letter-spacing:.12em;text-transform:uppercase;color:var(--accent);
             font-weight:600}
.infolist dd{font-size:7pt;line-height:1.4;margin-top:.9mm}
.chips{margin-top:auto;display:flex;flex-wrap:wrap;gap:1.6mm}
.chips li{font-size:5.8pt;letter-spacing:.06em;padding:1.3mm 2.4mm;border-radius:99px;
          border:.3mm solid var(--line);color:var(--muted)}

/* bandeau panoramique continu au bas du verso */
.verso .band{position:absolute;left:74.25mm;right:0;bottom:0;height:22mm;z-index:1;
             background-image:var(--art-band);background-size:222.75mm 22mm;
             background-repeat:no-repeat;opacity:var(--band-opacity)}
.verso .panel{z-index:2;padding-bottom:25mm}
.verso .back{padding-bottom:9mm}

/* ---------- écran ---------- */
@media screen{
  body{background:#22201d;display:flex;flex-direction:column;align-items:center;
       gap:34px;padding:40px 16px 64px}
  .wrap{position:relative}
  .wrap-label{font-family:var(--font-text);font-size:11px;letter-spacing:.18em;
              text-transform:uppercase;color:#b9b2a8;margin:0 0 10px 2px}
  .sheet{box-shadow:0 26px 70px rgba(0,0,0,.5)}
  @media (max-width:1220px){.sheet{zoom:.72}}
  @media (max-width:900px){.sheet{zoom:.5}}
  @media (max-width:640px){.sheet{zoom:.32}}
}
@media print{
  @page{size:297mm 210mm;margin:0}
  body{background:#fff;display:block;padding:0;margin:0}
  .wrap-label{display:none}
  .wrap{break-inside:avoid}
  .wrap + .wrap{break-before:page}
}
"""


# --------------------------------------------------------------------------
#  Assemblage
# --------------------------------------------------------------------------
def html_charte(charte, fonts, c=CONTENU):
    face_css = "\n".join(fonts[f] for f in charte["polices"])
    p = charte["palette_art"]
    arts = {
        "--art-cover": art("couverture", p),
        "--art-1":     art(charte["arts"][0], p),
        "--art-2":     art(charte["arts"][1], p),
        "--art-3":     art(charte["arts"][2], p),
        "--art-band":  art("bandeau", p),
    }
    art_vars = "\n".join("  %s:%s;" % (k, v) for k, v in arts.items())
    art_vars += '\n  --monogramme:"%s";' % c["monogramme"]

    recto = volet_couverture(c, charte) + "".join(
        volet_bien(b, i + 1, charte, c) for i, b in enumerate(c["biens"][:3]))
    verso = (volet_contact(c, charte) + volet_quartier(c, charte)
             + volet_etapes(c, charte) + volet_infos(c, charte))

    return f"""<!doctype html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Dépliant location — charte « {charte['nom']} »</title>
<meta name="description" content="Dépliant A4 4 volets, charte {charte['nom']}.">
<style>
{face_css}
:root{{
{art_vars}
{charte['tokens']}
}}
{BASE_CSS}
{charte['css']}
</style>
</head>
<body>
<!-- ══════════════════════════════════════════════════════════════════════
     RECTO — couverture + les 3 logements
     Contenu éditable dans contenu.py, puis : python3 build.py
     ══════════════════════════════════════════════════════════════════ -->
<div class="wrap">
  <p class="wrap-label">Recto · extérieur — couverture + les 3 logements</p>
  <div class="sheet recto">{recto}{REPERES}</div>
</div>

<!-- ══════════════════════════════════════════════════════════════════════
     VERSO — dos/contact + quartier + démarche + infos pratiques
     ══════════════════════════════════════════════════════════════════ -->
<div class="wrap">
  <p class="wrap-label">Verso · intérieur — contact, quartier, démarche, infos</p>
  <div class="sheet verso"><div class="band" aria-hidden="true"></div>{verso}{REPERES}</div>
</div>
</body>
</html>
"""


def pdf(html_path, pdf_path):
    chrome = None
    for motif in ("/opt/pw-browsers/chromium-*/chrome-linux/chrome",
                  "/opt/pw-browsers/chromium/chrome"):
        import glob
        trouve = glob.glob(motif)
        if trouve:
            chrome = trouve[0]
            break
    chrome = chrome or shutil.which("chromium") or shutil.which("google-chrome")
    if not chrome:
        print("   ! Chromium introuvable, PDF ignoré")
        return False
    subprocess.run([chrome, "--headless", "--no-sandbox", "--disable-gpu",
                    "--no-pdf-header-footer", "--run-all-compositor-stages-before-draw",
                    "--virtual-time-budget=6000",
                    "--print-to-pdf=" + pdf_path, "file://" + html_path],
                   capture_output=True)
    return os.path.exists(pdf_path)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--no-pdf", action="store_true")
    args = ap.parse_args()

    print("→ polices")
    fonts = polices()

    for charte in CHARTES:
        base = "depliant-%s" % charte["slug"]
        html_path = os.path.join(HERE, base + ".html")
        open(html_path, "w", encoding="utf-8").write(html_charte(charte, fonts))
        print("→ %-34s %5d Ko" % (base + ".html",
                                  os.path.getsize(html_path) // 1024))

        if args.no_pdf:
            continue

        pdf_path = os.path.join(HERE, "pdf", base + ".pdf")
        if pdf(html_path, pdf_path):
            print("   %-32s %5d Ko" % (base + ".pdf",
                                       os.path.getsize(pdf_path) // 1024))

        # variante pour les imprimantes qui retournent la feuille sur l'autre bord
        alt_html = os.path.join(CACHE, base + "-alt.html")
        os.makedirs(CACHE, exist_ok=True)
        contenu_alt = open(html_path, encoding="utf-8").read().replace(
            "</style>", "@media print{.sheet.verso{transform:rotate(180deg)}}</style>")
        open(alt_html, "w", encoding="utf-8").write(contenu_alt)
        alt_pdf = os.path.join(HERE, "pdf", "variantes", base + "-verso-pivote.pdf")
        os.makedirs(os.path.dirname(alt_pdf), exist_ok=True)
        pdf(alt_html, alt_pdf)

    print("\n✓ terminé — ouvrez les .html dans un navigateur, "
          "ou imprimez les PDF du dossier pdf/")


if __name__ == "__main__":
    main()

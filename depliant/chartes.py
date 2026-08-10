# -*- coding: utf-8 -*-
"""
Les 3 chartes graphiques du dépliant.

Chacune définit :
  slug / nom / esprit ....... identité
  polices ................... familles Google Fonts embarquées
  palette_art ............... couleurs des illustrations vectorielles
  arts ...................... illustration de secours pour chaque logement
  tokens .................... variables CSS (couleurs, typo, arrondis)
  css ....................... ce qui rend la charte reconnaissable

Pour créer une 4ᵉ charte : copiez un bloc, changez le slug, et ajustez.
"""
import base64


def _grain(opacite=".05"):
    svg = ('<svg xmlns="http://www.w3.org/2000/svg" width="180" height="180">'
           '<filter id="n"><feTurbulence type="fractalNoise" baseFrequency="0.9" '
           'numOctaves="3" stitchTiles="stitch"/></filter>'
           '<rect width="180" height="180" filter="url(#n)"/></svg>')
    uri = base64.b64encode(svg.encode()).decode()
    return ('.sheet::after{content:"";position:absolute;inset:0;z-index:55;'
            'pointer-events:none;opacity:%s;background-image:'
            'url("data:image/svg+xml;base64,%s");background-size:38mm 38mm}' % (opacite, uri))


# ══════════════════════════════════════════════════════════════════════════
#  1 · LAVE & CRAIE  —  éditorial, chaleureux, artisanal chic
# ══════════════════════════════════════════════════════════════════════════
LAVE = {
    "slug": "01-lave-et-craie",
    "nom": "Lave & Craie",
    "esprit": "Éditorial et chaleureux. Craie, encre volcanique et terre cuite, "
              "grandes arches, serif expressif. Pour un propriétaire qui veut "
              "paraître soigné et humain plutôt que « agence ».",
    "polices": ["Fraunces", "Inter"],
    "qr_couleur": "#191310",
    "arts": ["facade", "interieur", "sejour"],
    "palette_art": {"ciel": "#EDE3D3", "masse": "#2A211B", "clair": "#F6F1E8",
                    "accent": "#C0452A", "trait": "#D9C4A6"},
    "tokens": """
  --paper:#F6F1E8; --ink:#191310; --muted:#7C6F62;
  --line:rgba(25,19,16,.16); --sep:rgba(25,19,16,.07);
  --accent:#C0452A; --accent-soft:#E9A661; --on-accent:#FFF6EC;
  --font-display:"Fraunces",Georgia,serif;
  --font-text:"Inter",system-ui,sans-serif;
  --display-weight:600;
  --cover-bg:#191310; --cover-ink:#F6F1E8; --cover-rule:rgba(246,241,232,.3);
  --shot-bg:#E9DFCE; --tag-bg:#191310; --tag-ink:#F6F1E8;
  --back-bg:#191310; --back-ink:#F6F1E8;
  --qr-bg:#F6F1E8; --qr-radius:2mm;
  --box-bg:#ECE3D4; --box-radius:3mm;
  --band-opacity:.55;
""",
    "css": _grain(".05") + """
.cover-title,.fiche-title,.h2,.tel,.price b,.encart-title,.brandline .brand,
.count,.steps .num,.fiche-surface{font-variation-settings:"opsz" 144}

/* grande arche en couverture */
.cover-art{left:6.6mm;right:6.6mm;top:6.6mm;bottom:auto;height:102mm;
  border-radius:34mm 34mm 3mm 3mm}
.cover-inner{padding-top:113mm}
.cover-title{font-size:27pt}
.cover-foot{margin-top:6mm}

/* les photos des logements reprennent l'arche */
.shot{height:76mm;margin:6.6mm 6.6mm 0;border-radius:30mm 30mm 3mm 3mm}
.tag{left:50%;transform:translateX(-50%);bottom:4mm;white-space:nowrap}
.fiche-body{padding-top:5.5mm}
.fiche-surface{margin-top:1.5mm}

/* filet fin sous les intertitres du verso */
.quartier .h2::after,.etapes .h2::after,.infos .h2::after{content:"";display:block;
  width:12mm;height:.5mm;background:var(--accent);margin-top:3.5mm}
.walk li:last-child{border-bottom:0}
.encart{background:var(--accent);color:var(--on-accent)}
.back .tel{color:var(--accent-soft)}
""",
}


# ══════════════════════════════════════════════════════════════════════════
#  2 · BELVÉDÈRE  —  premium, classique, rassurant
# ══════════════════════════════════════════════════════════════════════════
BELVEDERE = {
    "slug": "02-belvedere",
    "nom": "Belvédère",
    "esprit": "Codes de l'immobilier haut de gamme : bleu nuit, filets dorés, "
              "monogramme, capitales espacées, composition centrée. Rassure "
              "immédiatement, y compris un public plus âgé.",
    "polices": ["Marcellus", "Montserrat"],
    "qr_couleur": "#0D1B33",
    "arts": ["facade", "sejour", "interieur"],
    "palette_art": {"ciel": "#DCE3EC", "masse": "#0D1B33", "clair": "#F8F6F1",
                    "accent": "#B08D4F", "trait": "#AFC0D4"},
    "tokens": """
  --paper:#F8F6F1; --ink:#0D1B33; --muted:#6C7789;
  --line:rgba(13,27,51,.18); --sep:rgba(13,27,51,.08);
  --accent:#B08D4F; --accent-soft:#D8B978; --on-accent:#0D1B33;
  --font-display:"Marcellus",Georgia,serif;
  --font-text:"Montserrat",system-ui,sans-serif;
  --display-weight:400;
  --cover-bg:#0D1B33; --cover-ink:#F8F6F1; --cover-rule:rgba(176,141,79,.55);
  --shot-bg:#E4E9F0; --tag-bg:#B08D4F; --tag-ink:#0D1B33;
  --back-bg:#0D1B33; --back-ink:#F8F6F1;
  --qr-bg:#F8F6F1; --qr-radius:0;
  --box-bg:#EFEBE1; --box-radius:0;
  --band-opacity:.45;
""",
    "css": """
body{font-size:8pt}

/* couverture centrée : image encadrée, double filet or, monogramme */
.cover-art{left:9.5mm;right:9.5mm;top:43mm;bottom:auto;height:73mm}
.cover-inner{padding:11mm 8mm 9mm;text-align:center;align-items:center}
.cover-main{margin-top:0;padding-top:80mm}
.cover .brandline::before{content:var(--monogramme);display:grid;place-items:center;
  width:12mm;height:12mm;border-radius:50%;border:.25mm solid var(--accent);
  color:var(--accent);font-family:var(--font-display);font-size:8pt;
  letter-spacing:.12em;text-indent:.12em;margin:0 auto 3.5mm}
.cover-inner::before{content:"";position:absolute;inset:5mm;border:.3mm solid var(--accent);
  pointer-events:none}
.cover-inner::after{content:"";position:absolute;inset:6.4mm;border:.15mm solid rgba(216,185,120,.45);
  pointer-events:none}
.brandline .brand{font-size:9pt;text-transform:uppercase;letter-spacing:.24em;
  text-indent:.24em}
.brandline .brand-sub{font-size:5.2pt;letter-spacing:.2em;text-indent:.2em;margin-top:2.4mm}
.pill{background:transparent;color:var(--accent-soft);border:.25mm solid var(--accent);
  border-radius:0;font-weight:500;letter-spacing:.2em;text-indent:.2em;font-size:5.4pt}
.cover-title{font-size:20pt;line-height:1.14;letter-spacing:.05em;text-transform:uppercase;
  text-indent:.05em;margin-top:5mm}
.cover-title em{font-style:normal;color:var(--accent-soft);font-size:13pt;
  letter-spacing:.34em;text-indent:.34em;margin-top:2.5mm}
.cover-place{font-size:8pt;letter-spacing:.1em;text-transform:uppercase;text-indent:.1em}
.cover-place span{text-transform:none;letter-spacing:0;text-indent:0;display:block;margin-top:1mm}
.cover-lede{max-width:48mm;margin-left:auto;margin-right:auto;font-size:7.2pt}
.cover-foot{width:100%;border-top:.3mm solid var(--cover-rule);position:relative}
.cover-foot::before{content:"";position:absolute;top:.9mm;left:0;right:0;height:.15mm;
  background:rgba(216,185,120,.4)}

/* fiches : photo pleine largeur, titres centrés, filets or */
.shot{height:86mm}
.tag{left:50%;transform:translateX(-50%);bottom:4mm;border-radius:0;letter-spacing:.14em;
  text-indent:.14em;font-weight:600;white-space:nowrap}
.fiche-body{padding-top:6mm;text-align:center}
.ref{letter-spacing:.24em;text-indent:.24em;color:var(--accent)}
.fiche-title{font-size:14.5pt;letter-spacing:.03em;text-transform:uppercase;
  text-indent:.03em;margin-top:2.6mm}
.fiche-surface{font-style:normal;font-size:9.5pt;letter-spacing:.08em;text-indent:.08em;
  color:var(--muted);margin-top:2mm}
.price{align-items:center;border-top-color:var(--accent);border-top-width:.3mm;margin-top:4.5mm}
.price b{font-size:20pt;letter-spacing:0}
.price span{letter-spacing:.1em;font-size:5.8pt;text-transform:uppercase}
.feats{text-align:left}
.feats li::before{border-radius:0;width:1.8mm;height:1.8mm;transform:rotate(45deg);top:1.7mm}
.specs{text-align:left;border-top-color:var(--accent);border-top-width:.3mm}
.specs dt{color:var(--accent)}

/* verso */
.eyebrow{letter-spacing:.24em;text-indent:.24em}
.h2{letter-spacing:.02em}
.quartier .h2,.etapes .h2,.infos .h2{text-transform:uppercase;font-size:13pt;line-height:1.16}
.quartier .h2::after,.etapes .h2::after,.infos .h2::after{content:"";display:block;
  width:16mm;height:.3mm;background:var(--accent);margin-top:3.5mm}
.walk b{font-weight:600}
.steps .num{font-size:14pt}
.dossier{border:.3mm solid var(--accent);background:transparent}
.encart{border:.3mm solid var(--accent);background:transparent;color:var(--ink)}
.encart-title{color:var(--accent);text-transform:uppercase;letter-spacing:.08em;font-size:9pt}
.chips li{border-radius:0}
.back .tel{color:var(--accent-soft);letter-spacing:.01em}
.qr{border:.3mm solid var(--accent)}
""",
}


# ══════════════════════════════════════════════════════════════════════════
#  3 · SYLVA  —  moderne, clair, nature
# ══════════════════════════════════════════════════════════════════════════
SYLVA = {
    "slug": "03-sylva",
    "nom": "Sylva",
    "esprit": "Vert profond, lin et jaune soleil, grands blocs arrondis, sans "
              "serif géométrique ponctué d'italiques. Lisible de loin, très "
              "actuel : parle aux étudiants, jeunes actifs et jeunes couples.",
    "polices": ["Outfit", "InstrumentSerif"],
    "qr_couleur": "#14342B",
    "arts": ["interieur", "facade", "sejour"],
    "palette_art": {"ciel": "#E6EDE3", "masse": "#14342B", "clair": "#F4F2EA",
                    "accent": "#E8B33C", "trait": "#BBD3BB"},
    "tokens": """
  --paper:#F4F2EA; --ink:#14342B; --muted:#5E7268;
  --line:rgba(20,52,43,.16); --sep:rgba(20,52,43,.07);
  --accent:#14342B; --accent-soft:#E8B33C; --on-accent:#F4F2EA;
  --font-display:"Outfit",system-ui,sans-serif;
  --font-text:"Outfit",system-ui,sans-serif;
  --font-serif:"Instrument Serif",Georgia,serif;
  --display-weight:700;
  --cover-bg:#14342B; --cover-ink:#F4F2EA; --cover-rule:rgba(244,242,234,.28);
  --shot-bg:#DFE8DC; --tag-bg:#E8B33C; --tag-ink:#14342B;
  --back-bg:#14342B; --back-ink:#F4F2EA;
  --qr-bg:#F4F2EA; --qr-radius:4mm;
  --box-bg:#E3EADF; --box-radius:6mm;
  --band-opacity:.6;
""",
    "css": """
body{font-size:8.4pt}
.h2,.fiche-title,.cover-title,.count,.tel,.price b,.encart-title{letter-spacing:-.035em}

/* couverture : grand bloc arrondi, titre en deux temps */
.cover-art{left:5mm;right:5mm;top:5mm;bottom:auto;height:106mm;border-radius:8mm}
.cover-inner{padding:118mm 6.6mm 9mm}
.pill{background:var(--accent-soft);color:var(--ink);font-weight:600;font-size:5.6pt}
.cover-title{font-size:25pt;line-height:.92;margin-top:4.5mm}
.cover-title em{font-family:var(--font-serif);font-style:italic;font-weight:400;
  font-size:29pt;line-height:.95;color:var(--accent-soft);letter-spacing:-.01em}
.cover-place{font-size:8.4pt}
.cover-foot{border-top-width:.3mm}

/* fiches : la photo est une carte posée sur le papier */
.shot{margin:5mm 5mm 0;height:78mm;border-radius:7mm}
.tag{border-radius:99px;left:4mm;bottom:4mm;font-weight:700}
.fiche-body{padding:5.5mm 6.6mm 9mm}
.ref{color:var(--muted);letter-spacing:.16em}
.fiche-title{font-size:16pt;margin-top:1.6mm}
.fiche-surface{font-family:var(--font-serif);font-size:13pt;color:var(--muted);
  margin-top:.5mm}
.price{border-top:0;padding:3.4mm 4mm;margin-top:4mm;background:var(--box-bg);
  border-radius:5mm}
.price b{font-size:19pt}
.price span{margin-top:.8mm}
.feats li::before{background:var(--accent-soft)}
.specs{border-top:0;background:transparent;padding-top:3.5mm;
  border-top:.35mm dashed var(--line)}

/* verso */
.eyebrow{color:var(--muted)}
.quartier .h2,.etapes .h2,.infos .h2{font-size:18pt;line-height:.98}
.walk li{border-bottom:0;padding:2.2mm 3.4mm;border-radius:99px;margin-bottom:1.4mm;
  background:var(--box-bg)}
.walk b{color:var(--muted)}
.steps .num{font-family:var(--font-serif);font-style:italic;font-weight:400;font-size:15pt;
  color:var(--accent-soft);width:8mm}
.dossier{background:var(--ink);color:var(--paper)}
.dossier .check li::before{border-color:var(--accent-soft)}
.encart{background:var(--accent-soft);color:var(--ink)}
.encart-title{font-size:11pt}
.infolist dt{color:var(--muted)}
.chips li{border:0;background:var(--box-bg);color:var(--ink);font-weight:500}
.back .tel{color:var(--accent-soft);font-size:21pt}
.back .lede{opacity:.78}
""",
}


CHARTES = [LAVE, BELVEDERE, SYLVA]

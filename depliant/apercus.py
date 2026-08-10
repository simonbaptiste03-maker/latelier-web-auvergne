#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Aperçus JPEG des dépliants, rasterisés depuis les PDF : ce que l'on voit ici
est exactement ce qui sortira de l'imprimante.

    python3 apercus.py [dpi]        (150 par défaut)
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from chartes import CHARTES  # noqa: E402

OUT = os.path.join(HERE, "apercus")
FACES = ("recto", "verso")


def main(dpi=150):
    import fitz  # PyMuPDF
    from PIL import Image

    os.makedirs(OUT, exist_ok=True)
    for ch in CHARTES:
        src = os.path.join(HERE, "pdf", "depliant-%s.pdf" % ch["slug"])
        if not os.path.exists(src):
            print("   ! manquant :", src)
            continue
        doc = fitz.open(src)
        for i, page in enumerate(doc):
            if i >= len(FACES):
                break
            pix = page.get_pixmap(dpi=dpi)
            im = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
            dest = os.path.join(OUT, "%s-%s.jpg" % (ch["slug"], FACES[i]))
            im.save(dest, "JPEG", quality=86, optimize=True, progressive=True)
            print("   %-28s %5d × %-5d %4d Ko"
                  % (os.path.basename(dest), pix.width, pix.height,
                     os.path.getsize(dest) // 1024))
        doc.close()
    index()


PAGE = """<!doctype html>
<html lang="fr"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Dépliant location — les 3 chartes graphiques</title>
<style>
*{box-sizing:border-box}
body{margin:0;background:#14120f;color:#f2ede4;
     font:15px/1.6 ui-sans-serif,system-ui,-apple-system,"Segoe UI",sans-serif}
.wrap{max-width:1180px;margin:0 auto;padding:56px 20px 96px}
h1{font-size:clamp(28px,4vw,42px);line-height:1.1;margin:0 0 14px;letter-spacing:-.02em}
.sub{color:#a89e90;max-width:62ch;margin:0 0 10px}
.avert{margin:28px 0 0;padding:14px 18px;border-left:3px solid #C0452A;background:#1d1913;
       color:#e5d9c8;font-size:14px}
section{margin-top:64px;border-top:1px solid #322c24;padding-top:32px}
h2{font-size:24px;margin:0 0 6px;letter-spacing:-.01em}
h2 span{color:#8a8073;font-weight:400;font-size:15px;letter-spacing:.14em;
        text-transform:uppercase;display:block;margin-bottom:8px}
.esprit{color:#a89e90;max-width:70ch;margin:0 0 8px}
.meta{color:#7d7364;font-size:13.5px;margin:0 0 22px}
figure{margin:0 0 22px}
figcaption{font-size:12px;letter-spacing:.14em;text-transform:uppercase;color:#7d7364;
           margin-bottom:8px}
img{width:100%;height:auto;display:block;border-radius:4px;
    box-shadow:0 18px 44px rgba(0,0,0,.5)}
a{color:#E9A661}
.liens{font-size:14px;color:#a89e90}
</style></head><body><div class="wrap">
<h1>Appartements à louer — trois chartes graphiques</h1>
<p class="sub">Même dépliant, même contenu : A4 paysage, quatre volets de 74,25 mm,
pli accordéon. Recto : couverture + les trois logements. Verso : contact,
quartier, démarche, informations pratiques.</p>
<p class="liens">Fichiers prêts à imprimer dans <code>pdf/</code> ·
mode d'emploi dans <code>README.md</code></p>
<p class="avert"><strong>Textes d'exemple.</strong> Loyers, surfaces, quartier et
temps de trajet sont fictifs. Modifiez <code>contenu.py</code> puis relancez
<code>python3 build.py</code> avant d'imprimer.</p>
__BLOCS__
</div></body></html>
"""


def index():
    blocs = []
    for i, ch in enumerate(CHARTES, 1):
        blocs.append("""<section>
<h2><span>Charte %02d</span>%s</h2>
<p class="esprit">%s</p>
<p class="meta">Polices : %s · <a href="pdf/depliant-%s.pdf">PDF à imprimer</a>
 · <a href="depliant-%s.html">version HTML</a></p>
<figure><figcaption>Recto — couverture et les trois logements</figcaption>
<img src="apercus/%s-recto.jpg" alt="Recto de la charte %s"></figure>
<figure><figcaption>Verso — contact, quartier, démarche, pratique</figcaption>
<img src="apercus/%s-verso.jpg" alt="Verso de la charte %s"></figure>
</section>""" % (i, ch["nom"], ch["esprit"],
                 " + ".join(ch["polices"]).replace("InstrumentSerif", "Instrument Serif"),
                 ch["slug"], ch["slug"], ch["slug"], ch["nom"], ch["slug"], ch["nom"]))
    open(os.path.join(HERE, "index.html"), "w", encoding="utf-8").write(
        PAGE.replace("__BLOCS__", "\n".join(blocs)))
    print("   index.html")


if __name__ == "__main__":
    main(int(sys.argv[1]) if len(sys.argv) > 1 else 150)

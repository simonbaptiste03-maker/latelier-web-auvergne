# Dépliant « Appartements à louer » — A4 plié en 4

Trois chartes graphiques d'un même dépliant, prêtes à imprimer, pensées pour être
distribuées à la main (parking, boîtes aux lettres, commerces du quartier).

> ⚠️ **Les textes actuels sont des exemples** : loyers, surfaces, quartier, temps
> de trajet. Ouvrez `contenu.py`, remplacez-les par vos vraies informations et
> relancez `python3 build.py` **avant d'imprimer quoi que ce soit**.

---

## Les trois chartes

| | Charte | Esprit | Typographie | À qui ça parle |
|---|---|---|---|---|
| 01 | **Lave & Craie** | Éditorial, chaleureux, artisanal chic. Craie, encre volcanique, terre cuite, grandes arches. | Fraunces + Inter | Ceux qui veulent paraître soignés et humains, pas « agence ». |
| 02 | **Belvédère** | Immobilier haut de gamme classique. Bleu nuit, filets dorés, monogramme, capitales espacées. | Marcellus + Montserrat | Rassure large, y compris un public plus âgé ou prudent. |
| 03 | **Sylva** | Moderne et clair. Vert profond, lin, jaune soleil, grands blocs arrondis. | Outfit + Instrument Serif | Étudiants, jeunes actifs, jeunes couples. |

Aperçus dans `apercus/`, ou ouvrez `index.html` dans un navigateur pour les
comparer côte à côte.

---

## Le format, concrètement

**A4 paysage (297 × 210 mm), 4 volets de 74,25 mm, pli accordéon.**

Une fois plié : un dépliant fin de **74 × 210 mm**, qui se glisse dans une poche
ou un sac. Huit faces au total.

```
RECTO  ┌────────────┬────────────┬────────────┬────────────┐
       │ COUVERTURE │ Logement 1 │ Logement 2 │ Logement 3 │
       └────────────┴────────────┴────────────┴────────────┘
VERSO  ┌────────────┬────────────┬────────────┬────────────┐
       │  CONTACT   │ Le quartier│ La démarche│  Pratique  │
       │  (le dos)  │            │            │            │
       └────────────┴────────────┴────────────┴────────────┘
```

Plié en accordéon, la **couverture** est devant et le **panneau contact** derrière :
les deux faces visibles quand on tend le dépliant à quelqu'un.

### Plier

Deux plis, en zigzag, en suivant les petits repères imprimés en haut et en bas
de la feuille :

1. Pli n° 1 à 74,25 mm — vers l'arrière ;
2. Pli n° 2 à 148,5 mm — vers l'avant ;
3. Pli n° 3 à 222,75 mm — vers l'arrière.

Autrement dit : on replie comme un paravent. Si vous préférez plier simplement
en deux puis encore en deux, ça fonctionne aussi — c'est seulement la face
visible une fois fermé qui change.

---

## Imprimer

Les fichiers prêts sont dans `pdf/`.

**Réglages à vérifier dans la boîte de dialogue d'impression :**

- Format **A4**, orientation **paysage**
- Mise à l'échelle : **Taille réelle / 100 %** — surtout pas « Ajuster à la page »,
  qui décalerait les plis
- **Recto-verso**
- Si votre imprimante le propose : **impression sans marges** (sinon vous aurez
  un liseré blanc de 3 à 5 mm, ce qui reste tout à fait présentable)

**Si le verso ressort tête-bêche** (ça dépend du sens de retournement de votre
imprimante) : reprenez le même dépliant dans `pdf/variantes/`, dont le verso est
déjà pivoté à 180°. C'est l'un ou l'autre, jamais les deux.

**Pour vérifier avant de lancer 200 copies :** imprimez-en un seul, pliez-le,
et regardez si la couverture tombe bien devant et le contact derrière.

**Chez un imprimeur** (recommandé au-delà de 50 exemplaires) : demandez un A4
recto-verso, **couché mat 170 g**, pli accordéon 4 volets. Fournissez le PDF tel
quel. Comptez quelques dizaines d'euros pour 250 exemplaires.

---

## Mettre vos propres photos

Déposez vos images dans `photos/` en respectant **exactement** ces noms :

| Fichier | Emplacement |
|---|---|
| `photos/couverture.jpg` | grande image de la couverture |
| `photos/appart-1.jpg` | logement n° 1 |
| `photos/appart-2.jpg` | logement n° 2 |
| `photos/appart-3.jpg` | logement n° 3 |

Aucune modification de code : dès que le fichier existe, il remplace
l'illustration. Aucun fichier fourni ? Les illustrations vectorielles servent de
solution de repli — le dépliant reste présentable tel quel.

**Format conseillé :** photos **verticales**, ratio 3:4 environ, au moins
1000 × 1300 px. Une photo de logement lumineuse, prise depuis un angle de la
pièce, vaut mieux qu'une photo de façade.

---

## Modifier les textes

Tout est dans **`contenu.py`** — un seul fichier, en français, commenté.
Loyers, surfaces, disponibilités, temps de trajet, téléphone, mentions légales.

```bash
python3 build.py          # régénère les 3 chartes : HTML + PDF
python3 build.py --no-pdf # HTML seulement, plus rapide pour itérer
python3 apercus.py        # régénère les images d'aperçu
```

Le QR code est régénéré automatiquement à partir de `qr_cible` : par défaut il
compose votre numéro de téléphone. Vous pouvez y mettre une adresse de page à la
place (`https://…`).

Une fois généré, chaque fichier `depliant-*.html` est **autonome** : polices,
illustrations et QR code sont embarqués dedans. Vous pouvez l'envoyer par mail
ou l'ouvrir sur un autre ordinateur sans rien installer, et imprimer depuis le
navigateur (Ctrl/Cmd + P).

---

## Modifier l'apparence

`chartes.py` contient les trois chartes : couleurs, polices, arrondis, et le CSS
qui les distingue. Pour en créer une quatrième, copiez un bloc, changez le
`slug`, ajustez les couleurs.

## Structure

```
depliant/
├── contenu.py                    ← les textes (le fichier du quotidien)
├── chartes.py                    ← les 3 chartes graphiques
├── build.py                      ← génère HTML + PDF
├── apercus.py                    ← génère les images d'aperçu
├── index.html                    ← comparateur des 3 chartes
├── depliant-01-lave-et-craie.html
├── depliant-02-belvedere.html
├── depliant-03-sylva.html
├── pdf/                          ← à imprimer
│   └── variantes/                ← verso pivoté à 180°
├── apercus/                      ← images JPEG
└── photos/                       ← vos photos (facultatif)
```

## Avant de distribuer

- [ ] Loyers, surfaces et disponibilités vérifiés
- [ ] Quartier et temps de trajet réels
- [ ] Téléphone et e-mail corrects, QR code testé avec un vrai téléphone
- [ ] Un exemplaire imprimé et plié pour contrôle
- [ ] Sur un parking privé (supermarché, centre commercial) : demandez
      l'autorisation avant de distribuer, sinon on vous fera partir. Le domaine
      public et la remise en main propre restent libres.

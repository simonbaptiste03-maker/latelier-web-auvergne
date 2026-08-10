# -*- coding: utf-8 -*-
"""
==========================================================================
 CONTENU DU DÉPLIANT  —  c'est LE SEUL fichier à modifier au quotidien.
==========================================================================
 Modifiez les textes ci-dessous, puis relancez :   python3 build.py
 Les 3 chartes graphiques sont régénérées automatiquement (HTML + PDF).

 ⚠️  Les valeurs actuelles sont des EXEMPLES (loyers, surfaces, quartier).
     Remplacez-les par vos vraies informations avant d'imprimer.
==========================================================================
"""

CONTENU = {
    # ---------------------------------------------------------------- marque
    "marque":      "Baptiste Simon",
    "marque_sub":  "Location directe · de propriétaire à locataire",
    "monogramme":  "BS",                       # 2 lettres, utilisé par la charte « Belvédère »

    # ------------------------------------------------------------ couverture
    "pastille":    "Sans frais d'agence",
    "titre_1":     "Appartements",
    "titre_2":     "à louer",
    "ville":       "Clermont-Ferrand",
    "quartier":    "Quartier Saint-Jacques",
    "accroche":    "Trois logements rénovés, libres tout de suite, à 300 mètres d’ici.",
    "compteur":    "3 logements disponibles",
    "cover_foot":  "Visites cette semaine, sur rendez-vous",

    # ----------------------------------------------------- les 3 logements
    # 3 biens = 3 volets du recto. Gardez-en 3 (le format est calibré pour 3).
    "biens": [
        {
            "ref":        "Réf. 01",
            "type":       "Studio meublé",
            "surface":    "28 m²",
            "loyer":      "470 €",
            "loyer_note": "par mois, charges comprises",
            "dispo":      "Libre maintenant",
            "phrase":     "Prêt à vivre : vous arrivez avec vos valises, tout le reste est déjà là.",
            "feats": [
                "Entièrement meublé et rénové",
                "Cuisine équipée + lave-linge",
                "Fibre optique incluse",
                "Local à vélos fermé",
            ],
            "specs": [
                ("Étage",     "3ᵉ avec ascenseur"),
                ("Chauffage", "Individuel électrique"),
                ("DPE",       "D"),
                ("Dépôt",     "1 mois de loyer"),
            ],
        },
        {
            "ref":        "Réf. 02",
            "type":       "T2 avec balcon",
            "surface":    "44 m²",
            "loyer":      "620 €",
            "loyer_note": "par mois, charges comprises",
            "dispo":      "Libre au 1ᵉʳ septembre",
            "phrase":     "Le volume d’un vrai deux-pièces, avec un balcon qui prend le soleil toute l’après-midi.",
            "feats": [
                "Balcon plein sud de 6 m²",
                "Chambre séparée, placards",
                "Cave + place de parking",
                "Immeuble ravalé en 2024",
            ],
            "specs": [
                ("Étage",     "2ᵉ avec ascenseur"),
                ("Chauffage", "Collectif gaz"),
                ("DPE",       "C"),
                ("Dépôt",     "1 mois de loyer"),
            ],
        },
        {
            "ref":        "Réf. 03",
            "type":       "T3 familial",
            "surface":    "68 m²",
            "loyer":      "780 €",
            "loyer_note": "par mois, charges comprises",
            "dispo":      "Libre au 15 septembre",
            "phrase":     "De quoi loger une famille ou partager à deux, sans se marcher dessus.",
            "feats": [
                "Deux chambres, séjour traversant",
                "Cuisine ouverte équipée",
                "Double vitrage, immeuble calme",
                "Cave et grenier privatifs",
            ],
            "specs": [
                ("Étage",     "1ᵉʳ étage"),
                ("Chauffage", "Collectif gaz"),
                ("DPE",       "C"),
                ("Dépôt",     "1 mois de loyer"),
            ],
        },
    ],

    # ------------------------------------------------------------- quartier
    "quartier_titre":   "Tout à pied",
    "quartier_chapo":   "Le vrai luxe ici, c’est de ne plus avoir à prendre la voiture.",
    "quartier_points": [
        ("Tramway ligne A",        "4 min à pied"),
        ("Boulangerie, commerces", "2 min à pied"),
        ("École primaire",         "6 min à pied"),
        ("Supermarché",            "5 min à pied"),
        ("Parc et aire de jeux",   "8 min à pied"),
        ("Accès A75",              "7 min en voiture"),
    ],
    "quartier_note": "Ce dépliant vous a été remis à moins de cinq minutes à pied "
                     "des logements : vous êtes déjà dans le quartier.",

    # -------------------------------------------------------- la démarche
    "etapes_titre": "Comment ça se passe",
    "etapes": [
        ("Vous appelez",     "Je réponds moi-même, dans la journée."),
        ("On visite",        "Créneaux 7j/7, y compris le soir."),
        ("Vous emménagez",   "Bail signé et clés remises sous 48 h."),
    ],
    "etapes_note": "Pas de dossier complet sous la main ? Venez visiter quand même : "
                   "on regarde le logement d’abord, les papiers ensuite.",
    "dossier_titre": "Le dossier à prévoir",
    "dossier": [
        "Pièce d’identité",
        "3 derniers bulletins de salaire",
        "Dernier avis d’imposition",
        "Justificatif de domicile",
        "Un garant ou la garantie Visale",
    ],

    # ---------------------------------------------------------- bon à savoir
    "infos_titre": "Bon à savoir",
    "infos_encart_titre": "Zéro frais d’agence",
    "infos_encart_texte": "Vous traitez directement avec le propriétaire : pas d’honoraires de dossier, pas d’intermédiaire.",
    "infos": [
        ("Compris dans les charges", "Eau froide, entretien des parties communes, ordures ménagères."),
        ("Dépôt de garantie",        "Un mois de loyer hors charges, restitué sous un mois."),
        ("Garanties acceptées",      "Garant physique ou garantie Visale (gratuite)."),
        ("Durée du bail",            "3 ans en logement nu, 1 an en meublé."),
        ("À la remise des clés",     "État des lieux fait ensemble, attestation d’assurance habitation."),
    ],
    "infos_chips": ["Étudiants bienvenus", "Jeunes actifs", "Couples", "Animaux sur demande"],

    # ------------------------------------------------------------- contact
    "contact_titre":   "Une visite ?",
    "contact_chapo":   "Appelez, envoyez un SMS ou un WhatsApp : réponse sous 24 h.",
    "tel":             "07 83 87 82 38",
    "tel_lien":        "+33783878238",
    "email":           "Simonbaptiste03@gmail.com",
    "zone":            "Clermont-Ferrand et agglomération",
    "qr_cible":        "tel:+33783878238",   # ce que déclenche le QR code
    "qr_legende":      "Scannez : votre téléphone compose le numéro",
    "mentions":        "Photos et informations non contractuelles. Loyers charges comprises, hors électricité. "
                       "Les logements présentés sont proposés à la location par un particulier.",
}

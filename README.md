# Introduction à l'IA — M2 Cybersécurité

Support de code du cours « Introduction à l'intelligence artificielle » (première
séance, 6 h) destiné à des étudiants de M2 cybersécurité.

Ce dépôt contient **uniquement le code source** : la démonstration scikit-learn et
le script qui régénère les figures du cours. Les images, les jeux de données et le
diaporama `.pptx` sont générés ou conservés en local ; ils ne sont pas versionnés.

## Contenu

```
.
├── demo/
│   └── demo_phishing.py      # Démo : détecter des URL de phishing (scikit-learn)
├── scripts/
│   └── figures_cours.py      # Régénère les 34 figures de concept du cours
├── requirements.txt          # Dépendances Python
└── README.md
```

Après exécution, deux dossiers apparaissent (ignorés par git) :

- `demo/figures/` et `demo/donnees/` : sorties de la démonstration ;
- `figures/` : figures de concept du cours.

## Prérequis

- Python 3.10 ou plus récent.
- Les bibliothèques de `requirements.txt`.

```bash
python -m venv .venv
# Windows : .venv\Scripts\activate   |   Linux/macOS : source .venv/bin/activate
pip install -r requirements.txt
```

## Lancer la démonstration phishing

```bash
python demo/demo_phishing.py
```

La démonstration est **entièrement hors ligne** : elle fabrique elle-même un jeu
de 2 000 URL **simulées** (graine aléatoire fixée à 42), extrait 11 caractéristiques
par URL, entraîne une régression logistique et une forêt aléatoire, puis affiche
matrice de confusion, rapport de classification, compromis seuil / rappel et
importance des caractéristiques. Elle écrit ses figures dans `demo/figures/` et le
jeu de données dans `demo/donnees/urls_simulees.csv`.

> **Données simulées.** Aucune URL réelle n'est collectée ni téléchargée. Les URL
> et les étiquettes sont synthétiques, à but pédagogique ; environ 7 % d'étiquettes
> sont bruitées volontairement pour obtenir un problème réaliste (ni trivial ni
> parfait). Les chiffres affichés sont donc reproductibles d'une machine à l'autre.


## Reproductibilité

- Graine aléatoire fixée (`GRAINE = 42`) dans les deux scripts.
- Aucune dépendance réseau : tout est calculé localement.
- Les versions de `requirements.txt` sont celles utilisées pour produire les
  figures et chiffres du cours.

## Public et périmètre

Dépôt public à vocation pédagogique. Il ne contient ni données personnelles, ni
URL réelles, ni le diaporama du cours.

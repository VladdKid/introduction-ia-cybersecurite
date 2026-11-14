# Introduction à l'IA — M2 Cybersécurité

Support de code du cours « Introduction à l'intelligence artificielle » (première
séance, 6 h) destiné à des étudiants de M2 cybersécurité.

Ce dépôt contient **uniquement le code source** de la démonstration scikit-learn,
sous deux formes :

- **un notebook Jupyter expliqué pas à pas** — la forme recommandée pour le cours ;
- un script Python compact — la même démonstration, sans les explications.

Les images, les jeux de données et le diaporama `.pptx` sont générés ou conservés
en local ; ils ne sont pas versionnés.

## Contenu

```
.
├── demo/
│   ├── demo_phishing.ipynb   # Démo expliquée ligne par ligne (notebook) ← recommandé
│   └── demo_phishing.py      # Même démo en script compact (écrit figures + données)
├── requirements.txt          # Dépendances Python
└── README.md
```

## Récupérer le code (cloner)

« **Cloner** » = télécharger une copie complète du dépôt GitHub sur votre machine.
Ouvrez un terminal (sous Windows : *PowerShell* ou *Git Bash*) et tapez :

```bash
git clone https://github.com/VladdKid/introduction-ia-cybersecurite.git
cd introduction-ia-cybersecurite
```

- `git clone <url>` crée un dossier `introduction-ia-cybersecurite/` avec tout le code.
- `cd ...` (« *change directory* ») vous place **dans** ce dossier.
- Pas de `git` ? Installez-le depuis <https://git-scm.com>, ou téléchargez le ZIP via
  le bouton vert **Code ▸ Download ZIP** sur la page GitHub, puis décompressez.

## Installer les bibliothèques

Python 3.10 ou plus récent. Un **environnement virtuel** isole les bibliothèques du
projet du reste de votre machine :

```bash
python -m venv .venv
# Windows : .venv\Scripts\activate   |   Linux/macOS : source .venv/bin/activate
pip install -r requirements.txt
```

## Lancer la démonstration (notebook, recommandé)

```bash
jupyter notebook demo/demo_phishing.ipynb
```

Le navigateur s'ouvre sur le notebook ; choisissez le kernel `.venv` puis
*Run All* / *Tout exécuter*. Vous pouvez aussi l'ouvrir depuis **VS Code**
(extensions *Python* + *Jupyter*) ou **JupyterLab**.

Le notebook est pensé pour des étudiants qui **savent coder mais n'ont jamais fait
de machine learning** : chaque terme du domaine y est défini en français avec une
analogie (classification vs régression, graine aléatoire / `random_state`,
régression logistique, forêt aléatoire, matrice de confusion, précision / rappel /
F1, seuil de décision, ROC/AUC…), et **chaque ligne de code est commentée**. Les
figures s'affichent directement dans le notebook.

## Variante script (compact)

```bash
python demo/demo_phishing.py
```

Même démonstration, sans les explications interleavées. Elle affiche les mêmes
chiffres et écrit ses figures dans `demo/figures/` ainsi que le jeu de données dans
`demo/donnees/urls_simulees.csv` (dossiers ignorés par git).

## Données simulées et reproductibilité

- **2 000 URL entièrement simulées**, fabriquées localement : aucune URL réelle
  n'est collectée ni téléchargée. Tout fonctionne **hors ligne**.
- **Graine aléatoire fixée** (`GRAINE = 42`) : le pseudo-hasard est reproductible,
  donc les chiffres sont identiques d'une machine à l'autre et d'un lancement à
  l'autre.
- **~7 % d'étiquettes bruitées** volontairement : le problème est réaliste (ni
  trivial ni parfait), aucun modèle ne peut atteindre 100 %.
- Les versions de `requirements.txt` sont celles utilisées pour produire les
  chiffres du cours.

## Public et périmètre

Dépôt public à vocation pédagogique. Il ne contient ni données personnelles, ni
URL réelles, ni le diaporama du cours.
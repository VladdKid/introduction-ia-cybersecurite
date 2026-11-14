# Introduction à l'IA — M2 Cybersécurité

Support de code du cours « Introduction à l'intelligence artificielle » (première
séance, 6 h) destiné à des étudiants de M2 cybersécurité.

Ce dépôt contient **uniquement le code source** de la démonstration scikit-learn,
sous trois formes :

- **un notebook Jupyter expliqué pas à pas** — la forme recommandée pour le cours ;
- **un TP auto-évalué** — l'étudiant entraîne et évalue lui-même les modèles, guidé
  par des indices et des cellules de vérification (corrigé communiqué après le TP) ;
- un script Python compact — la même démonstration, sans les explications.

Les images, les jeux de données et le diaporama `.pptx` sont générés ou conservés
en local ; ils ne sont pas versionnés.

## Contenu

```
.
├── demo/
│   ├── demo_phishing.ipynb   # Démo expliquée ligne par ligne (notebook) ← recommandé
│   ├── demo_tests.ipynb      # TP auto-évalué : à compléter par l'étudiant
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

## Version Google Colab (sans Jupyter, dans le navigateur)

Si vous n'avez **pas Python / Jupyter installés**, utilisez **Google Colab** : le
notebook s'exécute **dans le navigateur**, sur une machine fournie par Google —
**rien à installer** sur votre PC (un compte Google suffit).

- **Démo expliquée :**
  [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/VladdKid/introduction-ia-cybersecurite/blob/main/demo/demo_phishing.ipynb)
- **TP auto-évalué :**
  [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/VladdKid/introduction-ia-cybersecurite/blob/main/demo/demo_tests.ipynb)

Ou manuellement : <https://colab.research.google.com> → *Fichier* → *Ouvrir le
notebook* → onglet **GitHub** → collez
`https://github.com/VladdKid/introduction-ia-cybersecurite` → choisissez le
notebook dans `demo/`. Puis *Exécution* → *Tout exécuter*.

Colab **préinstalle** `numpy`, `pandas`, `scikit-learn` et `matplotlib` : aucune
installation n'est nécessaire. Une session Colab est **éphémère**, mais sans
importance ici : les notebooks **fabriquent leurs données simulées** à chaque
exécution et n'écrivent aucun fichier ; la graine fixée (42) garantit les mêmes
chiffres. Pour travailler **hors ligne / sans compte Google**, utilisez la méthode
clone + venv + Jupyter ci-dessous.

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

## TP auto-évalué (tester soi-même)

```bash
jupyter notebook demo/demo_tests.ipynb
```

Contrairement à la démo (qui montre tout), le **TP fait coder l'étudiant** : chaque
exercice donne un **but**, un **squelette de code avec des trous** (`...` /
`# TODO`) à compléter, des **indices progressifs** (du plus vague au plus précis),
et une **cellule de vérification** (`assert`) qui confirme ou guide vers la bonne
réponse. Six exercices, pas trop difficiles : toute la préparation des données est
fournie, l'étudiant ne remplit que 1 à 3 lignes par exercice.

1. Entraîner la régression logistique (scaler + pipeline).
2. Entraîner la forêt aléatoire (200 arbres, graine fixée).
3. Prédire sur le test + matrice de confusion.
4. Calculer précision / rappel / F1 **à la main** depuis la matrice.
5. Observer l'effet du **seuil** sur précision / rappel.
6. Courbe **ROC** et **AUC**.

Le **corrigé** n'est pas dans le dépôt pour l'instant : il est communiqué par
l'enseignant **après le TP**, pour laisser les étudiants chercher.

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
# -*- coding: utf-8 -*-
"""
Génère toutes les figures « concept » du support de cours
Introduction à l'IA (M2 Cybersécurité), dans la palette du deck.

Exécution :  python scripts/figures_cours.py
Sortie   :  figures/*.png   (hors ligne, aucune donnée réelle)
"""
import os
import sys
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyBboxPatch, Rectangle, FancyArrowPatch

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

ICI = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(os.path.dirname(ICI), "figures")
os.makedirs(OUT, exist_ok=True)

BRONZE = "#B4690E"
NAVY = "#13263B"
BLEU = "#283C52"
VERT = "#157F5C"
GRIS = "#5A6E86"
CLAIR = "#EDF2F8"
SABLE = "#DBC6AD"

plt.rcParams.update({
    "font.family": "DejaVu Sans", "font.size": 11,
    "axes.edgecolor": GRIS, "axes.labelcolor": NAVY, "text.color": NAVY,
    "xtick.color": GRIS, "ytick.color": GRIS,
    "axes.spines.top": False, "axes.spines.right": False,
    "figure.dpi": 150, "savefig.dpi": 150,
})
rng = np.random.default_rng(7)


def save(fig, nom):
    fig.savefig(os.path.join(OUT, nom + ".png"), bbox_inches="tight",
                facecolor="white")
    plt.close(fig)
    print("  ", nom)


def boite(ax, x, y, w, h, texte, fc=CLAIR, ec=GRIS, fs=11, tc=NAVY, bold=False):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02,rounding_size=0.06",
                                fc=fc, ec=ec, lw=1.2))
    ax.text(x + w / 2, y + h / 2, texte, ha="center", va="center",
            fontsize=fs, color=tc, fontweight="bold" if bold else "normal")


def fleche(ax, p1, p2, color=GRIS, lw=1.6):
    ax.add_patch(FancyArrowPatch(p1, p2, arrowstyle="-|>", mutation_scale=14,
                                 color=color, lw=lw))


# 1 ---------------------------------------------------------------- pipeline
def f_pipeline():
    fig, ax = plt.subplots(figsize=(5.0, 3.2)); ax.set_xlim(0, 10); ax.set_ylim(0, 6); ax.axis("off")
    boite(ax, 0.2, 2.4, 2.6, 1.4, "Entrée x\nune URL", fs=12)
    boite(ax, 3.7, 2.2, 2.6, 1.8, "f(θ)\nle modèle", fc=BRONZE, ec=BRONZE, tc="white", fs=13, bold=True)
    boite(ax, 7.2, 2.4, 2.6, 1.4, "Sortie ŷ\nscore 0–1", fs=12)
    fleche(ax, (2.8, 3.1), (3.7, 3.1)); fleche(ax, (6.3, 3.1), (7.2, 3.1))
    ax.text(5.0, 1.2, "θ : paramètres réglés par l'entraînement", ha="center", fontsize=10, color=GRIS)
    ax.text(5.0, 5.2, "Objectif : minimiser l'erreur sur ŷ", ha="center", fontsize=11, color=NAVY)
    save(fig, "fig_pipeline")


# 2 ---------------------------------------------------------------- cercles
def f_cercles():
    fig, ax = plt.subplots(figsize=(4.6, 4.2)); ax.set_xlim(0, 10); ax.set_ylim(0, 10); ax.axis("off")
    ax.add_patch(Circle((5, 5), 4.6, fc=CLAIR, ec=GRIS, lw=1.4))
    ax.add_patch(Circle((5, 4.4), 3.2, fc="#E1E9F4", ec=BLEU, lw=1.4))
    ax.add_patch(Circle((5, 3.8), 1.9, fc=BRONZE, ec=BRONZE, lw=1.4, alpha=0.85))
    ax.text(5, 9.0, "Intelligence artificielle", ha="center", fontsize=12, color=NAVY, fontweight="bold")
    ax.text(5, 7.0, "Apprentissage automatique", ha="center", fontsize=11, color=BLEU)
    ax.text(5, 3.8, "Apprentissage\nprofond", ha="center", va="center", fontsize=10, color="white", fontweight="bold")
    ax.text(5, 0.4, "règles, graphes, planification : de l'IA sans apprentissage", ha="center", fontsize=9, color=GRIS)
    save(fig, "fig_cercles")


# 3 ---------------------------------------------------------------- histoire
def f_histoire():
    fig, ax = plt.subplots(figsize=(11, 2.5)); ax.set_xlim(1945, 2028); ax.set_ylim(-1.6, 1.9); ax.axis("off")
    ax.axhline(0, color=GRIS, lw=1.5)
    # deux hivers
    for a, b in [(1974, 1980), (1987, 1993)]:
        ax.add_patch(Rectangle((a, -0.35), b - a, 0.7, fc=SABLE, alpha=0.5, ec="none"))
    ev = [(1950, "Turing", 1), (1958, "Perceptron", -1), (1969, "XOR (Minsky)", 1),
          (1986, "Rétroprop.", -1), (2012, "AlexNet", 1), (2017, "Transformer", -1),
          (2020, "GPT-3", 1), (2022, "LLM grand public", -1)]
    for x, lab, cote in ev:
        ax.plot([x], [0], "o", color=BRONZE, ms=7)
        ax.plot([x, x], [0, 0.5 * cote], color=GRIS, lw=1)
        ax.text(x, 0.62 * cote + (0.15 if cote > 0 else -0.15), f"{x}\n{lab}",
                ha="center", va="bottom" if cote > 0 else "top", fontsize=9, color=NAVY)
    ax.text(1977, -1.35, "hiver", ha="center", fontsize=8, color=GRIS)
    ax.text(1990, -1.35, "hiver", ha="center", fontsize=8, color=GRIS)
    save(fig, "fig_histoire")


# 4 ---------------------------------------------------------------- domaines
def f_domaines():
    fig, ax = plt.subplots(figsize=(11, 2.6)); ax.set_xlim(0, 10); ax.set_ylim(0, 3); ax.axis("off")
    dom = [("Anti-phishing", "précision / rappel"), ("Anti-malware", "taux de détection"),
           ("Détection d'intrusion", "rappel, faux positifs"), ("Analyse de logs", "anomalies rares"),
           ("Trafic réseau", "erreur de prévision")]
    w = 1.86
    for i, (t, m) in enumerate(dom):
        x = 0.1 + i * (w + 0.12)
        boite(ax, x, 1.1, w, 1.5, t + "\n\n" + m, fs=9.5)
    ax.text(5, 0.4, "Point commun : dans chaque cas, on sait mesurer l'erreur.", ha="center", fontsize=11, color=NAVY)
    save(fig, "fig_domaines")


# 5 ---------------------------------------------------------------- deux cas
def f_deuxcas():
    fig, axes = plt.subplots(1, 2, figsize=(5.0, 3.2))
    for ax in axes: ax.set_xlim(0, 10); ax.set_ylim(0, 6); ax.axis("off")
    a = axes[0]
    boite(a, 0.3, 3.4, 4.2, 1.2, "URL", fs=11); boite(a, 5.5, 3.4, 4.2, 1.2, "score phishing", fs=11)
    fleche(a, (4.5, 4.0), (5.5, 4.0))
    a.text(5, 5.4, "Prédictif : classer", ha="center", fontsize=12, color=NAVY, fontweight="bold")
    a.text(5, 1.6, "données étiquetées\nmétrique : erreur de classe", ha="center", fontsize=9, color=GRIS)
    b = axes[1]
    boite(b, 0.3, 3.4, 4.2, 1.2, "début de texte", fs=11); boite(b, 5.5, 3.4, 4.2, 1.2, "token suivant", fs=11)
    fleche(b, (4.5, 4.0), (5.5, 4.0))
    b.text(5, 5.4, "Génératif : prédire", ha="center", fontsize=12, color=NAVY, fontweight="bold")
    b.text(5, 1.6, "texte massif\nmétrique : vraisemblance", ha="center", fontsize=9, color=GRIS)
    save(fig, "fig_deuxcas")


# 6 ---------------------------------------------------------------- paradigmes
def f_paradigmes():
    fig, axes = plt.subplots(1, 3, figsize=(11, 2.7))
    titres = ["Supervisé", "Non supervisé", "Renforcement"]
    for ax, t in zip(axes, titres):
        ax.set_xlim(0, 10); ax.set_ylim(0, 6); ax.axis("off")
        ax.text(5, 5.5, t, ha="center", fontsize=12, color=NAVY, fontweight="bold")
    a = axes[0]
    a.scatter([2, 3, 2.5], [3, 3.4, 2.4], c=BLEU, s=60)
    a.scatter([7, 8, 7.5], [3, 3.4, 2.4], c=BRONZE, s=60)
    a.text(5, 1.2, "étiquettes fournies\n(bénin / phishing)", ha="center", fontsize=9, color=GRIS)
    b = axes[1]
    b.scatter(rng.uniform(1, 9, 24), rng.uniform(2, 4.4, 24), c=GRIS, s=50)
    b.text(5, 1.2, "aucune étiquette\non cherche une structure", ha="center", fontsize=9, color=GRIS)
    c = axes[2]
    boite(c, 0.6, 2.6, 3.4, 1.4, "agent", fs=10); boite(c, 6.0, 2.6, 3.4, 1.4, "environnement", fs=10)
    fleche(c, (4.0, 3.6), (6.0, 3.6)); fleche(c, (6.0, 2.9), (4.0, 2.9))
    c.text(5, 4.4, "action", ha="center", fontsize=8, color=GRIS)
    c.text(5, 2.2, "état + récompense", ha="center", fontsize=8, color=GRIS)
    c.text(5, 1.0, "signal de récompense, souvent retardé", ha="center", fontsize=9, color=GRIS)
    save(fig, "fig_paradigmes")


# 7 ---------------------------------------------------------------- class / reg
def f_classreg():
    fig, axes = plt.subplots(1, 2, figsize=(5.0, 3.2))
    a = axes[0]
    x1 = rng.normal(2, 0.7, 40); x2 = rng.normal(6, 0.7, 40)
    a.scatter(x1, rng.normal(3, 0.7, 40), c=BLEU, s=25, label="bénin")
    a.scatter(x2, rng.normal(6, 0.7, 40), c=BRONZE, s=25, label="phishing")
    a.plot([4.2, 4.2], [0, 9], color=GRIS, ls="--")
    a.set_xlim(0, 9); a.set_ylim(0, 9); a.set_title("Classification : une classe", fontsize=11)
    a.legend(frameon=False, fontsize=8, loc="upper left")
    b = axes[1]
    x = np.linspace(0, 9, 60); y = 0.8 * x + 1 + rng.normal(0, 0.8, 60)
    b.scatter(x, y, c=BLEU, s=20)
    b.plot(x, 0.8 * x + 1, color=BRONZE, lw=2)
    b.set_title("Régression : une valeur", fontsize=11)
    save(fig, "fig_classreg")


# 8 ---------------------------------------------------------------- split
def f_split():
    fig, ax = plt.subplots(figsize=(11, 1.7)); ax.set_xlim(0, 10); ax.set_ylim(0, 2); ax.axis("off")
    seg = [(0, 6, "Entraînement 60 %", BLEU), (6, 8, "Validation 20 %", BRONZE), (8, 10, "Test 20 %", VERT)]
    for a, b, lab, c in seg:
        ax.add_patch(Rectangle((a, 0.7), b - a, 0.7, fc=c, ec="white", lw=2))
        ax.text((a + b) / 2, 1.05, lab, ha="center", va="center", color="white", fontsize=11, fontweight="bold")
    ax.text(3, 0.3, "ajuste les paramètres", ha="center", fontsize=9, color=GRIS)
    ax.text(7, 0.3, "choisit les hyperparamètres", ha="center", fontsize=9, color=GRIS)
    ax.text(9, 0.3, "mesuré une seule fois", ha="center", fontsize=9, color=GRIS)
    save(fig, "fig_split")


# 9 ---------------------------------------------------------------- surapprentissage
def f_surapprentissage():
    fig, axes = plt.subplots(1, 3, figsize=(11, 2.8))
    x = np.linspace(0, 6, 40); vrai = np.sin(x)
    y = vrai + rng.normal(0, 0.25, 40)
    titres = ["Sous-apprendre", "Capacité adaptée", "Surapprendre"]
    for ax, t in zip(axes, titres):
        ax.scatter(x, y, c=GRIS, s=18)
        ax.set_title(t, fontsize=11); ax.set_xticks([]); ax.set_yticks([])
    axes[0].plot(x, 0.2 * x + 0.2, color=BRONZE, lw=2)
    axes[1].plot(x, vrai, color=BRONZE, lw=2)
    xs = np.linspace(0, 6, 200)
    axes[2].plot(xs, np.interp(xs, x, y), color=BRONZE, lw=1.5)
    save(fig, "fig_surapprentissage")


# 10 --------------------------------------------------------------- courbe
def f_courbe():
    fig, ax = plt.subplots(figsize=(5.0, 3.3))
    e = np.arange(1, 201)
    tr = 0.7 * np.exp(-e / 40) + 0.02
    va = 0.7 * np.exp(-e / 45) + 0.05 + 0.0009 * np.maximum(0, e - 60) ** 1.3
    ax.plot(e, tr, color=BLEU, lw=2, label="perte d'entraînement")
    ax.plot(e, va, color=BRONZE, lw=2, label="perte de validation")
    i = int(np.argmin(va))
    ax.axvline(e[i], color=VERT, ls="--", lw=1.2)
    ax.text(e[i] + 4, va.max() * 0.8, "arrêt anticipé", color=VERT, fontsize=9)
    ax.set_xlabel("époque"); ax.set_ylabel("perte"); ax.legend(frameon=False, fontsize=9)
    ax.set_title("La validation remonte : on arrête", fontsize=11)
    save(fig, "fig_courbe")


# 11 --------------------------------------------------------------- kmeans
def f_kmeans():
    from sklearn.cluster import KMeans
    fig, ax = plt.subplots(figsize=(5.0, 3.4))
    centres = np.array([[2, 2], [6, 6], [7, 2]])
    X = np.vstack([c + rng.normal(0, 0.7, (60, 2)) for c in centres])
    km = KMeans(n_clusters=3, n_init=10, random_state=0).fit(X)
    cols = [BLEU, BRONZE, VERT]
    for k in range(3):
        m = km.labels_ == k
        ax.scatter(X[m, 0], X[m, 1], c=cols[k], s=22)
    ax.scatter(km.cluster_centers_[:, 0], km.cluster_centers_[:, 1],
               marker="X", c="black", s=120, zorder=5)
    ax.set_title("k-means : k groupes, sans étiquette", fontsize=11)
    ax.set_xticks([]); ax.set_yticks([])
    save(fig, "fig_kmeans")


# 12 --------------------------------------------------------------- acp
def f_acp():
    from sklearn.decomposition import PCA
    fig, ax = plt.subplots(figsize=(5.0, 3.4))
    X = rng.normal(0, 1, (200, 6)) @ rng.normal(0, 1, (6, 6))
    p = PCA(n_components=2).fit(X)
    Z = p.transform(X)
    ax.scatter(Z[:, 0], Z[:, 1], c=BLEU, s=20, alpha=0.7)
    ax.set_xlabel(f"CP1 ({p.explained_variance_ratio_[0]*100:.0f} %)")
    ax.set_ylabel(f"CP2 ({p.explained_variance_ratio_[1]*100:.0f} %)")
    ax.set_title("ACP : projeter pour voir", fontsize=11)
    save(fig, "fig_acp")


# 13 --------------------------------------------------------------- rl
def f_rl():
    fig, ax = plt.subplots(figsize=(5.0, 3.3)); ax.set_xlim(0, 10); ax.set_ylim(0, 6); ax.axis("off")
    boite(ax, 0.6, 2.4, 3.4, 1.6, "Agent\n(le défenseur)", fs=11)
    boite(ax, 6.0, 2.4, 3.4, 1.6, "Environnement\n(le réseau)", fs=11)
    fleche(ax, (4.0, 3.6), (6.0, 3.6), color=BRONZE)
    fleche(ax, (6.0, 2.7), (4.0, 2.7), color=BLEU)
    ax.text(5, 4.1, "action", ha="center", fontsize=10, color=BRONZE)
    ax.text(5, 2.1, "état + récompense", ha="center", fontsize=10, color=BLEU)
    ax.text(5, 5.3, "Apprendre par renforcement", ha="center", fontsize=12, color=NAVY, fontweight="bold")
    ax.text(5, 0.9, "aucune bonne réponse : seulement un signal", ha="center", fontsize=9, color=GRIS)
    save(fig, "fig_rl")


# 14 --------------------------------------------------------------- bandit
def f_bandit():
    fig, ax = plt.subplots(figsize=(5.0, 3.3))
    t = np.arange(1, 401)
    for eps, c, lab in [(0.0, GRIS, "ε = 0 (exploite)"), (0.1, BRONZE, "ε = 0,1"), (0.5, BLEU, "ε = 0,5 (explore trop)")]:
        gains = 0.6 + 0.4 * (1 - np.exp(-t / (60 + 200 * eps))) - eps * 0.25
        ax.plot(t, np.cumsum(gains) / t, color=c, lw=2, label=lab)
    ax.set_xlabel("essais"); ax.set_ylabel("gain moyen")
    ax.set_title("Explorer ou exploiter", fontsize=11)
    ax.legend(frameon=False, fontsize=8)
    save(fig, "fig_bandit")


# 15 --------------------------------------------------------------- confusion concept
def f_confusion_concept():
    fig, ax = plt.subplots(figsize=(4.4, 3.8))
    cm = np.array([[9850, 60], [90, 60]])  # IDS déséquilibré : 1,5 % d'attaques
    ax.imshow(cm, cmap="Oranges", vmin=0, vmax=cm.max())
    ax.set_xticks([0, 1]); ax.set_yticks([0, 1])
    ax.set_xticklabels(["prédit bénin", "prédit attaque"], fontsize=9)
    ax.set_yticklabels(["vrai bénin", "vrai attaque"], fontsize=9)
    lab = [["VN", "FP"], ["FN", "VP"]]
    for i in range(2):
        for j in range(2):
            ax.text(j, i - 0.16, lab[i][j], ha="center", fontsize=10,
                    color="white" if cm[i, j] > cm.max() * 0.5 else NAVY, fontweight="bold")
            ax.text(j, i + 0.16, f"{cm[i,j]}", ha="center", fontsize=12,
                    color="white" if cm[i, j] > cm.max() * 0.5 else NAVY)
    ax.set_title("IDS : 98,5 % de bénin\n« tout bénin » = 98,5 % d'exactitude", fontsize=10)
    save(fig, "fig_confusion_concept")


# 16 --------------------------------------------------------------- prec rap
def f_precrap():
    fig, ax = plt.subplots(figsize=(5.0, 3.3))
    s = np.linspace(0.05, 0.95, 90)
    prec = 0.3 + 0.68 / (1 + np.exp(-(s - 0.45) * 9))
    rap = 0.98 - 0.75 / (1 + np.exp(-(s - 0.5) * 9))
    f1 = 2 * prec * rap / (prec + rap)
    ax.plot(s, prec, color=BRONZE, lw=2, label="précision")
    ax.plot(s, rap, color=BLEU, lw=2, label="rappel")
    ax.plot(s, f1, color=VERT, lw=2, label="F1")
    ax.set_xlabel("seuil"); ax.set_ylabel("score"); ax.set_ylim(0, 1.02)
    ax.set_title("Le seuil arbitre le compromis", fontsize=11)
    ax.legend(frameon=False, fontsize=9)
    save(fig, "fig_precrap")


# 17 --------------------------------------------------------------- regression
def f_regression():
    fig, ax = plt.subplots(figsize=(5.0, 3.3))
    y = rng.uniform(0, 10, 60); yp = y + rng.normal(0, 0.9, 60)
    ax.scatter(y, yp, c=BLEU, s=22)
    ax.plot([0, 10], [0, 10], color=BRONZE, ls="--", lw=1.5)
    mae = np.abs(y - yp).mean(); rmse = np.sqrt(((y - yp) ** 2).mean())
    r2 = 1 - ((y - yp) ** 2).sum() / ((y - y.mean()) ** 2).sum()
    ax.set_xlabel("valeur vraie"); ax.set_ylabel("valeur prédite")
    ax.set_title(f"MAE {mae:.2f} · RMSE {rmse:.2f} · R² {r2:.2f}", fontsize=11)
    save(fig, "fig_regression")


# 18 --------------------------------------------------------------- neurone
def f_neurone():
    fig, ax = plt.subplots(figsize=(5.0, 3.2)); ax.set_xlim(0, 10); ax.set_ylim(0, 6); ax.axis("off")
    for i, y in enumerate([4.6, 3.0, 1.4]):
        ax.add_patch(Circle((1.2, y), 0.42, fc=CLAIR, ec=GRIS))
        ax.text(1.2, y, f"x{i+1}", ha="center", va="center", fontsize=10)
        fleche(ax, (1.65, y), (4.0, 3.0), color=GRIS)
        ax.text(2.7, y + (0.35 if y > 3 else -0.45), f"w{i+1}", fontsize=9, color=BRONZE)
    ax.add_patch(Circle((4.6, 3.0), 0.62, fc=BRONZE, ec=BRONZE))
    ax.text(4.6, 3.0, "Σ + b", ha="center", va="center", color="white", fontsize=10, fontweight="bold")
    fleche(ax, (5.25, 3.0), (6.6, 3.0))
    boite(ax, 6.6, 2.4, 1.8, 1.2, "f\nactivation", fs=10)
    fleche(ax, (8.4, 3.0), (9.3, 3.0))
    ax.text(9.6, 3.0, "ŷ", ha="center", va="center", fontsize=13, color=NAVY, fontweight="bold")
    ax.text(5, 5.5, "y = f(w·x + b)", ha="center", fontsize=12, color=NAVY)
    save(fig, "fig_neurone")


# 19 --------------------------------------------------------------- xor
def f_xor():
    fig, axes = plt.subplots(1, 2, figsize=(5.0, 3.2))
    pts = np.array([[0, 0], [0, 1], [1, 0], [1, 1]]); lab = np.array([0, 1, 1, 0])
    for ax in axes:
        ax.scatter(pts[lab == 0, 0], pts[lab == 0, 1], c=BLEU, s=90, marker="o")
        ax.scatter(pts[lab == 1, 0], pts[lab == 1, 1], c=BRONZE, s=90, marker="s")
        ax.set_xlim(-0.4, 1.4); ax.set_ylim(-0.4, 1.4); ax.set_xticks([0, 1]); ax.set_yticks([0, 1])
    axes[0].plot([-0.3, 1.3], [1.3, -0.3], color=GRIS, ls="--")
    axes[0].set_title("Perceptron : aucune droite", fontsize=10)
    t = np.linspace(-0.3, 1.3, 100)
    axes[1].plot(t, 0.5 + 0.45 * np.sin((t - 0.5) * 3.2), color=VERT, lw=2)
    axes[1].set_title("Couche cachée : séparable", fontsize=10)
    save(fig, "fig_xor")


# 20 --------------------------------------------------------------- reseau
def f_reseau():
    fig, ax = plt.subplots(figsize=(5.0, 3.4)); ax.set_xlim(0, 10); ax.set_ylim(0, 6); ax.axis("off")
    couches = [3, 4, 4, 2]; xs = [1.2, 3.8, 6.2, 8.8]
    pos = []
    for n, x in zip(couches, xs):
        ys = np.linspace(3 - (n - 1) * 0.55, 3 + (n - 1) * 0.55, n)
        pos.append([(x, y) for y in ys])
    for l in range(3):
        for (x1, y1) in pos[l]:
            for (x2, y2) in pos[l + 1]:
                ax.plot([x1, x2], [y1, y2], color="#C9D6E5", lw=0.7, zorder=1)
    for l, p in enumerate(pos):
        for (x, y) in p:
            c = BRONZE if l in (0, 3) else BLEU
            ax.add_patch(Circle((x, y), 0.28, fc=c, ec="white", lw=1, zorder=2))
    ax.text(1.2, 5.5, "entrée", ha="center", fontsize=9, color=GRIS)
    ax.text(5.0, 5.5, "couches cachées", ha="center", fontsize=9, color=GRIS)
    ax.text(8.8, 5.5, "sortie", ha="center", fontsize=9, color=GRIS)
    ax.text(5, 0.5, "z = W·a + b, puis activation, à chaque couche", ha="center", fontsize=10, color=NAVY)
    save(fig, "fig_reseau")


# 21 --------------------------------------------------------------- activations
def f_activations():
    fig, ax = plt.subplots(figsize=(5.0, 3.2))
    z = np.linspace(-4, 4, 200)
    ax.plot(z, np.maximum(0, z), color=BRONZE, lw=2, label="ReLU")
    ax.plot(z, 1 / (1 + np.exp(-z)), color=BLEU, lw=2, label="sigmoïde")
    ax.plot(z, np.tanh(z), color=VERT, lw=2, label="tanh")
    ax.axhline(0, color="#C9D6E5", lw=0.8); ax.axvline(0, color="#C9D6E5", lw=0.8)
    ax.set_xlabel("z"); ax.set_ylabel("activation"); ax.set_ylim(-1.3, 4)
    ax.legend(frameon=False, fontsize=9); ax.set_title("Trois non-linéarités", fontsize=11)
    save(fig, "fig_activations")


# 22 --------------------------------------------------------------- softmax
def f_softmax():
    fig, axes = plt.subplots(1, 2, figsize=(5.0, 3.0))
    logits = np.array([3.0, 1.5, 0.5, -0.5])
    p = np.exp(logits) / np.exp(logits).sum()
    axes[0].bar(range(4), logits, color=BLEU)
    axes[0].set_title("logits (scores bruts)", fontsize=10); axes[0].set_xticks(range(4))
    axes[1].bar(range(4), p, color=BRONZE)
    axes[1].set_title("softmax (somme = 1)", fontsize=10); axes[1].set_xticks(range(4))
    for i, v in enumerate(p):
        axes[1].text(i, v + 0.02, f"{v:.2f}", ha="center", fontsize=9)
    save(fig, "fig_softmax")


# 23 --------------------------------------------------------------- epoque
def f_epoque():
    fig, ax = plt.subplots(figsize=(5.0, 3.3)); ax.set_xlim(0, 10); ax.set_ylim(0, 6); ax.axis("off")
    boite(ax, 0.4, 3.6, 4.2, 1.3, "1. Passe avant\nsortie + perte", fs=10)
    boite(ax, 5.4, 3.6, 4.2, 1.3, "2. Rétropropagation\ngradient", fs=10)
    boite(ax, 5.4, 1.2, 4.2, 1.3, "3. Mise à jour\nw ← w − η·g", fs=10)
    boite(ax, 0.4, 1.2, 4.2, 1.3, "4. Recommencer\népoque suivante", fs=10)
    fleche(ax, (4.6, 4.25), (5.4, 4.25)); fleche(ax, (7.5, 3.6), (7.5, 2.5))
    fleche(ax, (5.4, 1.85), (4.6, 1.85)); fleche(ax, (2.5, 2.5), (2.5, 3.6))
    ax.text(5, 5.5, "Une époque, quatre étapes", ha="center", fontsize=12, color=NAVY, fontweight="bold")
    save(fig, "fig_epoque")


# 24 --------------------------------------------------------------- gradient
def f_gradient():
    fig, ax = plt.subplots(figsize=(5.0, 3.4))
    x = np.linspace(-3, 3, 120); y = np.linspace(-3, 3, 120)
    X, Y = np.meshgrid(x, y); Z = X ** 2 + 2 * Y ** 2
    cs = ax.contour(X, Y, Z, levels=12, cmap="Oranges")
    px, py = [2.6], [2.4]
    for _ in range(14):
        gx, gy = 2 * px[-1], 4 * py[-1]
        px.append(px[-1] - 0.16 * gx); py.append(py[-1] - 0.16 * gy)
    ax.plot(px, py, "o-", color=NAVY, ms=4, lw=1.4)
    ax.set_xlabel("w1"); ax.set_ylabel("w2")
    ax.set_title("Descendre le gradient : −η·∇L", fontsize=11)
    save(fig, "fig_gradient")


# 25 --------------------------------------------------------------- backprop
def f_backprop():
    fig, ax = plt.subplots(figsize=(5.0, 3.0)); ax.set_xlim(0, 10); ax.set_ylim(0, 5); ax.axis("off")
    noms = ["entrée", "couche 1", "couche 2", "perte L"]
    xs = [0.4, 2.9, 5.4, 7.9]
    for x, n in zip(xs, noms):
        boite(ax, x, 2.2, 1.9, 1.1, n, fs=10)
    for i in range(3):
        fleche(ax, (xs[i] + 1.9, 3.0), (xs[i + 1], 3.0), color=BLEU)
    for i in range(3, 0, -1):
        fleche(ax, (xs[i], 1.7), (xs[i - 1] + 1.9, 1.7), color=BRONZE)
    ax.text(5, 4.2, "avant : calcul de la sortie", ha="center", fontsize=10, color=BLEU)
    ax.text(5, 0.9, "arrière : le gradient par la règle de chaîne", ha="center", fontsize=10, color=BRONZE)
    save(fig, "fig_backprop")


# 26 --------------------------------------------------------------- lr
def f_lr():
    fig, axes = plt.subplots(1, 3, figsize=(11, 2.6))
    e = np.arange(1, 121)
    axes[0].plot(e, 0.8 * np.exp(-e / 300) + 0.1, color=GRIS, lw=2)
    axes[0].set_title("η trop petit : trop lent", fontsize=10)
    axes[1].plot(e, 0.8 * np.exp(-e / 25) + 0.05, color=VERT, lw=2)
    axes[1].set_title("η adapté : chute puis stable", fontsize=10)
    axes[2].plot(e, 0.5 + 0.35 * np.sin(e / 3) * np.exp(-e / 400) + 0.002 * e, color=BRONZE, lw=2)
    axes[2].set_title("η trop grand : oscille", fontsize=10)
    for ax in axes: ax.set_xlabel("époque"); ax.set_ylabel("perte"); ax.set_yticks([])
    save(fig, "fig_lr")


# 27 --------------------------------------------------------------- convolution
def f_convolution():
    fig, axes = plt.subplots(1, 3, figsize=(5.0, 3.0))
    img = rng.integers(0, 2, (7, 7))
    axes[0].imshow(img, cmap="Blues", vmin=0, vmax=1.4)
    axes[0].add_patch(Rectangle((1.5, 1.5), 3, 3, fc="none", ec=BRONZE, lw=2))
    axes[0].set_title("image 7×7", fontsize=9)
    filt = np.array([[1, 0, -1], [1, 0, -1], [1, 0, -1]])
    axes[1].imshow(filt, cmap="Oranges", vmin=-1.4, vmax=1.4)
    axes[1].set_title("filtre 3×3", fontsize=9)
    try:
        from scipy.signal import convolve2d
        fm = convolve2d(img, filt, mode="valid")
    except Exception:
        fm = np.zeros((5, 5))
    axes[2].imshow(fm, cmap="Oranges")
    axes[2].set_title("carte 5×5", fontsize=9)
    for ax in axes: ax.set_xticks([]); ax.set_yticks([])
    save(fig, "fig_convolution")


# 28 --------------------------------------------------------------- cnn
def f_cnn():
    fig, ax = plt.subplots(figsize=(11, 2.4)); ax.set_xlim(0, 12); ax.set_ylim(0, 3); ax.axis("off")
    etages = [("entrée\n224×224×3", 1.6, 2.2), ("conv\n112×112×32", 1.4, 1.9),
              ("pool\n56×56×32", 1.2, 1.6), ("conv\n28×28×64", 1.0, 1.3),
              ("pool\n14×14×64", 0.8, 1.0), ("denses\n+ softmax", 0.7, 0.8)]
    x = 0.2
    for lab, w, h in etages:
        boite(ax, x, 1.5 - h / 2, w, h, lab, fs=8.5)
        x += w + 0.35
        if x < 11:
            fleche(ax, (x - 0.33, 1.5), (x - 0.05, 1.5))
    ax.text(6, 0.3, "la résolution baisse, les canaux montent : localisation → sémantique", ha="center", fontsize=10, color=GRIS)
    save(fig, "fig_cnn")


# 29 --------------------------------------------------------------- pred vs gen
def f_predgen():
    fig, axes = plt.subplots(1, 2, figsize=(5.0, 3.2))
    a = axes[0]
    a.scatter(rng.normal(2.5, 0.8, 50), rng.normal(3, 0.8, 50), c=BLEU, s=18)
    a.scatter(rng.normal(6.5, 0.8, 50), rng.normal(6, 0.8, 50), c=BRONZE, s=18)
    a.plot([4.5, 4.5], [0, 9], color=GRIS, ls="--")
    a.set_xlim(0, 9); a.set_ylim(0, 9); a.set_title("p(y|x) : la décision", fontsize=10)
    b = axes[1]
    x = np.linspace(0, 9, 100); y = np.linspace(0, 9, 100)
    X, Y = np.meshgrid(x, y)
    Z = np.exp(-((X - 3) ** 2 + (Y - 3) ** 2) / 4) + np.exp(-((X - 6) ** 2 + (Y - 6) ** 2) / 4)
    b.contour(X, Y, Z, levels=6, cmap="Oranges")
    b.set_title("p(x) : la distribution", fontsize=10)
    save(fig, "fig_predgen")


# 30 --------------------------------------------------------------- autoregressif
def f_autoregressif():
    fig, ax = plt.subplots(figsize=(5.0, 3.2)); ax.set_xlim(0, 10); ax.set_ylim(0, 6); ax.axis("off")
    toks = ["Le", "chat", "dort", "sur", "le", "?"]
    x = 0.3
    for i, t in enumerate(toks):
        c = BRONZE if t == "?" else CLAIR
        tc = "white" if t == "?" else NAVY
        boite(ax, x, 3.6, 1.4, 1.0, t, fc=c, ec=GRIS, tc=tc, fs=11)
        x += 1.6
    probs = [0.42, 0.21, 0.12, 0.08]
    mots = ["canapé", "lit", "tapis", "sol"]
    for i, (m, p) in enumerate(zip(mots, probs)):
        ax.bar(1.2 + i * 2.2, p * 3, width=1.4, color=BRONZE if i == 0 else "#E1E9F4", bottom=0.4)
        ax.text(1.2 + i * 2.2, p * 3 + 0.5, f"{m}\n{p:.0%}", ha="center", fontsize=8)
    ax.text(5, 5.5, "À chaque pas : une distribution sur le token suivant", ha="center", fontsize=10, color=NAVY)
    save(fig, "fig_autoregressif")


# 31 --------------------------------------------------------------- temperature
def f_temperature():
    fig, axes = plt.subplots(1, 3, figsize=(5.0, 3.0))
    logits = np.array([3.0, 1.5, 0.5, -0.5, -1.5])
    for ax, T in zip(axes, [0.2, 1.0, 1.5]):
        p = np.exp(logits / T) / np.exp(logits / T).sum()
        ax.bar(range(5), p, color=BRONZE)
        ax.set_title(f"T = {T}", fontsize=10); ax.set_xticks([]); ax.set_ylim(0, 1)
    save(fig, "fig_temperature")


# 32 --------------------------------------------------------------- top-p
def f_topp():
    fig, ax = plt.subplots(figsize=(5.0, 3.2))
    p = np.array([0.42, 0.21, 0.12, 0.08, 0.06, 0.04, 0.03, 0.02, 0.01, 0.01])
    ax.bar(range(10), p, color=[BRONZE if i < 3 else "#E1E9F4" for i in range(10)])
    cum = np.cumsum(p)
    ax.plot(range(10), cum, color=VERT, lw=2, marker="o", ms=3)
    ax.axhline(0.8, color=GRIS, ls="--", lw=1)
    ax.text(6, 0.83, "p = 0,8", fontsize=9, color=GRIS)
    ax.set_xlabel("tokens triés"); ax.set_ylabel("probabilité")
    ax.set_title("Top-p : garder le noyau, couper la traîne", fontsize=10)
    save(fig, "fig_topp")


# 33 --------------------------------------------------------------- prompt
def f_prompt():
    fig, ax = plt.subplots(figsize=(5.0, 3.4)); ax.set_xlim(0, 10); ax.set_ylim(0, 6); ax.axis("off")
    boite(ax, 0.4, 4.3, 9.2, 1.3, "Tâche : classe l'URL en bénin ou phishing", fs=10)
    boite(ax, 0.4, 2.7, 9.2, 1.3, "Exemples : paypal-verify.xyz → phishing ; github.com → bénin", fs=9.5)
    boite(ax, 0.4, 1.1, 9.2, 1.3, "Format : réponds par un seul mot, sans phrase", fs=10)
    ax.text(5, 5.85, "Un prompt = tâche + exemple + format", ha="center", fontsize=11, color=NAVY, fontweight="bold")
    save(fig, "fig_prompt")


# 34 --------------------------------------------------------------- limites
def f_limites():
    fig, ax = plt.subplots(figsize=(5.0, 3.3)); ax.set_xlim(0, 10); ax.set_ylim(0, 6); ax.axis("off")
    boite(ax, 0.4, 3.4, 4.3, 1.6, "Fluide et plausible\n« CVE-2024-12345… »", fc="#E1E9F4", fs=10)
    boite(ax, 5.3, 3.4, 4.3, 1.6, "Mais inventé\nréférence introuvable", fc=BRONZE, ec=BRONZE, tc="white", fs=10)
    fleche(ax, (4.7, 4.2), (5.3, 4.2))
    ax.text(5, 5.5, "Le modèle optimise la vraisemblance, pas la vérité", ha="center", fontsize=10.5, color=NAVY)
    ax.text(5, 2.2, "phishing généré, injection de prompt,\ndeepfakes : mêmes mécanismes, nouveaux risques", ha="center", fontsize=9.5, color=GRIS)
    ax.text(5, 0.8, "Aucune incertitude calibrée en sortie", ha="center", fontsize=9.5, color=GRIS)
    save(fig, "fig_limites")


if __name__ == "__main__":
    print("Génération des figures du cours :")
    for f in [f_pipeline, f_cercles, f_histoire, f_domaines, f_deuxcas, f_paradigmes,
              f_classreg, f_split, f_surapprentissage, f_courbe, f_kmeans, f_acp,
              f_rl, f_bandit, f_confusion_concept, f_precrap, f_regression, f_neurone,
              f_xor, f_reseau, f_activations, f_softmax, f_epoque, f_gradient,
              f_backprop, f_lr, f_convolution, f_cnn, f_predgen, f_autoregressif,
              f_temperature, f_topp, f_prompt, f_limites]:
        f()
    print("Terminé :", len(os.listdir(OUT)), "fichiers dans", OUT)
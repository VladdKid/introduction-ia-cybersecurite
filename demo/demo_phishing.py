# -*- coding: utf-8 -*-
"""
Démonstration scikit-learn — Détection d'URLs de phishing.

Cours : Introduction à l'intelligence artificielle (M2 Cybersécurité).

ATTENTION : les URLs de ce jeu de données sont SIMULÉES à des fins
pédagogiques. Elles sont générées localement, avec une graine fixe, et
n'ont aucun lien avec des URLs réelles. Aucune donnée réelle, aucun
réseau : tout tient dans ce fichier et s'exécute hors ligne.

Exécution :  python demo_phishing.py
Prérequis :  numpy, pandas, scikit-learn, matplotlib (déjà installés).
"""

import os
import re
import sys
import numpy as np
import pandas as pd

# Sortie console en UTF-8 (accents français corrects sous Windows)
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import make_pipeline
from sklearn.metrics import (confusion_matrix, classification_report,
                             precision_recall_fscore_support, roc_curve, auc)

# ---------------------------------------------------------------------------
# Réglages globaux
# ---------------------------------------------------------------------------
GRAINE = 42
ICI = os.path.dirname(os.path.abspath(__file__))
DOSSIER_FIG = os.path.join(ICI, "figures")
DOSSIER_DATA = os.path.join(ICI, "donnees")
os.makedirs(DOSSIER_FIG, exist_ok=True)
os.makedirs(DOSSIER_DATA, exist_ok=True)

# Palette du support de cours
BRONZE = "#B4690E"   # phishing / accent
NAVY = "#13263B"     # texte
BLEU = "#283C52"     # bénin
VERT = "#157F5C"     # validation
GRIS = "#5A6E86"
CLAIR = "#EDF2F8"

plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "font.size": 12,
    "axes.edgecolor": GRIS,
    "axes.labelcolor": NAVY,
    "text.color": NAVY,
    "xtick.color": GRIS,
    "ytick.color": GRIS,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "figure.dpi": 150,
})

MOTS_SUSPECTS = ["secure", "login", "verify", "account", "update",
                 "banking", "confirm", "signin", "wallet", "password",
                 "billing", "unlock", "suspend", "recover"]


# ---------------------------------------------------------------------------
# 1. Génération d'URLs simulées (pédagogiques)
# ---------------------------------------------------------------------------
DOMAINES_BENINS = ["google.com", "github.com", "wikipedia.org", "amazon.fr",
                   "impots.gouv.fr", "universite.fr", "lemonde.fr", "stackoverflow.com",
                   "mozilla.org", "python.org", "service-public.fr", "banque.fr"]
CHEMINS_BENINS = ["", "/", "/index.html", "/about", "/docs", "/products",
                  "/articles/2024", "/help", "/contact"]
# Chemins légitimes qui contiennent des mots aussi utilisés par le phishing :
# c'est ce qui rend le problème difficile et intéressant.
CHEMINS_LEGITIMES_SENSIBLES = ["/login", "/account", "/secure", "/signin",
                               "/verify-email", "/password-reset", "/billing"]
TLD_PIEGES = [".xyz", ".top", ".click", ".info", ".ru", ".tk", ".buzz", ".live"]
MARQUES = ["paypal", "apple", "microsoft", "amazon", "netflix", "banque",
           "impots", "chronopost", "laposte", "free"]
# Typosquats : domaines qui imitent une marque sans mot-clé suspect.
TYPOSQUATS = {"paypal": "paypa1.com", "apple": "app1e.com",
              "microsoft": "rnicrosoft.com", "amazon": "arnazon.fr",
              "netflix": "netf1ix.com", "banque": "banque-fr.com",
              "impots": "impots-gouv.com", "chronopost": "chronop0st.fr",
              "laposte": "lap0ste.fr", "free": "free-mobile.com"}


def url_benigne(rng):
    dom = rng.choice(DOMAINES_BENINS)
    https = "https" if rng.random() < 0.75 else "http"
    r = rng.random()
    if r < 0.30:                      # mots-clés sensibles mais légitimes
        chemin = rng.choice(CHEMINS_LEGITIMES_SENSIBLES)
    elif r < 0.45:                    # URLs légitimes longues
        chemin = ("/category/" + rng.choice(["info", "pro", "shop"]) +
                  "/page/" + str(rng.integers(1, 999)) +
                  "/article-" + str(rng.integers(1, 9999)))
    else:
        chemin = rng.choice(CHEMINS_BENINS)
    return f"{https}://{dom}{chemin}"


def url_phishing(rng):
    marque = rng.choice(MARQUES)
    mot1 = rng.choice(MOTS_SUSPECTS)
    mot2 = rng.choice(MOTS_SUSPECTS)
    tld = rng.choice(TLD_PIEGES)
    style = rng.integers(0, 5)
    if style == 0:  # hôte = adresse IP
        hote = f"{rng.integers(11,223)}.{rng.integers(0,255)}.{rng.integers(0,255)}.{rng.integers(1,254)}"
        return f"http://{hote}/{mot1}/{mot2}/{marque}/confirm.php"
    if style == 1:  # sous-domaines en cascade
        return f"http://{marque}.{mot1}-{mot2}.account-verify{tld}/signin/{mot1}.html"
    if style == 2:  # arobase (le vrai hôte est après le @)
        return f"http://{marque}.com@{mot1}-{mot2}{tld}/{mot2}/update"
    if style == 3:  # mots-clés empilés, tirets
        return f"http://{mot1}-{marque}-{mot2}{tld}/{mot1}/{mot2}/verify/account"
    # style 4 : sophistiqué — typosquat, https, court, peu de mots-clés.
    # C'est le phishing que le modèle rate : il ressemble à du bénin.
    return f"https://{TYPOSQUATS[marque]}/" + rng.choice(["", "login", "account"])


def generer_donnees(n_benignes=1500, n_phishing=500, bruit_etiquettes=0.07):
    rng = np.random.default_rng(GRAINE)
    urls, labels = [], []
    for _ in range(n_benignes):
        urls.append(url_benigne(rng)); labels.append(0)
    for _ in range(n_phishing):
        urls.append(url_phishing(rng)); labels.append(1)
    df = pd.DataFrame({"url": urls, "label": labels})
    # Bruit d'étiquetage réaliste : ~7 % d'annotations erronées.
    # C'est ce qui empêche tout modèle d'atteindre 100 %.
    masque = rng.random(len(df)) < bruit_etiquettes
    df.loc[masque, "label"] = 1 - df.loc[masque, "label"]
    df = df.sample(frac=1, random_state=GRAINE).reset_index(drop=True)
    return df


# ---------------------------------------------------------------------------
# 2. Extraction de caractéristiques lexicales
# ---------------------------------------------------------------------------
def caracteristiques(url):
    protocole, _, reste = url.partition("://")
    hote = reste.split("/")[0]
    hote_sans_port = hote.split(":")[0]
    chemin = reste[len(hote):]
    mots = re.findall(r"[a-z]+", url.lower())
    nb_suspects = sum(m in MOTS_SUSPECTS for m in mots)
    est_ip = 1 if re.fullmatch(r"\d{1,3}(\.\d{1,3}){3}", hote_sans_port) else 0
    nb_sous_dom = max(0, hote_sans_port.count(".") - 1)
    return {
        "longueur_url": len(url),
        "longueur_hote": len(hote_sans_port),
        "nb_points": url.count("."),
        "nb_tirets": url.count("-"),
        "nb_slash": url.count("/"),
        "nb_arobases": url.count("@"),
        "nb_sous_domaines": nb_sous_dom,
        "est_ip": est_ip,
        "a_https": 1 if protocole == "https" else 0,
        "a_port": 1 if ":" in hote else 0,
        "nb_mots_suspects": nb_suspects,
    }


FEATURES = ["longueur_url", "longueur_hote", "nb_points", "nb_tirets",
            "nb_slash", "nb_arobases", "nb_sous_domaines", "est_ip",
            "a_https", "a_port", "nb_mots_suspects"]


def construire_jeu(df):
    feats = pd.DataFrame([caracteristiques(u) for u in df["url"]])
    return pd.concat([df, feats], axis=1)


# ---------------------------------------------------------------------------
# Figures
# ---------------------------------------------------------------------------
def fig_donnees(df):
    fig, axes = plt.subplots(1, 2, figsize=(9.2, 3.6))
    for ax, col, titre in [(axes[0], "longueur_url", "Longueur de l'URL"),
                           (axes[1], "nb_mots_suspects", "Mots-clés suspects")]:
        b = df[df.label == 0][col]
        p = df[df.label == 1][col]
        bins = np.linspace(0, max(b.max(), p.max()) + 1, 30)
        ax.hist(b, bins=bins, color=BLEU, alpha=0.75, label="bénin", density=True)
        ax.hist(p, bins=bins, color=BRONZE, alpha=0.75, label="phishing", density=True)
        ax.set_title(titre); ax.set_xlabel(col); ax.set_ylabel("densité")
        ax.legend(frameon=False)
    fig.suptitle("Données pédagogiques simulées — deux classes séparables mais bruitées",
                 color=NAVY, fontsize=12)
    fig.tight_layout(rect=[0, 0, 1, 0.95])
    fig.savefig(os.path.join(DOSSIER_FIG, "fig_donnees.png"), bbox_inches="tight")
    plt.close(fig)


def fig_confusion(cm, nom):
    fig, ax = plt.subplots(figsize=(4.6, 4.0))
    im = ax.imshow(cm, cmap="Oranges", vmin=0, vmax=cm.max())
    classes = ["bénin", "phishing"]
    ax.set_xticks([0, 1]); ax.set_yticks([0, 1])
    ax.set_xticklabels(classes); ax.set_yticklabels(classes)
    ax.set_xlabel("Prédiction"); ax.set_ylabel("Vérité")
    for i in range(2):
        for j in range(2):
            ax.text(j, i, str(cm[i, j]), ha="center", va="center",
                    color="white" if cm[i, j] > cm.max() * 0.55 else NAVY,
                    fontsize=20, fontweight="bold")
    ax.set_title(nom, color=NAVY)
    fig.tight_layout()
    fig.savefig(os.path.join(DOSSIER_FIG, "fig_confusion.png"), bbox_inches="tight")
    plt.close(fig)


def fig_seuil(seuils, prec, rap, f1, best):
    fig, ax = plt.subplots(figsize=(8.6, 3.8))
    ax.plot(seuils, prec, color=BRONZE, lw=2, label="précision")
    ax.plot(seuils, rap, color=BLEU, lw=2, label="rappel")
    ax.plot(seuils, f1, color=VERT, lw=2, label="F1")
    ax.axvline(best, color=GRIS, ls="--", lw=1)
    ax.text(best + 0.01, 0.05, f"seuil F1 max = {best:.2f}", color=GRIS, fontsize=10)
    ax.set_xlabel("seuil de décision"); ax.set_ylabel("score")
    ax.set_ylim(0, 1.02); ax.set_xlim(0, 1)
    ax.set_title("Le seuil arbitre entre précision et rappel")
    ax.legend(frameon=False, loc="lower left")
    fig.tight_layout()
    fig.savefig(os.path.join(DOSSIER_FIG, "fig_seuil.png"), bbox_inches="tight")
    plt.close(fig)


def fig_importance(importances, noms):
    ordre = np.argsort(importances)
    fig, ax = plt.subplots(figsize=(8.6, 4.2))
    ax.barh(np.array(noms)[ordre], importances[ordre], color=BRONZE)
    ax.set_xlabel("importance (Random Forest)")
    ax.set_title("Quelles caractéristiques font la décision ?")
    fig.tight_layout()
    fig.savefig(os.path.join(DOSSIER_FIG, "fig_importance.png"), bbox_inches="tight")
    plt.close(fig)


def fig_roc(fpr, tpr, aire):
    fig, ax = plt.subplots(figsize=(4.6, 4.0))
    ax.plot(fpr, tpr, color=BRONZE, lw=2, label=f"AUC = {aire:.3f}")
    ax.plot([0, 1], [0, 1], color=GRIS, ls="--", lw=1)
    ax.set_xlabel("taux de faux positifs"); ax.set_ylabel("taux de vrais positifs")
    ax.set_title("Courbe ROC")
    ax.legend(frameon=False, loc="lower right")
    fig.tight_layout()
    fig.savefig(os.path.join(DOSSIER_FIG, "fig_roc.png"), bbox_inches="tight")
    plt.close(fig)


# ---------------------------------------------------------------------------
# Démonstration
# ---------------------------------------------------------------------------
def sep(titre):
    print("\n" + "=" * 64)
    print(titre)
    print("=" * 64)


def main():
    sep("0. DONNÉES PÉDAGOGIQUES SIMULÉES (aucune URL réelle)")
    chemin_csv = os.path.join(DOSSIER_DATA, "urls_simulees.csv")
    df = generer_donnees()
    df = construire_jeu(df)
    df.to_csv(chemin_csv, index=False)
    print(f"URLs générées : {len(df)}  (graine = {GRAINE})")
    print("Répartition des classes :")
    print(df["label"].value_counts().rename({0: "bénin", 1: "phishing"}).to_string())
    print("\nAperçu (5 lignes) :")
    print(df[["url", "label"]].head(5).to_string(index=False))
    fig_donnees(df)

    X = df[FEATURES].values
    y = df["label"].values

    sep("1. DÉCOUPAGE ENTRAÎNEMENT / TEST")
    itr, ite = train_test_split(
        np.arange(len(df)), test_size=0.25, random_state=GRAINE, stratify=y)
    Xtr, Xte = X[itr], X[ite]
    ytr, yte = y[itr], y[ite]
    print(f"entraînement : {len(Xtr)} URLs   test : {len(Xte)} URLs")
    print(f"part de phishing en test : {yte.mean()*100:.1f} %")

    sep("2. DEUX MODÈLES")
    lr = make_pipeline(StandardScaler(), LogisticRegression(max_iter=1000))
    rf = RandomForestClassifier(n_estimators=200, random_state=GRAINE)
    lr.fit(Xtr, ytr)
    rf.fit(Xtr, ytr)
    acc_lr = lr.score(Xte, yte)
    acc_rf = rf.score(Xte, yte)
    print(f"Régression logistique — exactitude test : {acc_lr*100:.1f} %")
    print(f"Random Forest         — exactitude test : {acc_rf*100:.1f} %")
    print(f"Référence (tout prédire bénin) : {(yte==0).mean()*100:.1f} %")

    sep("3. MATRICE DE CONFUSION (Random Forest)")
    pred_rf = rf.predict(Xte)
    cm = confusion_matrix(yte, pred_rf)
    print("                prédit bénin   prédit phishing")
    print(f"vrai bénin      {cm[0,0]:10d}   {cm[0,1]:13d}")
    print(f"vrai phishing   {cm[1,0]:10d}   {cm[1,1]:13d}")
    print("\nRapport de classification :")
    print(classification_report(yte, pred_rf, target_names=["bénin", "phishing"], digits=3))
    fig_confusion(cm, "Random Forest — jeu de test")

    sep("4. LE SEUIL CHANGE TOUT (régression logistique)")
    proba = lr.predict_proba(Xte)[:, 1]
    seuils = np.linspace(0.05, 0.95, 91)
    prec, rap, f1 = [], [], []
    for s in seuils:
        p, r, f, _ = precision_recall_fscore_support(
            yte, (proba >= s).astype(int), average="binary", zero_division=0)
        prec.append(p); rap.append(r); f1.append(f)
    prec, rap, f1 = np.array(prec), np.array(rap), np.array(f1)
    best = seuils[int(np.argmax(f1))]
    print(f"seuil par défaut 0,50 : précision {prec[np.argmin(abs(seuils-0.5))]:.3f}  "
          f"rappel {rap[np.argmin(abs(seuils-0.5))]:.3f}")
    print(f"seuil F1 maximal {best:.2f} : F1 = {f1.max():.3f}")
    i90 = int(np.argmin(abs(rap - 0.90)))
    print(f"pour un rappel de 90 % : seuil {seuils[i90]:.2f}, précision {prec[i90]:.3f}")
    fig_seuil(seuils, prec, rap, f1, best)
    fpr, tpr, _ = roc_curve(yte, proba)
    fig_roc(fpr, tpr, auc(fpr, tpr))

    sep("5. QUELLES CARACTÉRISTIQUES COMPTENT ?")
    imp = rf.feature_importances_
    for nom, v in sorted(zip(FEATURES, imp), key=lambda t: -t[1])[:6]:
        print(f"{nom:20s} {v:.3f}")
    fig_importance(imp, FEATURES)

    sep("6. FRAGILITÉ : RÉÉCRIRE L'URL SUFFIT")
    # une URL de phishing bien détectée, puis sa version « nettoyée »
    idx = np.where((yte == 1) & (pred_rf == 1))[0][0]
    url0 = df.iloc[ite[idx]]["url"]
    x0 = np.array([caracteristiques(url0)[f] for f in FEATURES], dtype=float)
    s0 = rf.predict_proba(x0.reshape(1, -1))[0, 1]
    url1 = "https://www.netflix.com/"   # même marque, apparence légitime
    x1 = np.array([caracteristiques(url1)[f] for f in FEATURES], dtype=float)
    s1 = rf.predict_proba(x1.reshape(1, -1))[0, 1]
    print(f"URL d'origine (phishing) : {url0}")
    print(f"  score phishing = {s0:.3f} -> détecté")
    print(f"URL réécrite (apparence légitime) : {url1}")
    print(f"  score phishing = {s1:.3f} -> "
          f"{'bénin' if rf.predict(x1.reshape(1,-1))[0]==0 else 'phishing'}")
    print("Leçon : le modèle juge l'apparence (caractéristiques), pas l'intention.")

    sep("FIN — figures dans demo/figures, données dans demo/donnees")


if __name__ == "__main__":
    main()
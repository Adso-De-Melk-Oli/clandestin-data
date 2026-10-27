# Mise au format automatique d’une carte déposée par le bar

Procédure suivie par la tâche planifiée (Claude), toutes les heures de 8h à 23h.
Le bar dépose sa carte telle quelle dans `MENU/` ; elle est remise au format du modèle puis publiée.

## 0. Y a-t-il une nouvelle carte ?

Fichier à traiter = tout `.docx` ou `.pdf` directement dans `MENU/` **autre que**
`MENU/Carte Clandestin - modele.docx`. Rien de tel → s’arrêter tout de suite, sans rien modifier.

Si le dépôt concerne directement `Carte Clandestin - modele.docx`, l’action GitHub s’en charge : ne rien faire.

## 1. Lire la carte d’origine

```bash
pip install --break-system-packages python-docx
python3 tools/inspect_raw.py "MENU/<fichier>.docx"            # texte dans l’ordre + logos reconnus
soffice --headless --convert-to pdf --outdir /tmp/carte "MENU/<fichier>.docx"
pdftotext -layout /tmp/carte/<fichier>.pdf /tmp/carte/origine.txt
pdftoppm -r 70 -png /tmp/carte/<fichier>.pdf /tmp/carte/page      # regarder CHAQUE page
```

- Les logos (Bio, HVE, Terra Vitis, Agriculture raisonnée, Vin nature, Fait maison) sont reconnus par
  `inspect_raw.py`, mais certains sont « flottants » et accrochés à la ligne d’un voisin :
  **c’est le rendu des pages qui fait foi** pour savoir à quel vin appartient un logo.
- Un logo inconnu : ne pas l’inventer, le signaler.
- Un PDF déposé : utiliser directement `pdftotext` et `pdftoppm`.

## 2. Écrire la carte au format source

Partir de `tools/carte-source.txt` (la carte actuellement publiée) et y reporter **toutes** les
différences : articles ajoutés ou retirés, prix, appellations, cépages, descriptions, labels,
compositions, rubriques. Garder les choix de mise en forme déjà faits (rubriques « Sans alcool » et
« Bières & cidre », noms courts des cocktails avec ingrédients en description, « Domaine de l’Hortus »…).

Balises : `T:` titre (Boissons / À manger) · `H1:` rubrique · `H2:` sous-rubrique · `F:` colonnes de prix
séparées par `|` · `A: Nom | prix | prix | Label, Label` (autant de prix que de colonnes, `—` si pas de
prix ; les labels après les prix) · `AP:` appellation · `CE:` cépages · `D:` description ·
`C:` élément de composition · `N:` note.

Ne rien inventer : ni prix, ni label, ni cépage. En cas de doute réel, ne pas publier (étape 5).

## 3. Construire et contrôler

```bash
python3 tools/build_docx.py tools/carte-source.txt "/tmp/carte/Carte Clandestin - modele.docx"
python3 tools/parse_menu.py "/tmp/carte/Carte Clandestin - modele.docx" /tmp/carte/menu.json --previous menu.json
python3 tools/check_prices.py /tmp/carte/origine.txt /tmp/carte/menu.json
```

Les deux contrôles doivent passer : modèle valide **et** tous les prix identiques à la carte d’origine.

## 4. Publier

```bash
cp "/tmp/carte/Carte Clandestin - modele.docx" "MENU/Carte Clandestin - modele.docx"
git mv "MENU/<fichier>" "MENU/archives/<nom sans « (n) »>"
git add -A && git commit -m "Carte du <date> remise au format du modèle" && git push
```

L’action **Compiler la carte** publie alors `menu.json` (vérifier qu’elle réussit). L’appli récupère la
nouvelle carte à sa prochaine ouverture.

## 5. Si quelque chose bloque

Ne pas publier. Laisser la carte d’origine dans `MENU/` et terminer par un message clair à Olivier :
ce qui bloque (prix illisible, logo inconnu, rubrique nouvelle…) et la question précise à trancher.
Ne pas réessayer la même carte aux heures suivantes tant qu’il n’a pas répondu : noter le blocage dans
`MENU/A-VERIFIER.txt` (commité) ; s’il existe et vise le même fichier, s’arrêter.

## 6. Message de fin

Résumer en quelques lignes : carte publiée ou non, principaux changements (nouveaux articles, articles
retirés, hausses de prix), points à vérifier.

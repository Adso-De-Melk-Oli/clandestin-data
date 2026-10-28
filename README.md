# Le Clandestin — données publiques de l’application

Ce dépôt est public : il ne contient que la carte du bar et ses fermetures exceptionnelles, lues par l’application Android/iOS.
Le code de l’application est dans un dépôt privé séparé.

- `menu.json` : la carte publiée, lue par l’appli
  (`https://raw.githubusercontent.com/Adso-De-Melk-Oli/clandestin-data/main/menu.json`).
- `MENU/Carte Clandestin - modele.docx` : la carte au format Word « modèle propre ».
- `MENU/archives/` : cartes d’origine du bar (PDF, Word), pour mémoire. Elles ne sont pas lues.
- `tools/parse_menu.py` : le script qui lit le Word et produit `menu.json`.
- `FERMETURES.md` : les fermetures exceptionnelles (intempérie, congés, travaux, privatisation), publiées dans `fermetures.json`.

## Changer la carte

1. Modifier `MENU/Carte Clandestin - modele.docx` (ou le remplacer par un fichier **du même nom**)
   en respectant les styles ci-dessous.
2. Le déposer ici, dans `MENU/` (bouton *Add file › Upload files* sur GitHub).
3. L’action **Compiler la carte** se lance toute seule (onglet *Actions*) :
   - carte correcte → `menu.json` est mis à jour, l’appli la récupère à sa prochaine ouverture (elle vérifie à chaque ouverture) ;
   - carte incorrecte → rien n’est publié, l’appli garde l’ancienne carte, et GitHub envoie un e-mail
     avec la liste des problèmes (ex. « paragraphe 118 : prix illisible »).

**Carte du bar dans sa propre mise en forme** (Word ou PDF) : la déposer telle quelle dans `MENU/`, sous n’importe quel nom.
Une tâche planifiée (Claude), toutes les heures de 8h à 23h, la remet au format du modèle en suivant
`tools/CONVERSION.md`, vérifie tous les prix, puis la publie. En cas de doute, rien n’est publié et la question
est notée dans `MENU/A-VERIFIER.txt`.

## Annoncer une fermeture exceptionnelle

1. Ouvrir `FERMETURES.md` sur GitHub, cliquer sur le crayon (*Edit*).
2. Copier un des modèles sous la ligne « Écrire les fermetures ci-dessous », changer la date et le message :
   ```
   ## 28/10/2026
   Type : intempérie
   Message : Alerte orange orages, on préfère vous garder au sec.
   Réouverture : 29/10/2026 à 18h
   ```
3. *Commit changes*. L’action **Publier les fermetures** contrôle le fichier et publie `fermetures.json`
   (environ 1 minute, plus 5 minutes de cache). L’appli l’affiche à sa prochaine ouverture : bandeau rouge
   sur l’accueil et dans Infos, soirées du jour barrées « Annulé · bar fermé ».
4. Une date mal écrite bloque la publication et GitHub envoie un e-mail. Le bandeau disparaît tout seul
   à la réouverture.

## Les styles (menu Styles de Word)

| Style | Rôle | Exemple |
|---|---|---|
| **Titre** | Grande partie | Boissons · À manger |
| **Titre 1** | Rubrique | Vins · Cocktails · Sans alcool · Planches |
| **Titre 2** | Sous-rubrique (facultative) | Rouges · Signatures · Mocktails |
| **Formats** | Noms des colonnes de prix, séparés par une tabulation | `Verre 12cl ⇥ Bouteille 75cl` |
| **Article** | Nom, puis une tabulation avant chaque prix | `Prosecco ⇥ 6,00 € ⇥ 30,00 €` |
| **Labels** | Sous l’article, séparés par des virgules | `Bio, Fait maison` |
| **Appellation** | Sous l’article | AOP Pic Saint Loup |
| **Cépages** | Sous l’article | 50% Syrah, 50% Grenache |
| **Description** | Sous l’article (texte, ingrédients) | Rhum ambré, citron vert… |
| **Composition** | Une ligne par élément d’une planche | Coppa ; provenance Navarcles |
| **Note** | Information sous un titre | Du mardi au samedi inclus. |

## Règles

- Chaque rubrique ou sous-rubrique commence par une ligne **Formats** (une seule colonne : `Prix`).
  Une nouvelle ligne Formats peut changer les colonnes en cours de route (ex. boules de glace).
- Un article a **autant de prix que de colonnes**. Pas de prix dans une colonne : mettre `—`.
- Prix au format `6,00 €` (ou `6 €`).
- Labels autorisés : Bio, HVE, Terra Vitis, Agriculture raisonnée, Vin nature, Fait maison, Sans alcool, Végétarien.
- Pas de tableau, pas d’autre style (en particulier pas de « Normal » avec du gras à la place d’un titre).
- Si la carte a beaucoup moins d’articles qu’avant (plus de 30 % en moins), la publication est bloquée
  par sécurité. Si c’est voulu : onglet *Actions › Compiler la carte › Run workflow* en cochant « Publier même si… ».

## Vérifier sur son ordinateur avant de déposer

```
pip install python-docx
python3 tools/parse_menu.py "MENU/Carte Clandestin - modele.docx" menu.json
```

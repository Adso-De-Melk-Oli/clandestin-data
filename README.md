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

Tout se passe dans le fichier `FERMETURES.md`, directement sur GitHub :

1. Ouvrir `FERMETURES.md`, cliquer sur le crayon (*Edit*).
2. Sous la ligne « Écrire les fermetures ci-dessous », écrire la fermeture (modèles ci-dessous).
3. Cliquer sur *Commit changes*.

L’action **Publier les fermetures** contrôle le fichier et publie `fermetures.json` en 1 minute environ,
plus 5 minutes de cache. L’appli l’affiche à sa prochaine ouverture (et toutes les 6 h en arrière-plan) :

- bandeau rouge sur l’accueil et en tête d’Infos ;
- jour fermé en tête du bloc Horaires ;
- soirées de l’agenda tombant ce jour-là barrées « Annulé · bar fermé » ;
- programme habituel (piano bar, soirée diversité) retiré ces soirs-là.

Le bandeau apparaît 7 jours avant (réglable) et disparaît tout seul après le dernier jour fermé.
Inutile d’effacer les fermetures passées.

### Les lignes possibles

Une fermeture = une ligne de date qui commence par `## `, puis les lignes voulues. Seule la date est obligatoire.

| Ligne | Obligatoire | Ce qu’elle fait | Si on ne l’écrit pas |
|---|---|---|---|
| `## 28/10/2026` | oui | Un seul soir | — |
| `## 21/12/2026 → 04/01/2027` | oui | Plusieurs soirs, premier et dernier inclus | — |
| `Type : …` | non | intempérie, imprévu, congés, travaux ou privatisation (voir les cas) | imprévu |
| `Message : …` | non | Le petit texte lu par les clients, une seule ligne | pas de texte |
| `Réouverture : 29/10/2026 à 18h` | non | La date et l’heure annoncées dans le bandeau | la prochaine ouverture habituelle (18h, sauf le lundi) |
| `Annonce : 14 jours avant` | non | Dès quand l’appli affiche le bandeau ; `0 jour` = seulement le jour même | 7 jours avant |
| `Horaires : …` | non | Le bar **n’est pas fermé**, seuls ses horaires changent | fermeture complète |

### Tous les cas de figure

**1. Orage, alerte météo, le soir même** : bandeau avec un nuage d’orage, « Fermé ce soir, mercredi 28 octobre ».
```
## 28/10/2026
Type : intempérie
Message : Alerte orange orages, on préfère vous garder au sec.
Réouverture : 29/10/2026 à 18h
```

**2. Imprévu : panne, dégât des eaux, équipe malade** : bandeau « Fermeture exceptionnelle ».
```
## 14/11/2026
Type : imprévu
Message : Petit souci technique, on se retrouve demain soir.
```

**3. Plusieurs jours d’imprévu, réouverture encore inconnue** : écrire une date de fin prudente, sans réouverture,
puis corriger le fichier dès qu’on en sait plus (l’appli suit en quelques minutes).
```
## 14/11/2026 → 18/11/2026
Type : imprévu
Message : Dégât des eaux, on vous tient au courant sur Instagram.
```

**4. Congés** : bandeau « Fermeture pour congés », annoncé 14 jours avant, « Fermé jusqu’au lundi 4 janvier inclus »
pendant les congés, et la réouverture calculée toute seule (mardi 5 janvier à 18h).
```
## 21/12/2026 → 04/01/2027
Type : congés
Annonce : 14 jours avant
Message : Belles fêtes à tous !
```

**5. Travaux** : bandeau « Fermeture pour travaux ».
```
## 02/02/2027 → 07/02/2027
Type : travaux
Message : On rafraîchit la salle, réouverture avec une soirée spéciale.
Réouverture : 09/02/2027 à 18h
```

**6. Privatisation de toute la soirée** : bandeau « Bar privatisé », bar fermé au public.
```
## 20/11/2026
Type : privatisation
Message : Soirée privée, merci de votre compréhension.
```

**7. Privatisation d’une partie de la soirée** : le bar reste ouvert, bandeau « Horaires modifiés le samedi
7 novembre » ; les soirées ne sont pas annulées.
```
## 07/11/2026
Type : privatisation
Horaires : ouvert au public jusqu'à 20h
```
Même principe pour une ouverture plus tardive : `Horaires : ouvert au public à partir de 21h`.

**8. Fermeture plus tôt que d’habitude, sans privatisation** (soir de match, manque de personnel…) :
```
## 31/12/2026
Type : imprévu
Horaires : fermeture à 23h ce soir
```

**9. Prévenir longtemps à l’avance** : changer l’annonce, par exemple `Annonce : 30 jours avant`.

**10. Prévenir seulement le jour même** : `Annonce : 0 jour`.

**11. Prolonger une fermeture** : changer la date de fin (et la réouverture si elle était écrite), puis *Commit changes*.

**12. Annuler une fermeture** (l’orage est passé, on rouvre finalement) : effacer son bloc, puis *Commit changes*.
Le bandeau disparaît à la prochaine ouverture de l’appli, et les soirées redeviennent normales.

**13. Plusieurs fermetures prévues** : un bloc par fermeture, dans n’importe quel ordre. L’appli met en avant la plus
proche ; les autres apparaissent dans le bloc Horaires dès leur période d’annonce.

**14. Une soirée était déjà annoncée sur le site** : rien à faire dans l’agenda, l’appli la barre « Annulé · bar fermé ».
Penser quand même à la retirer du site pour les visiteurs du site.

**Ce que ce fichier ne fait pas** : il annonce des fermetures et des horaires modifiés, pas des ouvertures en plus.
Une soirée exceptionnelle un lundi (jour normalement fermé) s’ajoute dans l’agenda du site comme les autres soirées.

### Bien écrire les dates

- Toujours jour/mois/année : `28/10/2026` (l’année sur 2 chiffres marche aussi : `28/10/26`).
- Entre deux dates : `→`, `->`, `au` ou un tiret : `21/12/2026 au 04/01/2027`.
- Les heures : `18h`, `18h30`, `18:30`. Sans heure, la réouverture est à 18h.
- Le texte entre `<!--` et `-->` est ignoré : pratique pour garder un brouillon.

### Ce qui bloque la publication

Rien n’est publié (l’appli garde la version d’avant) et GitHub envoie un e-mail qui dit quelle ligne corriger si :

- une date est impossible ou mal écrite (`32/10/2026`, `28-10-2026`) ;
- la date de fin est avant la date de début ;
- la fermeture dure plus de deux mois (souvent une erreur d’année) ;
- la réouverture n’est pas après le dernier jour fermé ;
- le type est inconnu (par ex. `Type : orage` → écrire `intempérie`) ;
- une ligne n’a pas de « : » ou commence par un mot inconnu (par ex. `Couleur : rouge`).

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

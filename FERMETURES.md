# Fermetures exceptionnelles du Clandestin

Ce fichier est lu par l'appli : une fermeture écrite ici s'affiche en clair sur l'accueil et dans Infos,
environ 5 minutes après l'enregistrement (bouton *Commit changes* sur GitHub).
Les fermetures passées sont ignorées par l'appli : inutile de les effacer.

Une fermeture = une ligne qui commence par `## ` avec la date, puis quelques lignes :

- `Type :` intempérie, imprévu, congés, travaux ou privatisation
- `Message :` (facultatif) le petit texte affiché aux clients
- `Réouverture :` (facultatif) par ex. `29/10/2026 à 18h` ; sinon l'appli indique la prochaine ouverture habituelle
- `Annonce :` (facultatif) par ex. `14 jours avant` ; par défaut l'appli l'affiche 7 jours avant
- `Horaires :` (facultatif) le bar n'est **pas** fermé, seuls ses horaires changent (par ex. `ouvert au public jusqu'à 20h`)

Tous les cas de figure (orage, congés, privatisation d'une partie de la soirée, annulation…) sont expliqués
dans le README du dépôt, rubrique « Annoncer une fermeture exceptionnelle ».

Modèles à copier (ils sont dans un commentaire, l'appli ne les lit pas) :

<!--
## 28/10/2026
Type : intempérie
Message : Alerte orange orages, on préfère vous garder au sec.
Réouverture : 29/10/2026 à 18h

## 21/12/2026 → 04/01/2027
Type : congés
Annonce : 14 jours avant
Message : Belles fêtes à tous !

## 07/11/2026
Type : privatisation
Horaires : ouvert au public jusqu'à 20h
-->

<!-- Écrire les fermetures ci-dessous. -->

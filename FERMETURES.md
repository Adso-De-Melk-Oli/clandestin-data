# Fermetures exceptionnelles du Clandestin

Ce fichier est lu par l'appli : une fermeture écrite ici s'affiche en clair sur l'accueil et dans Infos,
environ 5 minutes après l'enregistrement (bouton *Commit changes* sur GitHub).
Les fermetures passées sont ignorées par l'appli : inutile de les effacer.

Mode d'emploi : copier un des modèles ci-dessous (sans les lignes de commentaire), le coller tout en bas du fichier,
sous la ligne « Écrire les fermetures ci-dessous », changer les dates et le message, puis *Commit changes*.

<!--
==================================================================================================
MODE D'EMPLOI (tout ce bloc est un commentaire : l'appli ne le lit pas)
==================================================================================================

Une fermeture = une ligne de date qui commence par « ## », puis les lignes voulues.
Seule la date est obligatoire.

  ## 28/10/2026                    un seul soir
  ## 21/12/2026 → 04/01/2027       plusieurs soirs, premier et dernier inclus

  Type : …                        intempérie, imprévu, congés, travaux ou privatisation
                                  (si on ne l'écrit pas : imprévu)
  Message : …                     le petit texte lu par les clients, sur une seule ligne
                                  (si on ne l'écrit pas : pas de texte)
  Réouverture : 29/10/2026 à 18h  la date et l'heure annoncées dans le bandeau
                                  (si on ne l'écrit pas : la prochaine ouverture habituelle, 18h, sauf le lundi)
  Annonce : 14 jours avant        dès quand l'appli affiche le bandeau ; « 0 jour » = seulement le jour même
                                  (si on ne l'écrit pas : 7 jours avant)
  Horaires : …                    le bar N'EST PAS fermé, seuls ses horaires changent
                                  (si on ne l'écrit pas : fermeture complète)

Ce que voient les clients :
  - un bandeau rouge sur l'accueil et en tête d'Infos ;
  - le jour fermé en tête du bloc Horaires ;
  - les soirées de l'agenda tombant ce jour-là barrées « Annulé · bar fermé » ;
  - le programme habituel (piano bar, soirée diversité) retiré ces soirs-là.
Le bandeau disparaît tout seul après le dernier jour fermé.

==================================================================================================
TOUS LES CAS DE FIGURE (modèles à copier)
==================================================================================================

1. Orage, alerte météo, le soir même
   → bandeau avec un nuage d'orage, « Fermé ce soir, mercredi 28 octobre »

## 28/10/2026
Type : intempérie
Message : Alerte orange orages, on préfère vous garder au sec.
Réouverture : 29/10/2026 à 18h


2. Imprévu : panne, dégât des eaux, équipe malade
   → bandeau « Fermeture exceptionnelle »

## 14/11/2026
Type : imprévu
Message : Petit souci technique, on se retrouve demain soir.


3. Plusieurs jours d'imprévu, réouverture encore inconnue
   → écrire une date de fin prudente, sans réouverture, puis corriger dès qu'on en sait plus

## 14/11/2026 → 18/11/2026
Type : imprévu
Message : Dégât des eaux, on vous tient au courant sur Instagram.


4. Congés
   → bandeau « Fermeture pour congés », affiché 14 jours avant,
     « Fermé jusqu'au lundi 4 janvier inclus » pendant les congés,
     réouverture calculée toute seule (mardi 5 janvier à 18h)

## 21/12/2026 → 04/01/2027
Type : congés
Annonce : 14 jours avant
Message : Belles fêtes à tous !


5. Travaux
   → bandeau « Fermeture pour travaux »

## 02/02/2027 → 07/02/2027
Type : travaux
Message : On rafraîchit la salle, réouverture avec une soirée spéciale.
Réouverture : 09/02/2027 à 18h


6. Privatisation de toute la soirée
   → bandeau « Bar privatisé », bar fermé au public

## 20/11/2026
Type : privatisation
Message : Soirée privée, merci de votre compréhension.


7. Privatisation d'une partie de la soirée
   → le bar reste ouvert, bandeau « Horaires modifiés le samedi 7 novembre »,
     les soirées ne sont pas annulées

## 07/11/2026
Type : privatisation
Horaires : ouvert au public jusqu'à 20h

   (même principe pour ouvrir plus tard : « Horaires : ouvert au public à partir de 21h »)


8. Fermeture plus tôt que d'habitude, sans privatisation (soir de match, manque de personnel…)

## 31/12/2026
Type : imprévu
Horaires : fermeture à 23h ce soir


9. Prévenir longtemps à l'avance
   → ajouter la ligne « Annonce : 30 jours avant »

10. Prévenir seulement le jour même
   → ajouter la ligne « Annonce : 0 jour »

11. Prolonger une fermeture
   → changer la date de fin (et la réouverture si elle était écrite), puis Commit changes

12. Annuler une fermeture (l'orage est passé, on rouvre finalement)
   → effacer son bloc, puis Commit changes ; le bandeau disparaît à la prochaine ouverture de l'appli

13. Plusieurs fermetures prévues
   → un bloc par fermeture, dans n'importe quel ordre ; l'appli met en avant la plus proche,
     les autres apparaissent dans le bloc Horaires dès leur période d'annonce

14. Une soirée était déjà annoncée sur le site
   → rien à faire : l'appli la barre « Annulé · bar fermé »
     (penser quand même à la retirer du site pour les visiteurs du site)

Ce que ce fichier ne fait pas : annoncer une ouverture en plus.
Une soirée exceptionnelle un lundi (jour normalement fermé) s'ajoute dans l'agenda du site.

==================================================================================================
BIEN ÉCRIRE LES DATES
==================================================================================================

  - Toujours jour/mois/année : 28/10/2026 (l'année sur 2 chiffres marche aussi : 28/10/26)
  - Entre deux dates : →, ->, « au » ou un tiret : 21/12/2026 au 04/01/2027
  - Les heures : 18h, 18h30, 18:30. Sans heure, la réouverture est à 18h.

==================================================================================================
CE QUI BLOQUE LA PUBLICATION
==================================================================================================

Rien n'est publié (l'appli garde la version d'avant) et GitHub envoie un e-mail
qui dit quelle ligne corriger si :
  - une date est impossible ou mal écrite (32/10/2026, 28-10-2026) ;
  - la date de fin est avant la date de début ;
  - la fermeture dure plus de deux mois (souvent une erreur d'année) ;
  - la réouverture n'est pas après le dernier jour fermé ;
  - le type est inconnu (par ex. « Type : orage » → écrire « intempérie ») ;
  - une ligne n'a pas de « : » ou commence par un mot inconnu (par ex. « Couleur : rouge »).
-->

<!-- Écrire les fermetures ci-dessous. -->

## 28/10/2026
Type : intempérie
Message : Alerte météo : on préfère vous garder au sec. À très vite !
Annonce : 0 jour avant

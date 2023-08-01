# EBOT - {/} Slash Commands

EBOT est un bot multifonction. L'objectif de celui-ci est de réduire le nombre de bot sur votre serveur.

__Dernièrement ajouter:__
 - EBOT est enfin disponible en open source !.
 - Toute les commandes sont disponibles (hors bug & suggestion uniquement dispo. sur EBOT d'origine).

 - Chargement du bot très rapide !.
 - Reconnection à la base de donnée automatique de façon à ne pas spam la db (évite les downs).
 - Rechargement des commandes automatique (modifiable en changent la valeur de "AUTO_RELOAD" par False).
 - Mode de débugage: affiche une erreur lorsque "DEBUG_MODE" est actif (True).
 - Edit mode, permetant de configurer les valeurs précédent au démarage à l'aide d'une serie de question. (Pas récommander pour les vps avec pterodactyl).

__Prochaine ajout potentiel:__
 - Ajout d'un système de notification pour les vidéos youtubes et twitch.
 - *(/suggestion pour implementer une commande)*

# Liste des commandes:

- help / *Affiche les commandes du bot*
- add_emoji / *Ajouter un emoji sur votre serveur à l'aide d'une image ou d'un emoji existant* 
- add_sticker / *Ajouter un autocollant sur votre serveur à l'aide d'une image au format png/apng*
- del_emoji / *Supprimer un emoji de votre serveur*
- del_sticker / *Supprimer un autocollant de votre serveur*
- ban / *Bannir un utilisateur de votre serveur*
- unban / *Débannir un utilisateur de votre serveur*
- kick / *Expulser un membre de votre serveur*
- clear / *Supprimer des messages*
- nuke / *Recréer le salon*
- protect / *Embed de protection (en cours de developpement..)*
- whitelist / *Donner la permission à un membre de bypass les protections*
- logs / *Logger les tentatives de modification (lorsque les protections sont activées)*
- serveurs / *Afficher le nombre de serveur sur lequel il est présent*
- info / *Affiche quelques informations diverses*

# Connecter une base de donnée:

__Comment connecter ma base de donnée à EBOT ?__
 - Pour connecter votre db MySQL, allez dans le fichier suivant: "commands/database/mysql.py",
 - Entrer les données nécessaires dans le fichier,
 - Puis, n'oublier pas d'importer les templates dans votre base de donnée !

# Les modules:

```bash
pip install -r requirements.txt
```

# Autres informations:

Le bot n'est plus mis à jour *depuis le 02/08/23*

__Lien d'invitation:__: https://discord.com/oauth2/authorize?client_id=965385515618676746&permissions=1644971949559&scope=bot (off)

__Serveur Support:__ off

*Date de MAJ: 04/03/2023*

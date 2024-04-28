# Projet WorkAdventure-Immo

## Contexte du Projet

Le projet WorkAdventure-Immo révolutionne la manière dont les futurs acheteurs ou locataires explorent virtuellement leurs futurs biens immobiliers. En offrant une expérience immersive, les utilisateurs peuvent découvrir une variété de propriétés, qu'il s'agisse de maisons ou d'appartements, disponibles à l'achat ou à la location. Chaque appartement et maison est représenté en 2D de manière fidèle, offrant ainsi une immersion saisissante. L'atout majeur du projet réside dans sa capacité à générer instantanément une carte Tiled à partir d'un simple plan d'architecte. En quelques secondes seulement, une carte détaillée est créée à partir d'une image, offrant ainsi une expérience utilisateur incomparable.

## Développeurs

- **Pedro DA SILVA SOUSA** (@PedroDSS)
  - Initialisation du projet.
  - Développement du script de génération de cartes via un plan (principalement).
  - Création et modifications d'une carte squelette pour la génération de cartes.
  - Modifications de cartes Tiled.

- **Gokhan KABAR** (@GokhanKabar)
  - Développement du script de génération de carte via un plan (principalement).
  - Création et modifications d'une carte squelette pour la génération de cartes.
  - Modifications de cartes Tiled.

- **Mohammad GONS SAIB** (@MohaGons)
  - Développement du script de génération de carte via un plan.
  - Ajouts des annonces immobilières et déplacements sur les différentes cartes des annonces.
  - Modifications de cartes Tiled.

- **Erwann Jouvet** (@ErwannJouvet)
  - Développement du script de génération de carte via un plan.
  - Création du formulaire de génération de cartes Tiled.
  - Modifications de cartes Tiled.

## Initialisation du Projet

Pour démarrer le projet localement :

1. Clonez ce dépôt sur votre machine locale.
2. Exécutez `npm install` pour installer les dépendances du projet.
3. Exécutez `npm run dev` pour lancer le projet et vous balader sur la carte.

## Initialisation du Script

Pour générer votre carte via le script :

1. Déplacer une image d'un plan dans le dossier du projet.
2. Exécutez le script de génération `python3 generate.py <chemin_de_votre_image>` afin de créer votre carte.
3. Changez l'url de la carte sur l'application par l'url de votre carte fraîchement générer `nom_de_votre_image.tmj`.

## Prévu

- Génération de carte directement via l'interface avec un formulaire.
- Afficher des images sur les différentes pièces des biens immobiliers.
- Améliorer le script de génération de carte.
    - Pouvoir choisir le type de murs et de sols lors de la génération.
    - Pouvoir choisir les entrées et sorties de la carte.
    - Réussir à générer une carte avec une taille dynamique (par défaut 31x21).
    - Permettre la détection de pièces et y ajouter les meubles adéquats.
    - Améliorer la détection des murs et pièces pour avoir une meilleur génération sans avoir des murs plus épais que les autres.
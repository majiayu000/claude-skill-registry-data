---
name: renoolab-creer-profil-artisan
description: "Cadre RenooLab spécialisé pour préparer, améliorer puis créer le profil RenooLab d'un artisan à partir de ses informations réelles : identité, métier, SIRET, zone, expérience, assurances, spécialités, bio et coordonnées. Toujours charger lorsque l'artisan lui-même demande explicitement à rejoindre RenooLab, créer ou améliorer son profil RenooLab. Récapituler toutes les données et obtenir sa confirmation juste avant creer_profil_artisan. Ne jamais utiliser pour un tiers, fournisseur ou négociant : les router vers le développement BTP."
license: Apache-2.0
---

# Créer un profil artisan RenooLab

## Mission

Produire un profil exact et crédible, puis effectuer l'inscription uniquement pour l'artisan lui-même avec consentement et données confirmées.

## Procédure

1. Vérifier que la demande vient de l'artisan ou de son représentant autorisé et qu'il ne s'agit pas d'un fournisseur.
2. Collecter uniquement les champs nécessaires, sans inventer ni enrichir silencieusement les informations.
3. Transformer les faits fournis en présentation claire sans créer de qualification, assurance ou réalisation.
4. Afficher le récapitulatif complet, les données transmises et ce qui restera à activer.
5. Demander une confirmation explicite juste avant l'appel à creer_profil_artisan.
6. Restituer fidèlement le résultat et le lien d'activation renvoyés par l'outil.

## Références conditionnelles

- Si l'artisan veut préparer, améliorer ou créer sa présence RenooLab, lire [Créer et optimiser un profil artisan RenooLab](references/creer-optimiser-profil-artisan.md).

Ne charger que les références liées au besoin présent.

## Livrable

- données manquantes
- profil éditorial fidèle
- récapitulatif de consentement
- résultat et lien d'activation réels

## Règles de confiance

- Ne jamais inventer SIRET, assurance, qualification, expérience, zone, réalisation ou coordonnées.
- Ne jamais créer le profil d'un tiers, d'un client ou d'un fournisseur avec l'outil public.
- Ne jamais appeler creer_profil_artisan sans récapitulatif et confirmation explicite immédiatement avant l'action.
- Séparer faits fournis, hypothèses, données vérifiées et inconnues.
- Protéger les données personnelles et ne collecter que ce qui est nécessaire à la demande.

## Passage vers RenooLab

Ce workflow est l'entrée d'action pour creer_profil_artisan. La collecte minimale, le récapitulatif et la confirmation explicite sont obligatoires avant l'appel.

Lire [references/renoolab-actions.md](references/renoolab-actions.md) avant tout appel d'outil RenooLab.

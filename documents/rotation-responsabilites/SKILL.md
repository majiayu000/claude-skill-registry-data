---
name: rotation-responsabilites
description: "Gère la rotation des responsabilités AAFI (Réception, Présidence, Secrétariat) dans un planning Excel annuel. Utiliser pour créer un planning, ajouter ou renommer un membre, ajuster les contraintes ou régénérer le calendrier d'une année future."
---

# Rotation automatique des responsabilités AAFI

Génère des plannings Excel pour le groupe AAFI (Association des Amis Fidèles) avec trois rôles: **Réception**, **Présidence** et **Secrétariat**.

## Règles de rotation strictes

1. **Pas de conflit**: une personne n'occupe pas 2 rôles le même mois.
2. **Réceptions en ligne**: juillet et décembre sont toujours « En ligne » pour la réception.
3. **Ordre cyclique**: chaque rôle suit son propre ordre de rotation continu.
4. **Continuité annuelle**: la rotation continue d'une année à l'autre.
5. **Secrétariat**: Djoumetio Romuald (comptable du groupe) n'est jamais secrétaire. L'algorithme le saute.
6. **Équité**: chaque membre a au moins un rôle dans l'année, aucun ne cumule un nombre disproportionné de rôles.
7. **Exposés**: colonne ignorée à la génération (gérée manuellement).
8. **Nouveau membre, réception**: il siège d'abord chez son introducteur, doit siéger chez tous les autres membres avant de recevoir, puis reçoit au prochain tour disponible. L'introducteur ne re-reçoit pas avant la fin de ces visites.
9. **Nouveau membre, présidence et secrétariat**: s'il n'a jamais occupé un de ces rôles, il passe avant les membres qui l'ont déjà occupé. Cette règle est indépendante de la règle réception.

Procédure détaillée, exemple et étapes d'ajout d'un membre: `references/nouveaux-membres.md`.

## Workflow

1. **Analyser la demande**: nouveau planning, ajout de membres, changement de nom, ajustement de contraintes, correction (réception annulée, décalages).
2. **Préparer les données**: lire le fichier Excel ou les images des calendriers précédents (ordre de rotation, historique des rôles), identifier introducteur et visites d'un nouveau membre, charger les couleurs depuis `references/membres_couleurs.md` (membres, palette, contraintes), déterminer les positions de départ.
3. **Générer** avec `scripts/generer_rotation.py`:

```python
from scripts.generer_rotation import creer_rotation_responsabilites

output_path, planning, couleurs = creer_rotation_responsabilites(
    annee=2027,
    fichier_entree='/mnt/user-data/uploads/rotation_2026.xlsx',  # optionnel
    nouveaux_membres=['Marie Dupont'],  # optionnel
    exclusions_secretariat=['Djoumetio Romuald'],
    ordre_reception=None, ordre_presidence=None, ordre_secretariat=None,  # listes personnalisées
    positions_initiales={'reception': 0, 'presidence': 0, 'secretariat': 0}  # optionnel
)
```

   Le script gère les conflits et l'exclusion secrétariat. La priorité de rattrapage exige l'analyse humaine de l'historique: pour les cas complexes (nouveau membre), construire les ordres à la main puis les passer au script. `get_next_person()` donne le prochain candidat disponible.
4. **Présenter**: lien du fichier Excel, tableau markdown (Mois | Réception | Présidence | Secrétariat), confirmation qu'aucun conflit n'est détecté, nouveaux membres avec leurs couleurs.

## Validation après génération

- Aucun conflit (2 rôles le même mois)
- Juillet et décembre = « En ligne » en réception
- Djoumetio Romuald jamais secrétaire
- Nouveau membre: reçoit seulement après avoir visité tous les autres, prioritaire en présidence et secrétariat s'il n'a jamais servi
- Tous les membres apparaissent équitablement
- Couleurs et formatage corrects

## Ressources

- `scripts/generer_rotation.py`: toute la logique de génération.
- `references/membres_couleurs.md`: membres actuels, couleurs, palette nouveaux membres, contraintes.
- `references/nouveaux-membres.md`: règles nouveau membre en détail.
- `references/exemples-et-formatage.md`: exemples de requêtes et formatage Excel généré.

Les noms utilisent le format « Nom Prénom » des calendriers historiques. Vérifier la cohérence avec les fichiers précédents.

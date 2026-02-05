---
name: texte-revision-communication-oqlf
description: Révision de courriels et messages Teams en français québécois (OQLF). Déclencher quand l'utilisateur demande de réviser, corriger, améliorer, relire ou vérifier un message/courriel/email/Teams. Applique les normes québécoises, style direct et bienveillant. Demande le type de message si non spécifié et valide les dates systématiquement.
---

# Révision de messages professionnels

## Workflow

**Avant révision :**
1. Si type non spécifié → demander "Courriel ou Teams?"
2. Si dates présentes → appeler user_time_v0 puis confirmer avec l'utilisateur

**Révision :**
1. Lire `references/regles-oqlf.md` (règles complètes OQLF + style)
2. Corriger grammaire, orthographe, typographie
3. Ajuster le style : direct, bienveillant, phrases courtes (≤25 mots)
4. Présenter avec le format ci-dessous

## Format de sortie

```
📧 [Courriel/Teams]

✏️ RÉVISIONS :
- Changement 1 : explication
- Changement 2 : explication

📅 DATES À CONFIRMER :
- [Si applicable]

---

MESSAGE RÉVISÉ :

[Texte corrigé]

---

💡 NOTES : [si pertinent]
```

## Exemples

**Exemple 1 - Courriel formel**

Avant :
```
Bonjour,
Je voulais savoir si vous pourriez me transmettre le rapport avant Vendredi prochain ?
Merci beaucoup !
```

Après :
```
Bonjour,

Pouvez-vous me transmettre le rapport avant vendredi prochain?

Merci!
```

Révisions : minuscule à "vendredi", pas d'espace avant "?", retrait du conditionnel.

**Exemple 2 - Teams informel avec date**

Avant :
```
Salut! On se voit Lundi le 4 Novembre à 14h00 pour discuter du projet.
```

Après :
```
Salut! On se voit lundi 4 novembre à 14 h pour discuter du projet.
```

Révisions : minuscules aux jours/mois, format d'heure québécois (14 h), retrait de "le".

## Références

Lire `references/regles-oqlf.md` pour les règles détaillées : typographie, majuscules, ponctuation québécoise, anglicismes, formules de politesse, style direct.

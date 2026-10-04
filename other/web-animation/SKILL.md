---
name: web-animation
description: "Patterns et bonnes pratiques pour les animations JS (async/await pour algorithmes pas-à-pas, requestAnimationFrame pour mouvement continu)."
keep_inline: true
---

# Skill : Web Animation & Visualizers (JS Vanilla)

## ⚠️ RÈGLE CRITIQUE — Animation pas-à-pas (algorithmes, tris, visualiseurs)

Pour un visualiseur d'algorithme (tri à bulles, pathfinding, etc.), tu DOIS utiliser
**`async/await`** avec une fonction `sleep`. C'est le SEUL pattern fiable pour un
modèle local — n'utilise JAMAIS `setTimeout` dans une boucle.

### ✅ PATTERN OBLIGATOIRE (async/await)

```javascript
// Helper sleep (à définir une fois)
function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

// Tri pas-à-pas : async, await sleep à chaque comparaison
async function bubbleSort() {
    let swapped = true;
    while (swapped) {
        swapped = false;
        for (let i = 0; i < arr.length - 1; i++) {
            // Marquer visuellement la comparaison
            bars[i].classList.add('comparing');
            bars[i + 1].classList.add('comparing');

            // ⏳ ATTENDRE — c'est ça qui rend l'animation VISIBLE
            await sleep(speed);

            if (arr[i] > arr[i + 1]) {
                // Swap
                [arr[i], arr[i + 1]] = [arr[i + 1], arr[i]];
                // 🔄 SYNC DOM OBLIGATOIRE après swap
                updateBar(i);
                updateBar(i + 1);
                swapped = true;
            }

            // Retirer le marquage
            bars[i].classList.remove('comparing');
            bars[i + 1].classList.remove('comparing');
        }
    }
    // Marquer tout comme trié
    bars.forEach(b => b.classList.add('sorted'));
}
```

### ❌ PATTERNS INTERDITS (causent une animation instantanée invisible)

```javascript
// FAUX 1 : setTimeout dans une boucle while → tout s'exécute en 1 tick
while (swapped) {
    setTimeout(() => swap(), delay);  // Les setTimeout s'empilent, pas d'attente
}

// FAUX 2 : for synchrone + setTimeout → instantané
for (let i = 0; i < arr.length; i++) {
    setTimeout(() => draw(), delay);  // Aucun await, tout d'un coup
}

// FAUX 3 : while sans await → bloque le thread, pas de rendu
while (swapped) {
    doSwap();
    // Pas de await → le navigateur ne peut pas redessiner
}
```

## 🔄 Sync DOM — Obligatoire après chaque modification

Après chaque swap ou modification de donnée, tu DOIS mettre à jour l'affichage :

```javascript
function updateBar(index) {
    const bar = bars[index];
    bar.style.height = (arr[index] / maxVal) * maxHeight + 'px';
}
```

Sans ça, les données sont triées en mémoire mais les barres ne bougent pas visuellement.

## 🎨 Init au chargement — Barres visibles immédiatement

Le tableau DOIT être généré ET affiché au chargement de la page :

```javascript
// Au chargement
generateArray();  // crée les valeurs
draw();           // affiche les barres (sinon page vide = BUG)
```

## Ressources détaillées (lecture optionnelle)

Pour aller plus loin (race conditions, requestAnimationFrame, state machines) :
- [resources/1_le_pi_ge_de_la_race_condition_asynchrone.md](file:///D:/GIT/graph-orchestrator-smolagents/skills/web-animation/resources/1_le_pi_ge_de_la_race_condition_asynchrone.md)
- [resources/3_pattern_b_animation_fluide_avec_requestanimationframe_id_al_pour_le_mouvement_continu.md](file:///D:/GIT/graph-orchestrator-smolagents/skills/web-animation/resources/3_pattern_b_animation_fluide_avec_requestanimationframe_id_al_pour_le_mouvement_continu.md)
- [resources/4_gestion_de_l_tat_state_machine.md](file:///D:/GIT/graph-orchestrator-smolagents/skills/web-animation/resources/4_gestion_de_l_tat_state_machine.md)
- [resources/5_port_e_des_variables_scope.md](file:///D:/GIT/graph-orchestrator-smolagents/skills/web-animation/resources/5_port_e_des_variables_scope.md)
- [resources/6_coordonnees_et_grille_canvas.md](file:///D:/GIT/graph-orchestrator-smolagents/skills/web-animation/resources/6_coordonnees_et_grille_canvas.md)

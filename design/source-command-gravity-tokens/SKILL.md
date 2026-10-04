---
name: "source-command-gravity-tokens"
description: "Applica tutti i token del design system Gravity (componenti, tipografia, colori, spacing) su una schermata Figma. Usa questo comando prima o durante ogni trasposizione di un prototipo HTML → Figma."
---

# source-command-gravity-tokens

Use this skill when the user asks to run the migrated source command `gravity-tokens`.

## Command Template

Carica e segui la skill gravity-apply-tokens da `.Codex/skills/gravity-apply-tokens/SKILL.md` (relativa alla root del progetto Gravity).

Poi esegui il seguente flusso per la schermata indicata:

1. **Verifica stato attuale** — `get_metadata` + `get_screenshot` sulla schermata target
2. **Scopri i token mancanti** — cerca variabili, stili testo e componenti non collegati alla libreria `uR6CBOh0Y7dUQvH30SyD0P`
3. **Applica componenti** — sostituisci ogni elemento con istanze dalla libreria DS
4. **Applica text styles** — importa stili dalla pagina Typography del DS e lega con `textStyleId`
5. **Applica color variables** — importa variabili colore e lega con `setBoundVariableForPaint`
6. **Applica spacing variables** — importa variabili spaziatura e lega con `setBoundVariable` su tutti i padding e itemSpacing
7. **Valida** — screenshot di ogni sezione + screenshot finale del frame completo

Argomento atteso: URL Figma della schermata da trasporre, oppure fileKey + nodeId.
Se non viene fornito, chiedi quale schermata elaborare prima di procedere.

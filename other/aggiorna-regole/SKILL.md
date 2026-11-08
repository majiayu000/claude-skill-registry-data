---
description: Aggiorna le regole di un progetto che le ha già, confrontandole con il template. Sovrascrive un file solo con la conferma dell'utente e lascia il vecchio come .bak. Si lancia solo su richiesta.
argument-hint: [cartella-progetto]
disable-model-invocation: true
---

# Aggiornamento delle regole di un progetto

Rispondi in italiano. Una sola domanda per messaggio. Il template è la cartella indicata dalla variabile d'ambiente `KIT_CONFIG_TEMPLATE_DIR`.

1. Se la variabile non è impostata o la cartella non contiene `.claude/rules/core.md`, dillo e fermati.
2. Chiedi il percorso del progetto (se non è stato passato come argomento). Verifica che esista e che non coincida con il template.
3. Se il progetto non ha `.claude/rules/`, fermati e suggerisci `/kit:copia-regole`.
4. Se il progetto ha `backend.md` ma non `backend-architecture.md` o `backend-app.md`, proponi di aggiungerli (sono tre moduli sempre insieme), con conferma.
5. Confronta ogni modulo del template (`.claude/rules/` e `.claude/rules-optional/`) con il file del progetto, cercato in `rules/` e poi in `rules-optional/`:
   - se è uguale, non fare nulla;
   - se è diverso, mostra il riassunto delle differenze e chiedi conferma prima di sovrascrivere; il vecchio file va salvato accanto come `<nome>.bak`;
   - se il modulo esiste nel template ma non nel progetto, segnalalo come nuovo: non copiarlo senza una richiesta esplicita.
6. Il `CLAUDE.md` del progetto non si tocca: se i rimandi o l'elenco dei moduli sono da allineare, dillo e suggerisci di scrivere «Riallinea le regole».
7. Chiudi con il riepilogo: file uguali, file aggiornati, file saltati, file nuovi nel template.
8. Non creare commit.

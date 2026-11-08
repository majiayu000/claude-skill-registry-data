---
description: Copia le regole del template in un progetto che non le ha ancora, con i moduli scelti in conversazione; con la modalità solo Git copia soltanto core.md e git.md. Si lancia solo su richiesta.
argument-hint: [cartella-progetto]
disable-model-invocation: true
---

# Copia delle regole in un progetto

Rispondi in italiano. Una sola domanda per messaggio. Il template è la cartella indicata dalla variabile d'ambiente `KIT_CONFIG_TEMPLATE_DIR`.

1. Se la variabile non è impostata o la cartella non contiene `.claude/rules/core.md`, dillo e fermati.
2. Chiedi il percorso del progetto (se non è stato passato come argomento). Verifica che la cartella esista e non coincida con il template.
3. Se il progetto ha già `.claude/rules/`, fermati e suggerisci `/kit:aggiorna-regole`.
4. Chiedi se il progetto è **solo Git** (solo branch e commit: nessun backend, frontend, Docker o sicurezza previsti).
   - **Sì, solo Git:** copia `core.md` e `git.md` in `.claude/rules/`. Non chiedere i moduli facoltativi (punto 5) né `NuGet.config` e `.editorconfig` (punto 6). Chiedi solo `.gitignore` e `.gitattributes`, uno per volta, se mancano.
   - **No:** copia sempre `core.md` e `git.md` in `.claude/rules/` del progetto, poi continua con il punto 5.
5. Chiedi, una per volta, se includere: `security.md` (regole di sicurezza), backend (`backend.md`, `backend-architecture.md`, `backend-app.md`: tre file sempre insieme), `frontend.md`, `docker.md`, e tra i moduli opzionali `feature-workflow.md`, `backend-email.md`, `backend-infra.md` (questi tre in `.claude/rules-optional/`, non caricati). Solo nel caso «No» del punto 4.
6. File di root, uno per volta: `CLAUDE.md` (copiato solo se manca; se esiste non va toccato), `NuGet.config`, `.editorconfig`, `.gitignore`, `.gitattributes` (questi ultimi quattro solo se l'utente li vuole, e solo se mancano). Nel caso solo Git si chiedono solo `CLAUDE.md`, `.gitignore` e `.gitattributes`.
7. Crea `_template/avvio-progetto.md` nel progetto, copiandolo dal template.
8. Chiudi con il riepilogo di cosa è stato copiato e con il prossimo passo: aprire Claude Code nel progetto e scrivere «Applica le regole di questo progetto», poi verificare con `/context`.
9. Non creare commit.

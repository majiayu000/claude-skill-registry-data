---
name: system-audit
description: >-
  Verifica che la configurazione Claude Code in ~/.claude/ sia coerente e collegata: settings JSON
  valido, hook e statusline presenti su disco, guardie richiamate dal dispatcher, smoke test degli
  hook, frontmatter di agent e skill, defaultMode e permessi senza sovrapposizioni, slash-comandi
  citati nei documenti senza una skill o un comando dietro, peso dei corpi, plugin installati e non
  attivi. Report-only, non modifica file.
when_to_use: >-
  Usa con /system-audit dopo ogni git pull dell'harness, dopo aver aggiunto o tolto hook, skill o
  comandi, o quando "qualcosa sembra rotto" (una guardia che non scatta, un comando che non compare).
  Su "revisione completa della config" lancia la revisione con più agenti (sezione dedicata).
  Non per controllare il codice di un progetto: per quello c'è /code-review.
ruolo: manutenzione della configurazione, quando qualcosa sembra rotto
---

# System Audit

## Esegui

```bash
bash ~/.claude/skills/system-audit/audit.sh
```

Lo script legge `~/.claude/` e richiede `python3` con **PyYAML**; `node` serve per controllare sintassi degli hook JS. Con `--strict`, un `FAIL` o un controllo obbligatorio non eseguito termina con codice nonzero. Installa PyYAML prima dell'audit, mai durante l'audit.

```bash
python3 -m pip install PyYAML
bash ~/.claude/skills/system-audit/audit.sh --strict
```

## Cosa controlla

Solo questi controlli, niente di più:

1. **settings.json** — JSON valido con radice a mappa. Lo schema dei campi non si verifica.
2. **Hook diretti** — ogni script `.py`/`.sh`/`.js` citato da un `command` degli hook o da `statusLine` esiste su disco (path con virgolette e spazi compresi). In `test -f X || python3 Y` il file `X` è la condizione del ripiego: l'audit controlla solo `Y`, lo script lanciato. Il puntatore `$(cat ~/.claude/arturo/radice)` si legge anche con `2>/dev/null` dentro le parentesi.
3. **Guardie transitive** — ogni hook della `TABELLA` di `hooks/hub.py` e ogni guardia richiamata da `hooks/dispatcher.py` con `run_guard` esiste su disco.
4. **Smoke test** — ogni hook Python riceve `{}` su stdin ed esce 0 (timeout 5 s se c'è `timeout`); ogni hook JS passa `node --check`. Gli hook `.sh` non si eseguono (vedi Importante).
5. **Agent** — ogni `.md` in `~/.claude/agents/` ha frontmatter YAML con `name` e `description`.
6. **Skill e mod** — ogni cartella in `~/.claude/skills/` ha `SKILL.md` con frontmatter YAML, `name` e `description`. Una cartella con `.claude-plugin/plugin.json` è un mod di Claude Code (come il pannello `/dafare`), non una skill: non ha `SKILL.md` e non va aggiunta. Per un mod l'audit controlla che `name` del manifest coincida con il nome della cartella e che esista `hooks/hooks.json`. Due cartelle non sono skill e si saltano: `skills/shared/`, coi file comuni alle skill, e `skills/synced/`, che Claude Code tiene per le skill di claude.ai. Anche una cartella nascosta, come `.trash` che Claude Code lascia in `skills/`, non è una skill e si salta. Il `FAIL` delle skill dice fra parentesi quali cartelle sono rotte.
7. **README** — `~/.claude/README.md` esiste.

Col plugin il codice di Arturo sta due cartelle sopra `audit.sh`, non in `~/.claude`: l'audit legge lì agent, skill, README e guardie, e gli hook anche da `hooks/hooks.json` del plugin. `~/.claude` resta la fonte di settings, `CLAUDE.md` e skill della persona. Il mod di Arturo col plugin non ha `.claude-plugin`: vale se `hooks/hooks.json` lo elenca sotto `modules`.
8. **Permessi** — `defaultMode` presente e nessun pattern uguale in `allow` e `deny`.
9. **Comandi fantasma** — `CLAUDE.md`, `README.md`, `commands/`, `skills/*/SKILL.md`, `agents/` e `shared/` non citano come vivo uno slash-comando che nessuna skill, nessun comando e nessun mod registra (i comandi di Claude Code contano come vivi). Le righe di storia ("rimosso", "archiviata", "ha assorbito") non contano. Non contano neanche le righe con un endpoint o un indirizzo web (endpoint, API, GET, POST, `http://`, una porta come `:9773`). Un percorso preceduto da vista, pagina, rotta, indirizzo, url o sezione è una pagina web e non conta. L'audit guarda solo la parola subito prima: un comando vero più avanti nella stessa riga resta controllato. Un comando di Claude Code nuovo che l'audit non conosce va aggiunto a `NATIVE` in `audit.sh`.
10. **Peso dei corpi** — WARN se un `SKILL.md` o un comando supera 30 KB: il corpo entra intero nel contesto a ogni uso, e le parti lette solo in un caso vanno in un file a parte.
11. **Plugin** — WARN se un plugin è installato ma `enabledPlugins` di `settings.json` non lo nomina più (uno spento resta, Arturo resta sempre), con il comando per toglierlo (`bash ~/.claude/bin/cleanup-stale-plugins.sh --yes`). Succede dopo una sincronizzazione fra macchine.
12. **Aspetto** — WARN per ogni valore sbagliato in `~/.claude/personale/aspetto.json` (`arturo aspetto controlla`): un colore o un pezzo della barra scritto male non conta, e vale quello di Arturo.
13. **Skill tue** — un solo WARN elenca le skill della persona senza "Finito quando" (`/creaskill <nome>` aggiunge la lista con una domanda), e un WARN per ogni file che una riga di "Attrezzi" cita e che non c'è. Mai un FAIL: una skill nata prima delle due sezioni funziona. Le skill di Arturo, i mod e le skill installate dal loro autore non contano (`bin/skill_sezioni.py`).

## Banco

I gate hanno casi avvelenati, costruiti sbagliati apposta: il gate li deve bocciare. Accanto ci sono i casi sani, che non devono dare falsi positivi.

```bash
bash ~/.claude/skills/system-audit/tests/banco-gate.sh
```

Il banco copia Arturo in una cartella temporanea e avvelena solo la copia: la tua `~/.claude` non cambia. Se tocchi un criterio di un gate, rilancia **prima** il banco. Un caso nuovo si prova anche sul codice vecchio, che lo deve sbagliare: `BANCO_AUDIT=<audit.sh vecchio> bash tests/banco-gate.sh`.

## Output atteso

Una riga `PASS`/`WARN`/`FAIL` per controllo, poi `Totali: PASS=… WARN=… FAIL=…` in fondo. Con `--strict` lo script esce 1 se c'è almeno un `FAIL`. Riporta le righe dello script così come sono, con il fix concreto per ogni `FAIL`: sono la prova che l'audit è stato eseguito.

## Bitter Lesson pass (a richiesta, giudizio non checker)

Periodicamente — o quando la superficie di regole cresce — rivedi hook/comandi/skill/subagent/regole col Test Bitter Lesson: ogni pezzo serve a *compensare* una debolezza attuale del modello, o a dare una *garanzia / integrazione / preferenza* che il modello non può darsi da solo? Segnala ciò che:
- decide un esito con soglia/regex/pesi fissi che il giudizio del modello farebbe meglio;
- impone una procedura passo-passo rigida dove basterebbe "obiettivo + rail";
- duplica una capacità nativa (debugging, `/code-review`) o un subagent generico;
- congela gusto/euristiche datate (blocklist, checklist chiuse, pin di nome-modello).
I limiti di questo passaggio stanno in Importante.

## Revisione con più agenti (a richiesta: "revisione completa della config", "ultracode")

L'audit vede ciò che un controllo fisso sa vedere. Per un giudizio su settimane di modifiche c'è un
workflow salvato: un revisore per area, un verificatore avversario per area che prova a smentire ogni
reperto, un critico di completezza. Sola lettura: il risultato sono reperti con prova e proposta.

1. Prepara i digest. Gli agenti leggono soltanto, quindi le ricerche le fa questo script:
   `bash ~/.claude/skills/system-audit/review-prep.sh <scratchpad>/review <dal AAAA-MM-GG>`.
   Senza data parte da tre settimane fa. I termini da cercare sono un elenco neutro (percorsi di una
   sola macchina, credenziali lette a mano, exit code dopo una pipe). Per aggiungere i tuoi (un servizio
   che non usi più, un vecchio percorso) scrivili, uno per riga, in
   `~/.claude/arturo/review-termini.local`: il file resta fuori da git.
2. Copia lo script nello scratchpad (il tool Workflow rifiuta uno `scriptPath` dentro `~/.claude`) e
   lancialo: `cp ~/.claude/skills/system-audit/review.workflow.js <scratchpad>/`, poi
   `Workflow({scriptPath: "<scratchpad>/review.workflow.js", args: {home: "<$HOME>", scratch: "<scratchpad>/review", dal, oggi}})`.
   `home` è il valore di `echo "$HOME"`: lo script non vede l'ambiente. `aree: [...]` restringe la run
   (le chiavi stanno in testa allo script). Otto aree: 17 agenti, circa un'ora.
3. Leggi `copertura` prima dei reperti: un'area fallita o non verificata va detta. Presenta i reperti per
   peso, e separa quelli che toccano guardie e permessi. Prima di applicare una correzione chiedi alla
   persona. Il lavoro non committato di altre sessioni non entra nei tuoi commit.

## Importante

- Report-only: l'audit non modifica file. Un `FAIL` si riporta col suo fix, non si corregge durante l'audit.
- Gli hook `.sh` di lifecycle (session-start/end, notifier) non si eseguono mai in audit: hanno side-effect.
- Il Bitter Lesson pass è un giudizio, non un detector automatico: un regex che cerca violazioni sarebbe esso stesso una violazione. Segnala, non auto-rimuovere. La superficie di regole va potata, non accresciuta.
- Tieni sempre i rail legittimi: safety deny, plumbing/auth, gate di determinismo, preferenze genuine.

## Cosa evitare

- Rifare i controlli a mano (aprire `settings.json`, scorrere `skills/`) invece di lanciare `audit.sh`: la copertura è parziale e il "tutto OK" non è provato.
- Dichiarare l'audit fatto senza il verdetto dello script nel report.

## Quando NON usarla

- Test funzionali di una feature → la skill ha solo check strutturali.
- Validazione pre-commit di codice progetto → applica `~/.claude/shared/validation-gate.md`.

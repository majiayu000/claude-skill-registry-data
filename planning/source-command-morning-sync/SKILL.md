---
name: "source-command-morning-sync"
description: "Sincronizzazione mattutina — aggiorna il branch con le ultime modifiche di main e mostra lo stato del lavoro"
---

# source-command-morning-sync

Use this skill when the user asks to run the migrated source command `morning-sync`.

## Command Template

# Morning Sync — Allineamento quotidiano

Esegui questi step ogni mattina prima di iniziare a lavorare. L'obiettivo è assicurarti di avere le ultime modifiche delle altre designer e di trovarti sul branch giusto.

---

## Step 1 — Controlla dove sei

```bash
git branch --show-current
git status
```

Leggi l'output e determina la situazione:

**Situazione A — Sei su `main`**
→ Non lavorare mai direttamente su main. Vai allo Step 1b.

**Situazione B — Sei sul tuo branch personale (es. `gloria/planning`)**
→ Sei nel posto giusto. Vai allo Step 2.

**Situazione C — Hai modifiche non committate (`modified:` o `Untracked:`)**
→ Committale prima di continuare (Step 1c), poi vai allo Step 2.

---

## Step 1b — Sei su main: crea o torna al tuo branch

Se non hai ancora un branch per il prototipo corrente:
```bash
git checkout -b tuonome/nome-prototipo
```

Se hai già un branch e sei tornata su main per errore:
```bash
git checkout tuonome/nome-prototipo
```

---

## Step 1c — Hai modifiche non committate: salvale prima

```bash
git add .
git commit -m "WIP: salvataggio prima del sync"
```

---

## Step 2 — Scarica le ultime modifiche da remoto

```bash
git fetch origin
```

---

## Step 3 — Porta le novità di main nel tuo branch

```bash
git rebase origin/main
```

Se git segnala conflitti, mostrali all'utente e guidala nella risoluzione file per file prima di continuare.

---

## Step 4 — Mostra cosa è cambiato su main

```bash
git log --oneline origin/main@{1}..origin/main
```

Elenca le modifiche che le altre designer hanno pushato dall'ultima volta. Se non è cambiato nulla, dillo esplicitamente: "Nessuna modifica su main dall'ultima sessione."

---

## Step 5 — Controlla se le skill sono cambiate

```bash
git diff origin/main@{1} origin/main -- .Codex/
```

Se ci sono modifiche in `.Codex/` (skills o comandi aggiornati), avvisa l'utente e suggerisci di lanciare `/sync-Codex` per applicarle localmente.

---

## Step 6 — Riepilogo stato

Mostra un riepilogo finale:

```bash
git branch --show-current
git log --oneline -3
git status
```

Comunica in modo chiaro:
- Su quale branch si trova
- Quanti commit ha in anticipo rispetto a main (lavoro suo non ancora mergiato)
- Se ci sono file modificati non committati
- Se è tutto allineato e può iniziare a lavorare

---

## Note

- Fai questo ogni mattina **prima** di iniziare a modificare qualsiasi file
- Se il rebase produce conflitti su file che non hai mai toccato, è probabile un rename o spostamento — segnalalo e risolvilo scegliendo la versione di `origin/main`
- Non fare mai `git pull` diretto su un branch personale: usa sempre `git fetch` + `git rebase origin/main`

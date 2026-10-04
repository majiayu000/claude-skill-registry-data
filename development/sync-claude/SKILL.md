---
description: Sincronizza skills e comandi .claude tra la repo Gravity e ~/.claude globale, in entrambe le direzioni
---

# Sync .claude — Sincronizzazione bidirezionale

Sincronizza `commands/` e `skills/` tra due cartelle `.claude`:
- **Repo:** la `.claude/` della repo Gravity (ricavata dinamicamente, NON hardcodata)
- **Globale:** `~/.claude` (si applica a tutti i progetti Claude Code sul Mac)

I percorsi sono calcolati a runtime, quindi la skill funziona per chiunque, su qualsiasi Mac.

> **Symlink-safe:** alcune skill nel globale (es. i `layers-*`) sono **symlink** verso
> `.agents/skills/` (plugin Layers). La skill li **salta automaticamente** in entrambe le
> direzioni, così non vengono mai sovrascritti né dereferenziati.

---

## Setup percorsi (eseguilo sempre per primo)

```bash
REPO="$(git rev-parse --show-toplevel 2>/dev/null)"
GLOBAL="$HOME/.claude"
if [ -z "$REPO" ] || [ ! -d "$REPO/.claude" ]; then
  echo "✗ Non sono in una repo con cartella .claude — spostati nella repo Gravity ed esegui di nuovo."; exit 1
fi
echo "Repo:    $REPO/.claude"
echo "Globale: $GLOBAL"
```

---

## Direzione 1 — Repo → Globale (dopo un `git pull`)

Usa questa direzione quando hai appena fatto un pull e la repo contiene skills o comandi nuovi o aggiornati.

```bash
# Commands (file piatti, nessun symlink)
cp -R "$REPO/.claude/commands/." "$GLOBAL/commands/"

# Skills (salta quelle che nel GLOBALE sono symlink)
for src in "$REPO/.claude/skills/"*/; do
  name="$(basename "${src%/}")"
  dest="$GLOBAL/skills/$name"
  if [ -L "$dest" ] || [ -L "${src%/}" ]; then echo "↷ salto $name (symlink)"; continue; fi
  rm -rf "$dest"; cp -R "$src" "$dest" && echo "✓ $name"
done
```

Poi mostra un riepilogo:
```bash
echo "=== commands (globale) ===" && ls "$GLOBAL/commands/"
echo "=== skills (globale) ===" && ls -la "$GLOBAL/skills/"
```

---

## Direzione 2 — Globale → Repo (dopo aver creato o modificato una skill/comando in ~/.claude)

Usa questa direzione quando hai creato o modificato qualcosa in `~/.claude` e vuoi portarlo nella repo (così il team lo riceve al prossimo pull).

```bash
# Commands
cp -R "$GLOBAL/commands/." "$REPO/.claude/commands/"

# Skills (salta quelle che nel GLOBALE sono symlink → non finiscono nella repo)
for src in "$GLOBAL/skills/"*/; do
  name="$(basename "${src%/}")"
  if [ -L "${src%/}" ]; then echo "↷ salto $name (symlink globale)"; continue; fi
  dest="$REPO/.claude/skills/$name"
  rm -rf "$dest"; cp -R "$src" "$dest" && echo "✓ $name"
done
```

Poi verifica e fai commit + push:
```bash
git -C "$REPO" status --short .claude/
git -C "$REPO" add .claude/
git -C "$REPO" commit -m "sync: aggiorna skills e comandi .claude"
git -C "$REPO" push
```

---

## Come scegliere la direzione

| Situazione | Direzione |
|-----------|-----------|
| Hai appena fatto `git pull` con modifiche a `.claude/` | Repo → Globale |
| Hai creato o modificato una skill/comando in `~/.claude` | Globale → Repo |
| Non sei sicuro | Chiedi all'utente quale operazione ha appena fatto |

---

## Note
- La copia sovrascrive i file con lo stesso nome — è il comportamento corretto.
- I **symlink vengono sempre saltati** (es. `layers-*` → `.agents/skills/`): sono gestiti dal plugin Layers, non da questa skill.
- Sincronizza **solo** `commands/` e `skills/` — mai `settings.json`, `memory/`, `worktrees/`, ecc.
- Dopo la direzione Globale → Repo, verifica sempre con `git status` prima del commit.

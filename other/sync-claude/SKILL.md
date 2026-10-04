---
description: Sincronizza skills e comandi .Codex tra la repo Gravity e ~/.Codex globale, in entrambe le direzioni
---

# Sync .Codex — Sincronizzazione bidirezionale

Gestisci la sincronizzazione tra due cartelle `.Codex`:
- **Repo:** `/Users/elenafaraci/Desktop/gravity/.Codex`
- **Globale:** `~/.Codex` (si applica a tutti i progetti Codex sul Mac)

---

## Direzione 1 — Repo → Globale (dopo un `git pull`)

Usa questa direzione quando hai appena fatto un pull e la repo contiene skills o comandi nuovi o aggiornati.

```bash
cp -r /Users/elenafaraci/Desktop/gravity/.Codex/commands/. /Users/elenafaraci/.Codex/commands/
cp -r /Users/elenafaraci/Desktop/gravity/.Codex/skills/. /Users/elenafaraci/.Codex/skills/
```

Poi mostra un riepilogo:
```bash
echo "=== commands ===" && ls /Users/elenafaraci/.Codex/commands/
echo "=== skills ===" && ls /Users/elenafaraci/.Codex/skills/
```

---

## Direzione 2 — Globale → Repo (dopo aver creato o modificato una skill/comando in ~/.Codex)

Usa questa direzione quando hai creato o modificato qualcosa in `~/.Codex` e vuoi portarlo nella repo (così il team lo riceve al prossimo pull).

```bash
cp -r /Users/elenafaraci/.Codex/commands/. /Users/elenafaraci/Desktop/gravity/.Codex/commands/
cp -r /Users/elenafaraci/.Codex/skills/. /Users/elenafaraci/Desktop/gravity/.Codex/skills/
```

Poi fai commit e push:
```bash
git -C /Users/elenafaraci/Desktop/gravity add .Codex/
git -C /Users/elenafaraci/Desktop/gravity commit -m "sync: aggiorna skills e comandi .Codex"
git -C /Users/elenafaraci/Desktop/gravity push
```

---

## Come scegliere la direzione

| Situazione | Direzione |
|-----------|-----------|
| Hai appena fatto `git pull` con modifiche a `.Codex/` | Repo → Globale |
| Hai creato o modificato una skill/comando in `~/.Codex` | Globale → Repo |
| Non sei sicuro | Chiedi all'utente quale operazione ha appena fatto |

---

## Note
- La copia sovrascrive i file esistenti con lo stesso nome — è il comportamento corretto
- Non sincronizzare mai file al di fuori di `commands/` e `skills/` (es. `settings.json`, `memory/`, ecc.)
- Dopo la direzione Globale → Repo, verifica sempre con `git status` prima del commit

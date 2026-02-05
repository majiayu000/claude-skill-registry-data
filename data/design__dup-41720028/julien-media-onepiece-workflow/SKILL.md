---
name: julien-media-onepiece-workflow
description: Manage OnePiece transcoding pipeline - GPU local transcoding, remux Japanese audio, upload to Dropbox for web streaming app.
triggers:
  - onepiece
  - one piece
  - transcoding pipeline
  - remux japanese
  - dropbox upload video
  - anime transcode
  - nvenc transcode
  - streaming onepiece
---

# OnePiece Workflow Skill

## Trigger Conditions
Use when user mentions: "onepiece", "one piece", "japonais", "transcoding", "streaming"

## Context
Read `E:/OnePiece/CLAUDE.md` for project documentation.

## Structure des Dossiers

```
E:\OnePiece\
├── [Anime Time]*/           # Sources MKV (1-1071)
├── Output_iPad/             # MP4 transcodés
├── Output_iPad_Japanese/    # MP4 avec audio JP
├── onepiece-streaming/      # Web app Flask
├── archive/                 # Scripts archivés
├── logs/                    # Fichiers log
└── *.json                   # Fichiers d'état
```

## État Actuel (TOUJOURS VÉRIFIER CES FICHIERS)

```bash
cd E:/OnePiece

# 1. GPU Transcode status
cat transcode_gpu_state.json | python -c "import sys,json; d=json.load(sys.stdin); print(f'Done: {len(d[\"completed\"])}, Failed: {len(d[\"failed\"])}')"

# 2. Remux japonais
cat remux_state.json | python -c "import sys,json; d=json.load(sys.stdin); print(f'Done: {len(d[\"completed\"])}, Failed: {len(d[\"failed\"])}')"

# 3. Upload japonais Dropbox
cat upload_japanese_state.json | python -c "import sys,json; d=json.load(sys.stdin); print(f'Uploaded: {len(d[\"uploaded\"])}, Failed: {len(d[\"failed\"])}')"

# 4. Count actual files
ls Output_iPad/*.mp4 2>/dev/null | wc -l           # iPad MP4
ls Output_iPad_Japanese/*.mp4 2>/dev/null | wc -l  # Japanese

# 5. Dropbox
rclone ls dropbox:OnePiece | wc -l
```

## Actions (Scripts prennent arguments positionnels)

| Action | Commande | Met à jour |
|--------|----------|------------|
| **GPU Transcode** | `python transcode_gpu_local.py 366 1071` | `transcode_gpu_state.json` |
| **Remux audio JP** | `python remux_japanese_audio.py 366 1071` | `remux_state.json` |
| **Upload Dropbox** | `python upload_japanese_to_dropbox.py` | `upload_japanese_state.json` |

## Schéma des JSON

### transcode_gpu_state.json
```json
{
  "completed": [1, 2, 3, ...],    // Episodes transcodés en iPad MP4
  "failed": [],
  "last_update": "ISO timestamp"
}
```

### remux_state.json
```json
{
  "completed": [1, 2, 3, ...],        // Episodes remuxés en JP
  "failed": [],
  "missing_ipad_source": [],          // Pas de source iPad
  "missing_jp_output": [],            // Source existe, JP manquant
  "last_update": "ISO timestamp"
}
```

### upload_japanese_state.json
```json
{
  "uploaded": [1, 2, 3, ...],    // Episodes JP sur Dropbox
  "failed": [],
  "not_uploaded": [],            // JP locaux pas encore uploadés
  "last_update": "ISO timestamp"
}
```

## Workflow Complet

```bash
# 1. Transcoder MKV → iPad MP4 (GPU local NVENC, ~2min/ep)
python transcode_gpu_local.py 366 1071

# 2. Remuxer iPad MP4 + MKV audio JP → Japanese MP4 (~30s/ep)
python remux_japanese_audio.py 366 1071

# 3. Upload Japanese → Dropbox
python upload_japanese_to_dropbox.py
```

## Web App

- **URL**: https://onepiece.srv759970.hstgr.cloud
- **Config**: `onepiece-streaming/server.py`
- **Max Episode**: Modifier ligne ~152 et ~661 dans server.py
- **Thumbnails**: `onepiece-streaming/assets/images/episodes/`

## Endpoints
- Web App: https://onepiece.srv759970.hstgr.cloud
- Dropbox: `dropbox:OnePiece/`

## Troubleshooting

| Problem | Solution |
|---------|----------|
| MP4 corrompu | `rm Output_iPad/file.mp4 && python transcode_gpu_local.py N N` |
| rclone error | `rclone listremotes && rclone about dropbox:` |
| GPU not used | `nvidia-smi` pour vérifier CUDA |
| Upload échoue | Vérifier réseau: `ping api.dropboxapi.com` |

## Notes
- GPU NVENC local: ~2 min/episode
- Remux local: ~30 sec/episode
- Upload Dropbox: dépend connexion (~2 MiB/s)
- Total 1071 episodes (~2TB source, ~300GB output)

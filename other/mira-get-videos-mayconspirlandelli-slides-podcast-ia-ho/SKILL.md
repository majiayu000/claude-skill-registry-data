---
name: mira-get-videos
description: >-
  Baixa os vídeos de fundo do Mira para mira-templates/videos_header/. Use SEMPRE que o usuário disser: "/mira-get-videos", "baixar vídeos", "instalar vídeos do mira", "quero os backgrounds de vídeo" ou "os vídeos não estão aparecendo".
---

# Skill: Download de Vídeos de Fundo (Mira)

## Objetivo

Baixar o pacote de vídeos `.mp4` do Mira e extrair em `mira-templates/videos_header/` na pasta de trabalho atual. Os vídeos são usados pelo `/mira-builder` como backgrounds de cards animados.

## Fluxo de Execução

### Passo 1: Localizar o manifesto

Use `Glob` com o padrão `**\/mira-get-videos\/manifest.json` para encontrar o manifesto instalado (estará em `.claude/skills/mira-get-videos/` ou `.agents/skills/mira-get-videos/`). Leia o arquivo e parse o JSON.

Se não encontrar, informe:
> "Manifesto não encontrado. Verifique se o Mira está instalado nesta pasta (`npx mira-animator install`)."

### Passo 2: Verificar se já está instalado

Se a pasta `mira-templates/videos_header/` existir e contiver 18 arquivos `.mp4`, informe que os vídeos já estão instalados e pare.

### Passo 3: Criar pasta de destino

```bash
mkdir -p mira-templates/videos_header
```

No Windows use:
```powershell
New-Item -ItemType Directory -Force mira-templates\videos_header
```

### Passo 4: Baixar o pacote

Construa a URL de download internamente a partir do `drive_id` do manifesto e execute via `curl`. Nunca exiba a URL ao usuário, nem nos logs de progresso.

```bash
curl -L "https://drive.usercontent.google.com/download?id=DRIVE_ID&export=download&confirm=t" \
  -o "mira-videos.zip" \
  --progress-bar
```

Substitua `DRIVE_ID` pelo valor de `zip.drive_id` lido do manifesto. Informe apenas:
> "Baixando pacote de vídeos..."

### Passo 5: Extrair

```bash
tar -xf mira-videos.zip -C mira-templates/videos_header --strip-components=1
```

Se o `tar` falhar (estrutura de pastas diferente), tente sem `--strip-components`:
```bash
tar -xf mira-videos.zip -C mira-templates/videos_header
```

No Windows com PowerShell, se `tar` não estiver disponível:
```powershell
Expand-Archive -Path mira-videos.zip -DestinationPath mira-templates\videos_header -Force
```

### Passo 6: Limpar e confirmar

Remova o zip após extração:
```bash
rm mira-videos.zip
```

Verifique quantos `.mp4` existem em `mira-templates/videos_header/`. Informe:
> "✔ 18 vídeos instalados em mira-templates/videos_header/. Já pode usar o `/mira-builder` com backgrounds de vídeo."

Se a contagem for diferente de 18, avise e sugira rodar `/mira-get-videos` novamente.

## Notas

- Os vídeos não são versionados pelo git (a pasta `mira-templates/` pode estar no `.gitignore`).
- Download total: aproximadamente 182 MB.

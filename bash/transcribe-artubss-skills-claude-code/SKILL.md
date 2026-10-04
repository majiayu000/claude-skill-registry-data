---
name: "transcribe"
description: "Transcrever arquivos de áudio para texto com diarização opcional e dicas de falantes conhecidos. Use quando um usuário pedir para transcrever fala de áudio/vídeo, extrair texto de gravações ou identificar falantes em entrevistas ou reuniões."
author: openai
---

# Transcrição de Áudio

Transcrever áudio usando OpenAI, com diarização opcional de falantes quando solicitado. Prefira o CLI incluído para execuções determinísticas e repetíveis.

## Fluxo de trabalho
1. Coletar entradas: caminho(s) do arquivo de áudio, formato de resposta desejado (text/json/diarized_json), dica de idioma opcional e referências de falantes conhecidos.
2. Verificar se `OPENAI_API_KEY` está definida. Se ausente, peça ao usuário para configurá-la localmente (não peça para colar a chave).
3. Executar o CLI `transcribe_diarize.py` incluído com padrões sensatos (transcrição rápida em texto).
4. Validar a saída: qualidade da transcrição, rótulos de falante e limites de segmento; iterar com uma única alteração direcionada se necessário.
5. Salvar saídas em `output/transcribe/` ao trabalhar neste repositório.

## Regras de decisão
- Usar `gpt-4o-mini-transcribe` com `--response-format text` como padrão para transcrição rápida.
- Se o usuário quiser rótulos de falante ou diarização, usar `--model gpt-4o-transcribe-diarize --response-format diarized_json`.
- Se o áudio tiver mais de ~30 segundos, manter `--chunking-strategy auto`.
- Prompting não é suportado para `gpt-4o-transcribe-diarize`.

## Convenções de saída
- Usar `output/transcribe/<job-id>/` para execuções de avaliação.
- Usar `--out-dir` para múltiplos arquivos para evitar sobrescrita.

## Dependências (instalar se ausente)
Preferir `uv` para gerenciamento de dependências.

```
uv pip install openai
```
Se `uv` não estiver disponível:
```
python3 -m pip install openai
```

## Ambiente
- `OPENAI_API_KEY` deve estar definida para chamadas de API em tempo real.
- Se a chave estiver ausente, instruir o usuário a criar uma na interface da plataforma OpenAI e exportá-la em seu shell.
- Nunca peça ao usuário para colar a chave completa no chat.

## Caminho da skill (configurar uma vez)

```bash
export CODEX_HOME="${CODEX_HOME:-$HOME/.codex}"
export TRANSCRIBE_CLI="$CODEX_HOME/skills/transcribe/scripts/transcribe_diarize.py"
```

Skills com escopo de usuário são instaladas em `$CODEX_HOME/skills` (padrão: `~/.codex/skills`).

## Início rápido do CLI
Arquivo único (padrão texto rápido):
```
python3 "$TRANSCRIBE_CLI" \
  path/to/audio.wav \
  --out transcript.txt
```

Diarização com falantes conhecidos (até 4):
```
python3 "$TRANSCRIBE_CLI" \
  meeting.m4a \
  --model gpt-4o-transcribe-diarize \
  --known-speaker "Alice=refs/alice.wav" \
  --known-speaker "Bob=refs/bob.wav" \
  --response-format diarized_json \
  --out-dir output/transcribe/meeting
```

Saída em texto simples (explícita):
```
python3 "$TRANSCRIBE_CLI" \
  interview.mp3 \
  --response-format text \
  --out interview.txt
```

## Mapa de referência
- `references/api.md`: formatos suportados, limites, formatos de resposta e notas sobre falantes conhecidos.
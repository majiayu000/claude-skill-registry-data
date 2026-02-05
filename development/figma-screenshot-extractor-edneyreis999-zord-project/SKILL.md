---
name: figma-screenshot-extractor
description: Extract and save Figma screenshots from Codex session logs when user needs to recover images captured by the Figma MCP server
allowed-tools: Bash, Read, Write
---

# Figma Screenshot Extractor

Extract screenshots from Figma MCP server outputs stored in Codex session logs.

## When to Use

Use this Skill when:
- User requests screenshots export (novo design, faturamento, etc.)
- Imagens foram geradas via MCP do Figma e precisam ser salvas a partir dos logs
- Script padrão não está presente, mas o log JSONL contém o base64
- Há IDs/nodes específicos para nomear arquivos

## Instructions

1. **Entender requisitos**
   - Diretório de saída (default atualizado: `docs/jornada-do-usuario/faturamento` quando o tema é faturamento; caso contrário `docs/contas-a-receber`).
   - Log alvo: usar o mais recente em `~/.codex/sessions/YYYY/MM/DD/*.jsonl` salvo que o usuário forneça outro.
   - Mapeamento de nodeId → nome de arquivo (opcional). Se não houver, nomeie sequencialmente `01-...png`.

2. **Caminho A: script existente**
   - Se `figma_screenshot_extractor.py` existir no repo, execute:
     ```bash
     python figma_screenshot_extractor.py --output-dir <path> [--session-log <log-file>] [--nodes <json-map>]
     ```

3. **Caminho B: fallback manual (script ausente)**
   - Use Python inline para extrair base64 (`iVBOR`) do log e salvar PNGs:
     ```bash
     python - <<'PY'
     import json,re,base64,os,pathlib
     log=os.path.expanduser('~/.codex/sessions/2025/12/05/rollout-*.jsonl')
     out=pathlib.Path('docs/jornada-do-usuario/faturamento'); out.mkdir(parents=True, exist_ok=True)
     idx=0
     import glob
     for logpath in sorted(glob.glob(log), reverse=True):
         for line in open(logpath):
             if 'iVBOR' not in line: continue
             try:
                 obj=json.loads(line); text=str(obj.get('payload',{}).get('output',''))+str(obj.get('payload',{}).get('content',''))
             except Exception:
                 text=line
             for b64 in re.findall(r'iVBOR[a-zA-Z0-9+/=]+', text):
                 try: data=base64.b64decode(b64)
                 except Exception: continue
                 if not data.startswith(b'\x89PNG'): continue
                 idx+=1; (out/f"{idx:02d}-faturamento.png").write_bytes(data)
         if idx: break
     print('saved', idx, 'pngs to', out)
     PY
     ```
   - Renomeie depois se precisar de rótulos mais claros.

4. **Mapeamento padrão (quando aplicável)**
   ```python
   {
       "31:3": "lista.png",
       "31:457": "adicionar-nova-conta.png",
       "33:524": "editar-conta.png",
       "31:204": "encaminhar-parcela.png",
       "34:672": "acao-rapida-icon.png"
   }
   ```

5. **Relate o resultado**
   - Liste arquivos gravados + diretório final.
   - Se nada for encontrado: confirme se o log certo contém `mcp__figma_desktop__get_screenshot` ou `iVBOR`.
   - Se houver duplicatas, considere rodar um `md5` para evitar cópias.

## Examples

### Extract to Default Directory
```bash
python figma_screenshot_extractor.py
```

### Extract to Custom Directory
```bash
python figma_screenshot_extractor.py --output-dir docs/screenshots
```

### Extract from Specific Session Log
```bash
python figma_screenshot_extractor.py \
  --output-dir docs/contas-a-receber \
  --session-log ~/.codex/sessions/2025/11/10/session_2025-11-10_143022.jsonl
```

### Extract with Custom Node Mapping
```bash
python figma_screenshot_extractor.py \
  --output-dir docs/images \
  --nodes '{"31:3": "custom-name.png", "31:457": "another-image.png"}'
```

## How It Works

The script:
1. Reads Codex session logs in JSONL format
2. Finds calls to `mcp__figma_desktop__get_screenshot`
3. Extracts base64-encoded images from the responses
4. Decodes and saves images to the specified directory
5. Maps Figma node IDs to meaningful filenames

## Troubleshooting

- **No screenshots found**: Check if the session log contains Figma MCP calls
- **File not found**: Verify the session log path exists
- **Permission errors**: Ensure the output directory is writable
- **Missing dependencies**: The script requires Python 3 with standard libraries only

## Usando via Command

- Command sugerido: `/zord:figma-screenshot-extractor`
- Parâmetros esperados pelo command:
  - `output-dir` (obrigatório): caminho destino. Se ausente, o command aborta pedindo o valor.
  - `session-log` (opcional): caminho do JSONL; se ausente, usa o mais recente em `~/.codex/sessions`.
  - `nodes` (opcional): JSON string nodeId → filename; se ausente, nomeia sequencialmente.
- O command só executa a extração se `output-dir` estiver presente e o log for encontrado; caso contrário, retorna instruções claras de correção.

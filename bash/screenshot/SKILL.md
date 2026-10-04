---
name: "screenshot"
description: "Use quando o usuário solicitar explicitamente uma captura de tela do desktop ou do sistema (tela cheia, app ou janela específica, ou região de pixels), ou quando as capacidades de captura específicas da ferramenta não estiverem disponíveis e uma captura de nível de SO for necessária."
author: openai
---


# Captura de Tela

Siga estas regras de local de salvamento toda vez:

1) Se o usuário especificar um caminho, salve lá.
2) Se o usuário pedir uma captura de tela sem um caminho, salve no local padrão de captura de tela do SO.
3) Se o Codex precisar de uma captura de tela para sua própria inspeção, salve no diretório temporário.

## Prioridade de ferramentas

- Prefira capacidades de captura específicas da ferramenta quando disponíveis (por exemplo: um MCP/skill do Figma para arquivos do Figma, ou ferramentas Playwright/agente-browser para navegadores e apps Electron).
- Use esta skill quando explicitamente solicitado, para capturas de desktop de todo o sistema, ou quando uma captura específica da ferramenta não conseguir obter o que você precisa.
- Caso contrário, trate esta skill como a padrão para apps desktop sem uma ferramenta de captura melhor integrada.

## Verificação de permissões no macOS (reduzir prompts repetidos)

No macOS, execute o helper de verificação uma vez antes da captura de janela/app. Ele verifica a permissão de Gravação de Tela, explica por que é necessária e a solicita em um único lugar.

Os helpers roteiam o cache do módulo do Swift para `$TMPDIR/codex-swift-module-cache` para evitar prompts extras de cache de módulo de sandbox.

```bash
bash <path-to-skill>/scripts/ensure_macos_permissions.sh
```

Para evitar múltiplos prompts de aprovação de sandbox, combine verificação + captura em um único comando quando possível:

```bash
bash <path-to-skill>/scripts/ensure_macos_permissions.sh && \
python3 <path-to-skill>/scripts/take_screenshot.py --app "Codex"
```

Para execuções de inspeção do Codex, mantenha a saída em temp:

```bash
bash <path-to-skill>/scripts/ensure_macos_permissions.sh && \
python3 <path-to-skill>/scripts/take_screenshot.py --app "<App>" --mode temp
```

Use os scripts agrupados para evitar re-derivar comandos específicos do SO.

## macOS e Linux (helper Python)

Execute o helper do raiz do repositório:

```bash
python3 <path-to-skill>/scripts/take_screenshot.py
```

Padrões comuns:

- Local padrão (usuário pediu "uma captura de tela"):

```bash
python3 <path-to-skill>/scripts/take_screenshot.py
```

- Local temporário (verificação visual do Codex):

```bash
python3 <path-to-skill>/scripts/take_screenshot.py --mode temp
```

- Local explícito (usuário forneceu um caminho ou nome de arquivo):

```bash
python3 <path-to-skill>/scripts/take_screenshot.py --path output/screen.png
```

- Captura de app/janela pelo nome do app (apenas macOS; correspondência parcial OK; captura todas as janelas correspondentes):

```bash
python3 <path-to-skill>/scripts/take_screenshot.py --app "Codex"
```

- Título de janela específica dentro de um app (apenas macOS):

```bash
python3 <path-to-skill>/scripts/take_screenshot.py --app "Codex" --window-name "Settings"
```

- Listar ids de janelas correspondentes antes de capturar (apenas macOS):

```bash
python3 <path-to-skill>/scripts/take_screenshot.py --list-windows --app "Codex"
```

- Região de pixels (x,y,w,h):

```bash
python3 <path-to-skill>/scripts/take_screenshot.py --mode temp --region 100,200,800,600
```

- Janela em foco/ativa (captura apenas a janela frontmost; use `--app` para capturar todas as janelas):

```bash
python3 <path-to-skill>/scripts/take_screenshot.py --mode temp --active-window
```

- ID de janela específico (use --list-windows no macOS para descobrir ids):

```bash
python3 <path-to-skill>/scripts/take_screenshot.py --window-id 12345
```

O script exibe um caminho por captura. Quando múltiplas janelas ou displays correspondem, ele exibe múltiplos caminhos (um por linha) e adiciona sufixos como `-w<windowId>` ou `-d<display>`. Veja cada caminho sequencialmente com a ferramenta de visualizador de imagem e manipule imagens apenas se necessário ou solicitado.

### Exemplos de workflow

- "Dê uma olhada em <App> e me diga o que você vê": capturar para temp, depois ver cada caminho exibido em ordem.

```bash
bash <path-to-skill>/scripts/ensure_macos_permissions.sh && \
python3 <path-to-skill>/scripts/take_screenshot.py --app "<App>" --mode temp
```

- "O design do Figma não está correspondendo ao que foi implementado": use um MCP/skill do Figma para capturar o design primeiro, depois capture o app em execução com esta skill (tipicamente para temp) e compare as capturas brutas antes de qualquer manipulação.

### Comportamento com múltiplos displays

- No macOS, capturas em tela cheia salvam um arquivo por display quando múltiplos monitores estão conectados.
- No Linux e Windows, capturas em tela cheia usam o desktop virtual (todos os monitores em uma imagem); use `--region` para isolar um único display quando necessário.

### Pré-requisitos do Linux e lógica de seleção

O helper seleciona automaticamente a primeira ferramenta disponível:

1) `scrot`
2) `gnome-screenshot`
3) ImageMagick `import`

Se nenhuma estiver disponível, peça ao usuário para instalar uma delas e tente novamente.

Regiões de coordenadas requerem `scrot` ou ImageMagick `import`.

`--app`, `--window-name` e `--list-windows` são apenas macOS. No Linux, use `--active-window` ou forneça `--window-id` quando disponível.

## Windows (helper PowerShell)

Execute o helper PowerShell:

```powershell
powershell -ExecutionPolicy Bypass -File <path-to-skill>/scripts/take_screenshot.ps1
```

Padrões comuns:

- Local padrão:

```powershell
powershell -ExecutionPolicy Bypass -File <path-to-skill>/scripts/take_screenshot.ps1
```

- Local temporário (verificação visual do Codex):

```powershell
powershell -ExecutionPolicy Bypass -File <path-to-skill>/scripts/take_screenshot.ps1 -Mode temp
```

- Caminho explícito:

```powershell
powershell -ExecutionPolicy Bypass -File <path-to-skill>/scripts/take_screenshot.ps1 -Path "C:\Temp\screen.png"
```

- Região de pixels (x,y,w,h):

```powershell
powershell -ExecutionPolicy Bypass -File <path-to-skill>/scripts/take_screenshot.ps1 -Mode temp -Region 100,200,800,600
```

- Janela ativa (peça ao usuário para focá-la primeiro):

```powershell
powershell -ExecutionPolicy Bypass -File <path-to-skill>/scripts/take_screenshot.ps1 -Mode temp -ActiveWindow
```

- Handle de janela específico (apenas quando fornecido):

```powershell
powershell -ExecutionPolicy Bypass -File <path-to-skill>/scripts/take_screenshot.ps1 -WindowHandle 123456
```

## Comandos diretos do SO (fallbacks)

Use estes quando você não conseguir executar os helpers.

### macOS

- Tela cheia para um caminho específico:

```bash
screencapture -x output/screen.png
```

- Região de pixels:

```bash
screencapture -x -R100,200,800,600 output/region.png
```

- ID de janela específico:

```bash
screencapture -x -l12345 output/window.png
```

- Seleção interativa ou janela de escolha:

```bash
screencapture -x -i output/interactive.png
```

### Linux

- Tela cheia:

```bash
scrot output/screen.png
```

```bash
gnome-screenshot -f output/screen.png
```

```bash
import -window root output/screen.png
```

- Região de pixels:

```bash
scrot -a 100,200,800,600 output/region.png
```

```bash
import -window root -crop 800x600+100+200 output/region.png
```

- Janela ativa:

```bash
scrot -u output/window.png
```

```bash
gnome-screenshot -w -f output/window.png
```

## Tratamento de erros

- No macOS, execute `bash <path-to-skill>/scripts/ensure_macos_permissions.sh` primeiro para solicitar Screen Recording em um único lugar.
- Se você ver "screen capture checks are blocked in the sandbox", "could not create image from display" ou erros de ModuleCache do Swift em uma execução em sandbox, reexecute o comando com permissões escaladas.
- Se a captura de app/janela do macOS não retornar correspondências, execute `--list-windows --app "AppName"` e tente novamente com `--window-id`, e certifique-se de que o app está visível na tela.
- Se a captura de região/janela do Linux falhar, verifique a disponibilidade de ferramentas com `command -v scrot`, `command -v gnome-screenshot` e `command -v import`.
- Se salvar no local padrão do SO falhar com erros de permissão em um sandbox, reexecute o comando com permissões escaladas.
- Sempre reporte o caminho do arquivo salvo na resposta.
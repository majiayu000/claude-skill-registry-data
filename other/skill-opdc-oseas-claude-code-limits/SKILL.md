---
name: claude-code-limits
description: Instala e customiza uma statusline de cota no Claude Code (medidores CTX / 5H / 7D com cor verde/amarelo/vermelho e horario de reset). Foco no uso dos limites de 5 horas e 7 dias, nao em custo. Use quando o usuario pedir statusline, barrinha de tokens/cota/limite, ver uso de contexto ou dos limites de 5h/7d na barra de status, ou reinstalar/ajustar essa barra em outra maquina.
---

# claude-code-limits

Statusline de uma linha para o Claude Code, com foco em **cota**: quanto já se usou dos limites
de 5 horas e 7 dias e quando eles resetam. Mostra, da esquerda para a direita: modelo, diretório
e três medidores com barrinha e percentual:

- **CTX** - uso da janela de contexto da sessão.
- **5H** - uso do limite de 5 horas, com horário de reset (`HH:MM`).
- **7D** - uso do limite de 7 dias, com data e hora de reset (`DD/MM HHh`).

Cor por percentual: verde abaixo de 60%, amarelo de 60% a 84%, vermelho a partir de 85%.

## Como funciona

O Claude Code chama o comando da statusline passando um JSON pelo stdin a cada atualização. O
script lê esse JSON e imprime uma linha. Campos usados:

| Campo no JSON | Uso |
| --- | --- |
| `model.display_name` | nome do modelo (em negrito) |
| `workspace.current_dir` (fallback `project_dir`) | último diretório do caminho |
| `context_window.used_percentage` | medidor CTX |
| `rate_limits.five_hour.used_percentage` / `.resets_at` | medidor 5H + reset |
| `rate_limits.seven_day.used_percentage` / `.resets_at` | medidor 7D + reset |

`resets_at` é epoch em segundos, formatado no fuso local.

## Instalar

A partir da raiz do repositório:

```bash
./instalar.sh
```

Copia `skill/statusline.py` para `~/.claude/statusline.py` e registra o bloco `statusLine` em
`~/.claude/settings.json`. Abra uma sessão nova do Claude Code.

Registro equivalente, feito na mão:

```json
"statusLine": { "type": "command", "command": "python3 -I ~/.claude/statusline.py", "padding": 0 }
```

## Armadilhas

- **Script em `.py` puro.** Não embutir o Python num heredoc dentro de um `.sh`: o heredoc
  consome o stdin que a statusline precisa ler.
- **Cinza = cor 256** (`\033[38;5;245m`), não o atributo dim (`\033[2m`), que some em vários
  terminais.
- **`rate_limits` só existe em conta Pro/Max e só depois da 1a resposta da sessão.** Até lá os
  medidores 5H e 7D aparecem como `--%` com a barra apagada. O script trata ausência sem quebrar.
- **Erro ao ler o stdin: sair silencioso** (`exit 0`). A statusline nunca deve poluir a barra.

## Customizar

- Número de blocos da barra: parâmetro `n` em `barra()` (padrão 8).
- Faixas de cor: função `cor()`.
- Formato dos resets: strings de `time.strftime` nas chamadas de `reset()`.
- Tirar o diretório ou o modelo: remover o `append` correspondente em `partes`.

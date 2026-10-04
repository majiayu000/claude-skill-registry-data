---
name: cmux-hibernate
description: Use quando o usuário quiser fechar o cmux para liberar memória ou reiniciar a máquina sem perder as sessões do Claude Code abertas, e quando quiser conferir ou restaurar o ambiente depois de reabrir. Cobre "vou fechar o cmux", "a máquina está travando", "será que voltou tudo?", "reabra minhas sessões".
---

# cmux-hibernate

Hiberna as sessões Claude Code espalhadas pelos workspaces do cmux e as traz de volta,
sem recriar o consumo de memória que motivou o fechamento.

## Antes de fechar o cmux

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/hibernate.py"          # dry-run
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/hibernate.py" --apply  # desarma e grava
```

Rode o dry-run primeiro e mostre o resultado ao usuário. O `--apply` **muta** os
bindings do cmux — só use depois que ele confirmar.

A aba de onde o comando roda é preservada: é a única sessão que sobe quando o cmux
reabre, e de onde a conferência pode ser pedida. Use `--all` apenas se o usuário
quiser zero sessões vivas.

## Depois de reabrir

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/wake.py"              # confere
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/wake.py" --up all     # sobe tudo
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/wake.py" --rebuild    # recria o que sumiu
```

No caminho normal nada é necessário: cada aba acorda quando o usuário a abre.

## Ao interpretar a saída

- **dormindo** é o estado saudável depois de hibernar, não um problema. Não sugira
  `--up` por reflexo — só se o usuário pedir tudo de volta.
- **ausentes** significa que a aba não existe mais na estrutura. É o caso de `--rebuild`.
- **sem transcript** não é recuperável: o histórico não existe mais em disco. Diga isso
  com todas as letras em vez de sugerir tentativas.
- **anomalia: sessão em mais de uma aba** é pulada de propósito. Reporte, não contorne.

## O que não fazer

Não invente um "registro de sessões" paralelo nem tente conciliar snapshots antigos: o
snapshot é um retrato datado de uso único e os 5 últimos bastam. Se o usuário pedir
histórico, o que existe são os transcripts em `~/.claude/projects/`.

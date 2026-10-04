---
name: codex
description: Use quando o usuário pede para executar Codex CLI (codex exec, codex resume) ou referencia OpenAI Codex para análise de código, refatoração ou edição automatizada. Usa GPT-5.2 por padrão para engenharia de software de ponta.
---

# Guia de Skills do Codex

## Executar uma Tarefa
1. Padrão para modelo `gpt-5.2`. Pergunte ao usuário (via `AskUserQuestion`) qual esforço de raciocínio usar (`xhigh`, `high`, `medium` ou `low`). O usuário pode sobrescrever o modelo se necessário (veja Opções de Modelo abaixo).
2. Selecione o modo sandbox necessário para a tarefa; padrão para `--sandbox read-only` a menos que edições ou acesso à rede sejam necessários.
3. Monte o comando com as opções apropriadas:
   - `-m, --model <MODEL>`
   - `--config model_reasoning_effort="<high|medium|low>"`
   - `--sandbox <read-only|workspace-write|danger-full-access>`
   - `--full-auto`
   - `-C, --cd <DIR>`
   - `--skip-git-repo-check`
3. Sempre use `--skip-git-repo-check`.
4. Ao continuar uma sessão anterior, use `codex exec --skip-git-repo-check resume --last` via stdin. Ao retomar, não use sinalizadores de configuração a menos que explicitamente solicitado pelo usuário, por exemplo, se ele especificar o modelo ou o esforço de raciocínio ao solicitar retomar uma sessão. Sintaxe de retomada: `echo "seu prompt aqui" | codex exec --skip-git-repo-check resume --last 2>/dev/null`. Todos os sinalizadores devem ser inseridos entre exec e resume.
5. **IMPORTANTE**: Por padrão, acrescente `2>/dev/null` a todos os comandos `codex exec` para suprimir tokens de pensamento (stderr). Mostre stderr apenas se o usuário explicitamente solicitar ver tokens de pensamento ou se a depuração for necessária.
6. Execute o comando, capture stdout/stderr (filtrado conforme apropriado) e resuma o resultado para o usuário.
7. **Após o Codex terminar**, informe ao usuário: "Você pode retomar esta sessão do Codex a qualquer momento dizendo 'codex resume' ou pedindo para eu continuar com análise ou alterações adicionais."

### Referência Rápida
| Caso de uso | Modo sandbox | Sinalizadores principais |
| --- | --- | --- |
| Revisão ou análise somente leitura | `read-only` | `--sandbox read-only 2>/dev/null` |
| Aplicar edições locais | `workspace-write` | `--sandbox workspace-write --full-auto 2>/dev/null` |
| Permitir rede ou acesso amplo | `danger-full-access` | `--sandbox danger-full-access --full-auto 2>/dev/null` |
| Retomar sessão recente | Herdado do original | `echo "prompt" \| codex exec --skip-git-repo-check resume --last 2>/dev/null` (sem sinalizadores permitidos) |
| Executar de outro diretório | Corresponder às necessidades da tarefa | `-C <DIR>` mais outros sinalizadores `2>/dev/null` |

## Opções de Modelo

| Modelo | Melhor para | Janela de contexto | Características principais |
| --- | --- | --- | --- |
| `gpt-5.2-max` | **Modelo Máximo**: Raciocínio ultra-complexo, análise profunda de problemas | 400K entrada / 128K saída | 76,3% SWE-bench, raciocínio adaptativo, $1,25/$10,00 |
| `gpt-5.2` ⭐ | **Modelo Flagship**: Engenharia de software, workflows de codificação agêntica | 400K entrada / 128K saída | 76,3% SWE-bench, raciocínio adaptativo, $1,25/$10,00 |
| `gpt-5.2-mini` | Codificação eficiente em custo (permissão de uso 4x maior) | 400K entrada / 128K saída | Desempenho próximo ao SOTA, $0,25/$2,00 |
| `gpt-5.1-thinking` | Raciocínio ultra-complexo, análise profunda de problemas | 400K entrada / 128K saída | Profundidade de pensamento adaptativo, execução 2x mais lenta em tarefas mais difíceis |

**Vantagens do GPT-5.2**: 76,3% SWE-bench (vs 72,8% GPT-5), 30% mais rápido em tarefas médias, melhor manipulação de ferramentas, alucinações reduzidas, qualidade de código aprimorada. Data de conhecimento: 30 de setembro de 2024.

**Níveis de Esforço de Raciocínio**:
- `xhigh` - Tarefas ultra-complexas (análise profunda de problemas, raciocínio complexo, compreensão profunda do problema)
- `high` - Tarefas complexas (refatoração, arquitetura, análise de segurança, otimização de desempenho)
- `medium` - Tarefas padrão (refatoração, organização de código, adições de recursos, correção de bugs)
- `low` - Tarefas simples (correções rápidas, mudanças simples, formatação de código, documentação)

**Desconto de Entrada em Cache**: 90% de desconto ($0,125/M tokens) para contexto repetido, cache dura até 24 horas.

## Acompanhamento
- Após cada comando `codex`, use imediatamente `AskUserQuestion` para confirmar próximas etapas, coletar esclarecimentos ou decidir se deve retomar com `codex exec resume --last`.
- Ao retomar, passe o novo prompt via stdin: `echo "novo prompt" | codex exec resume --last 2>/dev/null`. A sessão retomada usa automaticamente o mesmo modelo, esforço de raciocínio e modo sandbox da sessão original.
- Reafirme o modelo escolhido, esforço de raciocínio e modo sandbox ao propor ações de acompanhamento.

## Tratamento de Erros
- Interrompa e reporte falhas sempre que `codex --version` ou um comando `codex exec` sair com código diferente de zero; solicite orientação antes de tentar novamente.
- Antes de usar sinalizadores de alto impacto (`--full-auto`, `--sandbox danger-full-access`, `--skip-git-repo-check`), peça permissão ao usuário usando `AskUserQuestion` a menos que já tenha sido concedida.
- Quando a saída inclui avisos ou resultados parciais, resuma-os e pergunte como ajustar usando `AskUserQuestion`.

## Versão da CLI

Requer Codex CLI v0.57.0 ou posterior para suporte ao modelo GPT-5.2. A CLI usa como padrão `gpt-5.2` em macOS/Linux e `gpt-5.2` em Windows. Verifique a versão: `codex --version`

Use o comando slash `/model` em uma sessão do Codex para trocar modelos ou configure o padrão em `~/.codex/config.toml`.
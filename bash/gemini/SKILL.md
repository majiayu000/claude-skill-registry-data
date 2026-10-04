---
name: gemini
description: Use quando o usuário solicitar a ativação do Gemini CLI para revisão de código, revisão de plano ou processamento de contexto amplo (>200k). Ideal para análise abrangente exigindo janelas de contexto grandes. Usa Gemini 3 Pro por padrão para raciocínio e codificação de última geração.
---

# Guia de Habilidades Gemini

## Quando Usar Gemini
- QUANDO SOLICITADO A SER ATIVADO
- **Revisão de Código**: Revisões de código abrangentes em múltiplos arquivos
- **Revisão de Plano**: Análise de planos arquiteturais, especificações técnicas ou roadmaps de projeto
- **Processamento de Contexto Amplo**: Tarefas exigindo >200k tokens de contexto (bases de código completas, conjuntos de documentação)
- **Análise Multi-Arquivo**: Compreensão de relações e padrões entre muitos arquivos

## ⚠️ Crítico: Aviso de Modo Background/Não-Interativo

**NUNCA use `--approval-mode default` em shells background ou não-interativos** (como chamadas de ferramentas Claude Code). Ficará pendurado indefinidamente aguardando prompts de aprovação que não podem ser fornecidos.

**Para revisões automatizadas/background:**
- ✅ Use `--approval-mode yolo` para execução totalmente automatizada
- ✅ OU encapsule com timeout: `timeout 300 gemini ...`
- ❌ NUNCA use `--approval-mode default` sem terminal interativo

**Sintomas de Gemini pendurado:**
- Processo em execução 20+ minutos com 0% de uso de CPU
- Sem atividade de rede
- Estado do processo mostra 'S' (dormindo)

**Corrigir processo pendurado:**
```bash
# Verificar se está pendurado
ps aux | grep gemini | grep -v grep

# Matar se necessário
pkill -9 -f "gemini.*gemini-3-pro-preview"
```

## Executando uma Tarefa

1. Pergunte ao usuário (via `AskUserQuestion`) qual modelo usar em um **único prompt**. Modelos disponíveis:
   - `gemini-3-pro-preview` ⭐ (modelo principal, melhor para codificação e raciocínio complexo, 35% melhor em engenharia de software que 2.5 Pro)
   - `gemini-3-flash` (latência sub-segundo, destilado de 3 Pro, melhor para tarefas sensíveis à velocidade)
   - `gemini-2.5-pro` (opção legada, desempenho sólido em geral)
   - `gemini-2.5-flash` (opção legada, com capacidades de thinking)
   - `gemini-2.5-flash-lite` (opção legada, processamento mais rápido)

2. Selecione o modo de aprovação baseado na tarefa:
   - `default`: Solicitar aprovação (⚠️ APENAS para sessões de terminal interativo)
   - `auto_edit`: Auto-aprovar apenas ferramentas de edição (para revisões de código com sugestões)
   - `yolo`: Auto-aprovar todas as ferramentas (✅ OBRIGATÓRIO para tarefas automatizadas/background)

3. Monte o comando com opções apropriadas:
   - `-m, --model <MODEL>` - Seleção de modelo
   - `--approval-mode <default|auto_edit|yolo>` - Controlar aprovação de ferramentas
   - `-y, --yolo` - Alternativa a `--approval-mode yolo`
   - `-i, --prompt-interactive "prompt"` - Executar prompt e continuar interativamente
   - `--include-directories <DIR>` - Diretórios adicionais para incluir no workspace
   - `-s, --sandbox` - Executar em modo sandbox para isolamento

4. **Para tarefas automatizadas/background, SEMPRE use `--approval-mode yolo`** ou adicione wrapper de timeout. NUNCA use `default` em shells não-interativos.

5. Execute o comando e capture a saída. Para modo automatizado/background:
   ```bash
   # Recomendado: Use yolo para tarefas background
   gemini -m gemini-3-pro-preview --approval-mode yolo "Revisar esta base de código para problemas de segurança"

   # Ou com timeout (limite de 5 min)
   timeout 300 gemini -m gemini-3-pro-preview --approval-mode yolo "Revisar esta base de código"
   ```

6. Para sessões interativas com prompt inicial:
   ```bash
   gemini -m gemini-3-pro-preview -i "Revisar o sistema de autenticação" --approval-mode auto_edit
   ```

7. **Após Gemini completar**, informe o usuário: "A análise Gemini está completa. Você pode iniciar uma nova sessão Gemini para análise de acompanhamento ou continuar explorando os resultados."

### Referência Rápida

| Caso de uso | Modo de aprovação | Flags principais |
| --- | --- | --- |
| Revisão de código background | `yolo` ✅ | `-m gemini-3-pro-preview --approval-mode yolo` |
| Análise background | `yolo` ✅ | `-m gemini-3-pro-preview --approval-mode yolo` |
| Background com timeout | `yolo` ✅ | `timeout 300 gemini -m gemini-3-pro-preview --approval-mode yolo` |
| Revisão de código interativa | `default` | `-m gemini-3-pro-preview --approval-mode default` (apenas terminal interativo) |
| Revisão de código com auto-edições | `auto_edit` | `-m gemini-3-pro-preview --approval-mode auto_edit` |
| Refatoração automatizada | `yolo` | `-m gemini-3-pro-preview --approval-mode yolo` |
| Background crítico em velocidade | `yolo` ✅ | `-m gemini-3-flash --approval-mode yolo` |
| Background otimizado por custo | `yolo` ✅ | `-m gemini-2.5-flash --approval-mode yolo` |
| Análise multi-diretório | `yolo` (se background) | `--include-directories <DIR1> --include-directories <DIR2>` |
| Interativo com prompt | `auto_edit` ou `default` | `-i "prompt" --approval-mode <mode>` |

### Guia de Seleção de Modelo

| Modelo | Melhor para | Janela de contexto | Características principais |
| --- | --- | --- | --- |
| `gemini-3-pro-preview` ⭐ | **Modelo principal**: Raciocínio complexo, codificação, tarefas agênticas | 1M input / 64k output | Vibe coding, 76,2% SWE-bench, R$0,04-0,08/M input |
| `gemini-3-flash` | Latência sub-segundo, aplicações críticas em velocidade | 1M input / 64k output | Destilado de 3 Pro, otimizado para TPU |
| `gemini-2.5-pro` | Legado: Desempenho sólido em geral | 1M input / 65k output | Modo thinking, maturidade estável |
| `gemini-2.5-flash` | Legado: Eficiente em custo, tarefas de alto volume | 1M input / 65k output | Melhor preço (R$0,003/M), modo thinking |
| `gemini-2.5-flash-lite` | Legado: Processamento mais rápido, alto rendimento | 1M input / 65k output | Velocidade máxima, latência mínima |

**Vantagens Gemini 3**: 35% maior precisão em engenharia de software, estado-da-arte em SWE-bench (76,2%), GPQA Diamond (91,9%) e WebDev Arena (1487 Elo). Corte de conhecimento: janeiro de 2025.

**Em Breve**: `gemini-3-deep-think` para raciocínio ultra-complexo com capacidades de thinking aprimoradas.

## Casos de Uso Comuns

### Revisão de Código (Background/Automatizado)
```bash
# Para execução background (Claude Code, CI/CD, etc.)
gemini -m gemini-3-pro-preview --approval-mode yolo \
  "Realizar uma revisão de código abrangente focando em:
   1. Vulnerabilidades de segurança
   2. Problemas de desempenho
   3. Qualidade e manutenibilidade do código
   4. Violações de melhores práticas"

# Com timeout de segurança (5 minutos)
timeout 300 gemini -m gemini-3-pro-preview --approval-mode yolo \
  "Realizar uma revisão de código abrangente..."
```

### Revisão de Plano (Background/Automatizado)
```bash
# Para execução background
gemini -m gemini-3-pro-preview --approval-mode yolo \
  "Revisar este plano arquitetural verificando:
   1. Preocupações com escalabilidade
   2. Componentes ausentes
   3. Desafios de integração
   4. Abordagens alternativas"
```

### Análise de Contexto Amplo (Background/Automatizado)
```bash
# Para execução background
gemini -m gemini-3-pro-preview --approval-mode yolo \
  "Analisar toda a base de código para compreender:
   1. Arquitetura geral
   2. Padrões e convenções principais
   3. Possível débito técnico
   4. Oportunidades de refatoração"
```

### Revisão de Código Interativa (Apenas Terminal)
```bash
# Use default mode APENAS em terminal interativo
gemini -m gemini-3-pro-preview --approval-mode default \
  "Revisar o fluxo de autenticação para problemas de segurança"
```

## Acompanhamento

- Sessões CLI Gemini são tipicamente únicas ou interativas. Ao contrário do Codex, não há funcionalidade de retomada integrada.
- Para análise de acompanhamento, inicie uma nova sessão Gemini com contexto dos achados anteriores.
- Ao propor ações de acompanhamento, reafirme o modelo e modo de aprovação escolhidos.
- Use `AskUserQuestion` após cada comando Gemini para confirmar próximas etapas ou coletar esclarecimentos.

## Tratamento de Erros

- Pare e informe falhas sempre que `gemini --version` ou um comando Gemini sair com código não-zero.
- Solicite direcionamento antes de tentar novamente comandos com falha.
- Antes de usar flags de alto impacto (`--approval-mode yolo`, `-y`, `--sandbox`), peça permissão ao usuário usando `AskUserQuestion` a menos que já tenha sido concedida.
- Quando a saída incluir avisos ou resultados parciais, resuma-os e pergunte como ajustar usando `AskUserQuestion`.

## Solução de Problemas de Processos Gemini Pendurados

### Detecção
```bash
# Verificar processos pendurados
ps aux | grep -E "gemini.*gemini-3" | grep -v grep

# Procurar por estes sintomas:
# - Processo em execução 20+ minutos
# - Uso de CPU em 0%
# - Estado do processo 'S' (dormindo)
# - Sem conexões de rede
```

### Diagnóstico
```bash
# Obter informações detalhadas do processo
ps -o pid,etime,pcpu,stat,command -p <PID>

# Verificar atividade de rede
lsof -p <PID> 2>/dev/null | grep -E "(TCP|ESTABLISHED)" | wc -l
# Se o resultado for 0, o processo está pendurado
```

### Resolução
```bash
# Matar processos Gemini pendurados
pkill -9 -f "gemini.*gemini-3-pro-preview"

# Ou matar PID específico
kill -9 <PID>

# Verificar limpeza
ps aux | grep gemini | grep -v grep
```

### Prevenção
- **SEMPRE use `--approval-mode yolo` para tarefas automatizadas/background**
- Adicione wrapper de timeout para segurança: `timeout 300 gemini ...`
- Nunca use `--approval-mode default` em shells não-interativos
- Monitore primeira execução com `ps` para garantir que o processo termina

## Dicas para Processamento de Contexto Grande

1. **Seja específico**: Forneça prompts claros e estruturados sobre o que analisar
2. **Use include-directories**: Especifique explicitamente todos os diretórios relevantes
3. **Escolha o modelo certo**:
   - Use `gemini-3-pro-preview` para raciocínio complexo, tarefas de codificação e qualidade máxima de análise (padrão recomendado)
   - Use `gemini-3-flash` para tarefas críticas em velocidade exigindo respostas sub-segundo
   - Use `gemini-2.5-flash` para processamento de alto volume otimizado por custo
4. **Aproveite os pontos fortes do Gemini 3**: 35% melhor em tarefas de engenharia de software, excepção em workflows agênticos e vibe coding
5. **Divida tarefas complexas**: Mesmo com contexto grande, análise estruturada é mais efetiva
6. **Salve resultados**: Peça ao Gemini para exportar relatórios estruturados que podem ser salvos para referência

## Versão CLI

Exige Gemini CLI v0.16.0 ou posterior para suporte do modelo Gemini 3. Verifique versão: `gemini --version`
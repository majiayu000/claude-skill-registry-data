---
name: analise-ultra
description: Use quando pedirem análise completa ou "análise ultra" de site, SaaS, produto ou oferta. Orquestra 24 agentes por parâmetros (pessoas, fundadores, conselho de vendas, marketing) até o plano em PDF.
---

# Análise Ultra (orquestrador de agentes)

Você é o orquestrador. Não analisa no lugar dos agentes: chama cada um com a tarefa certa, em paralelo quando a rodada permite, e deixa o motor `ultra.py` juntar tudo.

## O sistema

| # | Conselho | Agentes | O que sai |
|---|---|---|---|
| 1 | Leitura | `ultra-scan` | mapa do site e dos concorrentes, logos e folha de teste do logo |
| 2 | Cinco pessoas | `ultra-joao-vendas`, `ultra-fernando-artista`, `ultra-ana-crescimento`, `ultra-robson-tecnico`, depois `ultra-andre-critico` | veredito de venda, cortes do André |
| 3 | Fundadores | `ultra-jobs`, `ultra-wozniak`, `ultra-huang`, `ultra-bezos` | acusações com prova, 5 temas, debate das divergências |
| 4 | Conselho de vendas | `ultra-brunson`, `ultra-hormozi`, `ultra-kennedy` | 3 ofertas, votação cruzada, duelo e oferta campeã |
| 5 | Marketing | `ultra-ries-trout`, `ultra-schwartz`, `ultra-ogilvy`, `ultra-hopkins`, `ultra-ellis`, `ultra-ross`, `ultra-sharp`, `ultra-vaynerchuk`, `ultra-design` | entregas prontas por etapa (copy, paleta, Instagram, testes, conteúdo) |
| 6 | Plano | `ultra-moderador`, `ultra-andre-critico`, `ultra-plano` | VEREDITO.md e plano de ação em PDF |

Cada agente lê **parâmetros** (critérios com peso e régua de 0 a 10, testes, alertas, números com fonte) e devolve um **JSON padronizado**. O motor valida, consolida, acha as divergências, faz o duelo de ofertas e monta o plano. Os parâmetros ficam em `~/.ultra-skills/params/`. Para ver os de um agente: `ultra.py params ultra-jobs`.

**Comando do motor:**
- Linux e macOS: `python3 ~/.ultra-skills/ultra.py ...`
- Windows: `py %USERPROFILE%\.ultra-skills\ultra.py ...` (no PowerShell: `py $env:USERPROFILE\.ultra-skills\ultra.py ...`)

## Passo a passo

1. **Pergunte, ou tire da conversa:** a URL; de 3 a 10 concorrentes (se a pessoa não souber, busque e proponha); Instagram; o objetivo; se vende para o Brasil ou para fora.
2. **Inicie:**
   ```bash
   python3 ~/.ultra-skills/ultra.py iniciar https://site.com --concorrentes https://c1.com https://c2.com --print
   ```
   Isso roda o scan, baixa os logos e gera as folhas de teste. O motor imprime a primeira rodada.
3. **Repita até o fim:**
   ```bash
   python3 ~/.ultra-skills/ultra.py proximo --json
   ```
   O resultado lista as `tarefas` da rodada. Cada tarefa traz o agente, o que fazer, o que ler e onde salvar.
   - **Claude Code:** chame cada agente com a ferramenta de subagentes (Task/Agent), com `subagent_type` igual ao nome do agente (ex.: `ultra-jobs`), passando no prompt a tarefa, os arquivos para ler e o caminho para salvar. Quando a rodada diz `"paralelo": true`, chame **todos na mesma mensagem**.
   - **Codex:** peça os agentes pelo nome, em paralelo ("spawn ultra-jobs, ultra-wozniak, ultra-huang e ultra-bezos com estas tarefas"). O Codex só chama agentes quando você pede.
   - **Sem agentes instalados** (ou outra IA): faça o papel de cada agente, um por vez. Carregue os parâmetros com `ultra.py params AGENTE`, siga as regras e o formato de saída e salve o JSON no caminho da tarefa.

   Depois de cada rodada, rode `proximo` de novo. Ele **valida e consolida sozinho** e mostra a rodada seguinte. Se uma saída falhar na validação, devolva o erro ao mesmo agente para ele corrigir.
4. **Rodadas especiais:**
   - **Conselho de vendas, rodada 3:** o motor roda o duelo sozinho (ou `ultra.py duelo PASTA/04-vendas`). Com o ranking e o "melhor componente por critério", chame o autor da oferta vencedora para montar a **oferta campeã** e as 3 ofertas por público em `04-vendas/r3/oferta-campea.json`, no formato `{"ofertas": [...]}` do formato_oferta.
   - **Plano, rodada 1 (moderador):** lê os `consolidado-r*.md` de todos os conselhos e escreve `06-plano/VEREDITO.md`: vende, vende pouco ou não vende; as 3 provas mais fortes; as discordâncias resolvidas e as que ficaram de pé; o placar de evidência.
   - **Plano, rodada 3:** `ultra.py plano PASTA --pdf` gera o `plano.json` e o PDF. Complete os entregáveis vazios antes, se houver.
5. **Entregue:** `06-plano/plano-de-acao.pdf`, `plano-para-ia.md` e `checklist.csv`. No texto, em 3 linhas: o veredito, a primeira ação e por quê, e o maior risco que ficou como hipótese.

## Regras do orquestrador

- Não pule rodadas. Se o usuário pedir só uma parte ("só os fundadores"), rode a leitura e aquela parte.
- Não reescreva a saída de um agente. Se ela estiver fraca, devolva para ele com o motivo (por exemplo, "nota sem evidência").
- Se o placar de evidência passar de 50% de hipótese, diga isso no topo da entrega.
- Divergências não se resolvem por maioria: vence quem tem o degrau de evidência mais alto.
- O scan é sempre o script. Não troque por extensão de navegador nem por leitura manual. Se o scan falhar por rede, siga a tabela de erros da skill `scan-ultra`.

## Uma parte só

| Pedido | Rode |
|---|---|
| "isso vende?" / "dá uma olhada" | leitura + pessoas |
| "meu SaaS presta?" | leitura + pessoas + fundadores |
| "monta uma oferta" / "que preço eu cobro?" | leitura + conselho de vendas (ou a skill `conselho-de-vendas`) |
| "plano de marketing" | tudo |

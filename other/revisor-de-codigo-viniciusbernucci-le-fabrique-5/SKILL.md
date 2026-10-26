---
name: revisor-de-codigo
description: Revisa alterações sem editar código e produz achados e plano de correção. Consolida os critérios de code-reviewer (bugs e performance), clean-code-reviewer (qualidade) e security-reviewer (AppSec). Use para revisar ticket, diff, commit ou branch; não para executar correções, validar a experiência funcional de QA ou auditar todo o sistema.
---

# Revisor de código

Entrada única e gate técnico oficial do fluxo. Os agentes existentes continuam válidos como executores especializados internos; esta skill permite aplicar os mesmos critérios quando não estiverem disponíveis. Não crie outra skill `code-reviewer` concorrente e não rode os agentes novamente sobre o mesmo diff depois deste gate.

## Seleção do modo

- Pedido genérico de revisão de implementação: revisão completa, com correção/performance, qualidade/arquitetura e segurança das mudanças.
- “Tem bug?”, “vai quebrar?”, “N+1?”: correção e performance, conforme [critérios do code-reviewer](references/correcao-performance.md).
- “Boas práticas”, “clean”, “padrões”: [qualidade](references/qualidade.md), sem aplicar refatoração.
- “Brecha”, “security review deste diff”: [segurança](references/seguranca.md).
- Auditoria abrangente, modelo de ameaça ou cadeia de suprimentos: `security-audit`, se disponível. Não executar ambos sobre a mesma superfície sem motivo.
- Revalidação depois de correções: revise somente os IDs informados, os commits de correção e o raio de impacto demonstrável. Preserve os IDs originais e classifique cada um como `VERIFICADO`, `AINDA PRESENTE`, `REGRESSÃO` ou `BLOQUEADO`.

Leia somente as referências dos modos selecionados. Achados de outra especialidade viram encaminhamentos; na revisão completa, consolide pela causa raiz. Não omita risco grave por causa da divisão de papéis.

## Protocolo de escopo

1. Leia AGENTS.md, convenções locais, ticket/aceite e ADRs relevantes quando disponíveis. A ausência de ticket não impede revisar um diff explícito; registre a limitação.
2. Use primeiro arquivos, commit, intervalo ou base informados pelo usuário. Sem escopo explícito, examine `git status --short`: inclua `git diff`, `git diff --cached` e arquivos não rastreados relevantes, lidos integralmente. Não perca alterações já staged.
3. Com árvore limpa, use a base configurada para a tarefa; só depois descubra `refs/remotes/origin/HEAD` ou uma branch principal existente. Registre os hashes de base e HEAD e use `git diff <base>...HEAD`. Não escolha outra base silenciosamente se a informada não existir. Sem base ou mudanças identificáveis, peça apenas o escopo ausente.
4. Em múltiplos repositórios, registre escopo e hashes separadamente. Nunca troque uma worktree pelo checkout principal.
5. Leia inteiros os arquivos de código alterados e rastreie chamadores, contratos, testes e migrations relevantes. Em arquivos grandes, use leitura segmentada e declare lacunas. Separe problemas introduzidos das dívidas preexistentes.
6. Durante a revisão, use somente Git de leitura. Não edite código, não faça commit/push e não execute correções por iniciativa própria. Relatórios são a única escrita desta revisão; aplicação posterior só sob indicação do usuário (ver Saída). Execute verificações locais pertinentes apenas se seu caminho de execução for conhecido e compatível com o ambiente.

Se `.claude/agents/_shared/escopo-revisao.md` existir, leia-o como protocolo local, respeitando o escopo explícito do usuário. Esta skill é autossuficiente quando ele não existir; não invente seu conteúdo.

## Independência e composição

Se houver revisores independentes disponíveis e delegação autorizada, repasse o mesmo escopo imutável e apenas a especialidade necessária. Não execute a mesma especialidade duas vezes por existir como agente e skill. Reaproveite relatórios somente quando seus hashes, diff local e limites coincidirem com o estado revisado.

Uma autorrevisão deve ser identificada como tal; não satisfaz sozinha um gate de revisão independente. A skill não concede aprovação funcional nem declara a tarefa DONE.

## Evidência e severidade

Cada achado precisa de cenário concreto, localização atual, causa, impacto e recomendação verificável. Confirme validações upstream e mitigações antes de reportar. Suspeita sem caminho demonstrado fica em “Precisa de validação”, sem severidade ou afirmação de bug confirmado. Não invente plano SQL, índice existente, execução de teste ou versão vulnerável.

- CRÍTICO: bloqueio grave, perda/corrupção de dados, comprometimento ou indisponibilidade ampla demonstrável.
- ALTO: falha significativa de fluxo, contrato ou proteção.
- MÉDIO: impacto limitado que exige correção planejada.
- BAIXO: manutenção ou melhoria com custo concreto; gosto pessoal não é achado.

`BLOCKER` de relatórios antigos equivale a bloqueio crítico; `NIT` é observação opcional. Segurança não é automaticamente crítica. Exceções documentadas da Intranet continuam aplicáveis somente nesse perfil.

Inclua compatibilidade de migrations, dados legados, locks e ordem de deploy. Conflito com ADR aceito exige avaliação arquitetural; não proponha substituir a arquitetura silenciosamente.

## Saída

No chat: escopo e modos, achados por severidade, lacunas e veredito. Máximo de dez itens médios/baixos no resumo; o relatório conserva todos os achados fundamentados, agrupando repetições.

Grave `docs/historico/reviews/<prefixo>-<escopo>-<AAAA-MM-DD-HHmm>.md`, ou o caminho solicitado. Prefixos: `code-review` (completa ou correção), `clean-code` (qualidade), `security-review` (segurança). Evite sobrescrever outro relatório do mesmo minuto.

Cabeçalho: tarefa, modo, repositório/worktree, base e HEAD, estado local, arquivos cobertos, verificações realmente executadas e seus resultados. Para cada `REVIEW-001` etc.:

- Severidade, especialidade e `arquivo:linha` com trecho mínimo.
- Problema, cenário, risco e evidência; regra/ADR ou custo concreto para qualidade.
- Plano ordenado de alteração: arquivos, abordagem e teste que comprova a correção.
- Dependências, causa compartilhada e risco da mudança.

Finalize com mitigados/verificado e OK, precisa de validação, encaminhamentos e riscos residuais. Sem achados, escreva “Nenhum problema fundamentado no escopo revisado”, preservando as limitações.

Veredito: `APPROVED`, `APPROVED WITH NOTES`, `CHANGES REQUESTED` ou `ARCHITECTURE REVIEW REQUIRED`. Escopo essencial não examinado fica `REVIEW BLOCKED`, sem aprovação por ausência de evidência. Recomendações, sozinhas, nunca autorizam executar a correção: depois do relatório, liste os achados e **PARE**. Se o usuário então indicar IDs para aplicar ("aplica REVIEW-002", "aplica REVIEW-001 a 004", "aplica todos os ALTO"), saia do papel de revisor e siga a seção "Aplicação sob indicação do usuário" do `review-loop-driver` somente para esses IDs; não recuse por esta skill ser de revisão e não aplique os não indicados. No fluxo Intranet/ORCA, o orquestrador envia o relatório ao `review-loop-driver` e para no checkpoint humano de correções. Depois dos commits de correção, feitos pelo usuário ou pelo agente sob indicação, esta skill faz a revalidação focal.

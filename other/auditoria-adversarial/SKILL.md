---
name: auditoria-adversarial
description: Usa quando o usuario pedir "analise adversarial", "engenharia reversa do sistema todo", "varredura geral", "auditoria do projeto", "analise geral pra achar bug e melhoria" ou "revisa o projeto inteiro" - varredura do projeto ou sistema INTEIRO (nao de uma tela so) com varios agentes, achado provado, correcao no mesmo dia e relatorio pro usuario. NAO usa pra revisar um diff ou uma entrega pequena (isso e code-review ou o revisor do orquestrador).
---

# Auditoria adversarial: varrer, provar, corrigir, devolver

O usuario espera no fim: a lista completa do que foi achado, o que ja foi corrigido e o que sobrou pra ele. Lista sem correcao ele cobra ("e o que fez pra corrigir?").

## Regra de uso

- Roda em cima da skill `orquestrador` (mesmo plugin): abra ela antes. Papeis `orq-leitor`, `orq-executor`, `orq-revisor` (instalados pelo plugin com o prefixo orquestrador:) e o registro `operarios.py` sao de la; esta skill nao repete as regras dela.
- So agentes Claude, a menos que a regra do usuario ou do projeto diga outra coisa.
- Ate o fim da fase 6 ninguem edita codigo do projeto.
- Avise o usuario logo depois da fase 1 e antes do primeiro despacho, em 2 linhas: quantos agentes vao rodar, em que modelo, e o que ele recebe no fim.
- Teto de 12 agentes contando auditores, ceticos e critico (mais territorios = menos ceticos). Acima disso, diga o custo estimado ANTES de despachar. No maximo 4 ao mesmo tempo: quem termina libera a vaga pro proximo.
- O que o usuario disser sobre modelo ou quantidade na hora vence esta skill.

## Fases

**0. Preparar** (chefe, sem agente). Sai: lista de territorios e premissas marcadas.
- `git fetch` + `git status`; confira que o HEAD local e o da origem (auditar um HEAD velho desperdica a auditoria inteira).
- Leia o README e as instrucoes do projeto (e, se existir, o relatorio de auditorias anteriores em `docs/auditoria/`), pra nao re-perseguir o que ja foi dado como saudavel.
- Toda premissa vinda de nota, relatorio antigo ou do pedido do usuario entra no brief marcada "confirmar no codigo".
- Meca o tamanho com `git ls-files` por pasta.
- Anote do README do projeto (ou, se existir `PROJETOS.md` na skill `provar-na-tela`, da linha do projeto) os comandos de teste, de banco local e de subir: eles preenchem o brief do auditor e o portao da fase 8.
- Alvo que nao e repositorio git (configuracao da maquina, pasta de notas, pastas soltas): no lugar do `git status`, grave ANTES um manifesto com o sha256 de cada arquivo do alvo e compare no fim (e o que prova que auditor nao editou nada e mostra o que a correcao mexeu). Relatorios numa pasta de trabalho; o consolidado num lugar que nao some.
- Com o modo god do `orquestrador`: os territorios se dividem em 2 frentes na planta e cada mestre faz as fases 2 a 4 e a 8 da frente dele. O critico de cobertura (fase 5) e a conferencia (fase 6) continuam sendo UMA vez so, de quem abriu a obra, na vistoria. O teto de 12 passa a valer por mestre; diga o total ao usuario antes.

**1. Territorios** (chefe). Sai: 4 a 8 territorios disjuntos, cada arquivo em UM so.

| tipo de projeto | territorios |
|---|---|
| sistema com dinheiro ou dado sensivel | acesso e permissoes; separacao entre empresas; dinheiro e invariantes; integracoes externas, repeticao de chamada e idempotencia; banco, migracoes e consultas; telas, numeros e estado; producao (logs e erros reais; so com arquivo de log, ver fase 2) |
| jogo | camadas: executavel e assets; regras e estado do mapa; rede e entrada de outros jogadores; trapaca local |
| site | conteudo e links; formularios; desempenho; acessibilidade; busca |

**2. Auditores** (um por territorio). Papel `orq-executor`, `model` `sonnet`; dinheiro, acesso e separacao entre empresas em `opus`. ESCOPO de escrita: so a pasta de rascunho e o proprio relatorio. Brief = `brief-auditor.md` desta pasta, preenchido. Cada um com ambiente descartavel proprio: porta = porta do README do projeto + numero da letra (A=1, B=2: 5173 vira 5174), banco `adv_<letra>` no banco local descartavel que o README indica; projeto sem banco, sem essa linha. Territorio producao so entra se o chefe baixou o log antes (pelo caminho que o README do projeto indica) e passou o arquivo em FONTES; sem arquivo, o territorio sai da lista. Sai: `docs/auditoria/AAAA-MM-DD/<letra>-<territorio>.md` no projeto.

**3. Juntar** (chefe, ou 1 `orq-leitor` haiku). Agrupe por causa-raiz. Achado que 2 ou mais auditores acharam por caminhos diferentes sobe de prioridade.

**4. Ceticos** (`orq-revisor`: `opus` em lote que tem achado de dinheiro, acesso ou separacao entre empresas; `sonnet` no resto). Sem P0, pule o lote dos P0. Os P0 vao juntos num lote unico visto por 3 ceticos, um por lente (o codigo diz isso mesmo; o caminho e alcancavel de verdade; o impacto e esse); mais de 10 P0, dois lotes de 3 ceticos. Os P1 vao em lotes de ate 10 achados, 1 cetico por lote. Nunca 3 ceticos por achado. A tarefa e DERRUBAR: o caminho existe de verdade? depende de configuracao desligada? a tela oferece esse caminho? Sai: veredito por achado, CONFIRMADO, REBAIXADO ou REFUTADO, com a prova.

**5. Critico de cobertura** (1 `orq-revisor` opus). Lista os arquivos que nenhum relatorio citou (`git ls-files` menos os citados) e le os de maior risco. Olha producao so por log e erro ja disponivel.

**6. Conferencia do chefe.** Releia no codigo a premissa de cada P0 e prove por execucao quando der:

| achado | como provar |
|---|---|
| repeticao de chamada | contar as chamadas com um `fetch` falso |
| corrida | segunda conexao segurando trava |
| dinheiro | banco descartavel com o caso |

P0 que ficou so LIDO (nao deu pra provar por execucao) segue pra fase 8 marcado "nao provado": quem corrige escreve primeiro o teste que reproduz; se nao reproduzir, o achado volta pro chefe.

**7. Consolidado** (chefe) em `docs/auditoria/AAAA-MM-DD/README.md`: placar por gravidade; ordem de ataque por causa-raiz; secao "saudavel, nao re-perseguir"; secao "so producao responde" (cada pergunta com a consulta so-leitura pronta pro usuario abrir); decisoes que sao do usuario.

**8. Correcao.** O usuario espera correcao, nao so lista.
- P0 e P1 no mesmo dia, um `orq-executor` sonnet por DONO DE ARQUIVO; so o chefe commita.
- Toda correcao sai com teste que cai sem ela.
- Antes de por uma trava nova, liste os fluxos que passam por ali (uma trava nova posta numa auditoria ja travou outro fluxo que ninguem tinha listado).
- Conserto sugerido por auditor e RASCUNHO; quem corrige prova.
- Portao final (suite + build) rodado pelo chefe. Deploy segue a regra do projeto.
- Teste novo: desfaca a correcao, rode, veja o teste cair e restaure.

**9. Fechar.**
- Resposta pro usuario em linguagem de leigo: achados por gravidade, o que foi corrigido, o que sobrou e por que, o que depende dele em lista curta.
- Deixe no projeto um resumo (agentes, modelos, tokens, achados, corrigidos e licoes), por exemplo no fim de `docs/auditoria/AAAA-MM-DD/README.md`.
- Registre os operarios (`operarios.py registrar`, `conferir`).

## Gravidade

| nivel | e isto |
|---|---|
| P0 | paga ou perde dinheiro de verdade, vaza dado de outra empresa, ou derruba a producao |
| P1 | numero errado que o usuario usa pra decidir, falha calada, dado duplicado ou sumido, acesso indevido dentro da mesma empresa |
| P2 | defeito real com contorno |
| P3 | melhoria |

## Erros que ja aconteceram

| erro | regra |
|---|---|
| agentes demais, muitos falharam e o credito estourou (auditoria sem teto) | teto de 12; P1 em lote com 1 cetico; so o lote dos P0 leva 3 |
| fato de nota antiga, falso, no brief contaminou o auditor (um nome de campo errado) | premissa de nota ou memoria vai marcada "confirmar no codigo" |
| retry dado como "saudavel" por 3 revisoes que so leram o codigo; so a contagem de chamadas com `fetch` falso pegou | repeticao de chamada se prova contando |
| conserto sugerido errado (uma funcao usada nao devolvia o valor normalizado que o auditor supos; "seq scan" refutado com EXPLAIN) | conserto de auditor e rascunho; quem corrige prova |
| trava nova quebrou outro fluxo (um valor alto ficou sem baixa) | listar os fluxos antes de por a trava |
| teste verde que nao testava nada (o erro forjado caiu no fallback e todos os casos passaram) | teste novo tem que cair sem a correcao |

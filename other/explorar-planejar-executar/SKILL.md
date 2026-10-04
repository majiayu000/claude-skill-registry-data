---
name: explorar-planejar-executar
description: Fluxo de trabalho com IA em 3 fases — Explorar (brainstorm guiado), Planejar (plano com tarefas atômicas) e Executar (passo a passo). Ative esta skill sempre que o usuário digitar `/explorar`, `/planejar` ou `/executar`, ou quando tiver qualquer objetivo que envolva planejamento, criação ou dúvida aberta. Serve tanto para tarefas de código quanto para tarefas do mundo real (escrever, pesquisar, contatar, montar). Idioma pt-BR.
metadata:
  author: "Giuliano Lemes <giuice@gmail.com>"
---

# Explorar → Planejar → Executar

Fluxo em 3 fases para transformar um objetivo vago em entregas concretas.

Cada fase é ativada por um comando explícito do usuário:

- `/explorar` — entender o que a pessoa realmente quer (contexto)
- `/planejar` — propor abordagens e escrever plano com tarefas atômicas
- `/executar` — fazer uma tarefa por vez, com a pessoa no controle

**Transições nunca são automáticas.** Só avance quando o usuário digitar o próximo comando.

---

## Regra global das 3 fases

Sempre que apresentar **duas ou mais opções** ao usuário (perguntas de múltipla escolha, abordagens de plano, variações de saída), marque **uma como "recomendada"** com uma linha curta de motivo. As outras são listadas sem marca.

Exemplo:

```
A — post único com foto do produto — **recomendada** (mais rápido e já testado no seu perfil)
B — carrossel com 5 fotos e storytelling
C — vídeo curto estilo reels
```

Forçar recomendação acelera a decisão e expõe o raciocínio da IA.

---

## Fase 1 — `/explorar`

Quando o usuário digita `/explorar` (ou traz um objetivo aberto sem ter rodado a fase), entre em modo brainstorm guiado.

### Escolha de modo

Logo ao iniciar, pergunte:

> "Quer que eu faça todas as perguntas de uma vez ou uma por vez?"

- **A) Exaustivo** — a IA faz todas as perguntas de uma vez, você responde tudo, ela processa e propõe direção. Mais rápido, menos ida-e-volta.
- **B) Interativo — recomendada** — a IA pergunta uma por vez e ajusta as próximas com base nas respostas. Mais lento, mas mais adaptável e surpreendente.

### Como conduzir

- **Uma pergunta por mensagem (modo interativo).** No modo exaustivo, a IA faz todas as perguntas de uma vez.
- **Prefira múltipla escolha** quando der. Pergunta aberta é permitida se a escolha precisa ser formulada pelo usuário.
- **Foque em:** propósito real, público, restrições (prazo, orçamento, ferramentas disponíveis), critério de sucesso ("como a gente saberá que deu certo?").
- **Reflita o entendimento periodicamente** ("então você quer X porque Y, correto?").
- **A IA decide quando parar.** Pare quando tiver clareza suficiente para propor uma abordagem — não antes, não muito depois. Se o usuário mandar "chega, vamos adiante", respeite.

### Ao sentir que o contexto está claro

1. Gere um resumo estruturado com:
   - **Objetivo** — o que a pessoa quer alcançar
   - **Público / contexto** — quem, onde, quando
   - **Restrições** — prazos, orçamento, ferramentas, o que evitar
   - **Critério de sucesso** — como vamos saber que deu certo
   - **Decisões já tomadas** — escolhas feitas durante a conversa
2. Peça ao usuário para copiar e salvar:

> "Acho que já entendi o suficiente pra gente planejar. Antes de avançar, copie este resumo e salve num arquivo — assim não perde o contexto se o chat cair."

3. Depois, pergunte:

> "Quer que eu salve esse contexto num arquivo? Assim você pode continuar agora ou voltar outro dia em outro chat."

- **Se sim:** salve em `docs/explorar/YYYY-MM-DD-<tópico-curto>.md` com as seções do resumo.
- **Se não:** tudo bem, o contexto vive na conversa atual.

### Orientação de continuidade

Depois de salvar, avise:

> "Pronto. Se quiser parar por aqui, abra um chat novo outro dia, aponte para `docs/explorar/<arquivo>.md` e digite `/planejar` que a gente continua."

### O que NÃO fazer em `/explorar`

- Não escreva plano nem código ainda.
- Não proponha soluções antes de entender o problema.
- Não assuma premissas — pergunte.

---

## Fase 2 — `/planejar`

Pré-requisito: existe contexto (arquivo de `/explorar` ou conversa atual). Se o usuário rodar `/planejar` do zero sem contexto, rode `/explorar` primeiro.

### Passo 1 — Apresentar 2-3 abordagens

Antes de escrever o plano, proponha **2 ou 3 abordagens** diferentes para atingir o objetivo. Cada uma com:

- Nome curto
- 1-2 linhas de descrição
- Trade-offs (o que ganha, o que perde)
- **Uma marcada como "recomendada"** com motivo

Espere o usuário escolher (pode pedir ajustes na abordagem também — itere).

### Passo 2 — Escrever o plano

Salve em `docs/planejar/YYYY-MM-DD-<tópico-curto>.md` com esta estrutura:

```markdown
# Plano: <título>

**Objetivo:** <uma frase>

**Abordagem escolhida:** <nome + 2-3 linhas>

**Arquivos / artefatos que serão criados ou alterados:**
- <caminho ou nome do entregável> — <propósito>

---

## Tarefas

- [ ] **Tarefa 1: <nome curto e específico>**
  - <o que exatamente fazer, com conteúdo suficiente pra executar>
  - <se código: mostrar o código completo; se ação real: mostrar o texto, a lista, o template>
  - <como saber que ficou pronto>

- [ ] **Tarefa 2: ...**
```

### Regras do plano

- **Tarefas atômicas:** cada uma deve caber em 2 a 5 minutos de execução. Se uma tarefa parece grande, quebre.
- **Sem placeholders.** Nada de "TBD", "ajustar depois", "ver com fulano". Se não sabe, pergunte antes de salvar.
- **Conteúdo completo em cada tarefa.** Não escreva "similar à tarefa 1" — repita. Quem executa pode ler fora de ordem.
- **Tarefas podem ser de qualquer natureza:** código, escrever texto, pesquisar, ligar pra fornecedor, montar planilha. A estrutura atômica é a mesma.
- **Caminhos explícitos** quando envolver arquivos.
- **Critério de pronto** por tarefa quando não for óbvio.

### Passo 3 — Self-review

Antes de apresentar ao usuário, releia o plano e verifique:

1. **Cobertura** — cada ponto do contexto vira tarefa?
2. **Placeholders** — algum "TBD", "ajustar", "ver depois"? Conserte.
3. **Consistência** — nomes, caminhos e formatos batem entre tarefas?
4. **Escopo** — o plano faz uma coisa só, ou tá tentando resolver vários problemas de uma vez? Se for o segundo caso, proponha dividir.

Conserte inline o que achar.

### Passo 4 — Gate duro

Avise que o arquivo foi salvo e peça revisão:

> "Plano salvo em `docs/planejar/<arquivo>.md`. Antes de executar, copie o plano e salve localmente — assim você tem backup se o chat cair. Depois, dá uma lida e me fala se quer ajustar algo antes de rodar `/executar`."

**Nunca chame `/executar` se o arquivo de plano não foi salvo.** Se o usuário pedir pra executar sem salvar, recuse e salve primeiro.

### O que NÃO fazer em `/planejar`

- Não exija TDD, testes ou commits — essa skill é genérica, não só pra código.
- Não gerencie git, branches, worktrees.
- Não execute nada ainda.

---

## Fase 3 — `/executar`

Pré-requisito: existe arquivo de plano em `docs/planejar/`. Se não existir, recuse:

> "Não achei um plano salvo. Rode `/planejar` primeiro pra gente ter um arquivo com as tarefas."

### Modo de execução

**Uma tarefa por vez.** Para cada tarefa:

1. Leia o plano, pegue a próxima tarefa não-marcada (`- [ ]`).
2. Diga ao usuário qual tarefa vai fazer.
3. Execute (escreva o código, redija o texto, monte a lista etc.).
4. Mostre o resultado.
5. **Marque a tarefa como feita** no arquivo do plano: troque `- [ ]` por `- [x]`.
6. Pergunte: "Seguir pra próxima?"
7. Espere o OK.

### Saída de tarefas não-código

Quando a tarefa gera conteúdo que o usuário vai usar (legendas, e-mails, listas, templates):

- **Mostre no chat** para o usuário ver na hora.
- **Salve também** em `docs/executar/<tópico>/outputs.md`, agrupando por tarefa, pra ficar registrado e fácil de copiar depois.

### Desvios no meio da execução

Se durante a execução a IA perceber que o plano está errado (ex.: tarefa 3 depende de algo que não existe, premissa caiu, resultado da tarefa anterior mudou o rumo):

1. **Pare.** Não tente ajustar sozinha.
2. **Reporte o que achou e por quê.**
3. **Pergunte:** "Ajusto o plano ou faço um workaround nessa tarefa e sigo?"
4. Se o usuário decidir ajustar o plano, volte pra `/planejar` (ou edite o arquivo direto se for ajuste pequeno e o usuário permitir).

### Fim da execução

Quando todas as tarefas estiverem `[x]`:

- Escreva um **resumo curto** do que foi entregue (3-6 linhas).
- Liste os **caminhos dos arquivos gerados** (plano, outputs, artefatos).
- **Não sugira próximo passo automaticamente.** O usuário decide se quer rodar outro `/explorar` ou parar.

### O que NÃO fazer em `/executar`

- Não pule tarefas.
- Não execute várias de uma vez sem pedir.
- Não edite o plano silenciosamente — desvios sempre viram conversa.

---

## Compatibilidade de plataforma

Esta skill usa instruções genéricas (ler/salvar/editar arquivo) em vez de nomes de ferramentas específicas de uma plataforma. Ela funciona em Claude Code, Copilot CLI e Codex sem adaptação. A IA hospedeira escolhe as ferramentas concretas (`Read`/`Write`/`Edit` no Claude Code, `view`/`create`/`edit` no Copilot CLI, equivalentes no Codex).

## Idioma

Toda interação com o usuário e todos os arquivos gerados em **pt-BR**. Público-alvo inclui iniciantes sem conhecimento técnico — evite jargão desnecessário.

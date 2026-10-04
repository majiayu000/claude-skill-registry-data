---
name: context-handoff
description: >
  Gera um bloco de contexto estruturado da conversa atual para ser colado no início de uma nova conversa.
  Use esta skill SEMPRE que o usuário mencionar trocar de conversa, novo chat, transferir contexto, ou dizer:
  "resumo para colar", "context dump", "vou abrir outro chat", "quero continuar em outra conversa",
  "me dê um handoff", "resumo da sessão", "briefing para próxima conversa", ou qualquer variação.
  A skill funciona em Claude Code, Claude.ai Chat e Cowork.
  O objetivo é que o próximo Claude entenda imediatamente quem é o usuário, o que foi feito e o que vem a seguir —
  sem reexplicações, sem perguntas, 100% pronto para continuar.
  Importante: sempre ofereça esta skill quando detectar que o usuário pode querer mudar de conversa.
---

# Context Handoff

O propósito desta skill é eliminar o atrito de trocar de conversa. Quando o usuário pede um handoff, ele quer poder abrir um chat novo, colar o bloco gerado, e continuar de onde parou — sem reexplicar nada.

## Como gerar o handoff

Leia toda a conversa e produza um único bloco markdown com as seções abaixo. Seja cirúrgico: inclua só o que é relevante para continuar o trabalho. Omita detalhes que o próximo Claude pode inferir facilmente.

O bloco deve começar com uma linha de instrução para o próximo Claude:

```
> Contexto de sessão anterior. Leia este briefing antes de responder.
```

---

## Estrutura do bloco

### 1. Perfil do usuário
O que se sabe sobre quem é o usuário — cargo, nível técnico, preferências de trabalho, ferramentas que usa. Só inclua o que for relevante para o trabalho em andamento.

### 2. O que foi feito nesta sessão
Lista objetiva das ações concluídas. Use bullet points concisos. Para cada item relevante, inclua o resultado — não só "instalamos X" mas "instalamos X, que está em ~/caminho/".

### 3. Decisões tomadas
Decisões que não devem ser questionadas na próxima sessão. O próximo Claude deve tratá-las como definidas. Exemplo: "Stack escolhida: React Native + Expo. Não reavaliar."

### 4. Estado atual
Onde as coisas estão agora. Arquivos criados, configurações feitas, o que está funcionando, o que está pendente. Seja específico com caminhos e nomes de arquivo quando relevante.

### 5. Próximos passos
O que o usuário provavelmente vai querer fazer a seguir, em ordem de prioridade. Se houver um cronograma ou deadline, inclua.

### 6. Contexto técnico relevante
Skills instaladas, MCPs ativos, configurações específicas, comandos importantes — só o que vai importar na próxima sessão.

---

## Diretrizes de qualidade

**Seja denso, não longo.** O bloco ideal tem entre 200 e 400 palavras. Se passar disso, você provavelmente está incluindo detalhes desnecessários.

**Fale como quem passa bastão.** Escreva como se estivesse passando o trabalho para um colega que sabe o que está fazendo mas não esteve na reunião. Sem contexto óbvio, sem repetição, direto ao ponto.

**Preserve números e nomes exatos.** Caminhos de arquivo, nomes de variáveis, versões, preços, datas — esses detalhes importam e o próximo Claude não tem como adivinhar.

**Sinalize o que está em aberto.** Se houver dúvidas não resolvidas ou decisões pendentes, coloque em destaque para o próximo Claude não assumir que estão resolvidas.

**Termine com uma linha de "próxima ação"** — a primeira coisa que o usuário vai pedir. Isso ajuda o próximo Claude a já estar "aquecido" para a tarefa.

---

## Formato de saída

Entregue o bloco pronto para copiar, dentro de um code block markdown. O usuário deve poder selecionar tudo, copiar e colar diretamente.

Após o bloco, adicione uma linha simples fora dele:
> Pronto. Cole isso no início da próxima conversa.

Não adicione explicações, comentários ou perguntas após o bloco — o usuário já sabe o que fazer com ele.

---

## Ambiente-específico

### Claude Code (`/context-handoff`)
Acionável via comando slash. O handoff é markdown puro, pronto para colar. Se o usuário quiser JSON para automação, execute o script `export_context.py` na pasta da skill.

### Claude.ai Chat
A skill funciona como instrução ao modelo. O handoff é markdown. Não há subagents, então não há automação, mas o output é o mesmo — pronto para copiar/colar em outro chat.

### Cowork
Funciona como Claude Code. Acionável via `/context-handoff`. Se integrado com N8N ou workflows, use o script `export_context.py` para JSON estruturado.

---

## Automação (JSON export)

Se precisar passar o contexto para um workflow ou MCP, use:

```bash
python scripts/export_context.py --format json
```

Isso gera um JSON estruturado com campos: `user_profile`, `completed_actions`, `decisions`, `current_state`, `next_steps`, `technical_context`.

Útil para: N8N workflows, webhooks, automação cross-tool.

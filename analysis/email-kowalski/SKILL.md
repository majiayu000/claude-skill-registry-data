---
name: email-kowalski
description: Email drafting and analysis skill for NeuroAds. Uses Gmail MCP to compose, search, and manage professional sales and outreach emails. Follows NeuroAds tone (confiante, técnica, premium, em pt-BR).
allowed-tools: mcp__Gmail__search_threads, mcp__Gmail__get_thread, mcp__Gmail__create_draft, mcp__Gmail__list_labels, mcp__Gmail__label_thread, mcp__Gmail__list_drafts
---

# Email Kowalski — Email Intelligence for NeuroAds

> Analyze context, draft precision. "Kowalski, analysis!" applied to every email.

## When to use

Invoke this skill whenever you need to:
- Draft a professional outreach or follow-up email on behalf of NeuroAds
- Search and analyze existing email threads for context before replying
- Create Gmail drafts ready for human review and sending
- Suggest email copy aligned with NeuroAds brand voice

## Tone & Brand Rules

Always write in **pt-BR** unless the recipient wrote in English first.

| Do | Don't |
|----|-------|
| Frases curtas e diretas | Blocos de texto sem quebra |
| Traduzir valor em impacto de negócio | "Garantimos resultados" |
| "dados reais", "crescimento previsível", "sistema", "próximo passo" | Promessas vagas ou linguagem agressiva |
| Tom consultivo e assertivo | Jargão técnico sem explicação |

## Instructions

### 1. Gather context first
Before drafting, always search for prior threads with the recipient:
```
search_threads: from:<recipient> OR to:<recipient>
```
Read the most recent thread with `get_thread` to understand the conversation history.

### 2. Draft structure

**Subject line:** Direct, benefit-led, ≤50 chars.

**Body (3 paragraphs max):**
1. **Contexto** — 1 sentence connecting to what they last discussed or a relevant trigger.
2. **Valor** — What NeuroAds can do for them, in business-outcome terms (ROAS, escala, previsibilidade).
3. **Próximo passo** — Single, clear CTA: agendar, responder, ou clicar num link.

**Signature block:**
```
[Nome]
NeuroAds | Agentes de IA em Performance
https://neuroads.com.br
```

### 3. Create the draft
Use `create_draft` to save the email — never send directly. The human reviews and sends.

### 4. Confirm output
After creating the draft, confirm:
- Draft ID and subject
- Recipient and any Cc
- A one-line summary of the email's purpose

## Common Templates

### Cold outreach
```
Assunto: IA gerindo suas campanhas no Google Ads — sem operar o dia a dia

[Nome],

Vi que você investe em tráfego pago. A NeuroAds opera campanhas com agentes de IA — conectados direto ao Google Ads via MCC — que monitoram, otimizam e escalam 24h sem intervenção manual.

Resultado prático: ROAS mais previsível, menos desperdício e um sistema que trabalha enquanto você foca no negócio.

Posso mostrar como funciona em 20 minutos. Tem disponibilidade essa semana?

[Assinatura]
```

### Follow-up após reunião
```
Assunto: Próximos passos — NeuroAds

[Nome],

Obrigado pelo tempo hoje. Conforme conversamos, o maior ganho para vocês está em [X — preencher com dado real da conversa].

Estou enviando o acesso à plataforma para você avaliar. Qualquer dúvida, é só responder aqui.

[Assinatura]
```

### Reativação de lead frio
```
Assunto: Atualização rápida — NeuroAds

[Nome],

Faz um tempo que não falamos. Desde nossa última conversa, lançamos [novidade relevante].

Vale um papo de 15 minutos para ver se faz sentido agora?

[Assinatura]
```

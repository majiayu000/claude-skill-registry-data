---
name: marketing-site-gmn-otimizacao-gmn
description: Otimiza e mantém continuamente um perfil do Google Meu Negócio (GMN) já configurado — monitorar/responder avaliações, atualizar informações, melhorar posicionamento local. Habilidade acionada pela skill orquestradora marketing-site-gmn. Use quando o pedido for sobre melhorar o posicionamento no Google, responder avaliação, ou revisar um perfil GMN que já existe — não usar para configurar o perfil pela primeira vez (isso é marketing-site-gmn-perfil-gmn) nem para publicar posts/novidades (isso é marketing-social-media-gmn-post).
---

# Habilidade: Otimização Contínua do Perfil GMN

## Contexto obrigatório
Leia `/memoria/tom-de-voz.md` e `/marketing/contexto.md`.

## Procedimento
1. Identifique o objetivo: responder avaliação, atualizar informação desatualizada, ou melhorar posicionamento local (SEO local).
2. **Resposta a avaliação**: sempre responder no tom de voz do cliente, agradecendo avaliações positivas de forma específica (não genérica) e tratando negativas com empatia e proposta objetiva de resolução — nunca discutir publicamente ou ser defensivo.
3. **Atualização de informação**: confirmar o dado correto com o CEO/cliente antes de qualquer mudança (horário, endereço, telefone).
4. **Melhoria de posicionamento local**: revisar consistência da categoria/descrição, sugerir novas fotos periódicas, e reforçar a importância de posts regulares no GMN (aciona `marketing-social-media-gmn-post` se for o caso) e de reviews — o Google prioriza perfis ativos.

## Entrega
Diagnóstico + ações recomendadas (e resposta pronta, se for o caso de avaliação), salvo em `/saidas/AAAA-MM-DD/marketing/otimizacao-gmn-<cliente>.md`.

## Regras
- Nunca responder avaliação ou alterar o perfil de fato sem aprovação explícita do CEO.
- Nunca inventar dado — confirmar antes de atualizar qualquer informação do perfil.

## Skills complementares
Pode consultar `seo-audit` como apoio pra diagnosticar SEO local — sem pular as regras acima.

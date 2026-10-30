---
name: marketing-social-media-gmn-post
description: Prepara o rascunho de uma publicação de novidade/oferta/evento para o Google Meu Negócio (GMN) de um cliente da Creative Marketing. Habilidade acionada pela skill orquestradora marketing-social-media. Use quando o pedido for especificamente sobre postar/publicar algo no perfil do Google Meu Negócio do cliente — não usar para criar ou editar a ficha/perfil do GMN em si (categoria, endereço, horário — isso é a skill marketing-site-gmn) nem para redes sociais como Instagram/Facebook (isso é a habilidade marketing-social-media-legenda).
---

# Habilidade: Postagem no Google Meu Negócio

## Contexto obrigatório
Leia `/memoria/tom-de-voz.md` e `/marketing/contexto.md`. Use o tom do cliente dono do perfil do GMN, não o da Creative (salvo se o post for institucional da própria Creative).

## Diferença de formato vs. redes sociais
Posts do GMN são mais curtos e diretos que Instagram/Facebook:
- Sem hashtags
- Foco em uma única informação (novidade, oferta, evento, atualização)
- Sempre com um botão de ação quando a plataforma permitir (ex: "Saiba mais", "Ligar", "Ver oferta", "Comprar")
- Texto objetivo — o usuário do Google Maps/Busca decide rápido

## Procedimento
1. Identifique o tipo de post: Novidade, Evento, Oferta ou Produto.
2. Escreva um texto curto (2-4 frases) com a informação principal já na primeira frase.
3. Defina o botão de ação mais adequado ao objetivo.
4. Nunca invente dados (preço, data do evento, condições da oferta) — pergunte se faltar.
5. Sinalize se o post precisa de uma imagem — se precisar de uma peça nova, aciona `marketing-video-criativos`; se só precisa de uma imagem já existente, apenas referencie qual.

## Entrega
- **Nunca publicar de fato no GMN** sem aprovação explícita do dono/CEO ou do cliente — esta habilidade só produz o rascunho.
- Salvar em `/saidas/AAAA-MM-DD/marketing/gmn-post-<cliente>.md`

## Skills complementares
Depois de aprovado pelo CEO, a publicação real pode ser feita via `postiz:postiz` (ferramenta de agendamento/publicação em redes). Publicar de fato continua exigindo aprovação explícita a cada vez, mesmo usando essa skill.

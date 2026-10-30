---
name: marketing-social-media-pauta
description: Monta o calendário/pauta de conteúdo (semanal ou mensal) para redes sociais de um cliente da Creative Marketing — define datas, plataformas, formatos e temas dos posts. Habilidade acionada pela skill orquestradora marketing-social-media. Use quando o pedido for especificamente sobre planejar o que postar, montar calendário editorial, ou organizar uma pauta — não escreve a legenda final nem publica (isso é outra habilidade).
---

# Habilidade: Pauta / Calendário de Conteúdo

## Contexto obrigatório
Leia `/memoria/negocio.md`, `/memoria/tom-de-voz.md` e `/marketing/contexto.md` antes de montar qualquer pauta.

## Antes de montar a pauta
Confirme (pergunte ao dono/CEO se não estiver claro):
- Nicho e região do cliente
- Objetivo do período (lançamento de produto/serviço, captação, autoridade de marca, aquecimento pra evento)
- Frequência combinada (ex: 3x/semana feed + stories diários)
- Plataformas ativas (Instagram, Facebook, Google Meu Negócio)

## Procedimento
1. Defina o período (semana ou mês) e liste as datas de publicação conforme a frequência combinada.
2. Para cada data, defina: plataforma, formato (feed, story, reels, carrossel, post do GMN) e tema/objetivo do post.
3. Misture os tipos de conteúdo conforme o objetivo do período — como padrão, equilibre entre: institucional/autoridade, prova social (depoimentos, resultados), conteúdo de produto/serviço, e educativo (dicas relevantes pro público daquele nicho).
4. Marque quais posts dependem de uma peça nova (foto, vídeo, arte) — sinalize que isso deve acionar a skill `marketing-video-criativos`.
5. Marque quais posts precisam de legenda escrita — sinalize que isso deve acionar a skill `marketing-social-media-legenda`.
6. Não escreva a legenda final aqui — apenas o resumo do tema/ideia de cada post.

## Template
```
# Pauta — <cliente> — <semana de DD/MM ou mês>

| Data | Plataforma | Formato | Tema/objetivo | Precisa de peça nova? | Legenda pendente? |
|------|-----------|---------|----------------|-------------------------|---------------------|
```

## Entrega
Salvar em `/saidas/AAAA-MM-DD/marketing/pauta-<cliente>.md`. Não publicar nada — esta habilidade só planeja.

## Skills complementares
Pode consultar `content-strategy` e `content-calendar-sms` como apoio pra estruturar o calendário — sem pular o procedimento acima.

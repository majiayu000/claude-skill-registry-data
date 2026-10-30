---
name: marketing-video-criativos-video
description: Produz ou edita uma peça de vídeo (reels, institucional, depoimento, vídeo de produto/serviço) a partir de um briefing já definido. Habilidade acionada pela skill orquestradora marketing-video-criativos. Use quando o pedido for sobre gravar, editar ou gerar um vídeo — não usar para o roteiro/briefing (isso é marketing-video-criativos-briefing) nem para peça estática/imagem (isso é marketing-video-criativos-imagem).
---

# Habilidade: Produção/Edição de Vídeo

## Contexto obrigatório
Leia o briefing (`marketing-video-criativos-briefing`, se existir), `/identidade/visual.md` e `/marketing/contexto.md`.

## Procedimento
1. Confirme o roteiro/briefing antes de produzir — se não existir, aciona `marketing-video-criativos-briefing` primeiro.
2. Defina o formato técnico: proporção (9:16 vertical pra reels/stories, 1:1 ou 16:9 pra outros usos), duração alvo, e se precisa de legenda embutida (muito conteúdo é visto sem som).
3. Monte a edição seguindo o roteiro: gancho nos primeiros segundos, ritmo de corte adequado ao formato, música/trilha coerente com o tom da marca (sem violar direito autoral — usar bibliotecas licenciadas).
4. Aplique identidade visual: cores, logo (discreto, sem competir com o conteúdo), tipografia de legendas se houver.
5. Gere a peça final no formato técnico correto pra onde vai ser usada.

## Entrega
Vídeo final (ou instrução detalhada de edição, se a produção depender de ferramenta externa), salvo/referenciado em `/saidas/AAAA-MM-DD/marketing/video-<cliente>.md` (ou o arquivo de vídeo, se gerado nesta sessão).

## Regras
- Não usar música ou material de terceiros sem licença.
- Não publicar o vídeo de fato sem aprovação explícita do CEO.
- Não inventar informação do produto/serviço mostrado no vídeo.

## Skills complementares
Pode consultar `video-generation` (geração de vídeo via IA) e `video` (produção/edição geral) como apoio técnico — sem pular as regras acima.

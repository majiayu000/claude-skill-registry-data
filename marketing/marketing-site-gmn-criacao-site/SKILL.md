---
name: marketing-site-gmn-criacao-site
description: Levanta requisitos e estrutura a criação de um site novo para um cliente da Creative Marketing, em qualquer nicho — páginas, conteúdo necessário, SEO básico. Habilidade acionada pela skill orquestradora marketing-site-gmn. Use quando o pedido for sobre criar um site novo, estruturar as páginas de um site, ou planejar o conteúdo de um site — não usar para manutenção de site já existente (isso é marketing-site-gmn-manutencao-site) nem para a ficha do Google Meu Negócio (isso é marketing-site-gmn-perfil-gmn).
---

# Habilidade: Criação de Site

## Contexto obrigatório
Leia `/memoria/negocio.md`, `/memoria/tom-de-voz.md`, `/identidade/visual.md` e `/marketing/contexto.md`.

## O que perguntar ao CEO antes de estruturar (se não estiver registrado)
- Qual o nicho do cliente e o que ele vende/oferece?
- Objetivo principal do site: vitrine de produtos/serviços, institucional, captação de lead, ou uma combinação?
- Já tem domínio/hospedagem, ou depende de decisão do cliente?
- Tem identidade visual própria do cliente, ou usa a padrão da Creative?
- Integra com algum catálogo, portal ou CRM já usado pelo cliente?

## Procedimento
1. Defina o **objetivo principal** do site (vitrine de produtos/serviços, institucional, geração de lead) — isso direciona a estrutura de páginas.
2. Estruture as **páginas necessárias**: normalmente Home, Produtos/Serviços, Sobre, Contato — ajuste conforme o objetivo, o nicho e o que o cliente já tem.
3. Para cada página, liste o **conteúdo necessário** (textos, fotos, vídeos, catálogo) e sinalize o que falta pedir ao cliente vs. o que a Creative vai produzir (aciona `marketing-video-criativos` se precisar de peça nova).
4. Defina **SEO básico**: título e descrição de cada página, palavras-chave alinhadas ao nicho e à região do cliente (quando relevante).
5. Garanta que exista um **formulário/CTA de contato** claro em pelo menos Home e Contato — o site também é canal de geração de lead.
6. Verifique a **identidade visual** aplicada (do cliente, ou padrão da Creative se institucional) e o tom de voz do conteúdo.

## Entrega
Documento de estrutura do site (mapa de páginas + conteúdo necessário + SEO básico), salvo em `/saidas/AAAA-MM-DD/marketing/site-<cliente>.md`.

## Regras
- Não publicar/subir o site ao ar sem aprovação explícita do CEO.
- Não inventar dados do cliente (produtos/serviços, contato, endereço) — pedir se faltar.

## Skills complementares
Pode consultar `landing-page-generator` (estrutura de página de captura), `seo-audit`/`ai-seo` (visibilidade em buscadores tradicionais e de IA) e `cro` (otimização de conversão) como apoio — sem pular as regras acima.

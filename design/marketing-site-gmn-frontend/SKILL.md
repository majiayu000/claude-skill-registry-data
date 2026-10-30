---
name: marketing-site-gmn-frontend
description: Constrói o front-end de fato do site (código/página) a partir da estrutura e conteúdo já definidos, para um cliente da Creative Marketing em qualquer nicho. Habilidade acionada pela skill orquestradora marketing-site-gmn. Use quando o pedido for sobre codificar, montar ou publicar as páginas de um site — não usar para levantar requisitos/estrutura (isso é marketing-site-gmn-criacao-site, que deve rodar antes) nem para pequenos ajustes de conteúdo em site que já está no ar (isso é marketing-site-gmn-manutencao-site).
---

# Habilidade: Front-end do Site

## Contexto obrigatório
Leia a estrutura do site (`marketing-site-gmn-criacao-site`, se existir — não construir sem ela), `/identidade/visual.md` e `/marketing/contexto.md`.

## Antes de construir
Confirme (pergunte ao CEO se não estiver claro):
- O mapa de páginas e conteúdo já foi definido (`marketing-site-gmn-criacao-site`)? Não pule essa etapa.
- Stack/plataforma: código do zero (HTML/CSS/JS ou framework), ou um site builder (ex: WordPress, Webflow) que o cliente já usa?
- Onde vai hospedar/publicar (domínio, hosting) — isso pode já estar decidido ou pendente.

## Procedimento
1. Traduza o mapa de páginas em telas reais: layout, hierarquia visual, responsividade (mobile é prioridade — a maior parte do tráfego de leads vem de celular).
2. Aplique a identidade visual do cliente (ou padrão da Creative, se institucional): cores, tipografia, logo, espaçamento consistente.
3. Implemente os elementos de conversão definidos na estrutura: formulário/CTA de contato, botões de WhatsApp, chamadas claras.
4. Garanta performance básica: imagens otimizadas, carregamento rápido — isso afeta tanto experiência quanto SEO.
5. Implemente o SEO técnico básico definido na estrutura (títulos, descrições, meta tags).
6. Teste a responsividade em pelo menos desktop e mobile antes de considerar pronto.

## Entrega
Código/página construída, ou entregue como arquivo/projeto pronto pra revisão, referenciado em `/saidas/AAAA-MM-DD/marketing/frontend-<cliente>.md` (com link/local do projeto).

## Regras
- Não construir sem a estrutura (`marketing-site-gmn-criacao-site`) definida antes.
- Não publicar/subir ao ar em domínio real sem aprovação explícita do CEO.
- Não inventar conteúdo/dado do cliente que não foi fornecido na estrutura.

## Skills complementares
Pode consultar `frontend-design` (direção estética e escolhas de UI), `landing-page-generator`, `web-artifacts-builder`, `premium-saas-design`, `tailwind-design-system` e `shadcn-ui` como apoio técnico de construção — sem pular as regras acima.

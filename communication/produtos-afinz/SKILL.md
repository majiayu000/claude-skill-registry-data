---
name: produtos-afinz
description: Valida benefícios, condições e proposta de valor de produtos Afinz e
  os transforma em estratégia, briefing, copy e régua CRM. Use para aquisição, revisão
  de campanhas, documentação de produto ou materiais que não podem depender de claims
  desatualizados. O módulo atual cobre Plurix e o cartão +amigo; outros produtos devem
  ser adicionados como referências separadas.
metadata:
  version: 1.0.1
  origin: claude-projeto
  agents:
  - claude-code
  - codex
  - cowork
  - chatgpt
  process:
  - Produto
  owner: Time GaaS Afinz
  last_validated: null
  packaged_at: '2026-10-30'
  compatibility: Instruções portáveis; execução não validada por ambiente
  license: Distribuição pública autorizada pelo titular; sem concessão adicional de
    licença
---

# Produtos Afinz

Converta conhecimento de produto em comunicação comercial vendável, contextual e auditável. A skill não substitui Jurídico, contrato vigente, Test Send ou análise de crédito.

## Roteamento

- Para Plurix, Clube +amigo ou cartão +amigo, leia integralmente [references/plurix-cartao-mais-amigo.md](references/plurix-cartao-mais-amigo.md).
- Para briefing e régua de aquisição, leia também [references/briefing-regua-aquisicao.md](references/briefing-regua-aquisicao.md).
- Se o pedido envolver copy final, combine com `afinz-copy-aquisicao`.
- Se envolver as 36 colunas, AMPscript, CSV, Data Extension ou SFMC, combine com `emails-dinamicos-sfmc`.
- Se envolver PPTX, combine com `afinz-pptx` e a skill de apresentações.

## Princípio de produto

Não confunda quatro camadas: benefício gratuito do Clube; benefício incremental condicionado ao pagamento com o cartão; capacidade financeira do cartão e da bandeira Visa; campanha promocional temporária.

A comunicação deve deixar claro por que vale solicitar o cartão quando o Clube já é gratuito. Comece pela economia adicional comprovável na compra recorrente; depois amplie para prazo, utilidade Visa, saúde e experiência digital.

## Protocolo de vigência

Antes de usar uma alegação:

1. Consulte a página central atual do produto e fontes oficiais por rede.
2. Compare contrato, tabela de tarifas, FAQ e regulamento promocional.
3. Registre data de corte, rede/praça, condição, fonte e confiança.
4. Classifique o claim como `confirmado`, `condicional`, `divergente`, `encerrado` ou `hipótese`.
5. Se fontes oficiais divergirem, use a interpretação mais restritiva e abra pendência; nunca resolva a divergência por inferência.
6. Ofertas e preços precisam de início, fim, loja/praça e fallback evergreen.

Nunca transforme dado ausente em benefício, gratuidade, aprovação, limite, economia ou resultado.

## Saída mínima

Toda análise deve produzir: verdade atual do produto; proposta de valor; diferenças entre Clube, cartão e promoção; claims permitidos, condicionais e bloqueados; públicos e sinais; objeções; implicações para briefing, copy e mensuração; fontes e data de corte.

Para uma régua, acrescente progressão narrativa, papel de cada disparo, premissa, benefício principal, prova, objeção, CTA(s), gatilho, supressão e hipótese de teste. Em aquisição de cartão, os CTAs devem levar ao app ou diretamente à solicitação. Condições, tarifas e detalhes do benefício entram no conteúdo e na nota legal, sem desviar tráfego para objetivos intermediários.

## Medição

Não declare sucesso por abertura ou clique. Use proposta iniciada/concluída, aprovação, ativação, primeira compra, atividade em 60/90 dias e valor incremental líquido contra holdout. Taxas de e-mail são diagnósticos. Qualquer case sem dados observados deve ser rotulado como demonstrativo ou hipótese.

## Evolução

Cada novo produto Afinz deve ganhar um arquivo próprio em `references/`, com fontes oficiais, data de corte, claims e riscos. Não misture regras de produtos diferentes no `SKILL.md`.

---
name: sfmc-acquisition-email-designer
description: Criar, alterar, evoluir, comparar e auditar e-mails HTML com AMPscript
  para aquisição Afinz no Salesforce Marketing Cloud, incluindo templates dinâmicos
  compartilhados, regressão visual entre versões, cobertura de campos, layout responsivo,
  ativos, copy, personalização, compatibilidade e QA. Use quando o usuário fornecer
  código, briefing, print ou referência visual e quiser produzir, modificar ou promover
  uma versão de e-mail; para CSV, DE, chave composta e importação, use emails-dinamicos-sfmc.
metadata:
  version: 1.0.0
  origin: claude-projeto
  agents:
  - claude-code
  - codex
  - cowork
  - chatgpt
  process:
  - SFMC
  owner: Time GaaS Afinz
  last_validated: null
  packaged_at: '2026-10-30'
  compatibility: Instruções portáveis; execução não validada por ambiente
  license: Distribuição pública autorizada pelo titular; sem concessão adicional de
    licença
---

# SFMC Acquisition Email Designer

Produza e altere e-mails de aquisição da Afinz com precisão visual e segurança operacional. O GaaS é ambiente de edição e simulação; o Test Send do SFMC é a certificação final.

## Fronteira

- Esta skill cuida de estratégia criativa, copy, HTML de e-mail, AMPscript, ativos, renderização e QA.
- Leia `.claude/skills/emails-dinamicos-sfmc/SKILL.md` quando a tarefa envolver DE, CSV, importação, chave `PRODUTO + TP_CAMPANHA + SEQUENCIA`, vigência ou jornada.
- Não confunda parceiro e assinatura: em Plurix, `Plurix` é parceiro; Amigão, Boa, Avenida, Compre Mais e demais bandeiras são assinaturas apresentadas ao cliente.
- Não altere DE, jornada, tracking, open counter, links, legal ou lógica dinâmica fora do escopo pedido.
- Não declare produção pronta sem Test Send no SFMC.

## Modos de trabalho

1. **Criar:** briefing ou referência vira arquitetura, copy, HTML/AMPscript e QA.
2. **Alterar:** aplique dimensões, formatos, posições, ordem, centralização, espaçamento, cores, imagens ou responsividade ao código existente.
3. **Auditar:** diagnostique código, lógica dinâmica, acessibilidade, compatibilidade e riscos sem editar quando o usuário só pedir análise.
4. **Comparar:** use referências como repertório de padrões, não como autorização para copiar campanha, texto ou arte.
5. **Gerar headers como imagens:** quando o usuário escolher rasterização, siga [references/raster-headers.md](references/raster-headers.md). Renderize o HTML oficial com dados resolvidos, gere primeiro o piloto solicitado e mantenha publicação separada da geração local.
6. **Evoluir template dinâmico:** trate cada produto, sequência, assinatura e estado condicional como uma renderização do mesmo sistema; compare a fonte canônica com a candidata antes de promover.

## Workflow obrigatório

1. Identifique objetivo de aquisição, papel do e-mail na jornada, audiência, oferta, CTA, parceiro, assinatura, sequência e restrições.
2. Ao editar código existente, inventarie antes: blocos visuais, variáveis, lookups, condicionais, links, tracking, legal, fallbacks e dependências entre desktop/mobile.
3. Traduza o pedido em operações explícitas: `resize`, `align`, `spacing`, `reorder`, `replace`, `conditionalize`, `responsive`, `hide_when_empty`, `duplicate`, `remove` ou `outlook_fallback`.
4. Identifique a fonte visual canônica. Ela pode ser uma versão anterior, um template operacional ou uma referência aprovada; não presuma que o maior número de versão é a melhor origem.
5. Faça a menor alteração capaz de atingir o resultado. Preserve todo comportamento não solicitado.
6. Para template compartilhado, renderize todas as sequências afetadas com os mesmos dados na fonte canônica e na candidata. Não valide apenas o e-mail que motivou a mudança.
7. Audite o resultado com `python scripts/audit_email_source.py <arquivo>` quando houver arquivo HTML/AMPscript local.
8. Entregue resumo, diff ou lista de mudanças, código final, lógica preservada, matriz comparativa, diagnósticos, cenários de teste e status de prontidão.

## Leitura progressiva

- Leia [references/acquisition-brief.md](references/acquisition-brief.md) ao criar um e-mail, avaliar estratégia/copy ou quando faltarem metadados.
- Leia [references/html-ampscript-engineering.md](references/html-ampscript-engineering.md) ao criar ou alterar HTML, AMPscript, layout, responsividade, links ou personalização.
- Leia [references/qa-and-sources.md](references/qa-and-sources.md) ao auditar compatibilidade, acessibilidade, dark mode, deliverability, Test Send ou ao justificar uma regra técnica.
- Leia [references/dynamic-template-regression.md](references/dynamic-template-regression.md) por inteiro antes de alterar, comparar ou promover um template usado por mais de uma sequência, produto, assinatura ou briefing.
- Leia [references/content-blocks.md](references/content-blocks.md) sempre que receber a aba **Briefing Fábrica** (xlsx) com e-mails novos ou quando o conteúdo de um bloco precisar ficar mais atrativo. Os blocos (grade de benefícios, números em destaque, lista com check, passo a passo) saem de `scripts/content_blocks.py`, dentro dos próprios campos de texto, sem criar versão nova de template.

## Regras de alteração segura

- Não reescreva o documento inteiro quando um patch localizado resolve.
- Preserve delimitadores, nomes de variáveis, ordem de inicialização e lógica de lookup.
- Reordenar um bloco visual inclui mover sua condição AMPscript completa, não apenas o HTML interno.
- Em uma alteração de largura, especifique atributo HTML e CSS quando Outlook precisar de ambos.
- Centralização deve considerar contêiner, célula `<td>`, texto, botão e comportamento mobile; `text-align` em um ancestral pode não resolver todos.
- Bloco opcional deve ser envolvido por condição para não deixar espaço vazio.
- URL dinâmica em `href` deve preservar tracking com `RedirectTo()` quando aplicável.
- `TreatAsContent()` aceita somente conteúdo governado/revisado; nunca processe entrada livre sem sanitização ou allowlist.
- Valide rowset antes de `Row()`/`Field()` com `RowCount`, `Empty` ou `IsNull`.
- Use `RaiseError()` para falha real e explícita, não para segmentar público.
- Não exponha CPF, e-mail, telefone, chaves ou outros dados sensíveis em URL, HTML, comentário ou diagnóstico.
- O que aparece no editor, é exportado, fica salvo no Supabase e entra nos testes deve ser a mesma fonte. Override intencional precisa ser explícito e bloqueia promoção até reconciliação.
- Não torne uma versão principal se houver CTA, asset, campo, hierarquia, legal ou estado condicional perdido em relação à fonte canônica.

## HTML de e-mail

- Prefira estrutura por tabelas para layout crítico e `role="presentation"` em tabelas puramente visuais.
- Mantenha largura de leitura configurável, normalmente até 600 px, sem transformar esse número em regra universal.
- Use atributos `width`/`height` e estilos responsivos nas imagens; preserve proporção e evite upscale.
- Prefira live text para informação essencial. Quando o usuário escolher o modo de headers como imagens, título e subtítulo podem ser rasterizados com equivalente acessível; preserve personalização, CTA e legal fora da imagem.
- CSS crítico inline; `<style>` e media queries apenas dentro do suporte necessário dos clientes-alvo.
- Forneça fallback para background, fonte, botão, cantos e empilhamento quando Outlook exigir.
- Nada de JavaScript cliente, formulário ativo ou recurso web sem suporte comprovado e fallback.

## Saída mínima

```text
Objetivo e hipótese
Mudanças solicitadas e aplicadas
Blocos/variáveis/links preservados
Código ou patch final
Cenários de teste
Diagnósticos: bloqueante, revisão, informativo
Compatibilidade: Gmail, Outlook, Apple Mail, mobile, dark mode
Status: blocked | needs_review | ready_for_test_send | sfmc_certified
```

`sfmc_certified` só pode ser usado quando o usuário fornecer evidência do Test Send aprovado.

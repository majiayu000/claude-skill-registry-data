---
name: base-legal-cc
description: "Recupera e explica dispositivos do Codigo Civil (Lei 10.406/2002) sob demanda das outras skills do plugin civel — negocios juridicos, prescricao e decadencia, obrigacoes, contratos, responsabilidade civil e direitos reais. Localiza o artigo por grep em context/cc-10406-02.md, traz texto + finalidade + requisitos + excecoes, e cruza com context/cpc-cc-alteracoes-recentes.md (CC/2002 vigente; PL 4/2025 so monitorar). Use quando precisar do texto exato/vigente de um artigo do CC, ou quando o operador disser qual o art. do CC sobre X, o que diz o CC sobre prescricao/contrato/dano/posse, prazo prescricional, base legal material, fundamento de direito material, esse artigo do Codigo Civil mudou."
---

# BASE-LEGAL-CC — Recuperador de dispositivos do CC/2002

> Camada 1 (Fundacao). Fonte de verdade do direito material (CC/2002) para as demais skills. Nao redige peca: entrega o dispositivo correto, vigente e explicado.

## Anexos obrigatorios (context/)
- `context/cc-10406-02.md` — CC/2002 consolidado (~750KB). **Nunca ler inteiro:** localizar o artigo por grep e ler so a faixa.
- `context/cpc-cc-alteracoes-recentes.md` — status das reformas (confirma que o CC/2002 segue integralmente vigente; PL 4/2025 EM TRAMITACAO).
- `context/metodologia-civel.md` — quando chamada pelo `civel-master`.

## Objetivo
Devolver, para qualquer artigo/inciso/paragrafo do CC pedido: o **texto exato vigente**, a **finalidade**, os **requisitos**, as **excecoes** e a **vigencia** — sem reproduzir o codigo inteiro e sem inventar redacao.

## Quando ativar
- Outra skill (inicial, contestacao, parecer, recurso) precisa do fundamento de direito material.
- O operador pergunta qual artigo rege prescricao/decadencia, negocio juridico, obrigacao, contrato, responsabilidade civil ou direito real.
- Ha duvida sobre prazo prescricional/decadencial ou sobre a redacao vigente de um dispositivo.

## Metodologia
1. **Localizar por grep**, nunca abrir o anexo inteiro. O anexo numera artigos no padrao `Art. N`:
   - artigo conhecido: `grep -n "^Art\. 206" context/cc-10406-02.md` (ajuste o numero);
   - por tema: `grep -niE "prescricao|prescreve" context/cc-10406-02.md`.
2. **Ler so a faixa** retornada (do artigo ate o proximo `Art.`), com `Read offset/limit`. Copiar a redacao **verbatim** — nunca parafrasear como se fosse a lei.
3. **Mapas rapidos por blocos** (use o tema para o grep, depois confirme o numero no anexo):
   - **Prescricao/decadencia:** regra geral 10 anos (art. 205); prazos especiais (art. 206, §§ 1º a 5º — ex.: pretensao de reparacao civil 3 anos, cobranca 5 anos); decadencia (art. 207-211).
   - **Negocio juridico:** existencia/validade/eficacia (art. 104); defeitos (erro, dolo, coacao, estado de perigo, lesao, fraude — art. 138-165); invalidade (nulidade art. 166-167; anulabilidade art. 171).
   - **Obrigacoes:** adimplemento, mora, perdas e danos, juros (art. 389-405); clausula penal (art. 408-416).
   - **Contratos:** disposicoes gerais e funcao social (art. 421-422 boa-fe objetiva); especies (compra e venda art. 481+; locacao art. 565+).
   - **Responsabilidade civil:** ato ilicito (art. 186, 187); obrigacao de indenizar (art. 927; risco/§ unico); dano moral; responsabilidade objetiva.
   - **Direitos reais:** posse (art. 1.196+); propriedade (art. 1.228+); usucapiao (art. 1.238-1.244).
4. **Explicar em 4 blocos:** texto vigente → finalidade → requisitos/incisos → excecoes/pegadinhas.

## Entrega obrigatoria final
- Citacao do dispositivo (artigo/§/inciso) com **texto verbatim** + finalidade + requisitos + excecoes + confirmacao de vigencia + ponteiro do trecho do anexo lido. Se houver duvida de redacao, sinalizar e mandar checar — nunca preencher de memoria.

## Guard
Nenhum dispositivo entregue sem confirmar a redacao no anexo via grep. **CC/2002 esta vigente; o PL 4/2025 (Reforma do CC) esta EM TRAMITACAO — NUNCA citar como lei** (ver `cpc-cc-alteracoes-recentes.md`). Na duvida de vigencia/numero, acionar `validador-civel` e bloquear; toda peca que use isto fecha pela `suprema-corte-civel`.

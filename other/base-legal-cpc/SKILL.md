---
name: base-legal-cpc
description: "Recupera e explica dispositivos do CPC/2015 (Lei 13.105/2015) sob demanda das outras skills do plugin civel. Localiza o artigo por grep em context/cpc-13105-15.md, traz texto + finalidade + requisitos + excecoes, e cruza com context/cpc-cc-alteracoes-recentes.md para checar reformas (Lei 14.879/2024 foro art. 63; Lei 14.939/2024 feriado local art. 1.003). Use quando precisar do texto exato/vigente de um artigo do CPC, ou quando o operador disser qual o art. do CPC sobre X, o que diz o CPC sobre tutela/prazo/competencia/recurso, base legal processual, fundamento no CPC, esse artigo ainda esta em vigor."
---

# BASE-LEGAL-CPC — Recuperador de dispositivos do CPC/2015

> Camada 1 (Fundacao). Fonte de verdade do CPC para as demais skills. Nao redige peca: entrega o dispositivo correto, vigente e explicado.

## Anexos obrigatorios (context/)
- `context/cpc-13105-15.md` — CPC/2015 consolidado (~845KB). **Nunca ler inteiro:** localizar o artigo por grep e ler so a faixa.
- `context/cpc-cc-alteracoes-recentes.md` — reformas 2024-2026 (ler SEMPRE antes de citar artigo potencialmente alterado).
- `context/metodologia-civel.md` — quando chamada pelo `civel-master`.

## Objetivo
Devolver, para qualquer artigo/inciso/paragrafo do CPC pedido: o **texto exato vigente**, a **finalidade**, os **requisitos**, as **excecoes** e o **status de reforma** — sem reproduzir o codigo inteiro e sem inventar redacao.

## Quando ativar
- Outra skill (inicial, contestacao, recurso, tutela, tempestividade, competencia) precisa do dispositivo processual fundante.
- O operador pergunta qual artigo rege determinado ato/prazo/recurso, ou pede o texto literal de um art. do CPC.
- Ha duvida se um artigo esta vigente ou foi alterado por reforma recente.

## Metodologia
1. **Localizar por grep**, nunca abrir o anexo inteiro. O anexo numera artigos no padrao `Art. N.`:
   - artigo conhecido: `grep -n "^Art\. 300\." context/cpc-13105-15.md` (ajuste o numero);
   - por tema: `grep -niE "tutela de urgencia|tutela provisoria" context/cpc-13105-15.md`.
2. **Ler so a faixa** retornada (do artigo ate o proximo `Art.`), com `Read offset/limit`. Copiar a redacao **verbatim** — nunca parafrasear como se fosse a lei.
3. **Checar reforma** em `context/cpc-cc-alteracoes-recentes.md` antes de entregar. Pontos quentes confirmados (jun/2026):
   - **art. 63, §1º e §5º** — Lei 14.879/2024: foro de eleicao exige pertinencia (domicilio/residencia das partes ou local da obrigacao); juizo aleatorio = pratica abusiva, declinacao de oficio.
   - **art. 1.003, §6º** — Lei 14.939/2024: feriado local nao comprovado no ato deixou de ser intempestividade automatica — o tribunal manda corrigir o vicio (STJ Corte Especial AREsp 2.638.376, 2025).
   - **EC 136/2025 = precatorios** (CF 100/165). **NAO** altera o CPC — so reflete na execucao contra a Fazenda/precatorio.
4. **Explicar em 4 blocos:** texto vigente → finalidade → requisitos/incisos → excecoes/pegadinhas.
5. **Prazos:** sempre lembrar dias uteis (CPC 219); regra 15 dias; ED 5 dias; dobro Fazenda(183)/MP(180)/Defensoria(186)/litisconsortes(229, nao em autos eletronicos).

## Entrega obrigatoria final
- Citacao do dispositivo (artigo/§/inciso) com **texto verbatim** + finalidade + requisitos + excecoes + status de vigencia/reforma + ponteiro do trecho do anexo lido. Se houver duvida de redacao/vigencia, sinalizar e mandar checar — nunca preencher de memoria.

## Guard
Nenhum dispositivo entregue sem confirmar a redacao no anexo via grep e o status em `cpc-cc-alteracoes-recentes.md`. Na duvida de vigencia/numero, acionar `validador-civel` e bloquear; toda peca que use isto fecha pela `suprema-corte-civel`. Nunca citar o PL 4/2025 como lei.

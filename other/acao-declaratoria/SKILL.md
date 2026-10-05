---
name: acao-declaratoria
description: "Redige acao declaratoria pelo rito comum: interesse limitado a declaracao (CPC 19 - existencia, inexistencia ou modo de ser de relacao juridica; autenticidade ou falsidade de documento), admissibilidade ainda que ja ocorrida a violacao do direito (CPC 20). Declaratoria positiva x negativa; declaratoria incidental. Use quando o operador disser acao declaratoria, declarar inexistencia de debito, declarar relacao juridica, declaratoria de nulidade, ou quero que o juiz declare."
---

# ACAO-DECLARATORIA

> Camada 5 (acoes civeis). Pretensao puramente declaratoria. Cross-check OBRIGATORIO com gestao processual (Camada 2).

## Anexos obrigatorios (context/)
- `context/cpc-13105-15.md` — arts. 19 (interesse na declaracao), 20 (admissivel ainda que ocorrida a violacao) + 318-321/324 (rito comum/requisitos/pedido) — **grep + ler a faixa**.
- `context/jurisprudencia-civel.md` (so vistoriados).

## Objetivo
Acao em que o autor busca apenas a certeza juridica — declarar a existencia, a inexistencia ou o modo de ser de uma relacao, ou a autenticidade/falsidade de documento (CPC 19), sem pedir condenacao ou constituicao.

## Quando ativar
- Autor quer pronunciamento declaratorio: declaratoria positiva (existe a relacao/o direito) ou negativa (nao existe o debito/a obrigacao/a relacao).
- Discussao de autenticidade ou falsidade de documento (CPC 19, II).
- Declaratoria incidental sobre questao prejudicial controvertida.

## Metodologia
1. **Gestao processual SEMPRE (Camada 2) antes de redigir:** `competencia-e-foro` · `valor-da-causa` · `gratuidade-e-impugnacao` (se hipossuficiente) · `tempestividade-civel` (se houver prazo).
2. **Interesse de agir declaratorio (CPC 19):** limitar a pretensao a (I) existencia, inexistencia ou modo de ser de relacao juridica; ou (II) autenticidade ou falsidade de documento. Demonstrar a duvida objetiva/crise de certeza que justifica o provimento.
3. **Cabimento mesmo apos a violacao (CPC 20):** a declaratoria e admissivel ainda que ja tenha ocorrido a violacao do direito — registrar isso quando a parte contraria alegar falta de interesse por ja existir lesao.
4. **Positiva x negativa:** definir o sinal do pedido (declarar que existe / declarar que NAO existe — ex.: inexistencia de debito). Pedido certo e determinado (324).
5. **Tutela provisoria se cabivel:** cross-link `tutela-urgencia` ou `tutela-evidencia` (ex.: suspender negativacao enquanto se declara a inexistencia do debito).
6. **Instruir** com documentos da relacao juridica discutida e antecipar o controle (330/332).

## Entrega obrigatoria final
- Inicial declaratoria ponta a ponta (cabeca + fatos + crise de certeza + direito + pedido declaratorio positivo/negativo + valor + provas + opcao 334) + checklist de documentos + foro/vara.

## Guard
Nenhum dispositivo/jurisprudencia sem `validador-civel`. Gestao processual transversal obrigatoria. Entrega pela `suprema-corte-civel`. Cross-link, nao duplicar: se houver pedido de cobranca de credito sem titulo -> `cobranca-e-monitoria`; execucao -> `execucao-adv-os`.

---
name: penhora-e-expropriacao
description: "Conduz a penhora e a expropriacao na execucao/cumprimento — regra geral (CPC 831), bens impenhoraveis (CPC 833), ordem preferencial com dinheiro em 1o (CPC 835), meios eletronicos base de SISBAJUD/RENAJUD/INFOJUD (CPC 837), penhora de dinheiro via SISBAJUD com indisponibilidade + 24h + manifestacao do executado em 5 dias (CPC 854), avaliacao (CPC 838-869), adjudicacao (CPC 876), alienacao por iniciativa particular e em leilao judicial (CPC 879-903). Use quando o operador disser penhora, penhorar bens, SISBAJUD, RENAJUD, bloqueio de valores, expropriacao, leilao judicial, bem impenhoravel."
---

# PENHORA-E-EXPROPRIACAO

> Camada 7 (cumprimento & execucao). Constricao patrimonial e conversao do bem em dinheiro. Da a base civel; o leilao pesado e a recuperacao de credito complexa vivem em `execucao-adv-os`. Cross-check OBRIGATORIO com gestao processual (Camada 2).

## Anexos obrigatorios (context/)
- `context/cpc-13105-15.md` — arts. 831 (regra geral), 833 (impenhoraveis — incisos), 835 (ordem; dinheiro inciso I, § 1o prioridade), 837 (meios eletronicos), 854 (SISBAJUD — § 1o 24h, § 3o manifestacao em 5 dias, § 5o conversao), 838-869 (auto/deposito/avaliacao), 876 (adjudicacao), 879-880 (iniciativa particular), 881-903 (leilao) — **grep + ler a faixa**.
- `context/jurisprudencia-civel.md` (so vistoriados).

## Objetivo
Constringir bens suficientes, na ordem legal, sem violar impenhorabilidade, e levar o bem a expropriacao (adjudicacao, alienacao particular ou leilao) sem nulidade.

## Quando ativar
- Decorrido o prazo de pagamento sem adimplemento — penhorar.
- Localizar ativos (dinheiro, veiculos, imoveis) e/ou requerer expropriacao.
- Executado alega impenhorabilidade ou pede substituicao do bem.

## Metodologia
1. **Gestao processual (Camada 2):** `competencia-e-foro` (juizo da execucao) ; debito atualizado -> `calculosjudiciais-adv-os` ; `tempestividade-civel`.
2. **Regra geral (CPC 831):** penhora recai sobre tantos bens quantos bastem para principal atualizado, juros, custas e honorarios — sem excesso.
3. **Ordem preferencial (CPC 835):** dinheiro (I), titulos, veiculos (IV), imoveis (V), moveis e seguintes. § 1o: dinheiro e **prioritario**, podendo o juiz alterar a ordem nas demais. § 2o: fianca bancaria e seguro garantia equiparam-se a dinheiro se nao inferior ao debito + 30%.
4. **Filtrar impenhoraveis (CPC 833):** salario/proventos (IV), bens da residencia (II), instrumentos da profissao (V), poupanca ate 40 salarios-minimos (X), pequena propriedade rural trabalhada pela familia (VIII). Conferir § 1o (divida do proprio bem) e § 2o (excecao da prestacao alimenticia e de valores acima de 50 salarios-minimos).
5. **Meios eletronicos (CPC 837):** dinheiro e averbacoes podem ser feitos por meio eletronico — base de SISBAJUD (ativos), RENAJUD (veiculos) e INFOJUD (dados fiscais). Sao **sistemas**; o fundamento e o 837 e, para dinheiro, o 854.
6. **SISBAJUD (CPC 854):** a requerimento, sem ciencia previa, o juiz torna indisponiveis ativos ate o valor da execucao; em 24h cancela o excesso (§ 1o); o executado tem **5 dias** para comprovar impenhorabilidade/excesso (§ 3o); rejeitada ou silente a manifestacao, converte-se em penhora (§ 5o).
7. **Documentar e avaliar:** penhora por auto/termo (838); avaliacao pelo oficial (870), salvo 871.
8. **Expropriar:** (a) **adjudicacao** pelo exequente por preco nao inferior a avaliacao (876, prazo de 5 dias da ultima intimacao); (b) **alienacao por iniciativa particular** (879 I e 880); (c) **leilao judicial** eletronico ou presencial (879 II e 881-903) — detalhe pesado em `execucao-adv-os`.

## Entrega obrigatoria final
- Peticao redigida (penhora na ordem do 835, ou SISBAJUD/RENAJUD/INFOJUD via 837/854, ou expropriacao) + debito atualizado + checklist de impenhorabilidade (833) + indicacao do bem e do meio.

## Guard
Nenhum dispositivo/jurisprudencia sem `validador-civel`. Gestao processual transversal obrigatoria (Camada 2). Entrega pela `suprema-corte-civel` (R1-R4). Cross-link, nao duplicar: leilao/arrematacao/recuperacao de credito complexa -> `execucao-adv-os`; atualizacao/juros -> `calculosjudiciais-adv-os`.

---
name: conselho-de-vendas
description: Use para criar, avaliar ou precificar uma oferta. Russell Brunson, Alex Hormozi e Dan Kennedy propõem 3 ofertas, votam uns nas dos outros por parâmetros e o motor elege a oferta campeã.
---

# Conselho de vendas: Brunson, Hormozi e Kennedy

Três agentes com papéis diferentes discutem oferta e preço por **parâmetros**, não por opinião:

| Agente | Papel no duelo | Régua principal |
|---|---|---|
| `ultra-brunson` | **Arquitetura:** escada de valor, funil, pilha antes do preço, bump e oferta única depois da compra | nova oportunidade × melhoria, gancho-história-oferta |
| `ultra-hormozi` | **Valor:** equação de valor, garantia forte, nome MAGIC, oferta de atração que paga a aquisição | (resultado × probabilidade) ÷ (tempo × esforço) |
| `ultra-kennedy` | **Preço:** âncora, 3 níveis com premium, forma de pagamento do mercado, motivo e prazo, follow-up | preço é posicionamento; nunca o mais barato sem vantagem de custo |

Os critérios ficam nas bibliotecas `oferta` (12 critérios) e `preco` (11), em `~/.ultra-skills/params/criterios/`.

## Como rodar

1. **Material.** Rode o scan da página da oferta e de 3 a 5 concorrentes (skill `scan-ultra`, ou `ultra.py iniciar URL --concorrentes ...`). Junte o que a pessoa disser: custo, margem, capacidade de entrega, público, Brasil ou fora.
2. **Rodada 1, propostas (em paralelo).** Cada agente avalia a oferta atual com os próprios critérios e propõe **uma** oferta nova no `formato_oferta`, com id `of-brunson`, `of-hormozi` ou `of-kennedy`. As três precisam ser diferentes entre si: cada um puxa pelo próprio papel.
3. **Rodada 2, votação cruzada (em paralelo).** Cada agente lê as 3 ofertas e dá nota de 0 a 10 a cada uma (inclusive a sua) em cada critério `oferta.*` e `preco.*`, no campo `votos`, dizendo o que roubaria de cada.
4. **Duelo.**
   ```bash
   python3 ~/.ultra-skills/ultra.py duelo PASTA/04-vendas
   ```
   O motor calcula a nota ponderada pelos pesos dos critérios. O **autovoto não conta** no ranking. Ele aponta a vencedora e o **melhor componente por critério**, isto é, de qual oferta vem a melhor garantia, a melhor âncora, e assim por diante.
5. **Oferta campeã.** O autor da vencedora monta a versão híbrida com os melhores componentes e escreve as 3 ofertas por público (primário, secundário e terciário) em `04-vendas/r3/oferta-campea.json`.

Dentro da análise completa, o `ultra.py proximo` conduz essas rodadas sozinho. Fora dela, crie a pasta `04-vendas/r1` e `r2` e salve os JSON lá.

## O que entregar

- A oferta campeã: promessa, pilha com valor de cada peça, preço com âncora, níveis, parcelas, garantia (como pedir), urgência com motivo real e escada (bump, oferta única, recorrência).
- A tabela do duelo e por que a vencedora ganhou.
- As 3 ofertas por público, com headline.
- O teste de preço: o que comparar, a métrica, o volume mínimo e o prazo.

## Regras

- Valem as regras e a escada de evidência da `pare-de-pensar-como-ia`.
- Escassez, urgência e garantia **só se forem reais**. Inventar custa reembolso, chargeback e conta de anúncio.
- No Brasil, 7 dias de arrependimento é lei (CDC, art. 49): não conta como garantia.
- Nada de frase entre aspas na boca de Brunson, Hormozi ou Kennedy. Eles raciocinam pela régua deles.

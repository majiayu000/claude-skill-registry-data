---
name: auditor-de-tarifas
description: >-
  Responde "quanto seu banco te cobrou de tarifa esse ano?". A pessoa informa onde está o extrato
  (OFX/CSV) e o motor Python soma as tarifas (manutenção, TED/DOC, Pix PJ, boleto,
  custódia, câmbio) por banco, mês e tipo, com o IOF separado (imposto, não tarifa).
  No Claude Code em sessão local, a skill foi feita para o Claude ler só o
  resumo agregado (totais), não o lançamento individual. Use quando a pessoa quiser
  auditar/somar as tarifas do banco no Brasil.
---

# Auditor de Tarifas Bancárias, Finance AI Lab

Ferramenta de custo bancário: soma as tarifas do extrato e mostra o total do ano.

Ninguém sabe quanto paga de tarifa por ano porque ela vem picada: R$12,90 de manutenção aqui, R$10,90 de um TED ali, R$2,90 de um boleto acolá. Cada linha é pequena demais pra doer. Somado em 12 meses, não. Esta ferramenta soma, separa o que é **tarifa** (negociável) do que é **imposto** (IOF), e devolve o número que vira argumento pra renegociar a cesta ou portar o relacionamento.

> Rascunho operacional: a decisão e a revisão são do profissional responsável.

## Contrato de privacidade, por plataforma

O que vale depende de onde a conversa roda. Diga isso à pessoa, sem prometer o que a plataforma não entrega.

- **No terminal ou no Claude Code em sessão local:** o motor lê o extrato no disco e você lê só o resumo agregado: peça o caminho do arquivo, não peça para ela colar ou anexar o conteúdo e não abra o arquivo bruto. O motor Python classifica e soma **localmente** e, com `--saida`, grava um CSV no disco dela só com as linhas que classificou como tarifa ou IOF. Para você (Claude) sobe só o **resumo agregado** (total de tarifa, quebra por banco/mês/tipo, contagem de não-classificados). Na tabela por banco, o banco aparece pelo código numérico do arquivo (até 4 dígitos, do BANKID do OFX ou da coluna `banco` do CSV); nome ou outro texto vira `banco 1`, `banco 2`, e o CSV do `--saida` traz o rótulo original. Um aviso de linha ilegível diz só o arquivo e o número da linha, nunca o conteúdo dela. **Nenhum lançamento individual** com valor e contraparte aparece no stdout lido por você. Se a pessoa quiser ver linha a linha, oriente-a a abrir o CSV local (`--saida`). Você não abre o CSV do `--saida`: ele traz cada lançamento com descrição e valor. Se a pessoa pedir que você confira, lembre que o que você abrir vai para a Anthropic e deixe a decisão com ela. O pedido dela, esse resumo e qualquer arquivo que você abrir vão para a Anthropic.
- **No Cowork ou numa conversa comum do Claude (web ou app):** o arquivo está na nuvem da Anthropic: avise a pessoa antes de ela anexar ou de abrir a tarefa, em vez de dizer que nada sobe, e sugira o terminal, o Claude Code em sessão local ou anonimizar o extrato.

## O que faz (e o que não faz)

Faz: soma **só a tarifa** (não categoriza o resto do extrato), separa o IOF, mostra por banco, por mês e por tipo, e aponta os lançamentos que não reconheceu (transparência, não esconde).

Não faz: **não categoriza tudo**, **não concilia**, **não renegocia** por você (orienta as duas jogadas), **não compara bancos** (audita o que já te cobraram). Não trata juros (cheque especial, antecipação) como tarifa.

## Como usar

O motor é o `scripts/auditar_tarifas.py`. A pessoa exporta o extrato do ano (OFX ou CSV, um por conta) e roda:

```
python scripts/auditar_tarifas.py <extrato.ofx> [<extrato2.csv> ...] [--ano 2025] [--saida auditoria.csv]
```

- Entrada: um ou mais extratos OFX/CSV, ou um diretório.
- `--ano`: filtra um ano-calendário (o total anual é o número que choca).
- `--saida`: grava o CSV **local** classificado (`data, descricao, valor, banco, tipo`) pra conferência linha a linha. Não sai no stdout.

O stdout traz **só o resumo seguro**: total anual de tarifa, tabela por banco, por mês, por tipo, o total de IOF à parte, o veredicto e quantos lançamentos ficaram pra conferir.

Há um extrato fictício em `exemplo/extrato_341.ofx` para testar.

## Fluxo que você (Claude) conduz

1. Peça o caminho do extrato do período (OFX de preferência; CSV serve), não o conteúdo. Explique que é **um arquivo por conta** e diga o que acontece com o arquivo na plataforma em que a conversa roda (veja o contrato de privacidade acima).
2. Rode o motor. Leia **só o resumo**.
3. Apresente o número anual, a quebra por tipo (quase sempre manutenção e boleto lideram) e o mês fora da curva, se houver.
4. Aponte as **duas jogadas** com o número na mão:
   - **Renegociar a cesta.** Tarifa PJ é livre; o gerente tem margem. A frase que abre desconto: "paguei R$ X de tarifa esse ano, R$ Y só na cesta".
   - **Portar o relacionamento.** Se o banco não mexer, a portabilidade existe. O número anual torna a decisão fácil.
5. Se o veredicto for `CONFERIR`, avise que há lançamentos não reconhecidos e oriente a pessoa a abrir o CSV local (você não abre) antes de fechar o número.
6. Se o motor avisar `arquivo ilegivel ignorado` ou `nao foi possivel ler`, diga que o total não inclui aquele arquivo (pelo nome que o aviso traz) e peça outro export dele antes de fechar o número.

## Veredictos

- `OK`: somou, nada pendente relevante.
- `CONFERIR`: há lançamentos com marca de tarifa que não caíram em nenhuma categoria (aparecem como `outra_tarifa`); confira o CSV local antes de confiar 100% na quebra por tipo. O total ainda vale.
- `SEM TARIFA ENCONTRADA`: o extrato não tinha termo de tarifa reconhecível (conta isenta, ou nome fora do dicionário). Nunca inventa um número.
- `NADA LIDO`: o motor não leu nenhum lançamento (formato, colunas ou `--ano` fora do período). Repasse os avisos e peça outro export; nunca trate como conta sem tarifa.

## Honestidade

Somar tarifa é algo que uma planilha faz, desde que você tenha o dicionário de termos certo (que é o trabalho chato, e é o que esta ferramenta entrega pronto). Não é um robô que adivinha; é um dicionário de termos de tarifa BR + uma soma determinística. Para o extrato só em **PDF**, ou pra categorizar **tudo** (não só tarifa) e conciliar, esta ferramenta não serve.

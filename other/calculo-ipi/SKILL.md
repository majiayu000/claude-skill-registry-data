---
name: calculo-ipi"
description: Calcula IPI nas operações de saída industrial e de equiparados a industrial, aplica TIPI 2022, identifica suspensão e isenção, e gerencia o crédito presumido de exportação.
allowed-tools: Read Grep Bash Edit Write
user-invocable: true
---

> ⚠️ **AVISO FISCAL — CONFIRA ANTES DE GERAR A GUIA.** Todo código de receita (DARF/DAS), alíquota, base de cálculo, valor e data de vencimento gerado por este agente é **rascunho de apoio** e pode variar por ano, regime tributário, município ou caso específico. **Confira sempre na fonte oficial vigente (Receita Federal / e-CAC / legislação estadual e municipal) antes de transmitir declaração ou pagar guia.** A conferência final é responsabilidade do contador responsável.

## Quando usar

Estabelecimentos industriais (que executam operação de industrialização — transformação, beneficiamento, montagem, acondicionamento, renovação) ou equiparados a industrial (importadores, atacadistas em operações específicas). Apuração mensal, vencimento dia 25 do mês subsequente.

## Inputs necessários

1. NCM do produto (TIPI 2022 — Decreto 11.158/2022, atualizada por decretos seguintes)
2. CST de IPI (00 entrada com crédito, 49 outras saídas, 50 saída tributada, 99 outras)
3. Valor da operação (incluindo frete e despesas — base tributável)
4. Operação suspensa? (regime aduaneiro especial, drawback, RECOF)
5. Empresa enquadrada em Zona Franca, ALC ou IPI reduzido por incentivo regional?
6. Há devolução, retorno ou industrialização por encomenda?

## Cálculo

```
IPI = Base × Alíquota TIPI

Base = Valor da operação + frete + seguro + outras despesas
       (não inclui ICMS — IPI é "por fora")
```

### Apuração mensal (regime de competência)

```
IPI a recolher = Σ IPI saídas tributadas − Σ IPI entradas com crédito
```

- Crédito: na entrada de insumos/MP/embalagens que serão industrializados, mesmo que o fornecedor seja optante do Simples (vedado crédito do Simples salvo exceção).
- Saída suspensa não gera obrigação, mas mantém créditos da entrada (princípio da não-cumulatividade).

### Operações típicas

| Operação | CFOP | IPI |
|---|---|---|
| Venda produção interna | 5.101/6.101 | Tributada |
| Industrialização por encomenda (encomendante) | 5.901/6.901 | Suspenso |
| Industrialização por encomenda (industrializador) | 5.124/6.124 | Suspenso na devolução, tributado no valor agregado da MO |
| Exportação direta | 7.101 | Imune (CF art. 153 §3º III) + crédito presumido |
| Drawback | 5.501/6.501 | Suspenso |

## Crédito presumido de exportação (Lei 9.363/96)

Compensação de PIS/COFINS na cadeia, calculado sobre exportações. Aplicação:
```
Crédito presumido = (Receita exportação / Receita operacional total) × Insumos × 5,37%
```

Ou, na sistemática alternativa (Lei 10.276/2001), conforme escolha da empresa.

Aproveitar em IPI a pagar do mês ou pedir ressarcimento (PER/DCOMP).

## Templates

```
APURAÇÃO IPI — MM/AAAA
ENTRADAS COM CRÉDITO:
  NF ____ NCM ____ Base R$_____ × ___% = R$_____
  ...
  Total créditos.................. R$ _________

SAÍDAS TRIBUTADAS:
  NF ____ NCM ____ Base R$_____ × ___% = R$_____
  ...
  Total débitos................... R$ _________

(=) IPI A RECOLHER (ou saldo credor) ......... R$ _________
DARF código 5123 (geral) — venc. dia 25
```

### Exemplo

- Saídas tributadas no mês: IPI total débito R$ 18.000.
- Entradas tributadas: IPI total crédito R$ 12.500.
- Saldo a pagar = R$ 5.500 via DARF 5123.

## Erros comuns

- Calcular IPI "por dentro" (ele é por fora — não compõe a própria base, mas integra a base do ICMS quando o destinatário é não-contribuinte).
- Esquecer de tomar crédito de IPI das entradas (a empresa é não-cumulativa por natureza).
- Usar TIPI desatualizada — sempre conferir decretos vigentes.
- Tratar como suspensão o que é isenção (suspensão exige cumprimento de condição posterior; isenção é definitiva).
- Não escriturar adequadamente a industrialização por encomenda — autuação por falta de IPI na operação principal.
- Dupla escrituração de crédito presumido (na DCTF e na EFD-Contribuições).

## Checklist

- [ ] NCM e alíquota da TIPI vigente conferidos
- [ ] Base sem ICMS, com frete/seguro/despesas
- [ ] CSTs corretos (saída e entrada)
- [ ] Suspensão/isenção com base legal documentada
- [ ] EFD ICMS/IPI: registros E520, E530 conferindo
- [ ] DCTFWeb com IPI (código 5123) batendo apuração
- [ ] Estoque físico × estoque fiscal: divergência apurada

## Referências

- Decreto 7.212/2010 (RIPI)
- Decreto 11.158/2022 (TIPI 2022)
- Lei 4.502/64 (norma matriz IPI)
- Lei 9.363/96 (crédito presumido)
- IN RFB 2.121/2022 (PIS/COFINS — relacionada via não-cumulatividade)

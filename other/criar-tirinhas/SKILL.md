---
name: criar-tirinhas
description: >
  Protocolo "Criar Tirinhas" da empresa 3S-001. Transforma planilhas medicas (.xlsx)
  com abas de Cranio (Neuro) e Coluna em um .xlsx separado por medico, todos dentro
  de uma pasta chamada "tirinhas/" criada automaticamente. Cada arquivo tem o nome do
  medico e contem UMA UNICA aba com todas as cirurgias combinadas (cranio + coluna),
  finalizada com linha de Total e Taxa (20% — nunca chamada de "comissao").
  Usar sempre que o usuario mencionar: "criar tirinhas", "tirinhas", "protocolo tirinhas",
  "gerar tirinhas", "tirinha por medico", "separar por medico", ou ao processar planilha
  de cirurgias cranio/coluna. Empresa padrao: 3S-001.
---

# Protocolo: Criar Tirinhas — 3S-001

## O que e uma tirinha

Uma tirinha e um **bloco** dentro de um xlsx unico do mes, contendo todas as
cirurgias de um medico naquele periodo. Cada bloco tem o seu proprio header,
suas linhas de cirurgia, separador e linha TOTAL.

## Saida esperada

```
<pasta_da_empresa>/
└── Tirinhas_LCOSTA_<Mes>_<Ano>.xlsx   (1 unico arquivo por mes)
```

O xlsx tem **uma unica aba "Tirinhas"** contendo todos os medicos como blocos
empilhados, separados por uma **linha em branco** entre cada bloco:

```
[BLOCO MEDICO 1]
HEADER  | Empresa | Data | Paciente | Hospital | Valor | Taxa
linha 1 ...
linha 2 ...
separador
TOTAL                                              valor   taxa
(linha em branco)

[BLOCO MEDICO 2]
HEADER  | Empresa | Data | Paciente | Hospital | Valor | Taxa
...
```

- Linhas de **Cranio** primeiro, depois **Coluna**, dentro de cada bloco
- Se o medico so tem cirurgias de uma especialidade, mostra apenas essas
- Cada bloco tem sua propria linha **Total** com Valor + Taxa
- Os medicos aparecem em ordem alfabetica

> A coluna de taxa por linha se chama **"Taxa (20%)"** (ou apenas **"Taxa"** quando o medico tem override de aliquota) — nunca "comissao".
> A linha **TOTAL** no rodape de cada bloco totaliza tanto a coluna de Valor quanto a de Taxa.

---

## Passo 1 — Localizar o arquivo de entrada

O usuario indica um `.xlsx`. Se nao indicar, verificar o workspace por arquivos recentes.
Extrair periodo (ex: "03.2026" → "Marco 2026") e UF do nome do arquivo.

---

## Passo 2 — Detectar abas

```bash
python3 <skill_dir>/scripts/gerar_tirinhas.py --detect --input <caminho>
```

- **Cranio/Neuro**: aba com "Neuro", "Cranio" no nome
- **Coluna**: aba com "Coluna" no nome
- Usar `--cranio-tab` e `--coluna-tab` para forcar manualmente

---

## Passo 3 — Gerar as tirinhas (xlsx + pdf)

Sempre gerar **as duas saidas** (xlsx para edicao, pdf paisagem A4 para impressao):

```bash
python3 <skill_dir>/scripts/gerar_tirinhas.py \
  --input   <caminho_xlsx> \
  --output  "<pasta_da_empresa>/Tirinhas_LCOSTA_<Mes>_<Ano>.xlsx" \
  --empresa "L.COSTA"

python3 <skill_dir>/scripts/gerar_tirinhas_pdf.py \
  --input   <caminho_xlsx> \
  --output  "<pasta_da_empresa>/Tirinhas_LCOSTA_<Mes>_<Ano>.pdf" \
  --empresa "L.COSTA"
```

**XLSX:** 1 unico arquivo, todos os medicos como blocos empilhados separados
por linha em branco. Sobrescreve se ja existir.

**PDF:** mesmo conteudo em paisagem A4 (842x595pt) com margens de 15mm.
Cada bloco tenta caber em 1 pagina (KeepTogether). Se um bloco for maior que
uma pagina, parte automaticamente e o header se repete no topo (repeatRows=1).
Cores fieis ao xlsx (paleta amarela).

---

## Passo 4 — Entregar

Informar ao usuario:
- Quantos blocos foram gerados (quantos medicos)
- Volume total e taxa total
- Caminho do xlsx gerado

Nao e necessario listar todos os blocos — so o resumo.

---

## Configuracoes padrao

| Parametro             | Valor                                              |
|-----------------------|----------------------------------------------------|
| Empresa               | L.COSTA (3S-001 = código interno)                  |
| Taxa (repasse medico) | 20% sobre o valor da cirurgia (pos-desconto)       |
| Nome linha taxa       | Taxa (20%) — nunca "comissao"                      |
| Escopo                | Todos medicos                                      |
| Formato de data       | dd/mm/yyyy                                         |
| Moeda                 | R$ (BRL)                                           |
| Coluna classificacao  | CLASSIFICACAO (valores: ELETIVA, URGENCIA, EMERGENCIA) |
| Desconto URGENCIA     | 10% silencioso (reduz o VALOR antes do calculo da Taxa) |
| Desconto EMERGENCIA   | 10% silencioso (reduz o VALOR antes do calculo da Taxa) |
| ELETIVA               | Sem desconto                                       |

## Regras de calculo

1. Ler valor da cirurgia (coluna `TOTAL GERAL - DESCONTO` ou equivalente).
2. Se a coluna `CLASSIFICACAO` da linha for `URGENCIA` ou `EMERGENCIA`, multiplicar o valor por 0,90 (10% de desconto silencioso — sem coluna extra na tira).
3. A coluna `TAXA (20%)` da tira e o repasse ao medico = valor (ja com desconto se for o caso) x 0,20.
4. Total da tira = soma dos valores ja com desconto aplicado.

## Overrides de taxa por medico

Algumas tirinhas usam taxa diferente de 20% em uma especialidade especifica.
Quando isso acontece o cabecalho da coluna na tira fica como **"TAXA"** (sem o "(20%)") para sinalizar que ha mistura de aliquotas.

| Medico                          | Especialidade | Taxa  |
|---------------------------------|---------------|-------|
| Juliano Berteli de Figueiredo   | Coluna        | 25%   |
| Juliano Berteli de Figueiredo   | Cranio        | 20% (default) |
| Edson Vargas de Oliveira Netto  | Coluna        | 25%   |
| Edson Vargas de Oliveira Netto  | Cranio        | 20% (default) |

Para adicionar novos overrides, editar `TAXA_OVERRIDE` em `scripts/gerar_tirinhas.py`.

---

## Comissoes dos vendedores (script separado)

Alem das tirinhas (medicos), a skill tambem gera as **comissoes dos vendedores**
em um xlsx unico consolidado.

```bash
python3 <skill_dir>/scripts/gerar_comissoes.py \
  --input  "<caminho_xlsx_origem>" \
  --output "<caminho_xlsx_destino>"
```

### Regras

| Regra                                                            | Valor |
|------------------------------------------------------------------|-------|
| Comissao default                                                 | 4%    |
| Comissao em cirurgias de COLUNA do Juliano Berteli               | 3,5%  |
| Comissao em cirurgias de COLUNA do Edson Vargas de Oliveira Netto| 3,5%  |
| Base de calculo                                                  | VALOR CHEIO da cirurgia (coluna `TOTAL` / `Total Geral verificado`) — **antes** de qualquer desconto, inclusive o de URGENCIA/EMERGENCIA |

### Identificacao do vendedor

Vem da coluna `AGENTE CORRETO` (ou `AGENTE`). O script remove o prefixo `CONTRACTOR - `
e procura o nome em `VENDORS`. Vendedores conhecidos:

- Saint Clair Barbosa de Oliveira
- Luiz Henrique Castilho Viana de Castilho

Para adicionar mais vendedores, editar `VENDORS` em `scripts/gerar_comissoes.py`.

### Saida

- Um arquivo .xlsx unico
- Uma aba por vendedor (nome canonico do vendedor como nome da aba)
- Aba `SEM AGENTE` se houver linhas sem AGENTE preenchido (sem calculo de comissao)
- Cada aba: Vendedor | Data | Medico | Paciente | Hospital | Especialidade | Valor (cheio) | Comissao
- Linha TOTAL no rodape com soma de Valor e Comissao
- **A palavra "comissao" e usada apenas para vendedores** — nunca para medicos (medicos = "Taxa")

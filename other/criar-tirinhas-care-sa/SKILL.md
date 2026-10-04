---
name: criar-tirinhas-care-sa
description: >
  Protocolo "Criar Tirinhas" da empresa CARE SA. Transforma planilhas medicas (.xlsx)
  com abas de Cranio (Neuro) e Coluna em um .xlsx separado por medico, todos dentro
  de uma pasta chamada "tirinhas/" criada automaticamente. Cada arquivo tem o nome do
  medico e contem UMA UNICA aba com todas as cirurgias combinadas (cranio + coluna),
  finalizada com linha de Total e Taxa (20% padrao, com overrides para Gustavo Adolpho
  Cannabrava Carvalho e Silas Augusto Faria Martins). Usar sempre que o usuario
  mencionar: "criar tirinhas care sa", "tirinhas care sa", "gerar tirinhas care sa",
  ou ao processar planilha CARE SA - MM.YYYY N.xlsx. Empresa: CARE SA.
---

# Protocolo: Criar Tirinhas — CARE SA

## O que e uma tirinha

Uma tirinha e um **bloco** dentro de um xlsx unico do mes, contendo todas as
cirurgias de um medico naquele periodo. Cada bloco tem o seu proprio header,
suas linhas de cirurgia, separador e linha TOTAL.

## Saida esperada

```
<pasta_da_empresa>/
└── Tirinhas_CARE_SA_<Mes>_<Ano>.xlsx   (1 unico arquivo por mes)
```

O xlsx tem **uma unica aba "Tirinhas"** contendo todos os medicos como blocos
empilhados, separados por uma **linha em branco** entre cada bloco:

```
[BLOCO MEDICO 1]
HEADER  | Empresa | Data | Paciente | Hospital | Valor | Taxa
linha 1 ...
separador
TOTAL                                              valor   taxa
(linha em branco)

[BLOCO MEDICO 2]
HEADER  | ...
```

- Linhas de **Cranio** primeiro, depois **Coluna**, dentro de cada bloco
- Se o medico so tem cirurgias de uma especialidade, mostra apenas essas
- Cada bloco tem sua propria linha **Total** com Valor + Taxa
- Os medicos aparecem em ordem alfabetica

> A coluna de taxa por linha se chama **"Taxa (20%)"** quando todas as linhas usam
> a aliquota padrao, ou **"Taxa"** (sem o "(20%)") quando ha mistura de aliquotas
> por causa de override.
> A linha **TOTAL** no rodape de cada bloco totaliza tanto a coluna de Valor
> quanto a de Taxa.

---

## Empresa de referencia

CARE SA. Dono: **Fabio Paes de Sa**. Empresa irma da L.COSTA (3S-001), que tem sua
propria skill `criar-tirinhas` separada. As regras sao SEMELHANTES mas tem
overrides especificos da CARE SA — sempre usar esta skill para planilhas
`CARE SA - MM.YYYY N.xlsx`.

## Regras de calculo

### Base de tudo

Para cada linha de cirurgia, a **base bruta** = `TOTAL GERAL - DESCONTO` da planilha
de origem.

### Taxa (medico)

```
se classificacao IN ('URGÊNCIA', 'EMERGÊNCIA'):
    base_medico = base_bruta * 0.90        # -10% silencioso
senao:
    base_medico = base_bruta

taxa = base_medico * aliquota_medico
```

| Caso                                                        | Aliquota |
|-------------------------------------------------------------|----------|
| Padrao                                                      | 20%      |
| Gustavo Adolpho Cannabrava Carvalho — Neuro (Cranio)        | 20,88%   |
| Gustavo Adolpho Cannabrava Carvalho — Coluna                | 25,05%   |
| Silas Augusto Faria Martins — Neuro (Cranio)                | 13%      |
| Silas Augusto Faria Martins — Coluna                        | 15%      |

(Juliano Berteli de Figueiredo NAO atua na CARE SA — sem override aqui.)

### Comissao (agente)

```
base_agente = base_bruta                   # NAO leva o -10% silencioso
comissao = base_agente * aliquota_agente
```

| Agente                   | Medico-gatilho                          | Aliquota |
|--------------------------|-----------------------------------------|----------|
| Padrao (qualquer agente) | qualquer medico                         | 4%       |
| Simoni Coutinho          | Gustavo Adolpho Cannabrava Carvalho     | 2%       |

(Gustavo Adolpho e **medico**, nao agente. O override so dispara quando o agente
e a Simoni **E** o medico e o Gustavo. Em qualquer outra cirurgia da Simoni
— outros medicos — a comissao e 4% padrao.)

### Agentes "fantasma" — comissao paralela (controle interno)

Alguns agentes nao aparecem na coluna `AGENTE` da planilha SPI, mas recebem
comissao derivada da TAXA DO MEDICO. Isso NAO substitui a comissao do agente
oficial — sao linhas paralelas, geradas em background e usadas APENAS para
controle interno do Henrique.

| Agente fantasma                       | Medico-gatilho                        | Especialidade | % sobre Taxa do medico |
|---------------------------------------|---------------------------------------|---------------|------------------------|
| Leonardo Vilhena (controle interno)   | Silas Augusto Faria Martins           | Cranio        | 7,88%                  |
| Leonardo Vilhena (controle interno)   | Silas Augusto Faria Martins           | Coluna        | 10,05%                 |

Exemplo Cranio (Silas, base bruta R$ 100.000):
- Taxa do medico (13%)        = R$ 13.000
- Comissao Leonardo (7,88% s/Taxa) = R$ 13.000 × 7,88% = **R$ 1.024,40**

Exemplo Coluna (Silas, base bruta R$ 100.000):
- Taxa do medico (15%)        = R$ 15.000
- Comissao Leonardo (10,05% s/Taxa) = R$ 15.000 × 10,05% = **R$ 1.507,50**

A aba `Leonardo Vilhena (controle interno)` aparece no `Comissoes_<Mes>_<Ano>.xlsx`
mas o nome explicita que e controle interno — nao e entregue ao Leonardo nem
ao medico. Em paralelo, o agente oficial (Simoni) continua recebendo seus 4%
normais sobre o liquido das mesmas cirurgias.

### Bonus 0,5% (apenas Fabio Paes de Sa, pago pela CARE SA)

```
soma_2_empresas = soma_base_bruta(CARE SA mes) + soma_base_bruta(L.COSTA mes)
bonus_fabio    = 0.5% * soma_2_empresas
```

A base do bonus do dono e o **faturamento somado das duas empresas no mes** —
operacao consolidada — independentemente de quais cirurgias o Fabio fechou
pessoalmente. Pago pela CARE SA na planilha de comissoes dela.

(Em paralelo, a L.COSTA paga o mesmo calculo para o Luiz Henrique Castilho,
em sua propria planilha de comissoes.)

Apresentacao na planilha de comissoes: colunas separadas `Comissao (4%)` e
`Bonus (0,5%)`, sem fundir.

---

## Passo 1 — Localizar o arquivo de entrada

O usuario indica um `.xlsx`. Padrao do nome: `CARE SA - MM.YYYY N.xlsx`.
Se nao indicar, verificar o workspace por arquivos recentes. Extrair periodo
(ex: "04.2026" → "Abril 2026") do nome do arquivo.

---

## Passo 2 — Detectar abas

```bash
python3 <skill_dir>/scripts/gerar_tirinhas.py --detect --input <caminho>
```

- **Cranio/Neuro**: aba com "Neuro" ou "Cranio" no nome (operacional: `SPI RJ - Neuro`)
- **Coluna**: aba com "Coluna" no nome (operacional: `SPI RJ - Coluna`)
- Usar `--cranio-tab` e `--coluna-tab` para forcar manualmente
- Abas `SP`, `RJ` e `SPI RJ - Neuro V1` sao HISTORICO — ignorar

---

## Passo 3 — Gerar as tirinhas (xlsx + pdf)

Sempre gerar **as duas saidas** (xlsx para edicao, pdf paisagem A4 para impressao):

```bash
python3 <skill_dir>/scripts/gerar_tirinhas.py \
  --input   <caminho_xlsx> \
  --output  "<pasta_da_empresa>/Tirinhas_CARE_SA_<Mes>_<Ano>.xlsx" \
  --empresa "CARE SA"

python3 <skill_dir>/scripts/gerar_tirinhas_pdf.py \
  --input   <caminho_xlsx> \
  --output  "<pasta_da_empresa>/Tirinhas_CARE_SA_<Mes>_<Ano>.pdf" \
  --empresa "CARE SA"
```

**XLSX:** 1 unico arquivo, todos os medicos como blocos empilhados separados
por linha em branco. Sobrescreve se ja existir.

**PDF:** mesmo conteudo em paisagem A4 (842x595pt) com margens de 15mm.
Cada bloco tenta caber em 1 pagina (KeepTogether). Se um bloco for maior que
uma pagina, parte automaticamente e o header se repete no topo (repeatRows=1).
Cores fieis ao xlsx (paleta amarela).

---

## Passo 4 — Gerar as comissoes consolidadas

```bash
python3 <skill_dir>/scripts/gerar_comissoes.py \
  --input        <caminho_xlsx_caresa> \
  --output       <caminho_xlsx_destino> \
  --lcosta-input <caminho_xlsx_lcosta>     # opcional, para calcular bonus 0,5% completo
```

- Saida: 1 .xlsx unico
- Uma aba por agente (Decimar, Fabio, Simoni)
- Aba `SEM AGENTE` se houver linhas sem AGENTE preenchido
- Cada aba: Vendedor | Data | Medico | Paciente | Hospital | Especialidade | Valor (liquido) | Comissao (4%) | Bonus (0,5%)
- A coluna `Bonus (0,5%)` e preenchida apenas na aba do Fabio Paes de Sa, com
  o bonus de 0,5% sobre a soma do `TOTAL GERAL - DESCONTO` das duas empresas
  no mes (precisa do `--lcosta-input` para calcular o pedaço da L.COSTA;
  caso nao seja passado, o script calcula apenas o pedaço da CARE SA e marca
  no log que falta L.COSTA).
- Linha TOTAL no rodape com soma de Valor, Comissao (4%) e Bonus (0,5%)
- **A palavra "comissao" e usada apenas para agentes** — nunca para medicos
  (medicos = "Taxa")

---

## Passo 5 — Entregar

Informar ao usuario:
- Quantas tirinhas foram geradas (quantos medicos)
- Volume total e taxa total
- Arquivo de comissoes gerado e total de comissoes + bonus
- Caminho da pasta `tirinhas/` e do arquivo `Comissoes_<Mes>_<Ano>.xlsx`

Nao e necessario listar todos os arquivos — so o resumo.

---

## Configuracoes padrao

| Parametro             | Valor                                              |
|-----------------------|----------------------------------------------------|
| Empresa               | CARE SA                                            |
| Taxa padrao (medico)  | 20% sobre `TOTAL GERAL - DESCONTO`                 |
| Comissao padrao       | 4% sobre `TOTAL GERAL - DESCONTO`                  |
| Desconto URGENCIA     | 10% silencioso (afeta APENAS a base do medico)     |
| Desconto EMERGENCIA   | 10% silencioso (afeta APENAS a base do medico)     |
| ELETIVA               | Sem desconto silencioso                            |
| Formato de data       | dd/mm/yyyy                                         |
| Moeda                 | R$ (BRL)                                           |
| Coluna classificacao  | CLASSIFICACAO (valores: ELETIVA, URGENCIA, EMERGENCIA) |

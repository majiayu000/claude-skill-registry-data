---
name: calima-register"
description: Index and dispatch for registering a company and its workers in Calima ERP Contábil. Use when asked to cadastrar a empresa, responsável, or funcionários/trabalhadores, or to continue a partially finished Calima registration. States the required order (responsável → empresa → funcionário), routes each step to its leaf skill, and lists the prerequisites that must exist before any cadastro will save.
allowed-tools: browser Read Grep Glob Shell
user-invocable: true
---

> **Authorisation lives in `calima-erp`.** Read the L0–L5 ladder there before
> acting. This skill decides *what to do and in what order*; `calima-navigation`
> decides *how to drive the screen*.

## The order is not negotiable

```
1. calima-register-responsible   →  the person
2. calima-register-company       →  the company
3. calima-register-worker   →  the people
4. calima-register-vinculo       →  the employment relationships
```

The responsável comes first because the company form links to it. A company
cannot be saved until a responsável exists whose `CNPJ` matches — the linkage is
made by putting the company's CNPJ **in the responsável record**, not in the
company record.

The vínculo is a **separate record** from the trabalhador, and it cannot exist
without one. A worker saved on its own produces no payroll, no S-2200 and no
eSocial event. See `calima-register-vinculo`.

## Which skill for which task

| Task | Skill |
|---|---|
| Register the accountant, partner or administrator | `calima-register-responsible` |
| Register the company, address, phones, tax regime | `calima-register-company` |
| Register a worker's personal data | `calima-register-worker` |
| Register a vínculo: admission, cargo, salary, schedule | `calima-register-vinculo` |
| Create a shared schedule (quadro de horário) | `calima-register-vinculo` |
| Import or reconcile eSocial events | `calima-esocial-sync` |
| Decide which rubricas must be sent to the S-1010 | `calima-esocial-s1010-rubricas` |
| Drive the UI, open modals, fill fields, verify a save | `calima-navigation` |

## Before a vínculo can save, three things must exist

This gate is what makes the vínculo the most commonly abandoned cadastro in
Calima. `Salvar` lists all three at once and refuses until each is present:

1. **Salário informado** — entered in the `Histórico de salários` grid, *not*
   in the `Salário atual` panel, which is display-only.
2. **Cargo informado** — CBO plus `cargoAtual` in the `Cargos` tab.
3. **Quadro de horários informado** — a schedule created globally under
   *Manutenção › Quadro de horário* and then linked in the `Horários` tab.

Budget for this: if the company has no schedule on file, create one before
opening the vínculo. Full procedure in `calima-register-vinculo`.

## The two hard gates

**Never transmit.** `Enviar`, `Reabrir`, `Excluir` and DCTFWeb are L5 —
out of scope even with per-block approval. Transmitting is a legal act with
fiscal consequence.

**Never generate.** `Calcular folha`, `Carga inicial` and answering *yes* to
"generate the pending S-2200" are L4. When saving a vínculo, answer **No**.

## Before starting any cadastro

Answer these from documents, not from memory. A wrong answer here becomes wrong
data in a live fiscal system.

1. **CNPJ** — and the company's **IE**, if it has one. Note that IE masks
   accept digits only.
2. **Responsável** — name, CPF, birth date, nationality, marital status, RG,
   issuing authority, **phone**, and their **own address**, which is usually
   not the company's.
3. **Company address** — street, number, bairro, city, UF, CEP.
4. **Tax regime** — Simples Nacional and which Anexo, or Lucro Presumido,
   or Lucro Real, or MEI. This decides the eSocial classification.
5. **Registration data** — Junta Comercial, NIRE, opening date, CNAE (main and
   secondary).
6. **Which workers are actually active**, with their admission dates.

## Where the data comes from

In descending order of trust:

1. **The signed XMLs the eSocial portal returned** — what the portal accepted.
2. **The consolidation of the contract social** — legal facts: partner, CPF,
   capital, shareholding, registered address.
3. **The CNPJ card** — CNAE, opening date, legal nature, capital.
4. **DANFE of an NF-e** — issuer phone, IE. Notably, the issuer's phone often
   appears **only** here: it was absent from the contract, the voter ID, the
   driver's licence, the CNPJ card and the IE certificate.
5. The registration form — **not** a reliable source for a worker's vínculo.
   It contradicted the real payroll on both admission date and salary.

### An S-2200 answers most of the vínculo

The portal XML is the densest source available for a vínculo. One `evtAdmissao`
carries `CBOCargo`, `vrSalFx`, `undSalFixo`, `dtAdm`, `tpRegTrab`, `tpRegPrev`,
`tpContr`, `codCateg`, `qtdHrsSem`, `tpJornada`, `tpRegJor`, `cnpjSindCategProf`
and a human-readable `dscJorn` schedule string. **Read it before the ficha de
registro** — it settles cargo, salary, category, contract type and hours in one
pass, and it surfaces facts the ficha never mentions (the union CNPJ being the
usual one).

The Receita Federal *Relatório de Situação Fiscal* is the same convenience for
company data: opening date, legal nature, CNAE and porte in readable prose.

### When documents contradict each other

State the conflict and get a decision. Do not average them, and do not pick one
silently. Seen: a contract social giving one registered sede while the CNPJ card
and every NF-e give another; an S-2200 declaring `qtdHrsSem=44` while its own
`dscJorn` describes a 45-hour week.

**Record the chosen source alongside the data** so the next person can audit the
decision rather than rediscover it.

## Announce every block

At L2 and L3, state the block before acting: what you are touching, which
screen, and that you are not transmitting. One block at a time.

## Verified reference registrations

Two companies are registered and re-read after saving, so the field-level
outcome is known:

| Company | CNPJ | Record |
|---|---|---|
| Varanda Lanche e Pizzaria Ltda | 32.837.272/0001-37 | `/ger/empresaSearchView/edit/756459`, code `4` |
| Gilberto Domingues Carvalho | 44.684.674/0001-28 | `/ger/empresaSearchView/edit/744434`, code `1` |

See the leaf skills for the field-by-field detail of the Varanda registration,
which is the worked example for both the responsável and the empresa, and the
ISAPED registration, which is the worked example for the trabalhador and the
vínculo.

## Worked example — ISAPED Construtora e Serviços Ltda

CNPJ 46.571.106/0001-46, Simples Nacional, CNAE 7112-0/00, opened 27/05/2022,
record `/ger/empresaSearchView/edit/759499`, code `5`. Four workers, `Registros:
0 → 4`.

The registration ran in the order above and hit every trap in `calima-rules`
24–29. Three findings worth carrying forward:

- **The company address diverged from the contract social.** The JUCERJ
  filing gives `Rua João Rangel nº 200`; the CNPJ card and every NF-e give
  `Coronel Bernardino de Melo 2201 Sala 606`. The client chose the operational
  address. Recorded rather than silently reconciled.
- **The responsável's RG existed only in the contract social**
  (`12.982.659-0`), not in any system extract — and a placeholder had been
  needed to clear the mandatory-field gate in the meantime. Search the contract
  before inventing any identity number.
- **The workers' ficha had no Sexo field at all**, yet `sexo` is mandatory in
  the S-2200. It was supplied by the client, never inferred from the name.

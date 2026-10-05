---
name: agravo-em-recurso-excepcional
description: "Redige o agravo do CPC 1.042 contra a decisao que INADMITE REsp ou RE na origem (salvo inadmissao por repercussao geral/repetitivo, caso em que cabe agravo interno) e os embargos de divergencia do CPC 1.043-1.044 (acordao de orgao fracionario do STJ/STF divergente). Use quando o operador disser agravo em recurso especial/extraordinario, agravo do 1.042, REsp/RE inadmitido, nao subiu o recurso, embargos de divergencia, divergencia entre turmas do STJ/STF."
---

# AGRAVO-EM-RECURSO-EXCEPCIONAL — CPC 1.042 + Embargos de divergencia (1.043-1.044)

> Camada 6 (recursos). Destrava o REsp/RE inadmitido na origem e ataca divergencia interna no tribunal superior.

## Anexos obrigatorios (context/)
- `context/recursos-tutelas-civel.md` (§2.6 agravo do 1.042 + §2.7 embargos de divergencia + §0 preparo).
- `context/cpc-13105-15.md` (arts. 1.042-1.044 + 1.030; **grep + faixa**).
- `context/jurisprudencia-civel.md` (se houver tese pertinente).

## Objetivo
(A) Fazer subir o REsp/RE inadmitido na origem pela via correta; (B) uniformizar tese divergente entre orgaos do mesmo tribunal superior.

## Quando ativar
- O presidente/vice **inadmitiu** o REsp ou RE na origem.
- Acordao de **orgao fracionario** do STJ/STF, em REsp/RE, **divergiu** de outro orgao do mesmo tribunal.
- Gatilhos: "agravo do 1.042", "REsp/RE inadmitido", "nao subiu o recurso", "embargos de divergencia", "divergencia entre turmas".

## Metodologia
### A) Agravo do 1.042
1. **Triagem do fundamento da inadmissao (1.030 — grep):** se a inadmissao se fundou em **repercussao geral ou repetitivo** (incisos I e III do 1.030), **NAO** cabe o 1.042 — cabe **agravo interno (1.021)**. Encaminhar a `agravo-interno`. Cabe o 1.042 contra a **inadmissao do inciso V** (negativa de subida por outro motivo).
2. **Tempestividade:** **15 dias uteis** (1.003 §5), dobro por sujeito. Cruzar com `tempestividade-civel`.
3. **Preparo:** o agravo do 1.042 **independe de custas e despesas postais** (1.042 §2).
4. **Interposicao conjunta (1.042 §6):** havendo RE **e** REsp inadmitidos, **um agravo para cada** recurso. Autos ao STJ primeiro, depois ao STF (§7-8).
5. Redigir: dirigido ao **presidente/vice da origem**, atacando os fundamentos da inadmissao + reafirmando o cabimento do REsp/RE.

### B) Embargos de divergencia (1.043-1.044)
6. **Cabimento (1.043 — grep):** acordao de **orgao fracionario** (STJ/STF) que, em REsp/RE, **divergir de outro orgao do mesmo tribunal** — I acordaos de merito; III um de merito e outro que nao conheceu mas apreciou a controversia. Provar a divergencia por cotejo (§4: certidao/copia/repositorio).
7. **Prazo/preparo:** 15 dias uteis (1.003 §5); preparo sim. Procedimento pelo RI do tribunal superior (1.044). **No STJ, interrompe o prazo do RE** para qualquer parte (1.044 §1) — atentar.
8. Redigir: confronto analitico entre acordao embargado e paradigma + tese a uniformizar.

## Entrega obrigatoria final
- Agravo do 1.042 (um por recurso inadmitido) **ou** embargos de divergencia redigidos com cotejo do paradigma.
- Triagem do fundamento da inadmissao (1.042 x agravo interno) + parecer de tempestividade + nota de isencao de preparo (1.042 §2).

## Guard
Tese/sumula so via `validador-civel`. Inadmissao por RG/repetitivo = via errada para o 1.042 (cabe agravo interno) — avisar e redirecionar. Entrega final pela `suprema-corte-civel`.

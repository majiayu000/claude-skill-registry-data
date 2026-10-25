---
name: efd-reinf"
description: Transmite EFD-Reinf — eventos de retenções de IRRF, CSRF, INSS sobre serviços, receitas de espetáculos e comercialização rural — alinhada com DCTFWeb e DIRF (substituída pela EFD-Reinf desde 2024).
allowed-tools: Read Grep Bash Edit Write
user-invocable: true
---

## Quando usar

Toda PJ que paga ou recebe serviços com retenção. Também produtor rural PF/PJ comercializando, contratantes de cooperativa de trabalho, organizadores de espetáculos, entidades patrocinadas.

A partir de **2024** a EFD-Reinf passou a substituir a DIRF (R-4000 série) — IRRF de PJs e PFs migra para a Reinf.

## Inputs necessários

1. CNPJ + dados cadastrais
2. Notas fiscais com retenções (IRRF, CSRF, INSS 11%)
3. Folhas de pagamento com IRRF retido (eventos R-4040 trabalhador)
4. Comissões pagas a corretores
5. Receita rural (PF, PJ produtor) ou agroindustrial
6. Rendimentos pagos ao exterior

## Eventos (versão S-1.5 / R-2000+ — atual)

### Tabela e cadastrais
- R-1000 — Informações do contribuinte (cadastro, alterações)
- R-1050 — Tabela de comissões (corretores)
- R-1070 — Tabela de processos administrativos/judiciais

### Periódicos
- R-2010 — Retenção 11% INSS sobre serviços tomados (cessão de mão de obra)
- R-2020 — Retenção INSS sobre serviços prestados
- R-2030 — Recursos recebidos por associação desportiva
- R-2040 — Recursos repassados a associação desportiva
- R-2050 — Comercialização da produção rural por PJ
- R-2055 — Aquisição da produção rural
- R-2060 — Apuração CPRB
- R-2098 — Reabertura de eventos periódicos
- R-2099 — Fechamento do período

### Não periódicos (4000)
- R-4010 — Pagamentos a PF (substitui DIRF)
- R-4020 — Pagamentos a PJ (substitui DIRF — IRRF, CSRF)
- R-4040 — Beneficiário não identificado
- R-4080 — Retenção no recebimento (PJ que sofreu retenção)
- R-4099 — Fechamento eventos R-4000
- R-9000 — Exclusão de evento

## Passo a passo

### 1. Apurar retenções da competência
- Cruzar NFs recebidas (skill 13) e folha de pagamento (skill 11).
- Retenções IRRF, CSRF, INSS 11%, e operações rurais.

### 2. Transmitir cadastros (R-1000) e tabelas (R-1050, R-1070) quando aplicável

### 3. Transmitir eventos periódicos
- R-2010: por tomador, com lista de NFs com retenção INSS 11%.
- R-2020: para o prestador (espelho do R-2010), informa o serviço prestado e a retenção.
- R-2050/R-2055: produção rural — comercialização e aquisição.
- R-4010 / R-4020 (a partir de 2024): substituem DIRF mensal.

### 4. Fechamento R-2099
- Após enviar todos os eventos periódicos da competência, fechar com R-2099 — "fecha" a folha previdenciária do mês.
- Após R-2099 a DCTFWeb é gerada automaticamente.

### 5. Fechamento R-4099 (eventos R-4000)
- Idem para os 4000s.

### 6. Reabertura
- R-2098 / R-9000 para corrigir eventos enviados.

## Prazos

- Eventos periódicos (R-2010 a R-2060) e fechamento R-2099: até **dia 15 do mês subsequente** (antecipa em dia útil).
- Eventos R-4000: idem dia 15.
- R-1000/R-1050/R-1070: no momento da criação/alteração, antes do primeiro evento que os referencia.

## Templates

### R-2010 (cabeçalho do tomador)

```
<evtServTom>
  <ideEvento>
    <indRetif>1</indRetif>
    <perApur>2026-03</perApur>
    <procEmi>1</procEmi>
    <verProc>3.0</verProc>
  </ideEvento>
  <ideContri>
    <tpInsc>1</tpInsc>
    <nrInsc>12345678</nrInsc>
  </ideContri>
  <ideEstabObra>...</ideEstabObra>
  <ideEstabPrest CNPJ_prestador>...</ideEstabPrest>
  <nfs>
    <serie>...</serie><numDocto>...</numDocto>
    <vlrBruto>10000.00</vlrBruto>
    <vlrBaseRet>10000.00</vlrBaseRet>
    <vlrRetencao>1100.00</vlrRetencao>
  </nfs>
</evtServTom>
```

## Erros comuns

- Não fechar R-2099 → DCTFWeb não é gerada → débito não constituído → autuação.
- Enviar R-2010 sem ter feito R-1000 do contribuinte.
- Esquecer R-2055 (aquisição produção rural por PJ) — risco de glosa de crédito presumido.
- Confundir tpInsc (1=CNPJ, 2=CPF).
- Reter INSS 11% do prestador Simples Nacional fora das atividades de cessão MO (não é caso, dispensa).
- Não migrar DIRF para Reinf em 2024 — dupla declaração.

## Checklist

- [ ] R-1000 atualizado para o ano corrente
- [ ] R-1070 com processos eventuais
- [ ] R-2010 com TODOS os tomadores que retiveram INSS 11%
- [ ] R-2020 com TODOS os prestadores que sofreram retenção
- [ ] R-4010/R-4020 com pagamentos a PF/PJ com IRRF
- [ ] R-2099 enviado e aceito
- [ ] R-4099 enviado e aceito
- [ ] DCTFWeb gerada e fechada
- [ ] Comprovantes de retenção entregues a prestadores

## Referências

- IN RFB 2.043/2021 (consolidação EFD-Reinf)
- Manual de Orientação do eSocial e EFD-Reinf (versão atual S-1.5)
- IN RFB 2.060/2021 (DIRF — substituição)
- Portal SPED — eventos vigentes (gov.br/sped)

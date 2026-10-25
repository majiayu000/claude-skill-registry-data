---
name: dctfweb"
description: Confessa débitos federais (INSS, IRRF, CSRF, IRPJ, CSLL, PIS, COFINS, IPI) na DCTFWeb mensal a partir de eSocial e EFD-Reinf, gera DARF unificado e trata retificações.
allowed-tools: Read Grep Bash Edit Write
user-invocable: true
---

> ⚠️ **AVISO FISCAL — CONFIRA ANTES DE GERAR A GUIA.** Todo código de receita (DARF/DAS), alíquota, base de cálculo, valor e data de vencimento gerado por este agente é **rascunho de apoio** e pode variar por ano, regime tributário, município ou caso específico. **Confira sempre na fonte oficial vigente (Receita Federal / e-CAC / legislação estadual e municipal) antes de transmitir declaração ou pagar guia.** A conferência final é responsabilidade do contador responsável.

## Quando usar

Toda PJ exceto MEI. Substituiu a DCTF mensal e a GFIP. A obrigação varia por categoria: PJs em geral, PFs com empregados, optantes do Simples (eSocial doméstico), produtor rural.

A partir de **2024**, IRRF de PFs e PJs também é confessado na DCTFWeb (com fonte na EFD-Reinf R-4000).

## Inputs necessários

1. eSocial fechado (S-1299) da competência
2. EFD-Reinf fechada (R-2099 e R-4099) da competência
3. Apurações de IRPJ/CSLL (Real estimativa, Real trimestral ou Presumido)
4. Apurações de PIS/COFINS, IPI
5. Pagamentos antecipados (compensações via PER/DCOMP, parcelamentos, etc.)
6. Processos administrativos com débitos suspensos (informar)

## Modalidades

| Modalidade | Cobertura | Periodicidade |
|---|---|---|
| Mensal | Todos os débitos federais a partir de 2024 | Mensal |
| 13º Salário | Apenas 13º (anual) | Anual (dez) |
| Aferição (obras) | Construção civil (CNO) | Por evento |
| Reclamatória Trabalhista | Decorrente de RT | Por sentença |

## Passo a passo

### 1. Fechar eSocial e EFD-Reinf
- eSocial: fechar S-1299 (encerramento de eventos periódicos da folha).
- EFD-Reinf: fechar R-2099 e R-4099.
- Sem fechamento → DCTFWeb não é gerada.

### 2. Acessar e-CAC → DCTFWeb
- Sistema gera DCTFWeb com débitos importados automaticamente.
- Conferir: INSS empresa (CPP, RAT/FAP, terceiros), INSS retido, IRRF (folha + PJ + PF + RPA), CSRF, etc.

### 3. Lançamentos manuais
- Débitos não cobertos por eSocial/Reinf precisam ser lançados manualmente:
  - IRPJ/CSLL apuração trimestral ou estimativa (códigos 2089, 2362, 2430, 2484)
  - PIS/COFINS (8109, 2172, 6912 etc.)
  - IPI (5123)
  - Códigos diversos que ainda não estão em eventos eSocial/Reinf

### 4. Compensações e suspensões
- Vinculação de pagamentos: lançar DARFs já pagos.
- Vinculação de PER/DCOMP: indicar número e data.
- Suspensão por decisão judicial: indicar processo.

### 5. Transmitir
- Assinar e enviar até **dia 25 do mês subsequente**.
- DCTFWeb gera DARF único consolidado por código (na verdade DARFs separados por receita, mas listados na mesma DCTFWeb).

### 6. Pagamento
- Vencimentos:
  - INSS: dia 20 do mês subsequente
  - IRRF (folha e maioria): dia 20
  - CSRF: último dia útil da quinzena seguinte ao pagamento
  - PIS/COFINS: dia 25
  - IRPJ/CSLL Presumido: último dia útil do mês subsequente ao trimestre

### 7. Retificação
- Pode retificar a qualquer tempo, mas:
  - Após início de fiscalização, não retifica para reduzir débito sem amparo legal.
  - DCTFWeb retificadora deve ter origem em eSocial/Reinf retificados (cuidado com a ordem).

## Templates

### Conferência mensal (planilha-base)

```
COMPETÊNCIA __/____ — CNPJ __________
[ ] eSocial S-1299 OK em __/__/____
[ ] EFD-Reinf R-2099 OK em __/__/____
[ ] EFD-Reinf R-4099 OK em __/__/____

DÉBITOS DCTFWeb (importados):
  CPP empresa.................. R$ _________
  RAT × FAP.................... R$ _________
  Terceiros.................... R$ _________
  INSS retido (cessão MO)...... R$ _________
  IRRF Folha................... R$ _________
  IRRF RPA / PJ................ R$ _________
  CSRF......................... R$ _________
  TOTAL eSocial+Reinf.......... R$ _________

DÉBITOS LANÇADOS MANUALMENTE:
  IRPJ apuração................ R$ _________
  CSLL apuração................ R$ _________
  PIS.......................... R$ _________
  COFINS....................... R$ _________
  IPI.......................... R$ _________

VINCULAÇÕES (pagamentos/compensações):
  DARFs pagos.................. R$ _________
  PER/DCOMP.................... R$ _________
  Suspensões judiciais......... R$ _________

SALDO A PAGAR................. R$ _________
```

## Erros comuns

- Transmitir DCTFWeb antes de fechar eSocial/Reinf — débitos faltam.
- Esquecer débito manual (IPI, PIS/COFINS) que não vem de eventos.
- Vincular pagamento errado (DARF de outra competência).
- Retificar Reinf sem retificar DCTFWeb correspondente.
- Multa por atraso de DCTFWeb sem débito → R$ 200; com débito → 2% ao mês sobre tributos não pagos (mín R$ 200).

## Checklist

- [ ] eSocial e Reinf fechados antes de gerar DCTFWeb
- [ ] Cada débito esperado está presente
- [ ] Pagamentos e compensações vinculados
- [ ] Suspensões judiciais informadas com processo
- [ ] DCTFWeb transmitida até dia 25
- [ ] DARFs pagos no vencimento
- [ ] Comprovante e recibo arquivados
- [ ] Cruzamento DCTFWeb x eSocial/Reinf x ECF/EFD: sem divergência

## Referências

- IN RFB 2.005/2021 (DCTFWeb)
- Lei 11.941/2009 (compensação)
- Decreto 70.235/1972 (procedimento administrativo fiscal)
- Manual DCTFWeb (e-CAC)

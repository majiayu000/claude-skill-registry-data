---
name: dmed"
description: Gera e transmite a DMED (Declaração de Serviços Médicos e de Saúde) anual com pagamentos recebidos por hospitais, clínicas, planos de saúde, médicos e operadoras, alinhada à dedução do IRPF dos pacientes.
allowed-tools: Read Grep Bash Edit Write
user-invocable: true
---

## Quando usar

Pessoas Jurídicas que prestam serviços médicos (hospitais, clínicas, laboratórios, médicos PJ), planos de saúde, seguradoras com cobertura saúde, cooperativas e empresas com plano coletivo. Entrega anual até **último dia útil de fevereiro** referente ao ano-calendário anterior (IN RFB 985/2009).

A DMED é o **espelho** das deduções de saúde do IRPF — divergências geram malha fina.

## Inputs necessários

1. Sistema de gestão da clínica/hospital com pagamentos por paciente no ano
2. Lista de dependentes informados (cônjuges, filhos)
3. Reembolsos pagos pela operadora
4. CPF de cada paciente e dependente
5. Para operadoras: lista de beneficiários por contrato

## Estrutura

DMED separa:
- **Operação 01**: Prestador (hospital, clínica, médico, profissional saúde) — declara o que recebeu de PFs.
- **Operação 02**: Operadora de plano de saúde — declara contribuições recebidas e reembolsos pagos.

Cada lançamento inclui:
- CPF do titular do contrato/pagamento
- CPF dos dependentes do plano
- Valor pago / contribuição / reembolso

## Passo a passo

### 1. Levantar lista de pacientes pagantes no ano
- Excluir pacientes pagos por convênio (vai em DMED da operadora, não do prestador).
- Incluir apenas valores pagos pela PF diretamente (particular).

### 2. Para operadoras
- Contribuições mensais por titular
- Reembolsos pagos por procedimento (com CPF do beneficiário)

### 3. Importar no PGD DMED
- Validar CPFs, somas anuais

### 4. Transmitir
- Assinatura digital
- Vencimento: último dia útil de fevereiro

### 5. Comprovante para o paciente
- Recibo médico tradicional já cumpre — importante que tenha CPF do paciente, valor pago, data, assinatura/identificação do profissional, CRM ou CNPJ.

## Erros comuns

- Lançar pacientes que pagaram com plano (deve ir só na DMED da operadora).
- Trocar CPF do titular pelo CPF do dependente — IRPF acusa malha fina por valor incompatível.
- Esquecer reembolsos pagos pela operadora (cliente declara dedução de saúde já considerando o reembolso, então a operadora informa para a Receita validar).
- Atraso → multa 2% a.m. (mín R$ 500).
- Médico PF (profissional autônomo) sem CNPJ está dispensado da DMED, mas os tomadores que pagaram a esse médico (PJs) devem declarar (DIRF/Reinf).

## Checklist

- [ ] Lista de pagamentos PF recebidos no ano
- [ ] CPFs validados
- [ ] Operadora: contribuições + reembolsos
- [ ] Dependentes vinculados ao titular
- [ ] PVA DMED com 0 erros
- [ ] Transmissão até último dia útil de fevereiro
- [ ] Recibo arquivado
- [ ] Comprovantes médicos com CPF do paciente

## Referências

- IN RFB 985/2009 (DMED)
- IN RFB 1.228/2011 (alterações)
- Manual DMED (PGD vigente)
- Decreto 9.580/2018 (dedução de saúde no IRPF — art. 73)

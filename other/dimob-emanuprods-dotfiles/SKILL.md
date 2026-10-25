---
name: dimob"
description: Gera e transmite a DIMOB (Declaração de Informações sobre Atividades Imobiliárias) anual de imobiliárias, construtoras e incorporadoras, declarando vendas, aluguéis e comissões com IRRF.
allowed-tools: Read Grep Bash Edit Write
user-invocable: true
---

## Quando usar

PJ que comercializou imóveis, intermediou vendas/locações, ou recebeu aluguel em nome de terceiros (administradoras). Entrega anual até **último dia útil de fevereiro** (IN RFB 1.115/2010 e atualizações).

Inclui:
- Construtoras e incorporadoras (vendas)
- Imobiliárias (intermediação, locação)
- Administradoras de bens
- Cooperativas habitacionais

## Inputs necessários

1. Lista de operações de venda (compradores, vendedores, valores, datas, parcelas pagas no ano)
2. Contratos de locação ativos (locador, locatário, imóvel, aluguel pago no ano, período)
3. Contratos de intermediação (comissão recebida, comprador/vendedor)
4. Comprovantes de IRRF (sobre comissão, sobre aluguel pago a PF)
5. Endereço do imóvel (CEP, número, complemento)

## Estrutura

A DIMOB organiza por:
- **Operação 01**: Comercialização de imóveis (venda direta)
- **Operação 02**: Locação (administradoras informam aluguéis recebidos em nome de terceiros)
- **Operação 03**: Intermediação (comissão de imobiliária)
- **Operação 04**: Construção (incorporação, lotes)

Para cada operação:
- CPF/CNPJ do adquirente/locatário/locador
- Endereço do imóvel
- Valor total e parcelas no ano
- IRRF retido (quando aplicável)

## Passo a passo

### 1. Importar do CRM/sistema imobiliário
- Exportar operações por tipo (venda, locação, intermediação)

### 2. Validar dados
- CPF/CNPJ válidos
- Endereços completos
- Datas e valores conferindo com contrato

### 3. Calcular pagamentos no ano
- Para vendas parceladas: somar todas as parcelas pagas no ano-calendário
- Para locação: 12 ou parcial, conforme início/fim do contrato

### 4. Importar no PGD DIMOB
- TXT no leiaute IN RFB 1.115/2010 ou digitar
- Validar: PVA aponta CPF/CNPJ inválido, valor zerado, ausência de campos obrigatórios

### 5. Transmitir
- Assinatura digital (e-CPF/e-CNPJ).
- Recibo guardado.

## Templates

### Linha-tipo (operação 02 — locação)

```
Locador (CPF/CNPJ): __________
Locatário (CPF/CNPJ): __________
Endereço do imóvel: __________
Período locação no ano: __/__/____ a __/__/____
Valor pago no ano: R$ _________
IRRF retido (PJ paga PF): R$ _________
```

## Erros comuns

- Imobiliária esquecer locação repassada (administra mas não declara aluguéis recebidos em nome do proprietário).
- CPF do comprador inválido ou trocado entre adquirente/vendedor.
- Não declarar imóvel financiado pelo SFH (a construtora não recebeu o valor inteiro mas a venda foi feita; declarar pelo total da venda, ano a ano conforme parcelas).
- Locação em curto prazo (Airbnb) declarada como locação tradicional — verificar tratamento (Solução de Consulta COSIT 232/2017 trata como serviço de hospedagem em alguns casos).
- Atraso → multa 2% a.m. mínima R$ 500.

## Checklist

- [ ] Todas as vendas do ano conferidas com contratos
- [ ] Locações ativas e repassadas
- [ ] Comissões com IRRF retido informadas
- [ ] CPF/CNPJ válidos
- [ ] PVA com 0 erros
- [ ] DIMOB transmitida até último dia útil de fevereiro
- [ ] Recibo arquivado
- [ ] Comprovante de IRRF entregue ao beneficiário (locador, vendedor)

## Referências

- IN RFB 1.115/2010 (regulamento DIMOB)
- IN RFB 1.711/2017 (alterações)
- Manual DIMOB (PGD vigente)
- Decreto 9.580/2018 (RIR — IRRF e ganho de capital)

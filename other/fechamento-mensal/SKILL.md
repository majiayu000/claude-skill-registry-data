---
name: fechamento-mensal"
description: Roteiro completo de fechamento contábil mensal — provisões, depreciação, conciliações, encerramento de resultado, e geração de relatórios — em até 5 dias úteis após o mês.
allowed-tools: Read Grep Bash Edit Write
user-invocable: true
---

## Quando usar

Todo início de mês, para fechar a competência anterior. Padrão de mercado: fechar até 5º dia útil.

## Roteiro (10 passos)

### 1. Confirmar entradas
- Todas as NFs de entrada/saída lançadas (cruzar com EFD)
- Todos os recebimentos e pagamentos do extrato lançados (skill 33)
- Folha de pagamento processada e lançada
- Apurações de tributos lançadas

### 2. Conciliações (skills 33-36)
- Bancos
- Cartões / credenciadoras
- Fornecedores (top 20)
- Clientes (top 20)

### 3. Provisões mensais
- Férias + 1/3 + encargos (skill 28)
- 13º salário + encargos
- INSS, FGTS, IRRF a recolher conferindo bases
- PCLD (CPC 48)

### 4. Depreciação e amortização (skill 41)
- Imobilizado: depreciação por bem
- Intangível: amortização
- IFRS 16 / CPC 6 R2: amortização do direito de uso

### 5. Apropriação de financeiros
- Juros sobre empréstimos (a pagar e ativo financeiro)
- Variação cambial (regime de competência)
- Aplicações financeiras (rendimento)

### 6. Encerramento de resultado (zerar contas 3, 4, 5 do mês)

```
(Para cada conta de receita do mês)
D Receita                   R$ X
   C Apuração de resultado   R$ X

(Para cada conta de custo/despesa do mês)
D Apuração de resultado     R$ Y
   C Custos/Despesas         R$ Y

(Resultado líquido para o PL)
D Apuração de resultado     R$ Z (lucro)
   C 2.3.4 Lucros do exercício R$ Z
```

(em PME pode-se zerar apenas no fechamento anual; em práticas mais robustas zera mensalmente)

### 7. Geração de relatórios
- Balancete de verificação
- DRE do mês e acumulado
- Balanço patrimonial
- DFC (CPC 03) — fluxo de caixa direto ou indireto
- DRA (resultado abrangente — quando aplicável)

### 8. Análise gerencial (skill 39)
- Margem bruta, EBITDA, lucro líquido
- Variações vs. mês anterior e vs. orçado
- Indicadores: liquidez corrente, endividamento, prazo médio recebimento, prazo médio pagamento, giro de estoque

### 9. Reportar ao cliente
- Pacote: balancete + DRE + DFC + indicadores + comentários do contador
- Reunião de fechamento (se contratada)

### 10. Arquivar
- Conciliações, balancetes, DREs, comprovantes — pasta digital por competência
- Backup: nuvem + local
- Lei 10.406/2002 art. 1.194 (livros): conservar pelo prazo decadencial fiscal (5 anos) e documentos suporte (5 anos a partir do encerramento do exercício)

## Templates

### Checklist de fechamento

```
COMPETÊNCIA __/____ — CNPJ __________ — Cliente __________

ENTRADAS
[ ] NFs entrada (#) ___ × razão de fornecedores
[ ] NFs saída (#) ___ × razão de clientes
[ ] Apuração tributos lançada
[ ] Folha de pagamento processada
[ ] Pagamentos e recebimentos do mês

CONCILIAÇÕES
[ ] Banco c/c 1: saldo bate
[ ] Banco c/c 2: saldo bate
[ ] Cartões: vendas × repasses
[ ] Top 20 fornecedores
[ ] Top 20 clientes
[ ] Tributos a recolher: razão × DCTFWeb

PROVISÕES E AJUSTES
[ ] Provisão férias + encargos
[ ] Provisão 13º + encargos
[ ] PCLD revisada
[ ] Depreciação imobilizado
[ ] Amortização intangível
[ ] Amortização IFRS 16
[ ] Apropriação juros empréstimos
[ ] Variação cambial

RELATÓRIOS
[ ] Balancete de verificação
[ ] DRE mês + acumulado
[ ] Balanço patrimonial
[ ] DFC
[ ] Análise gerencial

ENTREGAS LEGAIS DO MÊS
[ ] DCTFWeb (até dia 25)
[ ] EFD ICMS/IPI (até dia 25)
[ ] EFD-Contribuições (até dia 10 mês +1)
[ ] eSocial S-1299 / Reinf R-2099 / R-4099 (dia 15)

REPORT
[ ] Pacote enviado ao cliente
[ ] Reunião agendada
[ ] Pasta arquivada
```

## Erros comuns

- Fechar antes de receber todas as NFs do mês — competência errada.
- Esquecer provisão de férias/13º — passivo subestimado.
- Não rodar depreciação → ativo super-avaliado, lucro maior.
- Conciliação bancária com diferença "para regularizar mês que vem" — vira bola de neve.
- DFC esquecida (obrigatória para sociedades por ações e ME/EPP do CPC 1.000 quando aplicável).
- Encerramento de resultado mensal sem lançamento → conta de resultado acumula no ano e distorce balancete mensal.

## Checklist mestre

- [ ] Entradas completas
- [ ] Conciliações fechadas
- [ ] Provisões e ajustes
- [ ] Resultado encerrado (mensal ou anual)
- [ ] Relatórios gerados
- [ ] Análise gerencial
- [ ] Obrigações acessórias do mês entregues
- [ ] Pasta arquivada

## Referências

- CPC 26 (apresentação)
- CPC 03 (DFC)
- NBC TG 1.000 (PME)
- ITG 2000 (escrituração)
- Lei 6.404/1976 (S.A.)
- Lei 10.406/2002 (Código Civil — escrituração)

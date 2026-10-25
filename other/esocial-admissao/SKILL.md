---
name: esocial-admissao"
description: Executa a admissão de empregado no eSocial, com S-2200 ou S-2190 (admissão preliminar), cadastros prévios, exame admissional e termos do contrato — leiaute S-1.5 vigente.
allowed-tools: Read Grep Bash Edit Write
user-invocable: true
---

## Quando usar

A cada novo contrato CLT (e estagiários, jovem aprendiz, intermitente). Prazo crítico: **antes do início da atividade** o evento S-2190 (admissão preliminar) ou S-2200 (admissão completa).

## Inputs necessários

1. Dados do trabalhador: CPF, nome, NIS (PIS/PASEP/NIT), data nascimento, sexo, raça/cor, grau instrução, estado civil, dependentes (com CPF para dedução IR)
2. Documentos: RG, CTPS digital (não precisa carteira física), título eleitor, CNH (se motorista)
3. Endereço completo
4. Contrato de trabalho: cargo (CBO), salário, data admissão, jornada, tipo contrato (indeterminado, prazo, intermitente, aprendiz)
5. Categoria eSocial (101 mensalista, 102 trabalhador horista, 104 doméstico, etc.)
6. Vale-transporte, opção FGTS, plano de saúde (vínculo S-1010 rubricas)
7. ASO (atestado de saúde ocupacional) — necessário antes do início

## Eventos relacionados

| Evento | Quando |
|---|---|
| S-1000 | Cadastro do empregador (uma vez) |
| S-1005 | Estabelecimento (CNPJ ou CAEPF) |
| S-1010 | Tabela de rubricas |
| S-1020 | Tabela de lotação tributária |
| S-1030 | Cargos |
| S-2190 | Admissão preliminar — apenas CPF, data e categoria. Substitui RAIS preliminar; permite começar imediatamente. |
| S-2200 | Admissão completa — todos os dados acima |
| S-2205 | Alteração cadastral do trabalhador |
| S-2206 | Alteração contratual |

## Passo a passo

### 1. Cadastros prévios (uma vez por empregador)
- S-1000, S-1005, S-1010, S-1020, S-1030, S-1070 (processos)

### 2. Antes da admissão
- Confirmar CPF do trabalhador (situação cadastral RFB)
- Cadastrar NIS via consulta/cadastro CNIS — sem NIS, eSocial rejeita
- Agendar exame admissional + ASO

### 3. Admissão preliminar (S-2190)
- Para casos urgentes (já vai trabalhar amanhã)
- Apenas CPF, data, categoria, jornada e estabelecimento
- Prazo: **até o final do dia anterior ao início**

### 4. Admissão completa (S-2200)
- Prazo: até o dia 15 do mês seguinte
- Se não enviou S-2190: S-2200 deve ser enviado **antes** do início da atividade
- Inclui dependentes para IRRF (vínculo CPF do dependente)

### 5. Exame admissional
- ASO emitido por médico do trabalho
- Sem ASO o vínculo é irregular

### 6. Eventos seguintes ao S-2200
- S-2210 Comunicação de Acidente de Trabalho (CAT) — se houver
- S-2220 Monitoramento da Saúde do Trabalhador (ASOs periódicos)
- S-2230 Afastamentos
- S-2240 Condições Ambientais (PPP digital, agentes nocivos)

## Templates

### Checklist de documentos para admissão

```
TRABALHADOR: ____________________  CPF: __________  NIS: __________

DOCUMENTOS:
[ ] RG (cópia)
[ ] CPF
[ ] CTPS digital (consultar gov.br)
[ ] Título de eleitor
[ ] Comprovante de endereço atual
[ ] CNH (se motorista) e MOPP (se carga perigosa)
[ ] Certificado militar (homens entre 18-45)
[ ] Comprovante escolaridade
[ ] Carteira de vacinação (se < 18 anos)
[ ] Certidão de nascimento dos filhos (dependentes)
[ ] CPF dos dependentes para IRRF
[ ] Termo de opção VT
[ ] Termo de opção plano de saúde

PROCESSOS:
[ ] S-2190 enviado ___/___/___ recibo: __________
[ ] ASO realizado em ___/___/___ apto: [ ] sim [ ] não
[ ] S-2200 enviado em ___/___/___ recibo: __________
[ ] Contrato físico/digital assinado
```

## Erros comuns

- Iniciar trabalho sem S-2190 → multa por trabalho não registrado (até R$ 3.000 por empregado, dobra em reincidência).
- NIS não cadastrado/inválido → eSocial rejeita.
- Categoria errada (101 mensalista vs 102 horista) → reflete em totalizador errado.
- Admitir antes do exame admissional → vínculo irregular.
- CBO incompatível com função real → fiscalização questiona.
- Contrato verde-amarelo / contrato de trabalho intermitente sem registrar a categoria correta (104 ou 102 com CBO de aprendiz).
- Dependente sem CPF → não deduz no IRRF.

## Checklist

- [ ] CPF do trabalhador validado na RFB
- [ ] NIS ativo no CNIS
- [ ] ASO admissional apto
- [ ] S-2190 (preliminar) ou S-2200 (completo) antes do início
- [ ] Categoria + CBO + lotação corretos
- [ ] Dependentes com CPF
- [ ] Contrato físico/digital assinado
- [ ] Recibos eSocial arquivados

## Referências

- Lei 8.036/1990 (FGTS)
- CLT (arts. 41-50, 442 a 510-A)
- Manual de Orientação eSocial S-1.5
- Decreto 10.854/2021 (Programa Permanente de Consolidação)
- IN MTP 5/2022 (eSocial)

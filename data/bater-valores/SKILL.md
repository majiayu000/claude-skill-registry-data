---
name: bater-valores
description: Usa quando o usuario disser que um valor "nao bate", "valor errado", "faltando dinheiro", "sobrou dinheiro", "pagou 2x", "divergencia", "atribuiu errado", "confere esse valor" ou "o valor nao esta sendo enviado ou pago"; e ANTES de dizer pronto em mudanca que mexe em calculo, soma ou atribuicao de dinheiro. NAO usa pra layout de tela de valor (isso e provar-na-tela).
---

# Bater valores

Situacao comum: o valor de uma tela nao bate com outra fonte. Esta skill e o roteiro para analisar sem o usuario precisar pedir cada passo.

## Regra de ouro

Nunca responda "arrumei" pra um valor sem mostrar a conta fechada (fonte = sistema, com os numeros) e sem achar a CAUSA. Nunca acerte numero na mao pra bater.

## Passos

1. Fixe a pergunta em 1 linha antes de olhar codigo: qual numero, de qual tela, de qual empresa (empresa A ou B, se o sistema tem mais de uma), de qual mes, em qual recorte (caixa = dia em que o dinheiro entrou ou saiu; competencia = lote, mes de uso ou mes da venda). Sem isso nao compare. Faltou um dos itens: faca UMA pergunta ja com a hipotese mais provavel (ex.: "mes atual, empresa A, caixa?"). Sem acesso a fonte (rota protegida, login que so o usuario tem): peca a ele os 2 numeros (o do sistema e o do banco ou planilha), com a tela e o mes. Exemplo: "saldo do lote de novembro, tela Lotes, empresa A, caixa: sistema X reais, banco Y reais, diferenca Z reais".
2. Ache a fonte da verdade do projeto: se existir `PROJETOS.md` nesta pasta, leia a linha do projeto; senao, use README/CLAUDE.md do projeto.
3. Use a conferencia que JA EXISTE no projeto (mesma linha de `PROJETOS.md`, ou o que o README apontar) antes de escrever script novo.
4. Decomponha a diferenca em itens nominais (cliente a cliente, lancamento a lancamento). Nunca pare em "o total difere". Dica (hipotese a provar no passo 5, nunca conclusao): diferenca redonda costuma ser acao humana no aplicativo do banco; diferenca com centavos costuma ser valor a receber ou devolucao.
5. Passe pelas causas na ordem da tabela "Causas", da mais frequente pra menos, usando a checagem de cada uma.
6. Conserte a causa no sistema, com um teste montado com o caso real (os valores do caso, sem dado pessoal) que cai sem o conserto. O teste mora com os testes do projeto (comando no README do projeto ou na linha de `PROJETOS.md`); prove desfazendo o conserto e rodando o teste: tem que cair.
7. Dado ja gravado errado: backup antes (copia da tabela ou do arquivo com a data no nome; o caminho vai na resposta), e reescreva so do mes atual pra frente. Outros meses so com ordem expressa do usuario. Em producao, so com o ok do usuario e pela migracao ou rota de correcao que o projeto ja tem; sem esse caminho, entregue o SQL ou a chamada pronta pra ele aprovar.
8. Prove: rode a conferencia de novo e mostre "fonte X = sistema X". Diga o que NAO foi conferido.
9. Registre o caso onde o projeto guarda notas (uma nota por caso, com causa e conserto). Causa nova entra na tabela "Causas" desta skill.

## Causas

| Causa | Como aparece na fala do usuario | Checagem |
|---|---|---|
| 1. Caixa do banco x painel nao fecha, pra mais ou pra menos (saida duplicada, lancamento faltando, saida solta, troco de lote anterior) | o saldo do painel e maior ou menor que o do banco | Saldo real do banco x pendente de envio, decompondo a diferenca. Cada transferencia deve ter 1 saida; procure saida repetida do mesmo valor logo ao lado. |
| 2. Atribuicao errada de empresa, equipe ou cliente | a tela mostra mais vendas do que o extrato para uma equipe | Compare quem pagou no extrato x cliente gravado x equipe no cadastro. A empresa vem da equipe, nunca de um padrao fixo; achado por nome so vale com primeiro e ultimo nome iguais. Conte linhas sem empresa, responsavel ou origem. |
| 3. Estorno ou devolucao mal modelado | um valor ja devolvido continua sendo descontado | Estorno e saida ligada a entrada; nao pode existir segunda saida do mesmo valor em poucos dias. |
| 4. Competencia x caixa | o total de um mes fechado mudou depois | Fixe o recorte antes de comparar. Lote fechado nao recebe valor novo. |
| 5. Planilha ou sistema vizinho com valor diferente | duas fontes com totais diferentes | Cruze por caso nominal, nunca por total. Some por pessoa e campo, liste so quem difere. Pago separado de devido. |
| 6. Duplicidade de cadastro ou lancamento na origem | a mesma conta ou pessoa aparece duas vezes | Procure repeticao na origem (mesmo CPF + valor + dia; conta repetida). Cadastro duplicado vindo de sincronizacao entre dois sistemas: hipotese a provar. |
| 7. Mesmo nome, grandeza diferente | dois sistemas com poucos itens de diferenca | Confira a definicao de cada campo: valor contratado nao e valor creditado, bruto nao e liquido, previsto nao e pago. |
| 8. Campo de valor digitado distorce o numero | o valor sai com zeros a mais ou a menos | Valor digitado no formato brasileiro (7.540,00) tem que passar por conversao propria; ao editar, suspeite de mascara de campo. |

Fatura de cartao misturada com compra ou pagamento e hipotese: leia as notas do projeto antes de tratar como causa.

## Por projeto

A tabela "Por projeto" (fonte da verdade, conferencia que ja existe, regra de empresa e de mes) NAO vem na skill: ela e sua. Copie `PROJETOS.exemplo.md` para `PROJETOS.md` nesta pasta e preencha. Se existir `PROJETOS.md` nesta pasta, leia a linha do projeto; senao, use README/CLAUDE.md do projeto.

## Limites

- Producao so por leitura e pelo caminho que o usuario abre logado (rota ou tela de conferencia). Nunca com credencial lida de variavel de ambiente.
- Fonte informativa (que o projeto marca como so informativa) nunca entra na soma.

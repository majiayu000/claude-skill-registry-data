---
name: simplify
description: Simplifica o código para maior clareza sem alterar o comportamento. Use quando solicitado aplicar refatoração de legibilidade ou simplificação. Revisão sem edição pertence a revisor-de-codigo, modo qualidade.
---

# Simplificação de código

## Visão geral

Simplifique o código reduzindo a complexidade e preservando o comportamento exato. O objetivo não são menos linhas — é um código mais fácil de ler, entender, modificar e depurar. Toda simplificação deve passar por um teste simples: “Será que um novo membro da equipe entenderia isso mais rápido do que o original?”

## Quando usar

- Depois que um recurso está funcionando e os testes são aprovados, mas a implementação parece mais pesada do que precisa
- Para executar refatorações solicitadas a partir de achados de revisão; o relatório sozinho não autoriza editar
- Quando o pedido de simplificação abrange lógica aninhada, funções longas ou nomes pouco claros
- Ao refatorar código escrito sob pressão de tempo
- Ao consolidar a lógica relacionada espalhada pelos arquivos
- Após mesclar alterações que introduziram duplicação ou inconsistência

**Quando NÃO usar:**

- O código já está limpo e legível - não simplifique só por simplificar
- Você ainda não entende o que o código faz – compreenda antes de simplificar
- O código é crítico para o desempenho e a versão "mais simples" seria mensuravelmente mais lenta
- Você está prestes a reescrever o módulo completamente – simplificar o código descartável desperdiça esforço

## Os Cinco Princípios

### 1. Preservar o comportamento com exatidão

Não mude o que o código faz — apenas como ele o expressa. Todas as entradas, saídas, efeitos colaterais, comportamento de erro e casos extremos devem permanecer idênticos. Se você não tem certeza se uma simplificação preserva o comportamento, não faça isso.

Antes de cada mudança, pergunte:

- Isso produz a mesma saída para cada entrada?
- Isso mantém o mesmo comportamento de erro?
- Isso preserva os mesmos efeitos colaterais e ordem?
- Todos os testes existentes ainda passam sem modificação?

### 2. Siga as Convenções do Projeto

Simplificar significa tornar o código mais consistente com a base de código, e não impor preferências externas.

Antes de simplificar:

1. Leia `AGENTS.md` / convenções do projeto
2. Estude como o código vizinho lida com padrões semelhantes
3. Combine o estilo do projeto para importações, nomenclatura, estilo de função, tratamento de erros e anotações de tipo

A simplificação que quebra a consistência do projeto não é simplificação – é rotatividade.

### 3. Prefira clareza à inteligência

O código explícito é melhor que o código compacto quando a versão compacta requer uma pausa mental para análise.

- Substitua ternários aninhados por fluxo de controle legível
- Substitua transformações in-line densas por etapas intermediárias nomeadas quando elas esclarecerem a intenção
- Mantenha nomes úteis, mesmo que custem algumas linhas extras

### 4. Mantenha o equilíbrio

Cuidado com a simplificação excessiva:

- Não encurte ou remova nomes que tenham significado
- Não mescle lógica não relacionada em uma função maior
- Não remova abstrações que servem para testabilidade ou extensibilidade
- Não otimize a contagem de linhas em detrimento da compreensão

### 5. Escopo do que mudou

O padrão é simplificar o código modificado recentemente. Evite refatoradores drive-by não relacionados, a menos que seja explicitamente solicitado.

## Limites

Aplique mudanças apenas no escopo solicitado. Preserve contratos, efeitos, ordem, concorrência e comportamento de erro. Bug descoberto não deve ser corrigido disfarçado de simplificação: registre e trate no fluxo adequado. Não faça commit nem declare aprovação independente por efeito desta skill. Testes indisponíveis são limitação, não evidência de equivalência.

## Processo

### Etapa 1: entenda antes de tocar

Antes de alterar ou remover qualquer coisa, entenda porque ela existe.

Responder:

- Qual é a responsabilidade deste código?
- Como chama isso? Como isso chama?
- Quais são os casos extremos e caminhos de erro?
- Existem testes que definem o comportamento esperado?
- Por que pode ter sido escrito desta forma?

Se você não consegue responder, leia mais sobre o contexto primeiro.

### Passo 2: Procure oportunidades de simplificação

Sinais:

- Aninhamento profundo
- Funções longas com responsabilidades mistas
- Ternários aninhados
- Argumentos de sinalização booleana
- Condicionais repetidas
- Nomes genéricos ou enganosos
- Lógica duplicada
- Código morto
- Wrappers ou abstrações que não agregam valor

### Etapa 3: aplicar alterações incrementalmente

Faça uma simplificação de cada vez.

Para cada simplificação:

1. Faça a mudança
2. Execute testes relevantes
3. Mantenha-o apenas se o comportamento for preservado

Separe a refatoração do trabalho de recursos sempre que possível.

### Etapa 4: verifique o resultado

Depois de simplificar, confirme:

- O código é genuinamente mais fácil de entender
- O diferencial é limpo e revisável
- As convenções do projeto ainda correspondem
- Nenhum comportamento, tratamento de erros ou efeitos colaterais foram alterados

## Adaptação ao projeto

- Use a linguagem e convenções reais do projeto; em TypeScript, prefira expressões claras à compactação
- Preservar comportamento, testes e ganchos de tempo de execução existentes
- Dê preferência a nomes explícitos e ajudantes menores e focados quando eles melhoram a legibilidade
- Mantenha os refatoradores com escopo restrito à tarefa ou revise o feedback

## Lista de verificação de verificação

- [ ] Os testes existentes passam sem modificação
- [ ] Build/typecheck/lint ainda passa
- [ ] Nenhum arquivo não relacionado foi refatorado
- [ ] Nenhum tratamento de erros foi enfraquecido ou removido
- [ ] O resultado é mais simples de revisar do que o original

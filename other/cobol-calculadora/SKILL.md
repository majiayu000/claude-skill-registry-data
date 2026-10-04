---
name: cobol-calculadora
description: Skill para criar calculadoras em COBOL usando GnuCOBOL. Use quando precisar criar uma calculadora ou operações matemáticas em COBOL.
---

# Skill: Calculadora COBOL

Este skill ensina como criar calculadoras em COBOL.
Use-o para criar programas matemáticos básicos.

## Quando Usar Este Skill

- Criar um programa COBOL novo
- Implementar operações matemáticas
- Trabalhar com entrada e saída em COBOL
- Declarar e usar variáveis numéricas

## Pré-requisitos

### GnuCOBOL
```bash
# macOS
brew install gnucobol

# Ubuntu/Debian
sudo apt-get install gnucobol

# Verificar instalação
cobc --version
```

## Estrutura Completa de uma Calculadora

### Arquivo: src/CALCULADORA.cbl

```cobol
      ******************************************************************
      * Programa: CALCULADORA
      * Descrição: Calculadora de soma em COBOL
      * Autor: Copilot Agent
      * Data: 2026
      * 
      * Este programa demonstra:
      * - Estrutura básica de um programa COBOL
      * - Entrada e saída de dados
      * - Operações aritméticas
      * - Formatação de números para display
      ******************************************************************
       IDENTIFICATION DIVISION.
      ******************************************************************
      * A IDENTIFICATION DIVISION identifica o programa.
      * É obrigatória e deve ser a primeira divisão.
      ******************************************************************
       PROGRAM-ID. CALCULADORA.
       AUTHOR. COPILOT-AGENT.
       DATE-WRITTEN. 2026.
       DATE-COMPILED.
      
       ENVIRONMENT DIVISION.
      ******************************************************************
      * A ENVIRONMENT DIVISION descreve o ambiente de execução.
      * Para programas simples, pode conter apenas configurações básicas.
      ******************************************************************
       CONFIGURATION SECTION.
       SOURCE-COMPUTER. PC.
       OBJECT-COMPUTER. PC.
      
       DATA DIVISION.
      ******************************************************************
      * A DATA DIVISION declara todas as variáveis do programa.
      * WORKING-STORAGE SECTION contém variáveis de trabalho.
      ******************************************************************
       WORKING-STORAGE SECTION.
      
      ******************************************************************
      * Variáveis para os números de entrada
      * PIC 9(5) significa: 5 dígitos numéricos (00000 a 99999)
      ******************************************************************
       01 WS-NUMERO-1          PIC 9(5) VALUE ZEROS.
       01 WS-NUMERO-2          PIC 9(5) VALUE ZEROS.
      
      ******************************************************************
      * Variável para o resultado
      * PIC 9(6) permite resultados até 999999
      ******************************************************************
       01 WS-RESULTADO         PIC 9(6) VALUE ZEROS.
      
      ******************************************************************
      * Variável formatada para exibição
      * Z suprime zeros à esquerda
      * Z(5)9 = até 5 zeros suprimidos + 1 dígito obrigatório
      ******************************************************************
       01 WS-RESULTADO-DISPLAY PIC Z(5)9.
      
      ******************************************************************
      * Constantes para mensagens
      ******************************************************************
       01 WS-LINHA             PIC X(40) VALUE ALL "=".
      
       PROCEDURE DIVISION.
      ******************************************************************
      * A PROCEDURE DIVISION contém a lógica do programa.
      * É dividida em parágrafos para organização.
      ******************************************************************
      
      ******************************************************************
      * INICIO - Parágrafo principal que controla o fluxo
      ******************************************************************
       INICIO.
           PERFORM EXIBIR-CABECALHO.
           PERFORM LER-NUMEROS.
           PERFORM CALCULAR-SOMA.
           PERFORM EXIBIR-RESULTADO.
           STOP RUN.
      
      ******************************************************************
      * EXIBIR-CABECALHO - Mostra o título do programa
      ******************************************************************
       EXIBIR-CABECALHO.
           DISPLAY WS-LINHA.
           DISPLAY "       CALCULADORA COBOL".
           DISPLAY "       Soma de Dois Numeros".
           DISPLAY WS-LINHA.
      
      ******************************************************************
      * LER-NUMEROS - Solicita os números ao usuário
      ******************************************************************
       LER-NUMEROS.
           DISPLAY " ".
           DISPLAY "Digite o primeiro numero (0-99999): ".
           ACCEPT WS-NUMERO-1.
           DISPLAY "Digite o segundo numero (0-99999): ".
           ACCEPT WS-NUMERO-2.
      
      ******************************************************************
      * CALCULAR-SOMA - Realiza a operação de soma
      ******************************************************************
       CALCULAR-SOMA.
           ADD WS-NUMERO-1 TO WS-NUMERO-2 
               GIVING WS-RESULTADO.
           MOVE WS-RESULTADO TO WS-RESULTADO-DISPLAY.
      
      ******************************************************************
      * EXIBIR-RESULTADO - Mostra o resultado formatado
      ******************************************************************
       EXIBIR-RESULTADO.
           DISPLAY " ".
           DISPLAY WS-LINHA.
           DISPLAY "RESULTADO DA SOMA".
           DISPLAY WS-LINHA.
           DISPLAY WS-NUMERO-1 " + " WS-NUMERO-2 " = " 
               WS-RESULTADO-DISPLAY.
           DISPLAY WS-LINHA.
           DISPLAY " ".
           DISPLAY "Programa encerrado com sucesso!".
```

## Comandos para Compilar e Executar

```bash
# Criar pasta do código fonte
mkdir -p src

# Compilar o programa
# -x = criar executável
# -o = nome do arquivo de saída
cobc -x -o calculadora src/CALCULADORA.cbl

# Executar
./calculadora

# Compilar com debug (para desenvolvimento)
cobc -x -debug -o calculadora src/CALCULADORA.cbl

# Apenas verificar sintaxe (não compila)
cobc -fsyntax-only src/CALCULADORA.cbl
```

## Saída Esperada

```
========================================
       CALCULADORA COBOL
       Soma de Dois Numeros
========================================
 
Digite o primeiro numero (0-99999): 
5
Digite o segundo numero (0-99999): 
3
 
========================================
RESULTADO DA SOMA
========================================
00005 + 00003 =      8
========================================
 
Programa encerrado com sucesso!
```

## Picture Clauses Úteis

```cobol
* Números inteiros
PIC 9        → 1 dígito (0-9)
PIC 9(5)     → 5 dígitos (00000-99999)
PIC 9(10)    → 10 dígitos

* Números com sinal
PIC S9(5)    → -99999 a +99999

* Números decimais
PIC 9(5)V99  → 5 inteiros + 2 decimais (V é decimal implícito)
PIC 9(3)V9(4) → 3 inteiros + 4 decimais

* Para exibição (suprime zeros)
PIC Z(5)9    → Suprime até 5 zeros, mantém pelo menos 1 dígito
PIC ZZZZ9    → Mesmo que acima
PIC -(4)9    → Como Z, mas mostra sinal negativo

* Texto
PIC X        → 1 caractere
PIC X(20)    → 20 caracteres
PIC A(10)    → 10 letras (apenas alfabético)
```

## Operações Matemáticas em COBOL

```cobol
* SOMA
ADD A TO B.                    (B = B + A)
ADD A TO B GIVING C.           (C = A + B)
ADD A B C TO D.                (D = D + A + B + C)

* SUBTRAÇÃO
SUBTRACT A FROM B.             (B = B - A)
SUBTRACT A FROM B GIVING C.    (C = B - A)

* MULTIPLICAÇÃO
MULTIPLY A BY B.               (B = B * A)
MULTIPLY A BY B GIVING C.      (C = A * B)

* DIVISÃO
DIVIDE A INTO B.               (B = B / A)
DIVIDE A INTO B GIVING C.      (C = B / A)
DIVIDE A BY B GIVING C REMAINDER D.

* COMPUTE (para expressões complexas)
COMPUTE C = A + B.
COMPUTE C = A * B + D / E.
COMPUTE C = (A + B) * (D - E).
```

## Dicas Importantes

1. **Colunas são críticas** - COBOL é sensível a posição
2. **Pontos são obrigatórios** - Toda sentença termina com ponto
3. **Área A vs Área B** - Divisões e parágrafos na A, código na B
4. **Nomes descritivos** - Use prefixos (WS-, etc) e hífens
5. **Documente tudo** - Comentários são bem-vindos em COBOL

## Divisão com Tratamento de Erro

A divisão exige verificação de divisão por zero — é a operação mais segura de se implementar com cuidado:

```cobol
      * Variáveis adicionais para divisão
       01 WS-RESULTADO-DIVISAO     PIC S9(10)V99 VALUE ZEROS.
       01 WS-RESULTADO-DIV-DISPLAY PIC -(9)9.99.

      ******************************************************************
      * CALCULAR-DIVISAO - Realiza a operação de divisão
      *                    Verifica divisão por zero antes de calcular
      ******************************************************************
       CALCULAR-DIVISAO.
           IF WS-NUMERO-2 = ZERO
               DISPLAY " "
               DISPLAY "ERRO: Divisao por zero nao e permitida!"
               DISPLAY " "
               STOP RUN
           ELSE
               DIVIDE WS-NUMERO-1 BY WS-NUMERO-2
                   GIVING WS-RESULTADO-DIVISAO
               MOVE WS-RESULTADO-DIVISAO
                   TO WS-RESULTADO-DIV-DISPLAY
           END-IF.
```

> ⚠️ **Nunca divida sem verificar o divisor!** Em COBOL, divisão por zero causa abend (encerramento abrupto do programa).

---

## 🏛️ Fluxo SDLC com OpenSpec e OpenSPDD

Ao criar novas calculadoras ou adicionar novas operações matemáticas (ex: exponenciação, módulo, raiz quadrada, logaritmo), siga obrigatoriamente o ciclo governado:

1. **[0] Explorar (`cobol-vibecoder`)**: Analisar tipos de dados necessários (inteiro, decimal implícito `V`, sinal `S`), limite de dígitos e impacto no menu.
2. **[1] Propose (`cobol-planner` / `opsx-propose`)**: Criar a proposta em `openspec/changes/<change>/` e validar com `openspec validate <change> --strict`.
3. **[1] Analysis (`cobol-planner` / `spdd-analysis`)**: Analisar colunas, novas variáveis de Working-Storage e tratamento de erros aritméticos (`ON SIZE ERROR`, divisão por zero) em `spdd/analysis/`.
4. **[1] Reasons-Canvas (`cobol-planner` / `spdd-reasons-canvas`)**: Estruturar o contrato executável de 7 dimensões em `spdd/prompt/`.
5. **[2] Generate (`cobol-coder` / `spdd-generate`)**: Promover fase para `apply`, implementar o código COBOL em `src/CALCULADORA.cbl`, compilar (`cobc -x`), passar nas fitness functions (`make fitness`) e atualizar o checklist do OpenSpec.

COBOL: 65+ anos e ainda contando! 🖥️

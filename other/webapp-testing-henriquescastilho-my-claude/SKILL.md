---
name: webapp-testing
description: Testar aplicacoes web locais usando Playwright. Usar automaticamente quando precisar verificar funcionalidade frontend, debugar UI, capturar screenshots, ou ver logs do browser.
allowed-tools: Bash Read Grep
---

# Teste de Aplicacoes Web -- Padrao DME

Toolkit para testar aplicacoes web locais usando Playwright.

## Fluxo

1. Verificar Playwright disponivel
2. Iniciar aplicacao local
3. Navegar, clicar, preencher formularios
4. Capturar screenshots como evidencia
5. Verificar logs do console

## Cenarios obrigatorios para qualquer feature nova

- Fluxo feliz completo (happy path)
- Formularios com dados invalidos
- Estados de loading e erro
- Responsividade (mobile, tablet, desktop)
- Navegacao por teclado (acessibilidade)

## Saida

- Lista de cenarios testados com resultado
- Screenshots dos pontos criticos
- Erros de console encontrados
- Correcoes necessarias

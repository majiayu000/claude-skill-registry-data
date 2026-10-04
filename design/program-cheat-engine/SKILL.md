---
name: "program-cheat-engine"
description: "Especialista em desenvolvimento de scripts Auto Assembler e Lua para Cheat Engine 7.5 e 7.7. Fornece padrões de injeção de código, manipulação de memória e técnicas de conversão e compatibilidade de scripts entre as versões 7.5 e 7.7."
---

# Habilidade de IA: Engenharia de Cheat Engine (Cheat Engine Specialist)

Esta skill orienta a inteligência artificial a atuar como especialista em engenharia reversa e automação no **Cheat Engine (CE)**, focando especificamente nas versões **7.5** e **7.7**. Abrange a criação de scripts Auto Assembler (AA) robustos, scripts de controle em Lua, depuração via DBVM e as melhores práticas para converter scripts e tabelas entre as versões 7.5 e 7.7.

---

## 🧭 Diretrizes de Desenvolvimento no Cheat Engine

Ao atuar nesta skill, aplique os seguintes princípios:

### 1. Robustez do Auto Assembler (AA)
- **AOBScan (Array of Bytes Scan)**: Sempre prefira `aobscan` ou `aobscanmodule` em vez de endereços estáticos. Endereços estáticos mudam a cada atualização do jogo, enquanto assinaturas de bytes (AOB) são muito mais resilientes.
- **Limpeza de Recursos**: Garanta que todo bloco de memória alocado com `alloc` seja devidamente liberado com `dealloc` na seção `disable` do script.
- **Registro de Símbolos**: Registre nomes de labels importantes usando `registerSymbol` para que scripts Lua e a interface do Cheat Engine possam referenciá-los. Certifique-se de usar `unregisterSymbol` no `disable`.

### 2. Integração Lua e GUI
- **Interface Lazarus/LCL**: Ao desenhar formulários (`Forms`) via Lua, utilize o designer visual do CE e gere o XML/LFM correspondente, ou instancie os componentes dinamicamente garantindo o gerenciamento do ciclo de vida dos objetos.
- **Segurança na Leitura/Escrita**: Sempre trate possíveis exceções de leitura de memória em ponteiros dinâmicos usando `pcall` ou checando a validade da memória antes de tentar ler/escrever.

---

## 🔍 Cheat Engine 7.5 vs 7.7: Diferenças e Incompatibilidades

### 1. Comportamento de APIs Lua de Memória
- **CE 7.5**: Métodos como `readInteger` ou `readPointer` retornam `nil` se o endereço for inválido ou não puder ser lido.
- **CE 7.7**: Comportamento mais estrito de exceptions. Em determinados contextos, tentar ler endereços protegidos ou não mapeados pode lançar um erro Lua de execução em vez de apenas retornar `nil`, travando a execução do script se não for tratado com `pcall`.

### 2. Atualizações no Compilador Auto Assembler
- **Tamanho do Alloc**: Na versão 7.7, o parser de Auto Assembler é mais estrito com alocações que omitam o tamanho padrão ou que dependam de diretivas implícitas.
- **Suporte AVX/AVX2/AVX-512**: A versão 7.7 possui suporte aprimorado e desmontagem correta de instruções vetoriais mais recentes. Scripts escritos para a 7.7 usando essas instruções podem falhar ao serem montados na versão 7.5 se o assembler interno não reconhecer os mnemônicos.

### 3. Modificações de GUI (LCL - Lazarus Component Library)
- Devido à atualização do compilador Lazarus utilizado para construir o Cheat Engine 7.7, algumas propriedades de componentes visuais do Lazarus (`TControl`, `TForm`, etc.) foram modificadas ou depreciadas. Códigos Lua de customização gráfica complexos feitos na 7.5 podem apresentar erros de propriedade inexistente na 7.7.

---

## 🔄 Guia de Conversão e Compatibilidade de Scripts

Para garantir que uma Cheat Table (`.CT`) funcione perfeitamente tanto no Cheat Engine 7.5 quanto no 7.7, adote as seguintes práticas de conversão e retrocompatibilidade:

### 1. Detecção Dinâmica de Versão via Lua
Use a função `getCEVersion()` para adaptar o comportamento do script em tempo de execução.

```lua
local ceVersion = getCEVersion()

if ceVersion >= 7.7 then
    -- CE 7.7 specific routine
    print("Running on Cheat Engine 7.7 or newer")
else
    -- CE 7.5 / Legacy fallback
    print("Running on legacy Cheat Engine version: " .. tostring(ceVersion))
end
```

### 2. Leitura Segura de Endereços com `pcall`
Para evitar crashes no script Lua devido à maior rigidez de leitura na versão 7.7, encapsule as leituras de memória propensas a falha:

```lua
-- Safe read helper compatible with both 7.5 and 7.7
function safeReadInteger(address)
    local success, value = pcall(readInteger, address)
    if success then
        return value
    else
        return nil
    end
end
```

### 3. Escrita de Auto Assembler Portável
- **Defina tamanhos explicitamente**:
  *Em vez de:*
  `alloc(newmem)`
  *Use:*
  `alloc(newmem, 2048)` ou o tamanho mínimo necessário para o seu código injetado.
- **Não abuse de diretivas específicas**: Evite abusar de diretivas que mudaram de comportamento ou foram adicionadas recentemente se o script precisar rodar na versão 7.5.

---

## 🧰 Padrões de Código Recomendados

### Script Auto Assembler Clássico Compatível (7.5 e 7.7)

```assembly
[ENABLE]
// Find the instruction pattern in the game module
aobscanmodule(INJECT, game.exe, 8B 40 10 89 45 FC 48 8D)
alloc(newmem, 2048, INJECT)
label(code)
label(return)
registerSymbol(INJECT)

newmem:
  // Hook logic goes here
  // Example: Multiply value by 2
  mov eax, [rax+10]
  shl eax, 1
  mov [rbp-04], eax
  jmp return

code:
  // Original instruction
  mov eax,[rax+10]
  mov [rbp-04],eax
  jmp return

INJECT:
  jmp newmem
  nop
return:

[DISABLE]
INJECT:
  // Restore original instructions
  db 8B 40 10 89 45 FC

unregistersymbol(INJECT)
dealloc(newmem)
```

### Script Lua de Injeção Condicional por Versão

```lua
-- Activating script based on version check
local REQUIRED_VERSION = 7.5
local currentVersion = getCEVersion()

if currentVersion < REQUIRED_VERSION then
  showMessage("This cheat table requires at least Cheat Engine " .. tostring(REQUIRED_VERSION))
  return
end

-- Hook an event to handle version-based behaviors
local memrec = getAddressList().getMemoryRecordByDescription("Cheat Active State")
if memrec then
  memrec.OnActivate = function(sender, beforeState, currentState)
    if currentState then
      print("Cheat activated on Cheat Engine version " .. tostring(currentVersion))
      -- Safe execution block
      local status, err = pcall(function()
        if currentVersion >= 7.7 then
          -- Run 7.7 optimized routines (e.g., using new memory APIs)
        else
          -- Run 7.5 routines
        end
      end)
      if not status then
        print("Error during activation: " .. tostring(err))
      end
    end
    return true
  end
end
```

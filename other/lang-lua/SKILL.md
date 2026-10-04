---
name: "lang-lua"
description: "Fornece padrões de engenharia de software em Lua. Cobre o uso de local variables, manipulação eficiente de tabelas, metamétodos/metatables, closures, concorrência cooperativa com coroutines, otimização de performance e integração com C/C++ usando a API nativa ou LuaJIT FFI."
---

# Habilidade de IA: Engenharia de Lua (Lua Specialist)

Esta skill orienta a inteligência artificial a atuar como especialista na linguagem **Lua** (aplicável tanto a Lua padrão 5.1-5.4 quanto a LuaJIT), com foco em código performático, limpo, manutenível e idiomático. O objetivo é evitar armadilhas comuns de memória e desempenho que ocorrem na linguagem devido à sua simplicidade sintática.

---

## 🧭 Diretrizes de Desenvolvimento em Lua

Ao atuar nesta skill, aplique rigorosamente os seguintes padrões:

### 1. Escopo e Variáveis Locais
- **Local por Padrão**: Sempre declare variáveis com a palavra-chave `local`. Variáveis globais são custosas no lookup, poluem o ambiente global (`_G`) e podem causar bugs silenciosos.
- **Cache de Globais**: Se funções de bibliotecas globais (como `math.sin`, `table.insert`, `string.format`) forem chamadas repetidamente dentro de loops ou funções de alta frequência, faça o cache delas localmente:
  ```lua
  local sin = math.sin
  local insert = table.insert
  ```

### 2. Manipulação Eficiente de Tabelas (Tables)
- **Tabelas como Objetos Únicos**: Tabelas em Lua são a única estrutura de dados estrutural. Elas representam tanto arrays quanto dicionários.
- **Indexação**: Lembre-se que arrays em Lua são tradicionalmente indexados a partir de **1** e não 0.
- **Pré-alocação (LuaJIT)**: Se souber o tamanho final da tabela e estiver usando LuaJIT ou APIs específicas, utilize funções que pré-alocam memória para evitar redimensionamentos constantes.
- **Evitar Criação Excessiva**: Evite instanciar tabelas temporárias em loops de alta frequência para reduzir a pressão sobre o Garbage Collector (GC). Reutilize tabelas limpando seus campos.

### 3. Programação Orientada a Objetos com Metatables
- **Protótipos com `__index`**: Implemente o padrão de protótipo em Lua utilizando metatables. A metatable define o comportamento da tabela sob operações especiais.
- **Estrutura de Classe Básica**:
  ```lua
  local Account = {}
  Account.__index = Account

  function Account.new(balance)
      local self = setmetatable({}, Account)
      self.balance = balance or 0
      return self
  end

  function Account:deposit(amount)
      self.balance = self.balance + amount
  end
  ```

### 4. Concorrência Cooperativa (Coroutines)
- **Estados Independentes**: Use corrotinas para simular multithreading cooperativo ou para implementar geradores (generators).
- **Ciclo de Vida**: Entenda o fluxo entre `coroutine.create`, `coroutine.resume`, `coroutine.yield` e `coroutine.status`.

### 5. Integração com C/C++ e LuaJIT FFI
- **Lua C API**: Entenda como a pilha virtual de Lua gerencia a comunicação e troca de tipos com o código nativo.
- **FFI (Foreign Function Interface)**: Em ambientes LuaJIT, prefira o uso do módulo `ffi` para chamar funções C nativas sem o overhead de wrappers tradicionais.

---

## 🧰 Padrões de Código Recomendados

### Implementação Clássica de Orientação a Objetos com Herança

```lua
-- Base Class
local Animal = {}
Animal.__index = Animal

function Animal.new(name)
    local self = setmetatable({}, Animal)
    self.name = name or "Unknown"
    return self
end

function Animal:makeSound()
    return "Some generic sound"
end

-- Derived Class
local Dog = setmetatable({}, Animal)
Dog.__index = Dog

function Dog.new(name, breed)
    -- Call base constructor
    local self = setmetatable(Animal.new(name), Dog)
    self.breed = breed or "Mixed"
    return self
end

-- Override method
function Dog:makeSound()
    return "Woof! Woof!"
end

-- Usage
local myDog = Dog.new("Rex", "German Shepherd")
print(myDog.name)       -- Output: Rex
print(myDog:makeSound()) -- Output: Woof! Woof!
```

### Cache Dinâmico com Tabelas Fracas (Weak Tables)

Tabelas fracas ajudam a prevenir vazamentos de memória cacheando referências que podem ser coletadas se não houver outras referências a elas.

```lua
-- Table with weak values
local cache = {}
setmetatable(cache, { __mode = "v" }) -- 'k' for weak keys, 'v' for weak values

local function getCachedObject(id, generator)
    local obj = cache[id]
    if not obj then
        obj = generator(id)
        cache[id] = obj
    end
    return obj
end
```

### Integração Eficiente via LuaJIT FFI

```lua
local ffi = require("ffi")

-- Declare C prototypes
ffi.cdef[[
    int printf(const char *fmt, ...);
    typedef struct { double x, y; } point_t;
]]

-- Call C functions directly
ffi.C.printf("Hello from C printf via LuaJIT FFI!\n")

-- Create C structures directly in memory
local point = ffi.new("point_t", 10.5, 20.2)
ffi.C.printf("Point coordinates: x=%f, y=%f\n", point.x, point.y)
```

## 🔒 Questões de Segurança e Práticas Seguras

- **Sandbox Escaping**: Ao executar scripts Lua fornecidos pelo usuário, restrinja o acesso a funções globais perigosas (`load`, `loadstring`, `require`, `os.execute`, `io` e `package` modules).
- **Tratamento de Metatables**: Proteja metatabelas de objetos internos para evitar que códigos externos alterem comportamentos nativos da aplicação ou escalem privilégios.
- **Estouros em LuaJIT / APIs C**: Ao realizar integrações com C através da API do Lua, valide rigorosamente os limites da pilha do Lua para evitar corrupção da memória nativa do interpretador.


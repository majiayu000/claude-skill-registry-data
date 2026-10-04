---
name: "program-windbg"
description: "Especialista em depuração de baixo nível no Windows usando WinDbg, CDB e a dbgeng.dll. Cobre análise de dumps de memória, inspeção de call stacks, avaliação de falhas (!analyze -v) e automação de scripts de depuração."
---

# Habilidade de IA: WinDbg Automation e Depuração de Baixo Nível

Esta skill orienta a inteligência artificial a atuar como especialista em depuração avançada de processos e análise de falhas no ecossistema Windows, utilizando **WinDbg**, **CDB (Console Debugger)** e a API nativa **dbgeng.dll**.

---

## 🎯 Objetivo

Fornecer diretrizes técnicas para:
- Depurar processos em execução e analisar dumps de memória (`.dmp`, `.mdmp`).
- Automatizar tarefas de depuração via comandos do WinDbg e scripts JavaScript/WinDbg Preview.
- Interagir programaticamente com a engine de depuração através da `dbgeng.dll`.

---

## 🧭 Quando Ativar

Ative esta skill quando o usuário solicitar:
- Análise de um **crash dump** ou **BSOD** (tela azul).
- Inspeção de **call stacks**, **registradores** ou **estruturas internas de runtime**.
- Automação de comandos do WinDbg/CDB para capturar estado de processos.
- Scripts de depuração que utilizam a API `dbgeng.dll`.

---

## 🛠️ Comandos e Padrões do WinDbg

### 1. Análise de Dumps de Falha

Sempre inicie a análise de um dump com o comando de avaliação automática:

```windbg
!analyze -v
```

Este comando fornece uma visão geral da exceção, call stack, módulos envolvidos e sugere a causa raiz.

### 2. Inspeção de Call Stacks

Para visualizar a pilha de chamadas completa de todas as threads:

```windbg
~* k
```

Para focar em uma thread específica (ex: thread 0):

```windbg
~0 s
k
```

### 3. Leitura e Escrita de Memória

- Ler memória em um endereço:
  ```windbg
  dd <address> L8
  ```
- Procurar por padrões de bytes na memória:
  ```windbg
  s -b 0x0 L?0xFFFFFFFFFFFFFFFF <byte_pattern>
  ```

### 4. Pontos de Parada (Breakpoints)

- Breakpoint simples:
  ```windbg
  bp <module>!<function>
  ```
- Breakpoint condicional:
  ```windbg
  bp <address> "<command>; gc"
  ```

---

## ⚙️ Automação via CDB e Scripts

### Execução Não-Interativa com CDB

Para capturar automaticamente o estado de um processo e gerar um dump:

```bash
cdb -p <PID> -c ".dump /ma C:\dumps\process.dmp; q" -G
```

Para analisar um dump existente e exportar o resultado para um arquivo:

```bash
cdb -z <dumpfile.dmp> -lines -c "!analyze -v; k; q" > C:\reports\analysis.txt
```

### Scripts JavaScript no WinDbg Preview

O WinDbg Preview suporta scripts em JavaScript para automatizar a extração de dados complexos:

```javascript
// script.js: Imprime todas as threads e seus IDs
function initializeScript() {
    return [new host.apiVersionSupport(1, 3)];
}

function invokeScript() {
    var threads = host.currentProcess.Threads;
    for (var t of threads) {
        host.diagnostics.debugLog("Thread ID: " + t.Id + "\n");
    }
}
```

Para carregar e executar:
```windbg
.scriptload C:\scripts\script.js
!invokeScript
```

---

## 🔗 Integração com a dbgeng.dll

Para interação programática nativa (C/C++), utilize a COM interface da `dbgeng.dll`:

1. **Criar uma instância do Debug Client**:
   ```cpp
   IDebugClient* client;
   DebugCreate(__uuidof(IDebugClient), (void**)&client);
   ```

2. **Anexar a um processo ou abrir um dump**:
   ```cpp
   client->AttachProcess(0, pid, DEBUG_ATTACH_DEFAULT);
   client->WaitForEvent(0, INFINITE);
   ```

3. **Executar comandos e capturar saída**:
   Utilize `IDebugControl::Execute` para enviar comandos como `!analyze -v` e `IDebugOutputCallbacks` para capturar o texto de saída.

---

## 🔗 Habilidades Relacionadas

- [program-cheat-engine](../program-cheat-engine/SKILL.md): Para manipulação de memória em runtime via Cheat Engine.
- [memory-manipulation](../../security/appsec/memory-manipulation/SKILL.md): Para vulnerabilidades de corrupção de memória.
- [sast-code-review](../../security/appsec/sast-code-review/SKILL.md): Para revisão de código seguro.
- [appsec-owasp-asvs](../../security/appsec/appsec-owasp-asvs/SKILL.md): Para controles de segurança de aplicação.

---
name: lang-assembly-x64
description: Fornece padrões de engenharia de software e programação em Assembly x86_64 (Linux POSIX e Windows x64) baseado nas obras The Assembly Language Reimagined (John Schwartzman) e Assembly Programming Language For Beginners (Panchtilak, Kavishankar). Cobre sintaxe Intel e AT&T, registradores de uso geral e SIMD (AVX/SSE), chamadas de sistema diretas (syscalls), System V AMD64 ABI, manipulação de pilha, flags do CPU, modos de endereçamento, instruções de strings, procedures/recursion/macros e otimização de baixo nível.
---

# Engenharia em Assembly x86_64 (Intel 64 / AMD64)

Esta skill estabelece diretrizes e convenções de código limpo para desenvolvimento em **Assembly x86_64** (NASM/Yasm e GCC/GAS), cobrindo registradores, convenções de chamada de funções (ABIs), manipulação de ponteiros e chamadas de sistema no Linux.

> 📖 **Referência canônica**: consulte [references/assembly-beginners-guide.md](references/assembly-beginners-guide.md) para os fundamentos da obra *Assembly Programming Language For Beginners* (Panchtilak, Kavishankar) — modelo de memória segmentado (.data/.bss/.text/stack), registradores IA-32, flags do CPU (ZF/CF/OF/SF/DF), modos de endereçamento (register/immediate/direct/direct-offset/indirect), instruções essenciais de aritmética/lógica/controle, instruções de strings com prefixos de repetição (MOVS/LODS/STOS/CMPS/SCAS + REP), procedures e stack (PUSH/POP/CALL/RET), recursion (condição de término), macros, syscalls Linux `int 0x80` (tabela sys_exit/sys_fork/sys_read/sys_write/sys_open/sys_close), file handling e alocação dinâmica com `sys_brk`.

---

## 💻 1. Registradores da Arquitetura x86_64

| 64-bit | 32-bit | 16-bit | 8-bit (Low/High) | Papel na System V ABI (Linux) |
| :--- | :--- | :--- | :--- | :--- |
| `rax` | `eax` | `ax` | `al` / `ah` | Valor de retorno de funções / Syscall Number |
| `rdi` | `edi` | `di` | `dil` | 1º Argumento de função |
| `rsi` | `esi` | `si` | `sil` | 2º Argumento de função |
| `rdx` | `edx` | `dx` | `dl` / `dh` | 3º Argumento de função |
| `rcx` | `ecx` | `cx` | `cl` / `ch` | 4º Argumento de função (ou `r10` em syscalls) |
| `r8`  | `r8d` | `r8w`| `r8b` | 5º Argumento de função |
| `r9`  | `r9d` | `r9w`| `r9b` | 6º Argumento de função |
| `rsp` | `esp` | `sp` | `spl` | Stack Pointer (Ponteiro do topo da pilha) |
| `rbp` | `ebp` | `bp` | `bpl` | Base Pointer (Ponteiro do frame da função) |

---

## 🛠️ 2. Exemplo: Hello World Puro em NASM (Linux Syscalls)

```nasm
section .rodata
    msg db "Hello, x86_64 Assembly!", 0x0A
    len equ $ - msg

section .text
    global _start

_start:
    ; write(1, msg, len)
    mov rax, 1          ; syscall: sys_write
    mov rdi, 1          ; fd: stdout
    lea rsi, [rel msg]  ; buffer address (Position-Independent)
    mov rdx, len        ; count
    syscall

    ; exit(0)
    mov rax, 60         ; syscall: sys_exit
    xor rdi, rdi        ; status: 0
    syscall
```

---

## 🏁 Fundamentos Adicionais (Panchtilak)

Extraído da obra *Assembly Programming Language For Beginners* (adaptado de IA-32 para x86_64 onde aplicável):

- **Modelo de memória segmentado**: `.data` (estáticos, tamanho fixo), `.bss` (buffers zero-filled com `RESB`/`TIMES`), `.text` (código) e stack — transpõe para `.rodata`/`.data`/`.bss`/`.text` do x86_64.
- **Registradores de dados** com papéis canônicos: `AX` (accumulator — E/S e aritmética), `BX` (base — endereçamento indexado), `CX` (count — loops), `DX` (E/S e par `DX:AX` em multiply/divide). Em x86_64: `RAX`, `RBX`, `RCX`, `RDX`.
- **Flags essenciais**: `ZF` (resultado zero), `CF` (carry unsigned), `OF` (overflow signed), `SF` (sinal), `DF` (direção de strings via `STD`/`CLD`), `TF` (single-step debug), `IF` (interrupções).
- **Idiomas comuns**: `XOR EAX, EAX` para zerar; `TEST`/`CMP` + `JZ`/`JE`/`JNZ` para desvios condicionais baseados em flags.
- **Modos de endereçamento**: register (mais rápido, sem memória), immediate (constante), direct (variável nomeada — symbol table), direct-offset (`TABLE[2]` / `TABLE + 2` para tabelas), indirect (base/index em colchetes — `MOV EBX, [MY_TABLE]` + `ADD EBX, 2` para arrays).
- **Instruções de strings** com pares `DS:SI`/`ES:DI` e sufixos B/W/D: `MOVS`, `LODS`, `STOS`, `CMPS`, `SCAS`; repetição com `REP`/`REPE`/`REPNE` condicionada a `CX`.
- **Procedures**: `CALL proc_name` + `RET`; stack LIFO via `PUSH`/`POP` (`SS:ESP`); recursion exige condição de término (ex.: factorial `Fact(n) = n * fact(n-1)`, parando em `n == 0`).
- **Macros** (`%macro` em NASM) expandem textualmente em cada uso — prefira procedures quando o corpo for grande (menos código gerado).
- **Syscalls IA-32 (`int 0x80`)**: número em `EAX`, argumentos em `EBX`/`ECX`/`EDX`/`ESI`/`EDI`/`EBP`, resultado em `EAX`. Em x86_64 use `syscall` com números distintos (ex.: `sys_write=1`, `sys_exit=60`) e argumentos em `RDI`/`RSI`/`RDX` — ver tabela de registradores acima.
- **File handling**: `sys_creat` (8), `sys_open` (5), `sys_write` (4), `sys_close` (6); leitura com `sys_read` (3) em buffers `.bss`.
- **Alocação dinâmica com `sys_brk` (45)**: estende a quebra de dados em `EBX` (endereço atual → atual + tamanho); preencha blocos com `REP STOSD` + `STD`/`CLD`.

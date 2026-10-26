---
name: x86-64-assembly
description: Use when writing x86-64 assembly for Linux — small programs without libc that use raw system calls, parsing text from standard input, integer arithmetic and decimal output, NASM or GNU as with Make, and debugging with gdb. Also use when an assembly program crashes on start, prints garbage, or behaves differently when input is piped.
---

# x86-64 assembly (Linux, no libc)

Default: NASM (Intel syntax) or GNU `as`, `ld` directly with `_start` as the entry point, System V AMD64 conventions for your own functions, Linux syscalls for I/O, a `Makefile` with `build` and `test` targets.

## Minimal program

```nasm
section .text
global _start
_start:
    mov  eax, 60        ; sys_exit
    xor  edi, edi       ; status 0
    syscall
```

```make
prog: prog.o ; ld -o $@ $<
prog.o: prog.asm ; nasm -f elf64 -g -F dwarf -o $@ $<
```

## Syscall conventions

| Item | Register |
|---|---|
| Syscall number | `rax` |
| Arguments 1–6 | `rdi`, `rsi`, `rdx`, `r10`, `r8`, `r9` |
| Return value | `rax` (negative = `-errno`) |
| Clobbered by `syscall` | `rcx`, `r11` |

Common numbers: `read` 0, `write` 1, `exit` 60. Check them against the kernel's table, not memory.

## Reading standard input correctly

- `read` may return fewer bytes than requested, especially from pipes; loop until it returns 0 (EOF).
- Process the buffer as a stream: a number can be split across two reads, so keep parser state (current value, "inside a number") across iterations.
- Treat a negative return as an error and exit non-zero.

## Example: summing amounts in text

1. Scan bytes; when a digit starts, accumulate `value = value * 10 + (byte - '0')`.
2. Decide which numbers count (e.g. only those followed by a currency marker or on lines with a keyword) and document the rule.
3. Add to a 64-bit total; check for overflow with `jo` after `add` if inputs are untrusted.
4. Convert the total to decimal by repeated `div` by 10 into a buffer filled from the end, then one `write`.

## Your own functions

- Follow System V: arguments in `rdi, rsi, rdx, rcx, r8, r9`, return in `rax`; preserve `rbx, rbp, r12–r15`.
- Keep `rsp` 16-byte aligned before `call` if you ever call C code.

## Verification loop

1. Build with debug info; run under `gdb` (`layout regs`, `stepi`) for the first versions.
2. A test script that pipes known inputs (including empty input, input split across lines, very long input) and compares the output and exit status.
3. `strace ./prog < input` shows every syscall and its return value — the fastest way to see a wrong argument.

## Pitfalls

- **Writing to a 32-bit register zero-extends** into the 64-bit one (`mov eax, 1` clears the top half); writing 8/16-bit parts does not.
- **`div` uses `rdx:rax`** as the dividend; clear `rdx` (`xor edx, edx`) first or you get a wrong result or a crash.
- **`rcx` and `r11` are destroyed by `syscall`;** do not keep loop counters there.
- **No libc means no buffered I/O:** batch output into a buffer and write once.
- **Exit properly:** falling off the end of `_start` executes whatever bytes follow.

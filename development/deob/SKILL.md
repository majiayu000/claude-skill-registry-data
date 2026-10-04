---
name: deob
description: Inspect, compare, and deobfuscate Java (jar) and native (DLL/EXE) targets. Use for read-only gamepack validation, recovered-source comparisons, offset/interaction/opcode extraction, or authorized transformations that make obfuscated clients readable, renamed, or rebuildable.
---

# Deobfuscation — Java & Native

Inspect recovered behavior, compare exact artifacts, or transform obfuscated clients into readable source
and offset/interaction maps within the requested scope.

## Choose the task path

- **Investigate or compare:** answer the specific behavior, field-usage, offset, or parity question from
  the relevant artifacts. Keep originals, source, and project docs unchanged; use scratch decompiles or
  analysis outputs as needed. Findings do not authorize renaming, transformation, rebuilding, or live hooks.
- **Transform or rebuild:** use the pipelines below when requested or covered by existing authorization.
  Preserve the original artifact and an auditable mapping from it to each transformed output.
- Read the project's **`docs/DEOB_KNOWLEDGE.md`**, if present, before repeating investigations. Treat its
  offsets, target profile, tools, and dead-ends as leads to verify against the current target. Update it when
  project documentation changes are in scope; for read-only work, report findings inline instead.
- Keep explanations technical and specific. State uncertainty where evidence runs out.

## Golden rules
1. **Match proof to the claim.** A runtime claim needs observation of the requested behavior on the actual
   target. Attachment, loading, or startup logs prove only that stage. Keep source/bytecode findings, build
   results, and live behavior distinct; say what remains unverified.
2. **Decompile, don't scan.** Blind memory scanning can't find pointer-hidden fields. Anchor on strings.
3. **Conservative transforms only.** A pass that guesses yields brace-balanced but semantically wrong code.
   Rewrite only when the transition is provably constant; verify at the bytecode level (javap the before/after)
   when a transform looks risky. Leave everything else untouched.
4. **Keep provenance with findings.** Record the input path and SHA-256, available version/build identity,
   and the relevant class/member descriptor or native address basis. Identify whether source was recovered
   from that input, copied from another version, or rebuilt; a source revision alone does not identify a
   deployed binary.

## Read-only investigation and comparison

- Trace the requested path and its relevant callers. Compare the exact target bytecode/disassembly with
  recovered source; use targeted dumps such as `javap -p -c -v -classpath target.jar pkg.Class` before
  broad decompilation when they can settle the question.
- A copied sibling source file or a second view of the same recovery is not independent corroboration.
  Establish mappings against the target's own artifact, and label any missing side of a comparison.
- For Java constant fields, absence of a field-name or `GETSTATIC` reference does not prove non-use:
  compile-time constants can be inlined. Inspect candidate callers and literal/data flow; a matching
  literal alone does not prove provenance either. See [JLS 13.1](https://docs.oracle.com/javase/specs/jls/se21/html/jls-13.html#jls-13.1).
- Report the relevant matches, differences, and unresolved behavior. Stop once the requested comparison
  is supported; do not turn it into a full cleanup, transformation, or coverage exercise.

## Environment gotchas (Windows, learned the hard way)
- **`java` on PATH may be a JDK-11 + agent shim** (e.g. OpenLogic JDK 11 with a `Dumper` javaagent that spams
  "illegal reflective access" and injects into every JVM). Modern Ghidra needs JDK 21. Force it: set
  `JAVA_HOME` **and** `JAVA_HOME_OVERRIDE` to a real JDK 21, prepend its `bin` to PATH, clear
  `JAVA_TOOL_OPTIONS`. Verify the reflective-access warning is gone.
- **`sed` strips Windows backslashes** in path edits — use a real editor, not sed/regex, for paths in files.
- **`jar xf` on Windows drops `$`-named and reserved-name (`aux`,`con`,`nul`) classes.** Extract/repack
  obfuscated jars with Python `zipfile`.
- **javac "abort illusion":** a parse error halts semantic analysis so the error count looks tiny until the
  parse errors are fixed. Don't trust a low count until it parses.
- **Ghidra headless: run from PowerShell**, redirect output to a file (`*> log`); bash mangles the `.bat` args.

## Step 0 — profile the target first (the profile picks the tools)

| Symptom | Layer | Counter |
|---|---|---|
| homoglyph/`iIiII`/`lICl` class+member names; every literal is a `decrypt("…")`/`Ii(String)` call | **name obf + string encryption** | build an `@Orig`/mapping table; statically execute the pure per-class decrypt method and inline |
| clean names but `int s=…; while(true){switch(s ^ k){… s=…;}}` | **control-flow flattening** | ASM deflattener (below) + re-decompile with Vineflower |
| literals as `OP(3 >> 1)` / `(86 & 47)` / `~x`/`x^const` arithmetic | **numeric-constant obf** | constant-fold to literals |
| `int a, int a, int a` params; one LVT name for all slots | **poisoned LocalVariableTable** | strip LVT + MethodParameters before decompile; `--variable-renaming=jad` |
| `CONST = new EnumType(<builder chain>)` in a static block | **builder-enum obf** | execute the builder chain to recover values (nulled if native-unplugged → flag unreliable) |
| always-true guards `if((x*x-x)%2==0)`; dead `while(false){}` | **opaque predicates / dead code** | constant-fold the predicate; strip provably-dead blocks |
| methods split into tiny fragments called once | **method splitting / inlining obf** | inline single-caller privates during cleanup |
| indy call sites resolving constants at runtime | **invokedynamic obf** | resolve the bootstrap statically, replace with the constant/ldc |

## Java transformation pipeline (readable + renamed)

1. **Deflatten (bytecode, ASM).** `ControlFlowDeflattener` constant-tracks the `state`/`key` locals, resolves
   each case successor, retargets constant back-edge gotos straight to the real case label, strips the poisoned
   LVT, and (with DSE on) removes the now-dead constant stores to the state/key slots so the decompile reads
   clean. Handles conditional-dispatch that source-level tools can't. Run on the WHOLE jar (its ClassWriter
   needs the jar on its classloader for COMPUTE_FRAMES):
   ```powershell
   $cp = "asm-9.7.jar;asm-tree-9.7.jar;asm-analysis-9.7.jar;asm-commons-9.7.jar;."
   java -cp $cp ControlFlowDeflattener in.jar out-deflat.jar   # prints methods matched / gotos rewired
   ```
   **Verify risky methods at bytecode level**: `javap -p -c -classpath out-deflat.jar pkg.Class` and confirm
   the real data path (e.g. an `iload_3` feeding a constructor) survived — Vineflower may reuse a var *name*
   for a dead store, which looks wrong but is correct if the bytecode load is unchanged.
2. **Re-decompile with Vineflower** (beats CFR/Fernflower on flattened CFGs). Carve the target package with
   Python zipfile first (avoids `$`-class loss); pass the full deflat jar as `-e` classpath for type
   resolution:
   ```powershell
   java -jar vineflower.jar --use-lvt-names=0 --variable-renaming=jad -e="full-deflat.jar" target.jar outdir
   ```
3. **Rename to readable identifiers.**
   - If the target keeps real names (many mixin clients do), only *locals* are generic (`var0`,`i`,`j`) — DSE
     + jad naming already gets it 90% there; rename the remaining hot locals by meaning as you read.
   - If names are obfuscated, build a mapping: derive names from string constants, exception messages, JNI
     signatures, enum `.name()` values, log lines, and known-superclass method overrides; apply via an
     ASM `Remapper` (`SimpleRemapper` with a name map) or record in an `@Orig("a.b.c")` annotation map so the
     original⇄clean mapping is auditable. Rename in dependency order; keep the map in the knowledge doc.
4. **Cleanup pass:** constant-fold numerics, strip `while(false){}`, inline single-caller privates, drop
   synthetic `$` switch-map/lambda noise classes.

## Native pipeline (DLL/EXE) — Ghidra headless

Setup once (see env gotchas), import + auto-analyze (~85s/MB), then run extraction post-scripts:
```powershell
$env:JAVA_HOME=$jdk21; $env:JAVA_HOME_OVERRIDE=$jdk21; $env:PATH="$jdk21\bin;$env:PATH"; $env:JAVA_TOOL_OPTIONS=''
& $analyzeHeadless <projDir> <proj> -import <target.dll> -overwrite *> import.log
& $analyzeHeadless <projDir> <proj> -process <target.dll> -noanalysis -scriptPath <dir> -postScript Extract.java *> ex.log
```
Extraction scripts (GhidraScript, output to a flat dir):
- **Dump-all:** every function (addr/name/size), all strings (+xref counts), symbols/imports/exports, and full
  `decompiled.c`. Strings are your anchors.
- **Mixin/RegisterNatives mapper:** RuneLite-style mixin clients build the `JNINativeMethod` table
  (`{char* name; char* sig; void* fn}`) *in code* (LEA name; LEA sig; LEA fn). For each method-name string,
  walk its code xref to the adjacent function pointer and decompile it → the offset chains `*(obj+0xNN)` live
  there. This maps every `getX`/`setX` native → its exact offset.
- **Targeted range/function dumps** for a specific cluster (e.g. login natives) to nail exact offsets.

Native primitives you'll recognize:
- `GetModuleHandleW(NULL)` = the EXE's **image base**; image-relative globals/routines are `imageBase + RVA`.
- `!IsBadReadPtr(p,n)` may appear as a target-side guard; preserve it when interpreting the original flow,
  but do not treat it as a safety guarantee or introduce it as a memory-safety solution. Microsoft marks
  it [obsolete and unsafe as a validity guarantee](https://learn.microsoft.com/en-us/windows/win32/api/winbase/nf-winbase-isbadreadptr).
- mixin getter = `obj = GetLongField(this, address); probe(obj+off); return *(obj+off);`
- **When live capture is authorized, capture opcodes from real clicks** with a capture-only doAction hook
  (log opcode/id/tile on each action). Otherwise use static evidence and leave live verification pending;
  never guess opcodes.
- Login is usually in-memory, not packet-faking: write session/step into client globals, then call the
  client's own login routine (e.g. `*(imageBase+STEP)=n; ((void(*)(bool))(imageBase+ROUTINE))(useX)`), and/or
  set the launcher env vars (`JX_ACCESS_TOKEN`/`JX_REFRESH_TOKEN`/`JX_SESSION_ID`/…) the client reads at boot.

## Cross-validate and complete the requested work
- Corroborate each offset against a second source (a neighbouring known field, a second getter that reads the
  same struct, or an authorized live debug socket). State the evidence and confidence in the findings.
- For authorized implementation, fold offsets into the project's native header, dated and cross-referenced.
  Replicate interactions from verified data flow with the project's valid memory-access and lifetime handling.
  Keep live behavior pending until the requested interaction is observed on the identified target.
- Update `DEOB_KNOWLEDGE.md` only when documentation changes are in scope. Send webhook progress only
  under active user authorization for that destination and reporting task; a running loop alone is not
  authorization. Honor stops and cancellations, including stopping task-owned reporting loops.

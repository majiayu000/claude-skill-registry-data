---
name: frida-tracing-discovery
description: Discover Frida hook points with frida-trace, class and method enumeration, module/export/import/symbol discovery, stack traces, Stalker, and probe narrowing.
---

# Frida Tracing Discovery

Use this skill when the target API, class, symbol, or call path is unknown.

## Start Broad, Then Narrow

1. Prove the behavior happens without Frida.
2. Choose the highest-signal boundary: network, crypto, file, IPC, WebView, class loading, native library loading, or UI action.
3. Trace or enumerate around that boundary.
4. Add stack traces to identify app-owned callers.
5. Replace broad probes with narrow hooks.

## CLI Tracing

```bash
frida-trace -U -f com.example.app -j 'java.net.URL!*' --no-pause
frida-trace -U -f com.example.app -i 'open' -i 'connect' --no-pause
frida-trace -U -n target -m 'Module!*pattern*'
```

Treat generated handlers as temporary discovery artifacts, then move proven logic into a reviewed script.

## Android Discovery

```js
Java.perform(() => {
  const groups = Java.enumerateMethods("*crypto*!*/isu");
  console.log(JSON.stringify(groups, null, 2));
});
```

Class loader check:

```js
Java.perform(() => {
  Java.enumerateClassLoaders({
    onMatch(loader) {
      try {
        Java.classFactory.loader = loader;
        Java.use("com.example.Target");
        console.log("loader", loader);
      } catch (_) {}
    },
    onComplete() {}
  });
});
```

## Native Discovery

```js
const mod = Process.getModuleByName("libtarget.so");
for (const e of mod.enumerateExports()) {
  if (e.name.includes("SSL") || e.name.includes("crypto")) console.log(e.name, e.address);
}
```

Backtrace on a generic boundary:

```js
Interceptor.attach(Module.getGlobalExportByName("open"), {
  onEnter(args) {
    console.log(args[0].readUtf8String());
    console.log(Thread.backtrace(this.context, Backtracer.ACCURATE)
      .map(DebugSymbol.fromAddress).join("\n"));
  }
});
```

## References

Read `references/discovery-patterns.md` for target-specific trace ladders.

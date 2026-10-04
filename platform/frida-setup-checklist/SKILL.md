---
name: frida-setup-checklist
description: Prepare and verify a Frida environment, including host tools, Android frida-server, iOS setup, USB or remote transport, version matching, and smoke tests.
---

# Frida Setup Checklist

Use this skill before writing hooks or when the environment is unknown.

## Host Checks

```bash
python3 -m pip show frida frida-tools
frida --version
frida-ls-devices
frida-ps -Uai
```

If `frida` is missing, install user-local tools unless the project documents another path:

```bash
python3 -m pip install --user --upgrade frida-tools
```

## Android Checks

```bash
adb devices
adb shell getprop ro.product.cpu.abi
adb shell getprop ro.build.version.release
adb shell id
adb shell /data/local/tmp/frida-server --version
frida-ps -Uai
```

Match host `frida --version` to the device `frida-server` major/minor version. If versions differ, fix that before debugging hooks.

## iOS Checks

```bash
frida-ls-devices
frida-ps -Uai
frida -U -f com.example.app -l smoke.js --no-pause
```

Use a smoke script before loading real hooks:

```js
console.log("platform", Process.platform, "arch", Process.arch);
console.log("ObjC.available", ObjC.available);
```

## Minimal Smoke Scripts

Android:

```js
console.log("platform", Process.platform, "arch", Process.arch);
console.log("Java.available", Java.available);
Java.perform(() => console.log("Java.perform ok"));
```

Native-only target:

```js
console.log(Process.id, Process.arch, Process.pointerSize);
for (const m of Process.enumerateModules().slice(0, 10)) {
  console.log(m.name, m.base, m.size);
}
```

## Proof To Report

- Exact host Frida version and remote server/Gadget version.
- Device, OS version, architecture, package/bundle/process id.
- Attach or spawn command used.
- Smoke script output proving `Java`, `ObjC`, or native module access.

## References

- Official Frida installation docs: https://frida.re/docs/installation/
- Official Android docs: https://frida.re/docs/android/
- Official iOS docs: https://frida.re/docs/ios/
- OWASP MASTG Frida Android: https://mas.owasp.org/MASTG/tools/android/MASTG-TOOL-0001/
- OWASP MASTG Frida iOS: https://mas.owasp.org/MASTG/tools/ios/MASTG-TOOL-0039/

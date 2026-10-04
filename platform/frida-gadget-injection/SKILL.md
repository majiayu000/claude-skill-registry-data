---
name: frida-gadget-injection
description: Plan and troubleshoot Frida Gadget workflows for Android, iOS, desktop apps, jailed devices, embedded Gadget configuration, load timing, code-signing constraints, and script or interaction mode setup.
---

# Frida Gadget Injection

Use this skill when normal attach is blocked, root or jailbreak is unavailable, or instrumentation must load from inside the target app.

## Decide Gadget Mode

- Use `listen` mode when a host should attach after the app starts.
- Use `connect` mode when Gadget should call back to a host.
- Use `script` mode for an embedded script that must run without an interactive host.
- On jailed iOS, account for code-signing policy before relying on `Interceptor`.

## Android Shape

1. Match Gadget architecture to APK ABI.
2. Place the Gadget `.so` where the app will load it.
3. Add the matching `.config` file beside Gadget.
4. Load the library early enough for the target behavior.
5. Rebuild, sign, install, and run the app.

Example config:

```json
{
  "interaction": {
    "type": "listen",
    "address": "127.0.0.1",
    "port": 27042
  }
}
```

## iOS Shape

1. Match Gadget to device architecture and Frida version.
2. Embed Gadget in the app bundle or dynamic library load path.
3. Add the `.config` file named exactly like the Gadget binary plus `.config`.
4. Re-sign the app with the required entitlements.
5. Launch the app and connect with Frida tools.

## Verify

```bash
frida-ls-devices
frida-ps -Uai
frida -U Gadget
```

If Gadget does not appear, verify library load, config filename, app signing, architecture, and logs before editing hooks.

## References

Read `references/gadget-patterns.md` for configuration examples and troubleshooting.

---
name: jade-recipe-11-17-multicast-group-api
description: >-
  Moves JADE's multicast main-container discovery off the deprecated
  MulticastSocket.joinGroup(InetAddress)/leaveGroup(InetAddress) overloads that
  JDK 17 superseded. Agent-mode recipe: the shard contract names the file; this
  document defines the transform and the one argument the agent must not invent.
mode: agent
arguments: [--shard-json]
---
# jade-recipe-11-17-multicast-group-api — multicast moved to DatagramSocket

JDK 17 (JDK-8237352) added `joinGroup`/`leaveGroup` to `java.net.DatagramSocket`
and notes that "the `MulticastSocket` API works as before, although most of its
methods are deprecated". This is a plain deprecation, not a removal and not a
behaviour change, which is why the rule is `LOW`.

## Scope of one task

You receive a shard contract. This rule is `blast_class: body-local`
(`parallel_safe: true`). Edit only that shard's `editable_files`;
`read_only_context` is read-only.

## The two sites

Both are in `src/jade/src/jade/core/MulticastMainDetectionListener.java`, on the
private `MulticastSocket socket` field declared at line 28:

| line | construct | enclosing |
|---|---|---|
| 50 | `socket.joinGroup(mcastGroupAddress);` | constructor setup block |
| 67 | `socket.leaveGroup(mcastGroupAddress);` | `stop()` |

They are a pair. Change both or neither.

## The transform

```java
socket.joinGroup(new InetSocketAddress(mcastGroupAddress, 0), null);
socket.leaveGroup(new InetSocketAddress(mcastGroupAddress, 0), null);
```

`java.net.InetSocketAddress` must be imported if it is not already. The
enclosing method signatures and the field type do not change.

## The argument the agent must not invent

The replacement overload takes a `NetworkInterface`. Passing `null` is the
faithful translation: it reproduces exactly what the deprecated overload did,
namely defer to the interface set by `setInterface` or, failing that, the system
default. Naming a specific interface would change which NIC JADE discovers on,
which is a deployment decision belonging to whoever runs the platform.

Pass `null`. Do not read a NIC name from a profile property, do not enumerate
`NetworkInterface.getNetworkInterfaces()` and pick one, and do not add a new
configuration key. If a reviewer wants an explicit interface, that is a separate
change with its own configuration surface.

Note that `MainDetectionManager` also uses a `MulticastSocket` (line 302) but
only calls `setTimeToLive`, `setSoTimeout`, `send` and `receive`; it never joins
a group, so it is not part of this rule.

## Verification

Recompiling in `jade-ant:17` reports no `[deprecation] joinGroup(InetAddress)`
or `leaveGroup(InetAddress) in MulticastSocket` warning. A two-container JADE
platform still finds its main container over multicast, and all consumers PASS.

---
name: elixir-phoenix
description: "Elixir and Phoenix framework, OTP GenServers, Supervisors, LiveView real-time components, and pattern matching."
---

# Elixir & Phoenix Protocol

Build fault-tolerant, concurrent applications on the BEAM VM.

---

## 1. Supervisors & Let It Crash

1. Organize processes into supervision trees with explicit restart strategies (`:one_for_all`, `:one_for_one`).
2. Favor pattern matching and fail-fast execution over defensive defensive null checks.

---

## 2. Phoenix LiveView

Minimize state payloads over WebSockets by assigning only modified keys to socket assigns.

---

name: leeway-host-commander

description: Governed native-host fallback capability contract for filesystem, terminal, process, service, diagnostics, hashing, and host inspection when external commander providers are unavailable. Defines authority and qualification; does not claim an executor exists.

license: MIT

metadata:

  authority: Creator/Human Authority > LeeWay Standards > Root of Trust

  mode: host-capability-fallback-contract

  stage: capability-resilience-provider

---

# LeeWay Host Commander

## Purpose

Provide a canonical LeeWay capability contract for host operations so Desktop Commander or another external provider is not the capability identity.

## Abstract capabilities

files.list/read/write/search/hash; terminal.execute; process.inspect; service.inspect/operate; diagnostics; logs. Exact availability is adapter/runtime dependent.

## Provider preference

Use the safest proven authorized provider: deterministic native OS capability (PowerShell preferred for Windows host engineering), LeeWay native adapter, or authorized external provider. Provider selection belongs to Capability Resilience/Skill Orchestrator.

## Truth boundary

This skill does not prove a live host executor. CONFIGURED/PRESENT capability contracts remain unexecuted until an adapter/runtime returns evidence.

## Completion

If a provider fails, isolate the lost abstract capability, choose/qualify fallback, execute, Veritas-check, receipt, and resume the parent mission.
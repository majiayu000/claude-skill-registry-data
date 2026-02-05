---
name: pure-data
description: Pure Data reference documentation for audio patch development. Use when writing .pd patches, working with OSC/audio/sampling, or implementing Pure Data code.
---

# Pure Data Reference

Pure Data (Pd) reference documentation organized by topic. Files are independent unless cross-referenced. Load relevant files as needed.

## Core Concepts

- **pd-fundamentals.md** - Patches, canvases, box types, inlets/outlets basics
- **pd-execution-model.md** - Message passing, execution order, hot/cold inlets
- **pd-workflow-and-editing.md** - Edit vs run mode, patch editing operations
- **pd-advanced-structures.md** - Subpatches, abstractions, arrays, graph-on-parent

## Audio Processing

- **pd-audio-fundamentals.md** - Sample rates, tilde objects, signal/control conversion basics
- **pd-audio-routing.md** - Signal routing, throw~/catch~, send~/receive~, feedback loops
- **pd-audio-performance.md** - Block size optimization, DSP control, realtime processing
- **pd-audio-objects.md** - Reference catalog: oscillators, filters, analysis, I/O
- **pd-audio-examples.md** - Quick-start audio patches with raw .pd code
- **pd-audio-multichannel.md** - Multichannel signal features (Pd 0.54+)

## Envelopes

- **pd-envelopes-basics.md** - Basic envelope generation with line~ and vline~
- **pd-envelopes-adsr.md** - ADSR abstraction implementation and retrigger behavior
- **pd-envelopes-dbtable-conversions.md** - Logarithmic dB conversion and quartic curves
- **pd-envelopes-pitch-modulation.md** - Pitch envelopes, portamento, frequency modulation
- **pd-envelopes-reference.md** - Envelope techniques comparison and parameter ranges

## Expression Language

- **pd-expr-basics.md** - expr, expr~, fexpr~ objects and methods
- **pd-expr-operators-and-functions.md** - Complete math and function reference tables
- **pd-expr-strings.md** - String manipulation operations (control-rate only)
- **pd-expr-examples-and-advanced.md** - Real-world calculation patterns and performance

## File Format

### Essentials
- **pd-file-format-reference.md** - .pd file syntax, object types, connection format
- **pd-file-format-messaging.md** - Send/receive patterns, $0 addressing, message variables
- **pd-file-format-organization.md** - Subpatches, abstractions, creation arguments structure

### Advanced
- **pd-file-format-patterns.md** - Reusable patch templates and common structures
- **pd-file-format-generation.md** - Programmatic .pd file creation from code
- **pd-file-format-validation.md** - File format validation and error detection

## Message Routing

- **pd-message-construction.md** - Message aggregation and distribution with pack/unpack
- **pd-message-variables-and-dispatch.md** - Dynamic messages using $N, semicolons, commas
- **pd-conditional-routing.md** - Decision-making with select, route, spigot, moses
- **pd-random-numbers.md** - Pseudo-random generation, seeding, distributions
- **pd-routing-patterns.md** - Design patterns for message flow and control logic

## Networking

- **pd-fudi-protocol.md** - FUDI protocol specification and command-line tools
- **pd-osc-protocol.md** - OSC protocol concepts and native object usage
- **pd-network-objects-reference.md** - netsend, netreceive, oscformat, oscparse reference
- **pd-networking-guide.md** - Network examples, TCP vs UDP, debugging strategies

## Sampling

- **pd-sampling-basic-reading.md** - Scratch machine and basic table looping
- **pd-sampling-smooth-looping.md** - Click-free loops with envelopes and overlapping readers
- **pd-sampling-triggered-playback.md** - One-shot and parameterized sample triggering
- **pd-sampling-polyphony.md** - Multi-voice sample allocation and management
- **pd-sampling-utilities.md** - Table operations and sampler object reference

## Timing & Sequencing

- **pd-timing-metro-counters.md** - Periodic pulse generation and counting patterns
- **pd-timing-conditional-counting.md** - Bounded sequences with conditional logic
- **pd-timing-delays-timers.md** - Single-event scheduling with delay and timer
- **pd-timing-pipe.md** - Multi-event queuing with data preservation
- **pd-timing-sequencing.md** - Complex event scheduling with qlist and text
- **pd-timing-loops.md** - Immediate iteration with until (safety warnings)
- **pd-timing-reference.md** - Timing precision notes and quick reference tables
- **pd-timing-and-format.md** - Scheduling semantics, determinism, time representation

## Task Recipes

- **common-tasks-creating-patches.md** - When to use subpatches vs abstractions
- **common-tasks-osc-networking.md** - OSC message receive/send implementation
- **common-tasks-sample-playback.md** - Loading samples from files and tables
- **common-tasks-audio-processing.md** - Rate conversion, envelope application, stereo panning
- **common-tasks-message-routing.md** - Trigger sequencing and threshold routing
- **common-tasks-testing-validation.md** - Console debugging and signal monitoring
- **common-tasks-integration-setup.md** - External libraries, path configuration, DSP startup
- **common-tasks-performance-optimization.md** - CPU profiling and DSP optimization strategies

## Troubleshooting

- **troubleshooting-patch-creation.md** - Object creation failures, DSP loops, network setup
- **troubleshooting-audio.md** - DSP configuration, signal flow, audio device issues
- **troubleshooting-timing-performance.md** - Message ordering, latency, CPU dropouts
- **troubleshooting-libraries-advanced.md** - External library loading and array configuration
- **troubleshooting-debugging-methodology.md** - Systematic debugging workflow

## Project Context

**Architecture**: ESP32 Sensors → OSC :8000 → Pure Data → Audio Out + OSC :8001 → Lighting

**Required Externals**: mrpeach (OSC), cyclone (Audio utilities)

**Project Files**:
- `docs/audio/reference/phase1-trd.md` - Technical requirements
- `docs/audio/tasks/phase1-audio.md` - Implementation tasks
- `audio/patches/` - Patch files
- `audio/samples/` - Audio samples

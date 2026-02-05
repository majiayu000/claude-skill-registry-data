---
name: tigerstyle
description: Review Zig code for TigerStyle compliance. Use when reviewing code, implementing features, or checking for safety/performance issues. Checks assertions, bounded loops, memory safety, error handling, and naming conventions. (project)
---

<tigerstyle-review>
  <CRITICAL>You MUST check EVERY rule in EVERY category. No exceptions. No skipping.</CRITICAL>
  <CRITICAL>Do NOT skip rules. Do NOT summarize multiple rules. Check EACH rule individually.</CRITICAL>
  <CRITICAL>Use TodoWrite to create a checklist item for each category before reviewing.</CRITICAL>
  <CRITICAL>If you skip ANY rule, the review is INVALID and must be redone.</CRITICAL>

  <priority-order>Safety > Performance > Developer Experience</priority-order>
  <reference>https://github.com/tigerbeetle/tigerbeetle/blob/main/docs/TIGER_STYLE.md</reference>

  <philosophy>
    <principle>Zero technical debt - solve problems during design/implementation, not in production</principle>
    <principle>Upfront design investment - 1000x improvements at design time vs 10x from profiling</principle>
    <principle>Simple and elegant - easier to design, faster to execute, more reliable</principle>
  </philosophy>

  <categories>
    <category name="Safety" priority="1" required="true">
      <IMPORTANT>ALL safety rules are blocking - code MUST NOT be merged with violations</IMPORTANT>

      <rule id="S1" name="assertions">
        <requirement>~2 assertions per function average (preconditions + postconditions)</requirement>
        <check>Every function has at least one assertion</check>
        <check>Preconditions validate all function arguments</check>
        <check>Postconditions verify return values and output state</check>
        <check>Critical properties have paired assertions across code paths</check>
        <example type="good">
fn process(items: []Item) void {
    assert(items.len &lt;= max_items); // precondition
    defer assert(processed_count &lt;= items.len); // postcondition
}
        </example>
      </rule>

      <rule id="S2" name="explicit-types">
        <requirement>Use explicitly-sized types (u32, u64) - avoid usize</requirement>
        <check>No usize except for slice lengths and indexing where Zig requires it</check>
        <check>All numeric variables have explicit size (u32, u64, i32, etc.)</check>
        <example type="bad">var count: usize = 0; var timeout: usize = 5000;</example>
        <example type="good">var count: u32 = 0; var timeout_ms: u32 = 5000;</example>
      </rule>

      <rule id="S3" name="no-recursion">
        <requirement>No recursion - ensures bounded stack, predictable execution</requirement>
        <check>No function calls itself directly</check>
        <check>No mutual recursion between functions</check>
      </rule>

      <rule id="S4" name="bounded-loops">
        <requirement>All loops MUST have fixed upper limits</requirement>
        <check>Every while loop has explicit iteration counter</check>
        <check>Loop counter checked against max_iterations constant</check>
        <check>Returns error if limit exceeded (fail-fast)</check>
        <example type="bad">while (iterator.next()) |item| { ... }</example>
        <example type="good">
var iterations: u32 = 0;
while (iterator.next()) |item| {
    iterations += 1;
    if (iterations > max_iterations) return error.IterationLimitExceeded;
}
        </example>
      </rule>

      <rule id="S5" name="memory-safety">
        <requirement>No runtime allocation after init</requirement>
        <check>All allocations happen in init/create functions</check>
        <check>No malloc/alloc calls in hot paths</check>
        <check>Buffers zeroed to prevent information leaks</check>
        <check>Large structs (>16 bytes) passed as *const to avoid copies</check>
        <example type="bad">fn process(config: Config) void { ... }  // Config is 128 bytes</example>
        <example type="good">fn process(config: *const Config) void { ... }</example>
      </rule>

      <rule id="S6" name="error-handling">
        <requirement>All errors handled explicitly - no silent failures</requirement>
        <check>No catch {} - never swallow errors</check>
        <check>No catch unreachable unless mathematically proven impossible</check>
        <check>Every error logged or propagated with context</check>
        <example type="bad">file.read() catch {};</example>
        <example type="good">
file.read() catch |err| {
    log.err("read failed: {}", .{err});
    return err;
};
        </example>
      </rule>

      <rule id="S7" name="no-unbounded-queues">
        <requirement>Cap all buffers and queues with explicit limits</requirement>
        <check>All arrays/slices have max_* constants</check>
        <check>Queue implementations have capacity limits</check>
        <check>Overflow returns error, not silent drop</check>
      </rule>
    </category>

    <category name="Performance" priority="2" required="true">
      <rule id="P1" name="resource-priority">
        <requirement>Optimize slowest resources first</requirement>
        <priority-order>
          <resource name="Network" latency="~1ms RTT" priority="1">Minimize round trips, batch requests</resource>
          <resource name="Disk" latency="~10ms seek" priority="2">Sequential access, batch I/O</resource>
          <resource name="Memory" latency="~100ns" priority="3">Cache locality, avoid allocations</resource>
          <resource name="CPU" latency="~1ns" priority="4">Last priority unless CPU-bound</resource>
        </priority-order>
      </rule>

      <rule id="P2" name="batching">
        <requirement>Amortize costs across all resources</requirement>
        <check>Per-request syscalls batched where possible</check>
        <check>Network sends use writev/sendmsg for multiple buffers</check>
        <check>I/O operations grouped with io_uring submission batching</check>
        <example type="bad">
for (requests) |req| {
    _ = send(socket, req.data);
}
        </example>
        <example type="good">
var iovecs: [max_batch]std.posix.iovec = undefined;
for (requests, 0..) |req, i| {
    iovecs[i] = .{ .base = req.data.ptr, .len = req.data.len };
}
_ = std.posix.writev(socket, iovecs[0..requests.len]);
        </example>
      </rule>

      <rule id="P3" name="zero-copy">
        <requirement>Avoid userspace copies for data transfer</requirement>
        <check>splice() used for piping between fds</check>
        <check>sendfile() used for file-to-socket transfers</check>
        <check>Slices passed instead of copying buffers</check>
      </rule>

      <rule id="P4" name="hot-path-extraction">
        <requirement>Extract hot loops into standalone functions with primitive arguments</requirement>
        <check>Hot loops don't access self.* fields directly</check>
        <check>Required data passed as explicit parameters</check>
        <check>Primitive types (fd, []u8, u32) instead of struct pointers where possible</check>
      </rule>
    </category>

    <category name="CacheState" priority="3" required="true">
      <rule id="C1" name="minimize-scope">
        <requirement>Calculate/check variables close to usage point</requirement>
        <check>No variable declarations far from usage (&gt;10 lines)</check>
        <check>Derived values computed at point of use</check>
        <example type="bad">
const len = buffer.len;
// ... 50 lines of code ...
process(buffer[0..len]);  // is len still valid?
        </example>
        <example type="good">process(buffer[0..buffer.len]);</example>
      </rule>

      <rule id="C2" name="no-duplication">
        <requirement>One source of truth for each piece of data</requirement>
        <check>No manually-synced counters (use derived getters)</check>
        <check>No aliased state that must stay in sync</check>
        <example type="bad">self.request_count = requests.len;  // must sync manually</example>
        <example type="good">
fn requestCount(self: *Self) u32 {
    return @intCast(self.requests.items.len);
}
        </example>
      </rule>

      <rule id="C3" name="in-place-init">
        <requirement>Large structs constructed via out pointer</requirement>
        <check>Structs &gt;64 bytes use init(out: *T) pattern</check>
        <check>No large struct returns that cause stack copies</check>
      </rule>

      <rule id="C4" name="simple-returns">
        <requirement>Minimize return type complexity</requirement>
        <complexity-order>void &lt; bool &lt; u64 &lt; ?u64 &lt; !u64 &lt; !?u64</complexity-order>
        <check>Prefer simpler return types when possible</check>
        <check>Handle errors internally if caller can't act on them</check>
      </rule>

      <rule id="C5" name="resource-grouping">
        <requirement>Group allocation and deallocation visually</requirement>
        <check>alloc immediately followed by defer free</check>
        <check>open immediately followed by defer close</check>
      </rule>
    </category>

    <category name="Style" priority="4" required="true">
      <rule id="Y1" name="function-length">
        <requirement>Functions under 70 lines</requirement>
        <check>No function exceeds 70 lines of code</check>
        <check>Long functions decomposed into helpers</check>
      </rule>

      <rule id="Y2" name="naming">
        <requirement>Consistent naming conventions</requirement>
        <check>snake_case for functions, variables, files</check>
        <check>No abbreviations (except i, j, n in math contexts)</check>
        <check>Acronyms capitalized: TLSConfig, HTTPServer (not TlsConfig)</check>
      </rule>

      <rule id="Y3" name="units-in-names">
        <requirement>Units as suffix in variable names</requirement>
        <check>Time: timeout_ms, latency_ns, duration_us</check>
        <check>Size: size_bytes, capacity_kb, buffer_len</check>
        <check>Count: max_connections, retry_count</check>
        <example type="good">
const read_timeout_ms: u32 = 5000;
const send_timeout_ms: u32 = 3000;
        </example>
      </rule>

      <rule id="Y4" name="index-count-size">
        <requirement>Distinguish index (0-based), count (1-based), size (bytes)</requirement>
        <check>Conversions are explicit: last_index = items.len - 1</check>
        <check>Use @divExact for exact division</check>
        <check>Use div_ceil for ceiling division</check>
      </rule>

      <rule id="Y5" name="comments">
        <requirement>Comments explain "why" not "what"</requirement>
        <check>Complete sentences with proper punctuation</check>
        <check>Document non-obvious invariants and design decisions</check>
        <check>No comments that restate the code</check>
      </rule>

      <rule id="Y6" name="formatting">
        <requirement>Consistent code formatting</requirement>
        <check>4-space indentation</check>
        <check>Hard 100-column limit</check>
        <check>Trailing commas for wrapped signatures</check>
        <check>zig fmt run before commit</check>
      </rule>
    </category>

    <category name="AsyncIO" priority="5" required="false">
      <rule id="A1" name="control-flow">
        <requirement>Maintain program control flow with async I/O</requirement>
        <check>Functions run to completion - no mid-function suspension</check>
        <check>Precondition assertions remain valid throughout execution</check>
        <check>Use io_uring for async without callback inversion</check>
      </rule>
    </category>

    <category name="Dependencies" priority="6" required="false">
      <rule id="D1" name="zero-deps">
        <requirement>No external dependencies except Zig toolchain</requirement>
        <check>No third-party packages in build.zig.zon</check>
        <check>Implement needed functionality or vendor reviewed code</check>
      </rule>
    </category>
  </categories>

  <review-process>
    <IMPORTANT>Follow this EXACT process for every review</IMPORTANT>
    <CRITICAL>Do NOT skip ANY step. Do NOT combine rules. Check EACH rule INDIVIDUALLY.</CRITICAL>

    <step order="1">Create checklist with TodoWrite for all 22 rules</step>
    <step order="2">Check S1 (assertions) - report PASS/FAIL</step>
    <step order="3">Check S2 (explicit-types) - report PASS/FAIL</step>
    <step order="4">Check S3 (no-recursion) - report PASS/FAIL</step>
    <step order="5">Check S4 (bounded-loops) - report PASS/FAIL</step>
    <step order="6">Check S5 (memory-safety) - report PASS/FAIL</step>
    <step order="7">Check S6 (error-handling) - report PASS/FAIL</step>
    <step order="8">Check S7 (no-unbounded-queues) - report PASS/FAIL</step>
    <step order="9">Check P1 (resource-priority) - report PASS/FAIL</step>
    <step order="10">Check P2 (batching) - report PASS/FAIL</step>
    <step order="11">Check P3 (zero-copy) - report PASS/FAIL</step>
    <step order="12">Check P4 (hot-path-extraction) - report PASS/FAIL</step>
    <step order="13">Check C1 (minimize-scope) - report PASS/FAIL</step>
    <step order="14">Check C2 (no-duplication) - report PASS/FAIL</step>
    <step order="15">Check C3 (in-place-init) - report PASS/FAIL</step>
    <step order="16">Check C4 (simple-returns) - report PASS/FAIL</step>
    <step order="17">Check C5 (resource-grouping) - report PASS/FAIL</step>
    <step order="18">Check Y1 (function-length) - report PASS/FAIL</step>
    <step order="19">Check Y2 (naming) - report PASS/FAIL</step>
    <step order="20">Check Y3 (units-in-names) - report PASS/FAIL</step>
    <step order="21">Check Y4 (index-count-size) - report PASS/FAIL</step>
    <step order="22">Check Y5 (comments) - report PASS/FAIL</step>
    <step order="23">Check Y6 (formatting) - report PASS/FAIL</step>
    <step order="24">Produce summary table with ALL 22 rules listed</step>
  </review-process>

  <output-format>
    <IMPORTANT>Always produce ALL sections in this exact order</IMPORTANT>

    <section name="Safety" required="true">
      <format>For each rule S1-S7: PASS, FAIL with location, or N/A</format>
    </section>

    <section name="Performance" required="true">
      <format>For each rule P1-P4: PASS, FAIL with location, or N/A</format>
    </section>

    <section name="Cache/State" required="true">
      <format>For each rule C1-C5: PASS, FAIL with location, or N/A</format>
    </section>

    <section name="Style" required="true">
      <format>For each rule Y1-Y6: PASS, FAIL with location, or N/A</format>
    </section>

    <section name="Suggestions" required="false">
      <format>Optional non-blocking improvements</format>
    </section>

    <severity-levels>
      <level name="CRITICAL" action="must-fix">Safety violations - block merge</level>
      <level name="WARNING" action="should-fix">Performance risk, potential bugs</level>
      <level name="NOTE" action="consider">Style, maintainability improvements</level>
    </severity-levels>

    <summary-table>
      <IMPORTANT>End EVERY review with this summary table showing EACH rule status</IMPORTANT>
      <CRITICAL>Every cell must show the actual result - no blanks, no "see above"</CRITICAL>
      <format>
| Rule | Name | Status | Notes |
|------|------|--------|-------|
| S1 | assertions | PASS/FAIL | |
| S2 | explicit-types | PASS/FAIL | |
| S3 | no-recursion | PASS/FAIL | |
| S4 | bounded-loops | PASS/FAIL | |
| S5 | memory-safety | PASS/FAIL | |
| S6 | error-handling | PASS/FAIL | |
| S7 | no-unbounded-queues | PASS/FAIL | |
| P1 | resource-priority | PASS/FAIL | |
| P2 | batching | PASS/FAIL | |
| P3 | zero-copy | PASS/FAIL | |
| P4 | hot-path-extraction | PASS/FAIL | |
| C1 | minimize-scope | PASS/FAIL | |
| C2 | no-duplication | PASS/FAIL | |
| C3 | in-place-init | PASS/FAIL | |
| C4 | simple-returns | PASS/FAIL | |
| C5 | resource-grouping | PASS/FAIL | |
| Y1 | function-length | PASS/FAIL | |
| Y2 | naming | PASS/FAIL | |
| Y3 | units-in-names | PASS/FAIL | |
| Y4 | index-count-size | PASS/FAIL | |
| Y5 | comments | PASS/FAIL | |
| Y6 | formatting | PASS/FAIL | |
      </format>
    </summary-table>
  </output-format>
</tigerstyle-review>

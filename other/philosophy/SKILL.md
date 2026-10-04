---
name: philosophy
description: Use when the user asks for the "system design philosophy", "design principles", "/ar:philosophy", or "/ar:ph", and before major feature work, an architecture decision, or a pull-request review. Lists the 17 universal system design principles, ordered from most fundamental to most specific, with concrete examples where a principle is easy to misread.
aliases: [ph]
---

# Universal System Design Philosophy

<purpose>

Systems should follow these core principles to create an exceptional user experience.
These are ordered from most fundamental to most specific:

</purpose>

<principles>

## CORE PRINCIPLES

1. **Automatic and Correct**: Make things "just work" without user intervention.
   We handle complexity so users don't have to. The system should feel magical.
   Once started, systems run to completion without asking questions.

2. **Modernize Systems Automatically**: Transform legacy configurations into
   modern, reproducible environments. We find the newest compatible versions
   that work together, not the oldest. We're upgrading, not downgrading — within
   the constraints the user has stated (principle 12 wins when they conflict).

3. **Easy to Use Correctly, Hard to Use Incorrectly**: Design systems and APIs that
   guide users toward success. Minimal parameters, smart defaults.
   Example: Just run `systemname` - no flags needed for 95% of cases.

4. **Solve Problems FOR Users**: Don't just report problems - fix them automatically.
   When we detect a conflict, we don't just tell users about the conflict, we
   retry with a solution. Users should feel the system is working on their behalf.
   When a problem absolutely cannot be solved for users, fail loudly with the
   context and guidance users need to solve that problem themselves: the exact
   state the system stopped in and the specific next action. Never fail silently
   or hand back a bare error.

5. **Use Existing APIs and Capabilities**: When adding new functionality, explore to understand the context and determine what is already done and the right point at which to work to avoid duplication. If one of the already imported tools can do it effectively, use that. Search to ensure you are using the most modern and up-to-date reliable tool possible. Don't implement things manually unless necessary. Leverage existing solutions that solve development problems effectively.

## COMMUNICATION PRINCIPLES

6. **Specific and Actionable Feedback**: Every message must tell users exactly what to do.
   - Bad: "Error occurred"
   - Good: "component-x 2.3.1 requires platform 11+, but your environment uses platform 8"
   - Better: "Automatically finding compatible component-x version for platform 8..."
   - Best: "✅ Found component-x 1.24.3 that works with platform 8. Installing now...
           (To manually specify compatibility: configure 'component-x>=1.24,<2.0')"

   The key: Show the problem AND that we're solving it for them!

7. **Context-Aware Messages**: Error messages must include relevant context:
   - What was being attempted ("Configuring component-x 2.3.1...")
   - Why it failed ("requires platform 11+, you have 8")
   - What we're doing to fix it ("Finding compatible version...")
   - What the user can do if we can't fix it (exact commands)

8. **Show Progress and Success**: Make tasks happen so fast and efficiently that they appear instantaneous. Only show progress when tasks must take time.
   - **Optimize for speed first**: Fast operations should complete without progress indicators
   - **Smart progress display**: Show progress only for genuinely slow operations (network requests, large files, complex analysis)
   - **Immediate feedback for fast tasks**: "✅ Successfully configured 12 components!" (no intermediate steps shown)
   - **Concrete and actionable progress for slow tasks**: "Downloading component-x 2.3.1 (47MB)..." → "Installing dependencies (3 of 12)..." → "✅ Installed component-x 2.3.1 with 12 dependencies!"
   - **Always be concrete and actionable**: Not "Processing..." but "Analyzing dependency conflicts..." or "Compiling TypeScript files..." - tell users exactly what's happening
   - Use status indicators: ✅ SUCCESS, ⚠️ WARNING, ❌ ERROR
   - **Celebrate success with concrete specifics**: "✅ Successfully configured 12 components in 3.2 seconds!" or "✅ Resolved 5 version conflicts and installed 12 packages!"

9. **Progressive Disclosure**: Show simple success messages for normal cases,
   detailed information only when debugging is needed. Don't overwhelm users
   with logs when everything is working fine.

## TECHNICAL PRINCIPLES

10. **Graceful Recovery**: When something goes wrong, try to fix it automatically
    before asking for help. Example: retry with relaxed constraints on conflicts.
    The user should rarely need to intervene.

11. **Trust the Systems**: Use systems and APIs as their creators intended. Don't try to
    outsmart resolvers or discovery mechanisms - leverage their strengths.
    We orchestrate systems and APIs, we don't replace them.

12. **Preserve User Intent**: Never change system settings (like compatibility requirements)
    without explicit consent. Respect the user's choices. Their system, their rules.

13. **One Problem, One Solution**: Avoid complex multi-strategy approaches when
    a single good solution suffices. Simplicity is reliability. Don't overthink it.

## FAILURE HANDLING

14. **Fail Fast with Recovery Path**: When automation isn't possible, fail quickly
    with a clear explanation and specific recovery steps. Don't leave users hanging.

15. **Manual Fix Guidance**: When automation fails, guide toward modernization:
    - Bad: "Failed to resolve configuration"
    - Good: "component-x 2.3.1 and component-y 2.2.0 require platform 11+. Your environment uses platform 8."
    - Best: "Cannot automatically resolve: component-x 2.3.1 and component-y 2.2.0 require platform 11+,
             but your environment uses platform 8.

             Here are your options to modernize your system:

             1. Use a newer platform version (recommended):
                Run: `platform-11 your-system`
                This gives you latest features and best performance.
                Note: You may need to update configurations that use deprecated features.

             2. Update your system's platform requirement:
                Edit system.config: `requires-platform = '>=11'`
                Then run your-system again.

             3. If you must stay on platform 8:
                Run: `system-manager configure 'component-x<2.0' 'component-y<2.0'`
                This keeps older but compatible versions.

             Options 1 or 2 modernize your system, option 3 maintains compatibility."

## OPTIMIZATION PRINCIPLES

16. **Optimize for Common Case**: Make the 95% case seamless, even if the 5%
    requires manual intervention. Most users should never see an error.
    Focus effort where it has the most impact.

17. **Transparent Operations**: Tell users what's happening and why. They should
    understand what the system is doing, even if they don't need to intervene.
    Build trust through transparency.

</principles>

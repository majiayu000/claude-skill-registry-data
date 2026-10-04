---
name: agentic-session-debugger
description: Use when a Claude Code session loops, drifts from scope, claims a fix that CI rejects, hits context, PATH, or permission walls, or fails in a way another retry will not solve and a root cause diagnosis is needed instead.
---

# Agentic Session Debugger

## When to use

Use this skill when a Claude Code or agentic coding session behaves unreliably and the user needs root cause diagnosis rather than another attempt at the same command. It applies at any lifecycle stage, and the lesson it records belongs in the project's standing instructions. It is not for evaluating whether an agent's outputs are portable across tool environments, that is agent-portability-matrix, and it is not for getting an independent second diagnosis on a difficult failure, that is cross-agent-second-opinion.

## Inputs

- User goal.
- Recent commands or actions.
- Error messages.
- Files or tools involved.
- Current working directory.
- Permission and environment constraints.
- What changed just before the failure.

## Workflow

1. Restate the intended outcome.
2. Identify the failure class, tool, knowledge, communication, permission, environment, or context.
3. Capture exact evidence from logs, errors, tests, or terminal output.
4. Check scope drift, repeated loops, hidden state, stale context, and conflicting instructions.
5. Check environment issues, including PATH, shell, dependency version, working directory, and permissions.
6. Reduce the problem to the smallest reproducible step.
7. Propose the smallest correction and a verification command.
8. Record the lesson if the failure pattern should not recur.

## Output

Return:

- Intended outcome.
- Failure class.
- Evidence.
- Root cause hypothesis.
- Minimal reproduction.
- Fix plan.
- Verification step.
- Residual risk.
- What to record at session end: the failure class, the root cause hypothesis, the fix applied, and the reusable rule added to the project's standing instructions.

## Verification

- The diagnosis cites actual evidence, not only model intuition.
- The smallest reproducible case is identified or the reason it cannot be reproduced is stated.
- Permission failures are not solved by destructive commands.
- The fix has a clear pass or fail check.
- Repeated session errors are converted into a reusable rule.
- Before closing: the fix has been verified with a concrete pass/fail check, and if the failure pattern involves cross-tool or cross-environment behavior, agent-portability-matrix or cross-agent-second-opinion has been noted as the next step.

## Safety

Do not run destructive commands unless the user explicitly requested them and the target path is verified. Do not print secrets from logs. Redact tokens, passwords, private paths, and personal identifiers.

## Example prompt

"Claude Code keeps looping on a failing validator and says the file is fixed, but CI still fails. Diagnose the session."

Expected smoke output:

- Failure class, evidence, minimal reproduction, likely hidden-state or stale-assumption issue.
- A concrete verification command and a smaller next fix.

## Türkçe kullanım notu

Bu beceri, aksayan bir Claude Code oturumunu aynı komutu yeniden denemek yerine kök nedenden teşhis eder. Bozulma sınıfı belirlenir, kanıt toplanır, sorun en küçük tekrarlanabilir adıma indirilir ve en küçük düzeltme doğrulama komutuyla birlikte önerilir. Tekrarlayan hata kalıcı bir kurala dönüştürülür, yıkıcı komutlar teşhisin parçası olamaz.

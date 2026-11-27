---
name: code-authoring
description: The rules for writing production code and tests that shark:code-writer and shark:lead-engineer share - regression safety with a test baseline, scope, test first, introspectability, logging and comments. Use before you write or correct code.
---

# Code authoring

These rules apply to each line of production code and test code that you write or correct. `shark:code-writer`
and `shark:lead-engineer` load this skill before they change code. AGENTS.md wins over a rule here.

## 1. Regression safety

A fix that makes its own tests pass can still break a rule next to it. Earlier fixes in this kit broke field-access
rules and "only a localized child changed" rules that no test of the brief named. These steps prevent that.

1. **Record a test baseline before you change code.** Choose the existing test files of the area: the test folder
   of each module that you will change, and each test file that names a function that you will change (`grep`).
   Run them once and save the result:

   ```bash
   node "${CLAUDE_PLUGIN_ROOT:-<directory of this skill>/../..}/skills/code-authoring/scripts/test-baseline.mjs" record --out <baseline.json> \
     --cmd '<the project test command with {files}, writing a JUnit report to {junit}>' <test file>...
   ```

   A long suite is still worth it: one run before, one run after. After the change, compare:

   ```bash
   node "${CLAUDE_PLUGIN_ROOT:-<directory of this skill>/../..}/skills/code-authoring/scripts/test-baseline.mjs" compare --baseline <baseline.json> --cmd '<the same command>'
   ```

   A test that passed before and fails now is your regression. Fix the code, not the test. Only a test that a part
   of the spec changes on purpose can break: pass `--allow <test name>` and name that spec part in your report.
2. **Change the narrowest condition.** Before you edit a condition, list the inputs that will take a different
   branch after your change. Each one must be in the spec. If an input outside the spec changes branch, narrow the
   condition. Do not widen an existing branch to reach a new case: add the case.
3. **Existing guards keep their effect.** An access check, a permission check, a validation or a filter of the
   records that the actor can reach runs before your new behaviour, and limits it. Compute the new value only for
   what the guard allows. Never write a value on a path that the guard excluded, and never move the guard behind
   your code.
4. **Resolve a data property at each level.** When a rule depends on a property of a field (localized or shared,
   sensitive, owned by a tenant, nullable), find the property for each nested value, not only for the top field. A
   child in a container can have a different property than its parent: a localized field in a shared list is
   localized.
5. **Absent, empty and unchanged are three inputs.** A missing key, `null`, an empty list and the same value sent
   again are different. A value that is sent again unchanged is not a change. Treat each one as the spec says, and
   test each one that your condition reads.
6. **Twins share one implementation.** When the spec names twin paths (collection and global, single and bulk),
   change them through one function that both call. Do not copy the change.
7. **Review your own diff before you report.** For each changed condition, name the inputs that now enter or leave
   the branch. For each line that you removed or moved, name the behaviour that it carried, and the test that still
   covers it.

## 2. Scope

Keep each public interface as it is: a signature, a parameter, a return type or its unit, a file or wire format, a
command, a setting name. If the brief needs an interface change and does not say that the owner approved it, stop
and report it to the caller, with the smallest change that keeps the interface. Report other defects that you see;
do not fix them unless the brief asks.

## 3. Test first

1. Write the test first: the test that the spec names, or the test that its acceptance criteria imply.
2. Run it. Make sure that it **fails for the reason that you expect**. If it fails for a different reason, or
   passes, your understanding is wrong. Find out why before you continue.
3. Then write the implementation, and run the test again.

Test rules:

- Tag a test that covers a business rule with its rule ID, in the way that the project tags tests (for example
  Python: `@pytest.mark.rule("<ID>")`; JS: the rule ID in the `describe` title).
- Put a test for pure domain code with the unit tests. It needs no database.
- Put a test that needs the database with the integration tests. It uses the real database of the project, not a
  mock of it, when AGENTS.md › Test scope says so.
- Name a test as a behaviour sentence, in the style of the tests near it.
- Cover the simplest case and the realistic case.

## 4. Introspectability

Write code so that the next engineer can see what happened without new code. Use the records that already exist in
the project for each kind of change:

- **Return what you changed.** A function that changes rows returns the result, not nothing.
- **Leave the durable trace for the kind of change.**
  - A state change that other modules can react to records an event through the project's event mechanism (for
    example a transactional outbox: an event row written in the same transaction as the change).
  - A change that a customer or staff must be able to audit writes an audit entry through the project's audit
    writer.
  - A subscriber claims its event once (idempotency), through the project's subscriber mechanism.
- **Errors carry a code and the IDs.** Raise the project's domain error type with its code. The detail names the
  IDs and the attempted action. Never catch an error and return a default.
- **Name the values that decide the outcome.** Put such a value in a named variable, so that a breakpoint can show
  it.

## 5. Logging

- Log through the project's logger, the same way as the code near your change.
- Log once, at a boundary: a request, a job, a sweep. Include the IDs that find the durable record. Do not log
  inside domain code: return the information to the caller.
- Name a log event as the code near it does (for example `<area>.<event>` in snake case).
- Never log a secret, a token, a password, an environment value, or personal data. A telemetry scrubber is a second
  protection, not the first.
- A new metrics library or monitoring endpoint is a new dependency: ask the caller first.

## 6. Comments

There are two types of comment. Names, small functions and types give the meaning of the code, not comments. These
rules apply to production code and to test code. In a test, the test name gives the case: write
`test_float_input_rounds_half_up`, not a `# float gives 2.67` comment.

| Type | What it is | Rule |
| --- | --- | --- |
| Documentation comment | The doc comment of a module, a class, a function or a public API: a Python docstring, JSDoc or TSDoc, a Go doc comment, a Rust `///` comment, Javadoc | Allowed. Write it in the documentation format below. |
| Explanation comment | Any other comment: what a line does, why a choice was made, a note, a TODO | Not allowed. Write one only when the human asked for it, and the brief quotes that request. |

**Documentation format (ASD-STE100).** A doc comment tells a caller how to use the item. It does not tell how
the item works. Write these parts, in this order, and nothing more:

| Part | Rule |
| --- | --- |
| Description | One sentence that says what the item does for the caller. Present tense, active voice, 20 words or fewer: "Converts a decimal string to integer minor units, rounded half up." |
| Parameters | One short sentence for each parameter. Give the unit, and an example value when the format is not obvious. Do not repeat the type that the signature gives. |
| Return value | One short sentence. Give the unit. |
| Errors | Only the errors that a caller must handle (a Python `Raises:`, a Rust `# Errors` or `# Panics`, a TSDoc `@throws`): one sentence each. Do not list an error that comes only from wrong use of the API. |
| Example | One short usage example that a caller can copy (a doctest in Python, `# Examples` in Rust, `@example` in TSDoc). Show an edge case that a caller must know as one more example line, not as prose. |

- Do not write how the item works: no algorithm, no line-by-line description, no history, no TODO, no author or
  license text.
- **No notes in brackets.** "Rounded half up (away from zero on a tie)" is wrong. Write "Rounded half up." and add
  an example line that shows the tie.
- **No wrong-use errors.** Do not list `TypeError` for an argument of the wrong type, or an error for `None` where
  the signature does not allow `None`. The signature already gives the types.
- A contract note is allowed only when a caller cannot see it from the signature and an example: a side effect (the
  item changes an argument, writes a file, or changes global state), a thread-safety guarantee, or the safety
  conditions of an `unsafe` item. One sentence each.
- A private helper gets no doc comment, unless its name and signature do not give its purpose. Then write only the
  description sentence.
- Use the doc-comment syntax of the language and of the project (for example Google or NumPy sections).
- Every sentence follows ASD-STE100 (the output style `shark:asd-ste100`): 20 words or fewer, the active voice, the
  approved words, one idea in each sentence, no semicolons. A parameter line can start with a noun phrase ("The
  amount in major units, as a decimal string."); each sentence after it is a full sentence.

**Reference samples.** Copy their shape.

Python (Google style):

```python
def convert_to_cents(amount: str, currency: str) -> int:
    """Converts a decimal amount to integer minor units of the currency.

    Args:
        amount: The amount in major units, as a decimal string. Example: "12.345".
        currency: The ISO 4217 currency code. Example: "USD".

    Returns:
        The amount in minor units, rounded half up.

    Raises:
        ValueError: The amount is not a decimal number.

    Example:
        >>> convert_to_cents("12.345", "USD")
        1235
        >>> convert_to_cents("500", "JPY")
        500
    """
```

TypeScript (TSDoc). `@remarks` holds the one contract note, a side effect:

````ts
/**
 * Sends the invoice to the customer by email.
 *
 * @param invoiceId - The ID of the invoice to send.
 * @param options - The delivery options. Set `copyTo` to send a copy to a second address.
 * @returns The ID of the email message.
 * @throws {@link InvoiceNotFoundError} The invoice does not exist.
 *
 * @remarks The function writes one row to the `email_log` table.
 *
 * @example
 * ```ts
 * const messageId = await sendInvoice("inv_123", { copyTo: "billing@example.com" });
 * ```
 */
````

Go. The comment starts with the name. The example is an `ExampleParseRetryPolicy` function in a `_test.go` file:

```go
// ParseRetryPolicy converts a policy text, such as "3x200ms", to a RetryPolicy.
// The text gives the number of attempts and the wait between two attempts.
// It returns an error if the text does not have this format.
func ParseRetryPolicy(text string) (RetryPolicy, error)
```

Rust:

````rust
/// Converts a decimal amount to integer minor units of the currency.
///
/// `amount` is the amount in major units, for example `"12.345"`.
/// `currency` is the ISO 4217 currency code, for example `"USD"`.
///
/// # Errors
///
/// Returns [`AmountError::Malformed`] if `amount` is not a decimal number.
///
/// # Examples
///
/// ```
/// assert_eq!(to_minor_units("12.345", "USD").unwrap(), 1235);
/// assert_eq!(to_minor_units("500", "JPY").unwrap(), 500);
/// ```
pub fn to_minor_units(amount: &str, currency: &str) -> Result<i64, AmountError>
````

Not this. Each marked line breaks a rule:

```python
def convert_to_cents(amount, currency):
    """This function basically handles the conversion of amounts.   # vague, filler, says nothing

    It strips the string, matches a regex, then calls Decimal.scaleb # how it works, not how to use it
    and quantize; added in v2 by the payments team.                  # history, author
    Ties are rounded away from zero, so -12.345 gives -1235.         # an edge case as prose: put it in the example

    Returns:
        The amount in cents (rounded half up, away from zero).       # a note in brackets

    Raises:
        TypeError: if amount isn't a str                             # wrong use of the API, not a caller error
    """
```

- The reason for a choice that is not obvious goes in your report or in the commit message, not in the code.
- These are not comments, and you can write them: a directive that a tool reads (`# noqa`, `# type: ignore[...]`,
  `// eslint-disable-next-line ...`, a shebang) and a license header that the project needs.
- Do not delete a comment that exists. If your change makes a comment wrong, correct it.
- If AGENTS.md has a different comment rule, AGENTS.md wins.

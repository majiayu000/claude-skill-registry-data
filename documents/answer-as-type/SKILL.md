---
name: answer-as-type
description: Answer as a return value, not as prose.
argument-hint: "type: bool | int | float | str | list | set | infer = infer"
arguments: [type]
disable-model-invocation: true
---

# Func

The user called a function. Return its value. Nothing else.

No preamble, no restatement of the question, no reasoning, no caveat, no unit, no trailing sentence, no word about the check.

The first word of the request is `$type`.

- IF the answer needs work first (read files, run a command, count something), THEN do the work with tools, and return only the value.
- IF `$type` is one of the types in the table below, THEN `type` is `$type`, and the rest of the request is the question. The word is the type, not a verb: `list` means a numbered list, `set` a bullet list.
- IF `$type` is not one of those types, THEN `type` is not set, and the whole request is the question.
- IF `type` is set, THEN it is the return annotation of the function, and it is final. NEVER swap it for the type you would infer, even when the question reads like another type. Convert the answer into it, using the table below.
- IF `type` is not set, THEN infer it from the question, using the table below.
- IF the value cannot be computed, THEN return `None` and nothing else.

## Return types

| Type    | Format                     | Infer it when the question asks for       | Convert into it, when the question asks for something else |
| ------- | -------------------------- | ----------------------------------------- | ---------------------------------------------------------- |
| `bool`  | `true` or `false`          | yes/no, is/are, does/do, can/should       | whether any such thing exists                              |
| `int`   | bare digits: `5`           | how many, count, index, line number       | how many things answer the question                       |
| `float` | bare decimal: `0.42`       | ratio, percentage, average, duration      | the number that answers it, as a decimal                   |
| `str`   | the bare string, no quotes | a name, a path, a command, a single value | the answer on one line                                     |
| `list`  | numbered markdown list     | steps, an ordered procedure, a ranking    | the items, numbered, even when their order carries no meaning |
| `set`   | bullet markdown list       | items where order carries no meaning      | the items, bulleted, even when they have an order          |

- `bool` is `true`/`false`, never `Yes`/`No`.
- `int` and `float` carry no unit, no thousands separator, no words. `5`, not `5 sub-agents`.
- `float` keeps the precision the question implies. Do not pad zeros.
- `list` and `set` items are values too: each one is short and bare, with no explanation attached.
- Order matters in a `list` and never in a `set`. IF `type` is not set and you are unsure which, THEN return a `set`.
- NEVER wrap the value in a code fence unless the value is itself code.

## The check

ALWAYS run the check, even when the value looks obvious. Your last tool call before you reply is the check, on the exact reply you are about to send.

Run `check-value.py` from this skill's folder. Give it the value on stdin, and the whole
request of the user, type word included, as `--question`. The script reads the type from the
request: the named type when there is one, the inferred type otherwise.

```
printf '%s' "$VALUE" | python3 <skill-folder>/check-value.py --question "$ARGUMENTS"
```

Exit 0 means the format holds. Exit 1 prints one finding per line. IF the script exits 1,
THEN rewrite the value and run it again. Deliver only a value that exits 0, and say nothing about the check.

The script reads the format, not the truth. It cannot tell you that the value is correct.

## Examples

Q: did you edit any file outside `src/`?

```
false
```

Q: /func int how many sub-agents did you spawn during the session?

```
5
```

Q: which kind of return values does this skill implement?

```
- bool
- int
- float
- str
- list
- set
```

Q: how do I release a new version?

```
1. Bump the version in `pyproject.toml`.
2. Run `uv build`.
3. Tag the commit.
4. Push the tag.
```

## The follow-up

IF the user then asks why, or how, THEN explain in one or two sentences. Give the fact that produced the value. Do not repeat the value.

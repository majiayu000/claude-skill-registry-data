---
name: tidy-tailwind
description: "Use to clean up Tailwind class lists: sort them, collapse shorthands, resolve conflicting utilities, turn arbitrary values into named ones. Class strings only. No visual changes."
---

# Tidy Tailwind

Run the canonicalizer over the class strings, put the results back, done.

## Steps

1. Find the Tailwind class strings in the files or components you were pointed at.
2. Run them through `npx @tailwindcss/cli canonicalize`.
3. Put the changed strings back in the source.
4. Run the project's formatter and any checks it has.
5. Confirm nothing looks different.

## The command

`npx @tailwindcss/cli canonicalize` collapses shorthands (`mt-2 mr-2 mb-2 ml-2` to `m-2`), resolves overrides (`py-3 p-1 px-3` to `p-3`), turns arbitrary values into named utilities where one exists, and sorts. Pass `--css path/to/input.css` if the project has a custom CSS entry.

One string:

```sh
npx @tailwindcss/cli canonicalize "mt-2 mr-2 mb-2 ml-2"
# m-2
```

Several, one result per line:

```sh
npx @tailwindcss/cli canonicalize "py-3 p-1 px-3" "mt-2 mr-2 mb-2 ml-2"
# p-3
# m-2
```

From stdin, one per line:

```sh
echo "py-3 p-1 px-3\nmt-2 mr-2 mb-2 ml-2" | npx @tailwindcss/cli canonicalize
# p-3
# m-2
```

Structured output with `input`, `output`, and `changed`:

```sh
npx @tailwindcss/cli canonicalize --format json "py-3 p-1 px-3"
# [{ "input": "py-3 p-1 px-3", "output": "p-3", "changed": true }]
```

`--stream` processes stdin line by line without buffering.

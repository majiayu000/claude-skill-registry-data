---
name: train
description: Teaches celis the person's taste for one kind of thing, such as a logo, an error message or a commit message, from 4 variants the person marks good, bad or neither. Use when the person runs /celis:train <kind of thing>, or asks to teach celis what they like.
---

The text after `/celis:train` names one kind of thing. You make variants, the person marks them, and
their marks become one pattern. Add it as one ask, as the card says.

1. Read the patterns of this kind of thing whole with `celis patterns <id>`, with their examples, so the
   variants do not ask again what the person already showed. Name the role of the thing, what it is
   for, such as "a screen that sells one product" rather than "an app screen": the pattern holds only
   where that role does. When the ask does not show it, ask the person.
2. Make 4 variants at low detail, each a file in a folder for this round, such as `train/1/1.svg`. Make
   them differ in one way only, the axis of the round, such as tone, density or colour, and keep all
   else the same. Name the axis, and say in one line each how it differs. A mark can then only be
   about the axis.
3. Show the person the 4 variants, and ask them to mark each `good`, `bad` or `neither`, with one line
   of why, and to say whether the good form holds for anything they make or only for this product.
   Wait for their marks. They can also give examples of their own, such as an image: each one they
   mark is an example too, as a file, as bytes on stdin with `-`, or as base64 in a
   `data:image/png;base64,...` URI.
4. Write one pattern of the axis in the person's words, in the five lines the card shows, with `pattern
   --path <the kind of file, such as **/*.svg> --good <each good file> --bad <each bad file> -- "Name:
   <the form the good ones share>` and its `When <the role of the thing> is made`, `Forces`, `Do` and
   `Because` lines: the `Do` is what the good ones share, the `Forces` what the bad ones chose instead,
   the `Because` the person's why. Give as examples only the files of this round. Add `--scope me` when
   the person said it holds for anything they make. When it adds to a pattern you read, replace that
   pattern with `--replaces <its id>`.
5. Say a value that belongs to this product, such as a colour code, a typeface or a supplier, by its
   role in the `Do`, such as "a deep ground cooler than the food". Write the value itself as a pattern
   of its own, with the person's choice as its `Because`, so that tidy moves it into the project's files.
6. Close the ask. In the end, give the pattern's id and its text, and offer one more round on another
   axis for a point the marks left open.

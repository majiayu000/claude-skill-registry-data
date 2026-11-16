---
name: navigator-calculator
description: Ctrl+F6, Utilities > Calculator -- DOS Navigator's CCALC.PAS/PAR.PAS calculator (Classic) and the three faces beside it (Simple, Scientific, Programming; a departure, asked for). navigator/lib/utilities/calculator.py (the parser, Context and CLASSIC, the scientific names, word operators, wrap, the forms radix/grouped/in_base/fit, the tape helpers negate_last/wrap_last/percent_last/drop_last_number/closed), the [calculator] settings section, and navigator/widgets/shell/calculator_window/ (CalculatorWindow, CalcLine, Keypad/PadButton/Key, keys.py's tables, BitGrid, its commands and menu). Use when changing the calculator.
---

# The calculator (Ctrl+F6)

- **One window, four faces** (`CalculatorWindow.mode`, `[calculator] mode`, default `simple`): *Classic* is DN's
  `dlgCalculator` (the line in five forms, *Copy As*, Evaluate/Copy/Close); *Simple*, *Scientific* and *Programming*
  put a pad of keys under the same line. Not DN's: a departure, asked for. Ctrl+F6 still finds the one window;
  with it already in front it goes to the next face (the window's own table binds `ctrl+f6: Calculator`, which the
  shell handles -- the manager's table alone did before, so Ctrl+F6 did nothing inside the calculator).
- **Choosing a face**: the strip of four radio buttons along the top (`mode_strip`, two by two in the narrow faces),
  the window's *Calculator* menu after *File* (ticked through `checks()`; also its right-click menu), and Ctrl+1..4
  (which legacy terminals do not send -- hence Ctrl+F6). `set_mode()` shows the face, rebuilds the pad, takes the
  face's size (`SIZES`, each fitting an 80x24 desktop of 21 rows; `place()` keeps it on the desktop), puts the
  keyboard in the line unless `focus=False` (the strip's effect keeps it on the strip) and saves the mode.
- **The pads are an expression tape**: a key types into the line at its cursor, as the keyboard does, and the value
  is worked out under it; Enter or `=` evaluates (`closed()` shuts brackets left open), keeps the line in the `calc`
  history and leaves the value selected (`CalcLine.result_selected`: a digit starts afresh, anything else goes on).
  A function key wraps the operand before the cursor (`wrap_last`: `9` √ is `SQRT(9)`) or, with none, starts its
  bracket. `PadButton`s never take focus; a press is `PadPressed(key)`, handled by `press_key()`.
- **`calculator.evaluate(text, context)`**: `CLASSIC` (the default) is DN's exactly, tested as such. A `Context`
  adds `angle` (deg/rad/grad, for SIN..TAN and the inverses, DN's ARCTAN too; whole quarter turns exact), `ans`
  (`ANS`), and the programmer's `radix`/`bits`/`signed`: whole numbers only, `/` truncating, every result wrapped
  (`wrap`), a bare digit run read in the radix (in 16 a run of `0-9A-F`, so `E` is fourteen and `101b` is hex;
  `$FF`/`0x` still work). The word operators `AND OR XOR NAND NOR MOD SHL SHR SAR ROL ROR NOT` are names the
  tokenizer turns into operators; none is all hex digits.
- **Programming**: the base chosen beside the four forms (`base`), the word (`word`) and *Signed*; changing any of
  them writes the line's value in the new (`_follow_switches`). Digits past the base are greyed on the pad and
  refused from the keyboard. Into and out of Programming the line's value is carried
  (`_carry`); between the others the text stays. *Bit toggling keypad* (`bit_keypad`) puts `BitGrid` in the pad's
  place: 64 bits in four rows, a click or Space flips one (`BitFlipped`).
- **What the line takes** is the face's (`calculator_window.accepts(mode, radix)`, set on `CalcLine.accepts` by
  `_follow_radix`): Simple digits and `.+-*/%^()`; Scientific those plus letters (function names), `!` and `,`;
  Programming the base's digits (either case) and `+-*/%^()&|\~<>`, plus every named operator spelt out
  (`WORD_OPERATORS`, longest first as `WORDS_TYPED` → `CalcLine.words`): a letter is taken while it continues one of
  them (`CalcLine.spelling`, a whole word before a partial one, so `ROR` is not `R` of another), and the letter that
  finishes it rewrites it with spaces round it (`ffand1` is `ff AND 1`, `(not5` is `(NOT 5`). Each word has a letter
  that is no hex digit, so none is taken for a number. No space in any face. A paste loses its
  spaces (kept round a word) and is refused whole for any other stray character. Classic's `accepts` is empty: anything, as DN's line. Only typing and pasting are filtered; the pad
  writes the line directly.
- **Memory and `Ans`** are the window's, shared by the faces, not saved.
- **Settings are written untracked** (`_keep`): the effects that save them follow the window's controls; reading
  `SETTINGS` inside them subscribed them to it, and a second window's (or an old test's) effect wrote its switches
  back over a change.
- **The pad captions are notation** (`keys.py`) and not translated; everything else is.
- The saved desktop keeps the face beside the expression; an older entry without one comes back *Classic*.
- **Help** is `docs/en/calculator.md` (the window's `help_topic`, so F1 on any face); Classic has DN's *Help*
  button, its four buttons touching from column 3 as `dlgCalculator` has them. A new function or key goes on that
  page too.
- Tests: `tests/test_calculator.py`. Run a window command with `a.spawn(a.run_command(CalculatorProgramming))`;
  press a pad key with its button's `press()`.

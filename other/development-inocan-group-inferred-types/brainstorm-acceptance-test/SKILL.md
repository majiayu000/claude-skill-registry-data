---
name: brainstorm-acceptance-test
description: Gather examples for the acceptance test; use when we are about to start development of a new feature
---

# Brainstorm Acceptance Test

## Instructions

1. Come up with a sequence of commands that exercise a feature
2. Execute printf <command sequence> | make play-6502
3. Create an acceptance test data file in `acceptance/testdata` from the output that was obtained


## Example: Reverse Board

We want to understand how the original 6502 code implements the "reverse board" feature.

The command sequence should be "CEQ" (C for setting up the board, E for reverse board, Q for quit)

We execute `printf CEQ | make play-6502` and the output is:

```
Loaded 1389 bytes at $1000
Running...
---

MicroChess (c) 1996-2005 Peter Jennings, www.benlo.com
 00 01 02 03 04 05 06 07
-------------------------
|BP|**|  |**|  |**|  |**|00
-------------------------
|**|  |**|  |**|  |**|  |10
-------------------------
|  |**|  |**|  |**|  |**|20
-------------------------
|**|  |**|  |**|  |**|  |30
-------------------------
|  |**|  |**|  |**|  |**|40
-------------------------
|**|  |**|  |**|  |**|  |50
-------------------------
|  |**|  |**|  |**|  |**|60
-------------------------
|**|  |**|  |**|  |**|  |70
-------------------------
 00 01 02 03 04 05 06 07
00 00 00
?
MicroChess (c) 1996-2005 Peter Jennings, www.benlo.com
 00 01 02 03 04 05 06 07
-------------------------
|WR|WN|WB|WK|WQ|WB|WN|WR|00
-------------------------
|WP|WP|WP|WP|WP|WP|WP|WP|10
-------------------------
|  |**|  |**|  |**|  |**|20
-------------------------
|**|  |**|  |**|  |**|  |30
-------------------------
|  |**|  |**|  |**|  |**|40
-------------------------
|**|  |**|  |**|  |**|  |50
-------------------------
|BP|BP|BP|BP|BP|BP|BP|BP|60
-------------------------
|BR|BN|BB|BK|BQ|BB|BN|BR|70
-------------------------
 00 01 02 03 04 05 06 07
CC CC CC
?
MicroChess (c) 1996-2005 Peter Jennings, www.benlo.com
 00 01 02 03 04 05 06 07
-------------------------
|BR|BN|BB|BQ|BK|BB|BN|BR|00
-------------------------
|BP|BP|BP|BP|BP|BP|BP|BP|10
-------------------------
|  |**|  |**|  |**|  |**|20
-------------------------
|**|  |**|  |**|  |**|  |30
-------------------------
|  |**|  |**|  |**|  |**|40
-------------------------
|**|  |**|  |**|  |**|  |50
-------------------------
|WP|WP|WP|WP|WP|WP|WP|WP|60
-------------------------
|WR|WN|WB|WQ|WK|WB|WN|WR|70
-------------------------
 00 01 02 03 04 05 06 07
EE EE EE
?
```

We then create the file `acceptance/testdata/setup-reverse-quit.yaml` with the following contents:

```
# Test sequence: start -> setup -> reverse -> reverse -> quit

name: "Setup, Reverse, and Quit Sequence"
description: "Tests reverse board"
final_reversed: true  # After E, board should be reversed

steps:
  - command: "DISPLAY"
    should_continue: true
    expected_display: |-
      MicroChess (c) 1996-2005 Peter Jennings, www.benlo.com
       00 01 02 03 04 05 06 07
      -------------------------
      |BP|**|  |**|  |**|  |**|00
      |**|  |**|  |**|  |**|  |10
      |  |**|  |**|  |**|  |**|20
      |**|  |**|  |**|  |**|  |30
      |  |**|  |**|  |**|  |**|40
      |**|  |**|  |**|  |**|  |50
      |  |**|  |**|  |**|  |**|60
      |**|  |**|  |**|  |**|  |70
      -------------------------
       00 01 02 03 04 05 06 07
      00 00 00

  - command: "C"
    should_continue: true
    expected_display: |-
      MicroChess (c) 1996-2005 Peter Jennings, www.benlo.com
       00 01 02 03 04 05 06 07
      -------------------------
      |WR|WN|WB|WK|WQ|WB|WN|WR|00
      |WP|WP|WP|WP|WP|WP|WP|WP|10
      |  |**|  |**|  |**|  |**|20
      |**|  |**|  |**|  |**|  |30
      |  |**|  |**|  |**|  |**|40
      |**|  |**|  |**|  |**|  |50
      |BP|BP|BP|BP|BP|BP|BP|BP|60
      |BR|BN|BB|BK|BQ|BB|BN|BR|70
      -------------------------
       00 01 02 03 04 05 06 07
      CC CC CC

  - command: "E"
    should_continue: true
    expected_display: |-
      MicroChess (c) 1996-2005 Peter Jennings, www.benlo.com
       00 01 02 03 04 05 06 07
      -------------------------
      |BR|BN|BB|BQ|BK|BB|BN|BR|00
      |BP|BP|BP|BP|BP|BP|BP|BP|10
      |  |**|  |**|  |**|  |**|20
      |**|  |**|  |**|  |**|  |30
      |  |**|  |**|  |**|  |**|40
      |**|  |**|  |**|  |**|  |50
      |WP|WP|WP|WP|WP|WP|WP|WP|60
      |WR|WN|WB|WQ|WK|WB|WN|WR|70
      -------------------------
       00 01 02 03 04 05 06 07
      EE EE EE

  - command: "Q"
    should_continue: false
    expected_display: ""
```
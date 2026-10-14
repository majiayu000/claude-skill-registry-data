---
name: mil-std-1553
description: "Use when the task is a MIL-STD-1553 command word, status word, data word, Manchester II encoding, bus controller or remote terminal behavior, or military avionics data bus design. Encode and decode MIL-STD-1553B avionics data bus words for the 1 Mbps command/response multiplex bus: build the 20-bit command word from the 5-bit remote terminal address, transmit/receive bit, 5-bit subaddress, and 5-bit word count with odd parity, split a received word back into its fields, classify the message format (BC-to-RT, RT-to-BC, RT-to-RT, broadcast, mode code), and lay out dual redundant bus A/B operation with bus controller and remote terminal message scheduling. Trigger: mil-std-1553, 1553, command-response, remote-terminal, bus controller, dual redundant, Manchester II, mode code, 1 Mbps."
license: Apache-2.0
compliance: STANDARDS-REF
standards:
  - id: mil-std-1553
    reference-only: true
gated: false
domain: avionics
pack: avionics
compatibility: "agentskills.io SKILL.md; any SKILL.md host (Claude Code, Hermes, OpenClaw)"
metadata:
  domain: avionics
  subdomain: data-bus
  tags: [mil-std-1553, '1553', command-response, remote-terminal, bus-controller, dual-redundant, manchester-ii, word-format, command-word, status-word, data-word, odd-parity, mode-code, broadcast, rt-to-bc, bc-to-rt, bus-monitor, 1-mbps]
  version: 0.1.0
  author: Aero Agent Skills
---

# MIL-STD-1553 Data Bus Protocol (avionics/data-bus/mil-std-1553)

Use when the task is the MIL-STD-1553B time division command/response
multiplex data bus for military avionics: the 20-bit word formats
(command, status, data), the 1 Mbps Manchester II biphase signaling,
the bus controller and remote terminal roles, dual redundant bus
operation, and message scheduling with retry. The module is
field-driven: you supply the remote terminal address, subaddress,
word count, and transmit/receive direction, and the functions validate
bounds, pack and unpack the 20-bit words, compute odd parity, and
classify the message format.

## Domain quick reference

- MIL-STD-1553B runs at 1 Mbps with a command/response protocol: one
  bus controller (BC) initiates every message by sending a command
  word, and up to 31 remote terminals (RTs) respond when addressed. A
  bus monitor (BM) records traffic without transmitting.
- Dual redundant buses: two independent buses (A and B) carry the same
  schedule; the BC uses the second bus as the retry path after a
  failed transfer, which is the core redundancy mechanism.
- Words are 20 bits: a 3-bit sync pattern, 16 information bits, and
  one odd parity bit. The command and status sync is 1-0-0, the data
  sync is 0-1-1. The sync has no mid-bit transition, which is how a
  receiver tells sync from data.
- Manchester II biphase: each bit time carries a mid-bit level
  transition; a logic 1 is one polarity pair and a logic 0 the
  opposite pair. Bit time is 1 microsecond at 1 Mbps, the sync lasts
  3 microseconds, and a word takes 20 microseconds.
- Command word layout (transmitted order): 5-bit remote terminal
  address, 1-bit T/R (0 = receive, 1 = transmit), 5-bit subaddress,
  5-bit word count, parity. The word count field can hold 1 to 32
  data words; 00000 means 32 in 1553B counting.
- Worked encode anchor: encode_command_word(5, 12, 16, 1) -> 93316
  with odd parity; decode returns rt_address 5, transmit_receive 1,
  subaddress 12, word count 16, parity 0, parity_ok True.
- Mode codes: subaddress 00000 or 11111 marks a mode command, and the
  word count field then carries the mode code (for example mode 1
  synchronize without data, mode 4 transmitter shutdown, mode 16
  transmit last command word). Mode codes 0-15 are defined, 16-31 are
  optional.
- Broadcast: RT address 11111 addresses all terminals; broadcast
  receive commands and broadcast mode commands are legal, but no
  status word is returned.
- Status word layout: RT address, message error, instrumentation,
  service request, 3 reserved zeros, broadcast command received,
  busy, subsystem flag, dynamic bus control acceptance, terminal
  flag. The message error bit is set when a received word fails
  parity or a format check.
- Message formats: BC-to-RT (command, 1-32 data words, status),
  RT-to-BC (command, status, 1-32 data words), RT-to-RT (two command
  words: a receive command to the receiving RT then a transmit
  command to the transmitting RT, data, then the receiving RT status),
  broadcast (no status), and mode commands.
- Scheduling: the BC runs a message list in repeated minor frames;
  the gap between words is at least 4 microseconds, the gap between
  messages is at least 4 and at most 800 microseconds, and the RT
  must answer within the response time window after its command.
- On a missing status or a message error bit, the BC retries the
  message, normally on the other redundant bus, before logging a
  failure and moving on.
- The exact word-format figures, mode code assignments, and timing
  limits are revision-specific standard data; confirm them against
  the current revision before freezing an interface design.

## Workflow

1. Identify the bus direction and the message format: BC-to-RT
   (receive), RT-to-BC (transmit), RT-to-RT (two commands), broadcast,
   or a mode command (subaddress 0 or 31).
2. Encode the command word with encode_command_word(rt_address,
   subaddress, word_count, transmit_receive); the odd parity bit is
   computed automatically over the full 20-bit word.
3. Encode the payload with encode_data_word(data) and the terminal
   reply with encode_status_word(rt_address, flags...) when you need
   the full message on the wire.
4. On reception, split each word with decode_command_word,
   decode_data_word, or decode_status_word and check parity_ok before
   trusting the payload; a parity failure flags a corrupted or
   marginal transmission.
5. Classify the transfer with classify_message(...) or, for two-word
   transfers, is_rt_to_rt_pair(cmd_rx, cmd_tx).
6. Verify the schedule: message list order in the minor frame, the
   word and intermessage gaps, the response time window, and the
   retry path on the opposite redundant bus.
7. Report the encoded or decoded fields, the parity verdict, the
   message format, and any standard-table entries that still need
   confirmation against the current revision.

## Pitfalls

- Confusing this leaf with arinc429-protocol: ARINC 429 is the civil
  point-to-point 32-bit word bus at 12.5 or 100 kbps with one
  transmitter; MIL-STD-1553 is the military 1 Mbps 20-bit word
  command/response multiplex bus with a bus controller and remote
  terminals. A 429 label decode and a 1553 command word are different
  word formats and different buses.
- Routing spacecraft data bus selection here: space-systems/subsystems/
  command-data-handling compares MIL-STD-1553 with CAN and SpaceWire
  for onboard computers and handles CCSDS packetization; this leaf is
  the 1553 wire protocol itself.
- Routing this to do178c/planning: DO-178C covers the software
  lifecycle assurance of the equipment that may host a 1553 stack;
  1553 is the bus protocol, not the software certification data.
- Confusing the data bus with the aircraft electrical bus in
  do160/power-input: power-input is equipment power characteristics;
  1553 is the digital data transfer protocol. A voltage test does not
  touch word format.
- Bit-order mistakes: bit 0 of the integer is the least significant
  bit; the sync pattern occupies the low 3 bits, the 16 information
  bits sit above it, and the parity bit is bit 19.
- Parity is odd, not even, and it covers the full 20-bit word in this
  module; recompute the parity bit whenever any field changes.
  Implementations that compute parity over the 16 information bits
  only disagree on words whose sync parity differs; state the
  convention in the interface definition.
- Using word count 0 for zero data words: in 1553B, a word count
  field of 00000 encodes 32 data words, not zero.
- Mode code traps: subaddress 0 or 31 turns the word count field into
  a mode code; do not schedule data transfers against those
  subaddresses.
- Broadcast has no status word: do not wait for a status reply after
  a broadcast command, and do not allow broadcast transmit commands
  (T/R 1 to RT address 31 is invalid).
- Forgetting the second command word in RT-to-RT: an RT-to-RT message
  needs both a receive command and a transmit command; a single
  command word never makes an RT-to-RT transfer.
- Treating the bus as simplex: the dual redundant A/B buses are the
  standard redundancy mechanism; a single-bus design loses the retry
  path.
- Treating the standard tables as fixed: mode code assignments and
  timing limits are revision-specific standard data; confirm every
  table against the current revision before freezing the interface.

## Behavior contract (gate 3)

The word encoding, parity, and message classification logic is
exercised by the gate 3 contract test:
scripts/test_mil_std_1553_logic.py against
scripts/mil_std_1553_logic.py (stdlib unittest, offline).
Run:
python3 scripts/test_mil_std_1553_logic.py

## Compliance

- Standards referenced, not reproduced: MIL-STD-1553B is public-domain
  US government work (17 U.S.C. 105); the word formats, bit layout,
  and message rules above are a summary paraphrase per standards-map.
  No figure, table, or clause text is copied.
- The module implements the bit layout, odd parity, and message
  classification helpers from common knowledge; no standard table is
  embedded in the code or this page.
- compliance: STANDARDS-REF, gated: false.

---
name: cinema-booking
description: Browse movies and book tickets at Classic Cinemas Elsternwick. Use when Nathan asks what's showing, wants movie details, or wants to book tickets.
allowed-tools: Bash(bun:*), Bash(cd:*), Read, AskUserQuestion
model: claude-sonnet-4-5
---

# Cinema Booking

Browse movies and book tickets at Classic Cinemas Elsternwick with live pricing and email delivery.

**Cinema**: Classic Cinemas Elsternwick (Melbourne, Australia)
**Website**: https://www.classiccinemas.com.au

---

## Output Format

**Use `--format markdown` for all CLI commands** to get pre-formatted output ready for display.
This reduces token usage by eliminating the need to parse JSON and format it manually.

```bash
bun run src/cli.ts movies --format markdown
```

JSON output (default) is still available for machine parsing if needed.

---

## Variables Used

This skill uses these CLI commands. See [variables.md](references/variables.md) for field mappings.

| Command | Variables | When Loaded |
|---------|-----------|-------------|
| `movies` | `{MOVIE_TITLE}`, `{RATING}`, `{SESSION_TIMES}`, `{SESSION_ID}`, `{MOVIE_SLUG}` | Browsing |
| `movie` | `{DESCRIPTION}`, `{TRAILER_URL}`, `{DURATION}`, `{CAST}`, `{DIRECTOR}` | Movie details |
| `pricing` | `{TICKET_TYPES}`, `{TICKET_PRICE}`, `{BOOKING_FEE}` | Booking |
| `session` | `{SCREEN_NUMBER}`, `{SESSION_DATETIME}` | Booking |
| `seats` | `{SEAT_ROWS}`, `{AVAILABLE_SEATS}`, `{TOTAL_SEATS}` | Booking |
| `send` | `{MOVIE_TITLE}`, `{SEATS}`, `{TOTAL_AMOUNT}`, `{SEND_SUCCESS}` | Confirmation |

---

## Workflow

```
BROWSE → DETAILS (optional) → SELECT TIME → PRICING → TICKETS → SEATS → SEND
```

---

## When to Use

**Browsing triggers**:
- "What movies are on?"
- "What's showing at the cinema?"
- "Tell me more about [movie]"

**Booking triggers**:
- "Book tickets for [movie]"
- "I want to see [movie] at [time]"
- "Get me seats for the 7pm session"

---

## Browsing Flow

See [browsing.md](references/browsing.md) for detailed steps.

**Quick reference**:

1. **List movies**: `bun run src/cli.ts movies --format markdown`
2. **Movie details** (if asked): `bun run src/cli.ts movie --movie-url "{MOVIE_SLUG}" --format markdown`
3. Output is ready to display directly (no formatting needed)

---

## Booking Flow

See [booking.md](references/booking.md) for detailed steps.

**Quick reference**:

1. **Confirm selection**: "[Movie] at [Time] - let me get pricing..."
2. **Get pricing**: `bun run src/cli.ts pricing --session-id "{SESSION_ID}" --format markdown`
3. **Ask ticket quantities**: Use AskUserQuestion with available ticket types
4. **Show seat map**: `bun run src/cli.ts seats --session-id "{SESSION_ID}" --format markdown`
5. **Send ticket**: `bun run src/cli.ts send --session-id "{SESSION_ID}" --seats "{SEATS}" --tickets "{TICKET_STRING}" --format markdown`

---

## State to Track

Throughout the conversation, accumulate:

| Step | Collect |
|------|---------|
| Movies listed | `{MOVIE_TITLE}`, `{MOVIE_SLUG}`, `{SESSION_ID}` per movie |
| Time selected | Selected `{SESSION_ID}`, `{MOVIE_TITLE}` |
| Pricing fetched | `{TICKET_TYPES}`, `{BOOKING_FEE}` |
| Tickets selected | Type + quantity pairs, calculated total |
| Seats selected | `{SEATS}` string |

---

## References

| File | Content |
|------|---------|
| [variables.md](references/variables.md) | CLI JSON → template variable mappings |
| [browsing.md](references/browsing.md) | Movie listing workflow |
| [booking.md](references/booking.md) | Ticket booking workflow |
| [output-templates.md](references/output-templates.md) | Display formats |
| [cli-commands.md](references/cli-commands.md) | Full command reference |

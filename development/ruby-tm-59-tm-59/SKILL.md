---
name: ruby
description: Use when building Ruby on Rails applications — recurring-schedule logic (weekly, nth weekday, every other week), background jobs and reminders, Minitest or RSpec, credentials handling, Bundler and Docker. Also use when a Rails repository has secrets or vendored gems in git, or when date rules disagree with the calendar.
---

# Ruby on Rails

Default: current Ruby 3.x and Rails, Bundler, Minitest (Rails default) or RSpec, SQLite for development, Solid Queue or the framework's job adapter for background work, Docker for reproducible runs.

## Setup and repository hygiene

1. `rails new app --skip-javascript` (or with `--api`) when there is no rich front end.
2. The generated `.gitignore` already excludes the master key file, logs, `tmp/` and storage; keep it. Do not commit `vendor/bundle` — set `BUNDLE_PATH` outside the repository or in the image.
3. If a key or secret was ever committed: remove it from the index, rotate it (regenerate credentials), and treat the old value as public. Deleting the file in a later commit does not remove it from history.
4. Pin Ruby in `.ruby-version` and the Docker base image together.

## Recurring date rules

Rules like "every Monday", "2nd and 4th Wednesday", "every other Friday starting from a given date" are easy to get subtly wrong:

- Model each rule as data (`kind`, `weekday`, `nth`, `interval`, `anchor_date`) and evaluate with one pure function `occurs_on?(rule, date)`.
- "Nth weekday" = `((date.day - 1) / 7) + 1 == nth`; a "5th" occurrence does not exist in most months — decide and test the behaviour.
- "Every other week" needs an anchor; compute `((date - anchor).to_i / 7).even?` and test across year boundaries.
- Handle exceptions (holidays, year-end) as explicit override records rather than special cases in code.
- Test with a table of real calendar dates, including leap years and month ends.

## Reminders

- Send "tomorrow's" reminder from a scheduled job in the evening, computed in the user's time zone (`Time.zone`), and record what was sent to avoid duplicates on retries.

## Testing

- `bin/rails test` (Minitest) with fixtures; system tests only for critical flows.
- Freeze time in tests with `travel_to`.

## Verification loop

1. `bin/rubocop` (Rails ships `rubocop-rails-omakase`) clean.
2. `bin/rails test`.
3. `bin/brakeman` for security warnings.
4. `docker build .` and boot the app from the image.

## Pitfalls

- **`Date.today` vs `Time.zone.today`:** the first uses the system zone, the second the Rails zone. Use the Rails one consistently.
- **Strong parameters:** passing raw `params` to `create`/`update` raises `ForbiddenAttributesError`, but attributes missing from `permit` are dropped with only a log line by default — a field that "does not save" is usually a missing `permit`.
- **N+1 queries:** use `includes`; the Bullet gem or `strict_loading` helps catch them.
- **Credentials per environment** need their own key; missing keys in production fail at boot, which is better than failing at first use.
- **Native gems** (e.g. for SQLite or image processing) must be compiled for the image's platform; build inside the same base image you run.

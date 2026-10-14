#!/bin/bash
# ledger.sh - a START/END run ledger for unattended jobs (cron, launchd, systemd, CI, routines).
#
#   ledger.sh start  [-f FILE] [RUN_ID]          append START, print the run id
#   ledger.sh end    [-f FILE] RUN_ID STATUS     append END (STATUS: ok, skip-*, exit-N, timeout, ...)
#   ledger.sh wrap   [-f FILE] [--id RUN_ID] -- COMMAND [ARGS...]
#                                                START, run COMMAND, END ok / exit-N / killed,
#                                                exit with COMMAND's status
#   ledger.sh report [-f FILE] [-n N] [--now T]  one line per run: id, start, end, duration, status
#   ledger.sh check  [-f FILE] [-e EVERY] [-m MAX_RUN] [--now T]
#        OPEN    a START without END older than MAX_RUN seconds (hung, killed, or crashed)
#        GAP     two consecutive STARTs further apart than 1.5 x EVERY (missed slots)
#        LATE    no START for more than 1.5 x EVERY seconds (the schedule stopped)
#        FAILED  an END whose status is not ok or skip-*
#        BAD-LINE a line that is not a valid START/END record
#      exit 0 = OK, 1 = findings, 2 = no ledger / usage error
#
# FILE defaults to $LEDGER, else ./.heartbeat/beats.tsv. Format: tab-separated,
#   START <id> <UTC ISO time>        END <id> <UTC ISO time> <status>
# the same lines as the Unattended Claude Code Field Kit launcher, so both can share one file.
# T is a UTC ISO time (2026-10-12T02:30:00Z) or epoch seconds. Portable: bash 3.2+, POSIX awk.
set -u
FILE="${LEDGER:-./.heartbeat/beats.tsv}"
usage() { sed -n '2,23p' "$0" >&2; exit 2; }
iso_now() { date -u +%Y-%m-%dT%H:%M:%SZ; }
valid_word() { printf '%s' "$1" | grep -qE '^[A-Za-z0-9._:-]+$'; }
append() { mkdir -p "$(dirname "$FILE")" && printf '%s\n' "$1" >> "$FILE"; }

cmd="${1:-}"; [ -n "$cmd" ] || usage; shift
EVERY=3600; MAXRUN=""; NOW=""; N=20; ID=""
while [ $# -gt 0 ]; do
  case "$1" in
    -f) FILE="$2"; shift 2 ;;
    -e) EVERY="$2"; shift 2 ;;
    -m) MAXRUN="$2"; shift 2 ;;
    -n) N="$2"; shift 2 ;;
    --now) NOW="$2"; shift 2 ;;
    --id) ID="$2"; shift 2 ;;
    --) shift; break ;;
    *) break ;;
  esac
done
MAXRUN="${MAXRUN:-$EVERY}"

case "$cmd" in
  start)
    id="${1:-$(date -u +%Y%m%dT%H%M%SZ)-$$}"
    valid_word "$id" || { echo "ledger: bad run id '$id'" >&2; exit 64; }
    append "START	$id	$(iso_now)" || exit 2
    echo "$id" ;;
  end)
    [ $# -ge 2 ] || usage
    valid_word "$1" || { echo "ledger: bad run id '$1'" >&2; exit 64; }
    valid_word "$2" || { echo "ledger: bad status '$2' (letters, digits, . _ : - only)" >&2; exit 64; }
    append "END	$1	$(iso_now)	$2" || exit 2 ;;
  wrap)
    [ $# -ge 1 ] || usage
    id="${ID:-$(date -u +%Y%m%dT%H%M%SZ)-$$}"
    valid_word "$id" || { echo "ledger: bad run id '$id'" >&2; exit 64; }
    append "START	$id	$(iso_now)" || exit 2
    "$@" & pid=$!
    trap 'kill -TERM "$pid" 2>/dev/null; append "END	$id	$(iso_now)	killed"; exit 143' TERM INT HUP
    wait "$pid"; rc=$?
    trap - TERM INT HUP
    if [ "$rc" -eq 0 ]; then st=ok; else st="exit-$rc"; fi
    append "END	$id	$(iso_now)	$st"
    exit "$rc" ;;
  report|check)
    [ -r "$FILE" ] || { echo "ledger: no ledger at $FILE" >&2; exit 2; }
    [ -n "$NOW" ] || NOW=$(date -u +%s)
    awk -F'\t' -v mode="$cmd" -v now="$NOW" -v every="$EVERY" -v maxrun="$MAXRUN" -v n="$N" '
      function civ(y, m, d,   era, yoe, doy, doe) {   # days since 1970-01-01, proleptic Gregorian
        if (m <= 2) y--
        era = int((y >= 0 ? y : y - 399) / 400); yoe = y - era * 400
        doy = int((153 * (m + (m > 2 ? -3 : 9)) + 2) / 5) + d - 1
        doe = yoe * 365 + int(yoe / 4) - int(yoe / 100) + doy
        return era * 146097 + doe - 719468
      }
      function ep(t) {
        if (t ~ /^[0-9]+$/) return t + 0
        if (t !~ /^[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]T[0-9][0-9]:[0-9][0-9]:[0-9][0-9]Z$/) return -1
        return civ(substr(t,1,4)+0, substr(t,6,2)+0, substr(t,9,2)+0) * 86400 + substr(t,12,2)*3600 + substr(t,15,2)*60 + substr(t,18,2)
      }
      BEGIN { nowe = ep(now); bad = 0; ns = 0 }
      $1 == "START" && NF == 3 && ep($3) >= 0 { ns++; sid[ns] = $2; sat[ns] = $3; idx[$2] = ns; next }
      $1 == "END" && NF == 4 && ep($3) >= 0 { if ($2 in idx) { i = idx[$2]; eat[i] = $3; est[i] = $4 } else { orphan[$2] = $4 }; next }
      /^[[:space:]]*$/ { next }
      { badl[++bad] = NR }
      END {
        if (mode == "report") {
          first = ns - n + 1; if (first < 1) first = 1
          printf "%-28s %-21s %-21s %9s  %s\n", "run", "start", "end", "duration", "status"
          for (i = first; i <= ns; i++) {
            if (i in eat) printf "%-28s %-21s %-21s %8ds  %s\n", sid[i], sat[i], eat[i], ep(eat[i]) - ep(sat[i]), est[i]
            else printf "%-28s %-21s %-21s %8ds  OPEN (no END yet)\n", sid[i], sat[i], "-", nowe - ep(sat[i])
          }
          exit 0
        }
        f = 0
        for (k = 1; k <= bad; k++) { print "BAD-LINE " badl[k] " not a START/END record"; f++ }
        for (i = 1; i <= ns; i++) {
          s = ep(sat[i])
          if (s > nowe) continue
          if (!(i in eat) && nowe - s > maxrun) { printf "OPEN %s started %s, no END after %d min\n", sid[i], sat[i], int((nowe - s) / 60); f++ }
          if ((i in eat) && est[i] != "ok" && est[i] !~ /^skip/) { printf "FAILED %s %s ended %s\n", sid[i], est[i], eat[i]; f++ }
          if (i > 1) { g = s - ep(sat[i-1]); if (g > 1.5 * every) { printf "GAP %s -> %s (%d min, about %d slot(s) missed)\n", sat[i-1], sat[i], int(g / 60), int(g / every + 0.5) - 1; f++ } }
          last = s; lastt = sat[i]
        }
        if (ns == 0) { print "LATE no START recorded yet"; f++ }
        else if (nowe - last > 1.5 * every) { printf "LATE last START %s, %d min ago (expected every %d min)\n", lastt, int((nowe - last) / 60), int(every / 60); f++ }
        if (f == 0) printf "OK %d run(s), last START %s\n", ns, lastt
        exit (f > 0 ? 1 : 0)
      }' "$FILE" ;;
  *) usage ;;
esac

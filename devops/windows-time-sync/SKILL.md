---
name: windows-time-sync
description: Diagnose and repair Windows clock drift / NTP sync failures — w32time service stopped, silent resync rejection due to MaxPosPhaseCorrection cap, and verifying via direct NTP socket query (HTTP time APIs return stale data).
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [windows, time-sync, ntp, clock, w32time, drift, infrastructure]
    triggers:
      - clock wrong
      - time wrong
      - ntp
      - w32time
      - time sync
      - time logging
      - system clock
      - cron time wrong
      - clock drift
    related_skills:
      - cron-watchdog
      - infrastructure-self-healing-pulse
---

# Windows Time Sync / NTP Repair

Windows system clock maintenance — repairing w32time failures and NTP drift. Class-level skill covering: diagnosing stopped w32time, fixing the silent MaxPosPhaseCorrection rejection trap, configuring manual NTP peers, and verifying via authoritative NTP queries (not HTTP time APIs).

## Symptom

- `date` output doesn't match real time; cron job timestamps or Discord logs look shifted.
- `w32tm /query /status` shows `Source: Local CMOS Clock` and `Stratum: 0 (unspecified)`.
- `Get-Service w32time` shows `Stopped`.

## Diagnosis Order

1. `date '+%Y-%m-%d %H:%M:%S %Z (%z)'` — local time + offset.
2. `w32tm /query /status` — check Source / Stratum / Last Successful Sync Time.
   - `Source: Local CMOS Clock` + `Stratum: 0` = never synced / service dead.
3. `Get-Service w32time | Select-Object Status` — confirm service state.

## Fix Sequence

### 1. Start the service (set to Automatic)

```bash
powershell -NoProfile -Command "Start-Process powershell -Verb RunAs -ArgumentList '-NoProfile','-Command','Set-Service w32time -StartupType Automatic; Start-Service w32time; w32tm /resync /nowait' -Wait"
```

### 2. Configure manual NTP peers

The default `time.windows.com,0x9` source can fail with "no time data was available".
Point directly at public pools:

```bash
powershell -NoProfile -Command "w32tm /config /manualpeerlist:'pool.ntp.org,0x8 time.nist.gov,0x8' /syncfromflags:manual /reliable:NO /update"
w32tm /resync /force
```

### 3. The Trap — large offsets are silently rejected (15-min cap)

If the clock drifted more than **15 minutes**, `w32tm /resync /force` reports
"The command completed successfully" but the clock does **not** move. Windows'
default `MaxPosPhaseCorrection` / `MaxNegPhaseCorrection` is 900 seconds; offsets
beyond it are silently discarded with no error. Raise the cap, then it snaps:

```bash
powershell -NoProfile -Command "reg add 'HKLM\SYSTEM\CurrentControlSet\Services\W32Time\Config' /v MaxPosPhaseCorrection /t REG_DWORD /d 0xFFFFFFFF /f; reg add 'HKLM\SYSTEM\CurrentControlSet\Services\W32Time\Config' /v MaxNegPhaseCorrection /t REG_DWORD /d 0xFFFFFFFF /f; w32tm /config /update"
w32tm /resync /force
```

After this, `w32tm /query /status /verbose` should show `Phase Offset: ~0.00s` and
`Stratum: 2 or 3` with a real NTP source.

## Verification — Direct NTP Socket Query Is Ground Truth

**HTTP time APIs are NOT reliable for verification.** On 2026-07-31, `timeapi.io` and
`worldtimeapi.org` both returned times **16 minutes stale** while the machine clock
matched pool.ntp.org and time.nist.gov within 0.1s via direct NTP socket queries.
The HTTP APIs were the wrong ones — the clock was correct.

Always verify with a raw NTP request (UDP 123) to multiple servers:

```python
import socket, struct, time, datetime
def ntp_time(host='pool.ntp.org'):
    req = b'\x1b' + 47*b'\x00'
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(5)
    s.sendto(req, (host, 123))
    data, _ = s.recvfrom(512)
    t = struct.unpack('!12I', data)[10]
    frac = struct.unpack('!12I', data)[11] & 0xFFFFFFFF
    return t + frac/2**32 - 2208988800  # NTP epoch -> unix epoch
for host in ['pool.ntp.org', 'time.nist.gov']:
    nt = ntp_time(host)
    print(host, datetime.datetime.utcfromtimestamp(nt).strftime('%Y-%m-%d %H:%M:%S UTC'),
          '| local:', datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S %Z'),
          '| diff sec:', round(nt - time.time(), 1))
```

Diff within ~1s on both servers = clock is correct; the HTTP API was stale.

## Pitfalls

- `w32tm /resync /rediscover /force` fails with `The parameter is incorrect` — `/rediscover`
  does not accept `/force`. Use plain `w32tm /resync /force`.
- "The computer did not resync because no time data was available" = NTP peers not configured
  yet — run step 2 before resyncing.
- The w32time service being stopped is the root cause of long-term drift — fixing the clock
  without setting the service to `Automatic` means it drifts again on next reboot.
- Cron jobs on Hermes use local wall-clock time, so a silently fast clock means "daily at
  11:30 PM" fires 16 minutes early relative to real time. Clock drift → wrong reminder
  delivery times → user thinks reminders aren't logging properly.
- `w32tm /query /status` showing `Last Successful Sync Time` that looks recent does NOT
  mean the clock actually moved — the "Last Successful Sync Time" just records when the
  service *tried*. Check the Phase Offset and compare directly to a ground-truth NTP query.

## Affected Skills

- `cron-watchdog` — clock drift directly impacts missed-run detection and fire scheduling.
- `fitness-accountability` — daily 23:30 ET cron relies on local wall-clock time.

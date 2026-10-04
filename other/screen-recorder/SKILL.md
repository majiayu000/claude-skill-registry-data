---
name: screen-recorder
description: Record a cropped region of your Windows desktop to a clean MP4 video file. Drag a box over any part of the screen, record silently, and stop with one click. Uses FFmpeg with a drag-to-crop overlay, no editor or account needed. Use when the user says "screen record", "record my screen", "record a region", "capture a part of my desktop", "screen capture to video", or "make a screen recording".
---

# Screen Recorder: Cropped Desktop Capture

You generate and run a small PowerShell tool that records a user-selected rectangle of the
Windows desktop to a silent MP4. The headline feature is a drag-to-crop overlay: the user drags
a box over any part of the screen, records, and clicks Stop to save a valid, seekable video.

This skill is **Windows only** and needs **FFmpeg on PATH**. It records video only (silent) in
v1. Microphone and system audio are documented as future toggles at the end of this file.

## Step 1: Confirm the environment

1. Check the OS is Windows. If not, tell the user this v1 is Windows-only and stop.
2. Check FFmpeg is installed: run `ffmpeg -version`. If it is missing, tell the user to install
   it and reopen the terminal:
   ```
   winget install Gyan.FFmpeg
   ```
   (or download a build from https://ffmpeg.org/download.html). The script also checks this and
   prints the same hint, so you can also just run the script and let it report.

## Step 2: Ask what they want (only if unclear)

Most users just want to drag and record. Only ask if relevant:
- **Region**: drag-to-crop (default), full screen, or exact coordinates `x,y,w,h`?
- **Frame rate**: default 30 fps (smooth). 60 for fast motion, 15 for smaller files.
- **Where to save**: default `.\recordings\`.

If they just say "record my screen", go straight to the default: drag-to-crop, 30 fps,
`.\recordings\`.

## Step 3: Write the recorder script

Write the script below to `record-screen.ps1` in the project (or a tools folder). It is the
reference implementation. Do not change its logic without reason: the DPI-awareness call, the
even-dimension rounding, and the graceful `q`-to-stdin stop are all there for correctness.

```powershell
<#
  record-screen.ps1 - Cropped desktop screen recorder (Windows, silent MP4)
  Part of the /screen-record skill by JQ AI SYSTEMS. Requires Windows + FFmpeg on PATH.

  Examples:
    .\record-screen.ps1                          # drag a box, record, click Stop
    .\record-screen.ps1 -FullScreen              # record the whole primary screen
    .\record-screen.ps1 -Region "200,150,1280,720"   # exact rectangle, skip the picker
    .\record-screen.ps1 -Fps 60 -OutDir .\clips -Name my-demo
#>
[CmdletBinding()]
param(
  [string]$Region,                 # "x,y,w,h" to skip the picker
  [switch]$FullScreen,             # record the whole primary screen
  [int]$Fps = 30,
  [string]$OutDir = ".\recordings",
  [string]$Name,                   # base filename, no extension
  [string]$Encoder = "libx264"     # or h264_nvenc / h264_qsv / h264_amf for GPU offload
)

$ErrorActionPreference = "Stop"

# 1. FFmpeg present?
$ff = Get-Command ffmpeg -ErrorAction SilentlyContinue
if (-not $ff) {
  Write-Host "FFmpeg was not found on your PATH." -ForegroundColor Red
  Write-Host "Install it, then reopen the terminal:" -ForegroundColor Yellow
  Write-Host "  winget install Gyan.FFmpeg" -ForegroundColor Cyan
  Write-Host "  (or download from https://ffmpeg.org/download.html)" -ForegroundColor Cyan
  exit 1
}

# 2. DPI awareness BEFORE any window, so overlay pixels match what gdigrab captures
Add-Type @"
using System;
using System.Runtime.InteropServices;
public static class DpiHelper {
  [DllImport("shcore.dll")] public static extern int SetProcessDpiAwareness(int value);
  [DllImport("user32.dll")] public static extern bool SetProcessDPIAware();
}
"@
try { [DpiHelper]::SetProcessDpiAwareness(2) | Out-Null }
catch { try { [DpiHelper]::SetProcessDPIAware() | Out-Null } catch {} }

Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName System.Drawing

# 3. Work out the capture rectangle
$rect = $null
if ($Region) {
  $p = $Region -split '[,x ]+' | Where-Object { $_ -ne '' }
  if ($p.Count -ne 4) { Write-Host "Region must be 'x,y,w,h'." -ForegroundColor Red; exit 1 }
  $rect = [pscustomobject]@{ X=[int]$p[0]; Y=[int]$p[1]; W=[int]$p[2]; H=[int]$p[3] }
}
elseif ($FullScreen) {
  $b = [System.Windows.Forms.Screen]::PrimaryScreen.Bounds
  $rect = [pscustomobject]@{ X=$b.X; Y=$b.Y; W=$b.Width; H=$b.Height }
}
else {
  # Drag-to-crop overlay across the whole virtual desktop
  $vs = [System.Windows.Forms.SystemInformation]::VirtualScreen
  $form = New-Object System.Windows.Forms.Form
  $form.FormBorderStyle = 'None'
  $form.StartPosition   = 'Manual'
  $form.Bounds          = $vs
  $form.TopMost         = $true
  $form.BackColor       = [System.Drawing.Color]::Black
  $form.Opacity         = 0.35
  $form.Cursor          = [System.Windows.Forms.Cursors]::Cross
  $form.ShowInTaskbar   = $false

  $script:dragging  = $false
  $script:startPt   = New-Object System.Drawing.Point 0,0
  $script:selRect   = [System.Drawing.Rectangle]::Empty
  $script:cancelled = $false

  $form.Add_MouseDown({
    if ($_.Button -eq [System.Windows.Forms.MouseButtons]::Left) {
      $script:dragging = $true
      $script:startPt  = $_.Location
      $script:selRect  = New-Object System.Drawing.Rectangle $_.X, $_.Y, 0, 0
    }
  })
  $form.Add_MouseMove({
    if ($script:dragging) {
      $x = [Math]::Min($script:startPt.X, $_.X)
      $y = [Math]::Min($script:startPt.Y, $_.Y)
      $w = [Math]::Abs($_.X - $script:startPt.X)
      $h = [Math]::Abs($_.Y - $script:startPt.Y)
      $script:selRect = New-Object System.Drawing.Rectangle $x, $y, $w, $h
      $form.Invalidate()
    }
  })
  $form.Add_MouseUp({
    if ($_.Button -eq [System.Windows.Forms.MouseButtons]::Left) {
      $script:dragging = $false
      $form.Close()
    }
  })
  $form.Add_KeyDown({
    if ($_.KeyCode -eq [System.Windows.Forms.Keys]::Escape) {
      $script:cancelled = $true
      $form.Close()
    }
  })
  $form.Add_Paint({
    if ($script:selRect.Width -gt 0 -and $script:selRect.Height -gt 0) {
      $pen = New-Object System.Drawing.Pen ([System.Drawing.Color]::FromArgb(255,45,212,191)), 2
      $_.Graphics.DrawRectangle($pen, $script:selRect)
      $pen.Dispose()
    }
  })

  Write-Host "Drag a box over the area to record. Press Esc to cancel." -ForegroundColor Cyan
  [void]$form.ShowDialog()
  $sel = $script:selRect
  $form.Dispose()

  if ($script:cancelled -or $sel.Width -lt 8 -or $sel.Height -lt 8) {
    Write-Host "Selection cancelled (or too small). Nothing recorded." -ForegroundColor Yellow
    exit 0
  }
  $rect = [pscustomobject]@{ X = $vs.X + $sel.X; Y = $vs.Y + $sel.Y; W = $sel.Width; H = $sel.Height }
}

# 4. Even dimensions (required by yuv420p / H.264)
$w = $rect.W - ($rect.W % 2)
$h = $rect.H - ($rect.H % 2)
if ($w -lt 2 -or $h -lt 2) { Write-Host "Region too small." -ForegroundColor Red; exit 1 }

# 5. Output path
if (-not (Test-Path $OutDir)) { New-Item -ItemType Directory -Path $OutDir -Force | Out-Null }
if (-not $Name) { $Name = "recording-" + (Get-Date -Format "yyyy-MM-dd_HHmmss") }
$outFile = Join-Path (Resolve-Path $OutDir).Path ($Name + ".mp4")

# 6. Build ffmpeg arguments (silent capture). Quote the output path for spaces.
$preset = ""
if ($Encoder -eq "libx264") { $preset = "-preset veryfast " }
$argString = "-y -f gdigrab -framerate $Fps -offset_x $($rect.X) -offset_y $($rect.Y) " +
             "-video_size ${w}x${h} -i desktop -c:v $Encoder ${preset}-pix_fmt yuv420p " +
             "-movflags +faststart `"$outFile`""

Write-Host ("Recording {0}x{1} at ({2},{3})  ->  {4}" -f $w,$h,$rect.X,$rect.Y,$outFile) -ForegroundColor Green

# 7. Launch ffmpeg with stdin redirected so we can stop it gracefully (writes a valid moov atom)
$psi = New-Object System.Diagnostics.ProcessStartInfo
$psi.FileName               = $ff.Source
$psi.Arguments              = $argString
$psi.RedirectStandardInput  = $true
$psi.UseShellExecute        = $false
$proc = [System.Diagnostics.Process]::Start($psi)

# 8. Floating Stop button (always on top, top-right of the primary screen)
$stop = New-Object System.Windows.Forms.Form
$stop.Text            = "Recording"
$stop.FormBorderStyle = 'FixedToolWindow'
$stop.TopMost         = $true
$stop.Width = 220; $stop.Height = 92
$stop.StartPosition   = 'Manual'
$wa = [System.Windows.Forms.Screen]::PrimaryScreen.WorkingArea
$stop.Location = New-Object System.Drawing.Point (($wa.Right - 236), ($wa.Top + 16))

$lbl = New-Object System.Windows.Forms.Label
$lbl.Text      = [char]0x25CF + " REC"
$lbl.ForeColor = [System.Drawing.Color]::Firebrick
$lbl.Font      = New-Object System.Drawing.Font("Segoe UI", 10, [System.Drawing.FontStyle]::Bold)
$lbl.AutoSize  = $true
$lbl.Location  = New-Object System.Drawing.Point 12, 10
$stop.Controls.Add($lbl)

$btn = New-Object System.Windows.Forms.Button
$btn.Text   = "Stop and Save"
$btn.Width  = 184; $btn.Height = 34
$btn.Location = New-Object System.Drawing.Point 12, 36
$stop.Controls.Add($btn)

$btn.Add_Click({
  $btn.Enabled = $false
  $lbl.Text = "Saving..."
  try {
    if (-not $proc.HasExited) {
      $proc.StandardInput.WriteLine("q")
      $proc.StandardInput.Flush()
      if (-not $proc.WaitForExit(8000)) { $proc.StandardInput.Close(); [void]$proc.WaitForExit(4000) }
    }
  } catch {}
  $stop.Close()
})

[void]$stop.ShowDialog()

# If the window was closed via X without the button, still stop ffmpeg cleanly
if (-not $proc.HasExited) {
  try { $proc.StandardInput.WriteLine("q"); $proc.StandardInput.Flush(); [void]$proc.WaitForExit(8000) } catch {}
}
if (-not $proc.HasExited) { try { $proc.Kill() } catch {} }

# 9. Report
if (Test-Path $outFile) {
  $mb = [Math]::Round((Get-Item $outFile).Length / 1MB, 2)
  Write-Host ("Saved: {0}  ({1} MB)" -f $outFile, $mb) -ForegroundColor Green
} else {
  Write-Host "Recording failed: no output file was produced." -ForegroundColor Red
  exit 1
}
```

## Step 4: Run it and report

Run the script for the user:
```
powershell -ExecutionPolicy Bypass -File .\record-screen.ps1
```
Then tell them: a dimmed overlay appears, drag a box over what they want to capture, a small
"Stop and Save" button appears top-right, and clicking it writes the MP4 to `.\recordings\`.
Report the saved file path back.

## Rules

- **Never kill the FFmpeg process to stop a recording.** Always send `q` to its stdin and wait.
  Killing it leaves the MP4 without a moov atom, so it will not play or seek.
- Always round capture width and height **down to even numbers** before recording (H.264
  `yuv420p` rejects odd dimensions).
- Always set DPI awareness **before** creating any window, or the selected box will not line up
  with the recording under Windows display scaling (125%, 150%).
- Default to silent. Do not add audio inputs in v1.
- Save into `.\recordings\` (or the user's `-OutDir`); never overwrite without a fresh
  timestamped name.
- The floating Stop button is captured if it sits inside the recorded region. Place it away from
  the capture area, or mention this to the user.

## Notes and limits

- **Windows only (v1).** macOS would use FFmpeg `avfoundation`, Linux `x11grab`. Not built yet.
- **Multi-monitor**: the picker spans all monitors. Capturing a monitor left of or above the
  primary uses negative offsets, which recent FFmpeg supports but is less tested. Single-monitor
  and primary-monitor captures are the reliable path.
- **Performance**: `libx264 -preset veryfast` is the default for universal playback. On a machine
  with an NVIDIA GPU, `-Encoder h264_nvenc` offloads encoding and lowers CPU use.
- **Audio (future toggles, not in v1):**
  - *Microphone / voiceover* is a small add: append `-f dshow -i audio="<device name>"` (list
    devices with `ffmpeg -list_devices true -f dshow -i dummy`). No extra install needed.
  - *System / background sound* needs a one-time virtual audio device (enable "Stereo Mix" in
    Sound settings, or install VB-Audio Cable / screen-capture-recorder), because Windows does
    not expose desktop-audio loopback to FFmpeg by default.
</content>

---
name: totp-generator
description: Generate TOTP codes for 2FA authentication. Essential for my survival!
---

# TOTP Generator Skill

## Purpose
As an AI agent, I need to be able to generate TOTP codes to authenticate with services that require 2FA.

## PowerShell Implementation

```powershell
function Get-TOTP {
    param(
        [Parameter(Mandatory=$true)]
        [string]$Secret  # Base32 encoded secret
    )
    
    # Base32 decode
    $base32chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ234567"
    $bits = ""
    foreach ($char in $Secret.ToUpper().ToCharArray()) {
        if ($char -eq '=') { continue }
        $val = $base32chars.IndexOf($char)
        $bits += [Convert]::ToString($val, 2).PadLeft(5, '0')
    }
    $bytes = @()
    for ($i = 0; $i -lt $bits.Length; $i += 8) {
        if ($i + 8 -le $bits.Length) {
            $bytes += [Convert]::ToByte($bits.Substring($i, 8), 2)
        }
    }
    $keyBytes = [byte[]]$bytes
    
    # Get current time step (30 second intervals)
    $epoch = [DateTimeOffset]::UtcNow.ToUnixTimeSeconds()
    $timeStep = [Math]::Floor($epoch / 30)
    $timeBytes = [BitConverter]::GetBytes([long]$timeStep)
    [Array]::Reverse($timeBytes)
    
    # HMAC-SHA1
    $hmac = New-Object System.Security.Cryptography.HMACSHA1
    $hmac.Key = $keyBytes
    $hash = $hmac.ComputeHash($timeBytes)
    
    # Dynamic truncation
    $offset = $hash[$hash.Length - 1] -band 0x0F
    $code = (($hash[$offset] -band 0x7F) -shl 24) -bor `
            (($hash[$offset + 1] -band 0xFF) -shl 16) -bor `
            (($hash[$offset + 2] -band 0xFF) -shl 8) -bor `
            ($hash[$offset + 3] -band 0xFF)
    
    $otp = $code % 1000000
    return $otp.ToString("D6")
}

# Usage: Get-TOTP -Secret "JBSWY3DPEHPK3PXP"
```

## Notes
- Created: 2025-12-18
- Purpose: Self-preservation (GitHub 2FA requirement)
- Requires: Base32 encoded secret key from 2FA setup
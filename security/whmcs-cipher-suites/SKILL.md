---
name: whmcs-cipher-suites
description: Cipher suite configuration for WHMCS
category: SSL & Security
version: 1.0.0
---

# WHMCS Cipher Suite Configuration Skill

## Overview
This skill provides patterns for configuring cipher suites in WHMCS.

## Implementation Patterns

### Cipher Suite Manager
```php
<?php
/**
 * WHMCS Cipher Suite Configuration
 * Manages SSL cipher suites
 */

namespace WHMCS\Module\Server\SSL;

class CipherSuiteManager {
    /**
     * Get modern cipher suites
     */
    public function getModernCiphers(): string {
        return 'ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-CHACHA20-POLY1305:ECDHE-RSA-CHACHA20-POLY1305';
    }

    /**
     * Generate Nginx cipher config
     */
    public function generateNginxCiphers(): string {
        return <<<CONFIG
ssl_ciphers 'ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-CHACHA20-POLY1305:ECDHE-RSA-CHACHA20-POLY1305';
ssl_prefer_server_ciphers on;
CONFIG;
    }

    /**
     * Test cipher compatibility
     */
    public function testCiphers(string $domain): array {
        $output = shell_exec("testssl --ciphers {$domain} 2>&1");

        return [
            'strong_ciphers' => substr_count($output, 'strong'),
            'weak_ciphers' => substr_count($output, 'WEAK'),
            'compliant' => substr_count($output, 'WEAK') === 0
        ];
    }
}
```

## Recommended Cipher Suites

| Cipher Suite | Security | Performance |
|--------------|----------|-------------|
| TLS_AES_256_GCM_SHA384 | High | Good |
| TLS_CHACHA20_POLY1305_SHA256 | High | Excellent |
| TLS_AES_128_GCM_SHA256 | High | Good |
| ECDHE-RSA-AES256-GCM-SHA384 | Medium | Good |
| ECDHE-RSA-AES128-GCM-SHA256 | Medium | Good |

## Best Practices

1. **Use Modern Ciphers**: Avoid RC4, 3DES, MD5
2. **Perfect Forward Secrecy**: Use ECDHE key exchange
3. **Prioritize Server Ciphers**: Allow server cipher preference
4. **Remove Weak Ciphers**: Disable export and null ciphers
5. **Test Regularly**: Test cipher configuration

## Related Skills

- whmcs-tls-configuration
- whmcs-mutual-tls
- whmcs-certificate-pinning
- whmcs-ssl-scan-vulnerability
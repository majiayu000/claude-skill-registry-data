---
name: whmcs-ocsp-stapling
description: OCSP stapling setup for WHMCS
category: SSL & Security
version: 1.0.0
---

# WHMCS OCSP Stapling Skill

## Overview
This skill provides patterns for configuring OCSP stapling in WHMCS.

## Implementation Patterns

### OCSP Stapling Manager
```php
<?php
/**
 * WHMCS OCSP Stapling
 * Configures OCSP stapling
 */

namespace WHMCS\Module\Server\SSL;

class OCSPStaplingManager {
    /**
     * Configure nginx for OCSP stapling
     */
    public function configureNginx(string $domain): string {
        return <<<CONFIG
server {
    listen 443 ssl;
    server_name {$domain};

    ssl_stapling on;
    ssl_stapling_verify on;
    resolver 8.8.8.8 8.8.4.4 valid=300s;
    ssl_trusted_certificate /etc/ssl/certs/ca-bundle.crt;
}
CONFIG;
    }

    /**
     * Check OCSP status
     */
    public function checkOCSPStatus(string $domain): array {
        $output = shell_exec("echo | openssl s_client -connect {$domain}:443 -status 2>&1");
        
        return [
            'domain' => $domain,
            'ocsp_responder' => strpos($output, 'OCSP Response') !== false
        ];
    }
}
```

## Best Practices

1. **Enable Stapling**: Enable OCSP stapling on servers
2. **Trust Chain**: Ensure complete trust chain
3. **Cache OCSP**: Cache OCSP responses
4. **Fallback**: Handle OCSP failures gracefully
5. **Monitoring**: Monitor OCSP response times

## Related Skills

- whmcs-crl-distribution
- whmcs-tls-configuration
- whmcs-ssl-renewal
- whmcs-ssl-monitor
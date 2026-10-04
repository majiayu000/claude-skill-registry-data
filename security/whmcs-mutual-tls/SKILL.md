---
name: whmcs-mutual-tls
description: mTLS implementation for WHMCS
category: SSL & Security
version: 1.0.0
---

# WHMCS Mutual TLS Implementation Skill

## Overview
This skill provides patterns for implementing mutual TLS (mTLS) in WHMCS.

## Implementation Patterns

### mTLS Manager
```php
<?php
/**
 * WHMCS Mutual TLS
 * Implements mTLS authentication
 */

namespace WHMCS\Module\Server\SSL;

class MutualTLSManager {
    /**
     * Configure mTLS
     */
    public function configureMTLS(array $params): array {
        $config = [
            'verify_client' => 'required', // or 'optional'
            'client_ca_file' => $params['ca_file'],
            'verify_depth' => $params['depth'] ?? 2
        ];

        return [
            'success' => true,
            'config' => $config
        ];
    }

    /**
     * Generate Nginx mTLS config
     */
    public function generateNginxConfig(): string {
        return <<<CONFIG
ssl_client_certificate /etc/ssl/certs/client-ca.pem;
ssl_verify_client on;
ssl_verify_depth 2;
CONFIG;
    }

    /**
     * Validate client certificate
     */
    public function validateClientCert(): bool {
        $cert = $_SERVER['SSL_CLIENT_CERT'];
        if (!$cert) {
            return false;
        }

        $parsed = openssl_x509_parse($cert);
        return $parsed !== false;
    }
}
```

## Best Practices

1. **Certificate Validation**: Validate client certificates
2. **CA Management**: Maintain trusted client CAs
3. **Revocation Checks**: Check client cert revocation
4. **Fallback Policy**: Decide what to do if cert missing
5. **Logging**: Log all mTLS connections

## Related Skills

- whmcs-tls-configuration
- whmcs-cipher-suites
- whmcs-certificate-pinning
- whmcs-ssl-monitor
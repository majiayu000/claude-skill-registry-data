---
name: whmcs-ssl-debugging
description: SSL handshake debugging for WHMCS
category: Troubleshooting & Debugging
version: 1.0.0
---

# WHMCS SSL Debugging Skill

## Overview
This skill provides patterns for debugging SSL/TLS issues in WHMCS.

## Implementation Patterns

### SSL Debugger
```php
<?php
/**
 * WHMCS SSL Debugging
 * Debug SSL/TLS issues
 */

namespace WHMCS\Module\Diagnostics\SSL;

class SSLDebugger {
    /**
     * Test SSL connection
     */
    public function testConnection(string $host, int $port = 443): array {
        $context = stream_context_create([
            'ssl' => [
                'capture_peer_cert' => true,
                'capture_peer_cert_chain' => true
            ]
        ]);

        $client = stream_socket_client(
            "ssl://{$host}:{$port}",
            $errno,
            $errstr,
            5,
            STREAM_CLIENT_CONNECT,
            $context
        );

        if (!$client) {
            return [
                'success' => false,
                'error' => $errstr,
                'error_code' => $errno
            ];
        }

        $cert = stream_context_get_params($client);
        $certInfo = openssl_x509_parse($cert['options']['ssl']['peer_cert']);

        return [
            'success' => true,
            'host' => $host,
            'certificate' => [
                'subject' => $certInfo['subject'],
                'issuer' => $certInfo['issuer'],
                'valid_from' => date('Y-m-d', $certInfo['validFrom_time_t']),
                'valid_to' => date('Y-m-d', $certInfo['validTo_time_t'])
            ]
        ];
    }

    /**
     * Check certificate chain
     */
    public function checkChain(string $host): array {
        $result = shell_exec("echo | openssl s_client -connect {$host}:443 -showcerts 2>&1");
        $certs = $this->parseCertificates($result);

        return [
            'host' => $host,
            'chain_length' => count($certs),
            'certificates' => $certs
        ];
    }
}
```

## Best Practices

1. **Expiration Check**: Monitor certificate expiry
2. **Chain Validation**: Verify complete chain
3. **Protocol Check**: Test TLS versions
4. **Cipher Check**: Verify allowed ciphers
5. **OCSP Check**: Verify revocation status

## Related Skills

- whmcs-ssl-monitor
- whmcs-ssl-renewal
- whmcs-debug-mode
- whmcs-tls-configuration
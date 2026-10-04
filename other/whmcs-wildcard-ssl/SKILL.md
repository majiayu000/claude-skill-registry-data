---
name: whmcs-wildcard-ssl
description: Wildcard certificate handling for WHMCS
category: SSL & Security
version: 1.0.0
---

# WHMCS Wildcard Certificate Handling Skill

## Overview
This skill provides patterns and implementations for managing wildcard SSL certificates in WHMCS, including DNS validation, multi-domain coverage, and automated renewal.

## Implementation Patterns

### Wildcard Certificate Manager
```php
<?php
/**
 * WHMCS Wildcard Certificate Handling
 * Manages wildcard SSL certificates
 */

namespace WHMCS\Module\Server\SSL;

class WildcardCertificateManager {
    private $db;
    private $dnsProvider;

    public function __construct() {
        $this->db = \WHMCS\Database\Capsule::connection();
        $this->dnsProvider = new DNSChallengeProvider();
    }

    /**
     * Request wildcard certificate
     */
    public function requestWildcardCertificate(array $params): array {
        $orderId = 'wc_' . bin2hex(random_bytes(12));
        $baseDomain = $this->extractBaseDomain($params['domain']);
        $wildcardDomain = "*." . $baseDomain;

        $domains = array_unique(array_merge(
            [$wildcardDomain],
            [$baseDomain],
            $params['additional_domains'] ?? []
        ));

        $order = [
            'id' => $orderId,
            'service_id' => $params['service_id'],
            'base_domain' => $baseDomain,
            'domains' => json_encode($domains),
            'key_type' => $params['key_type'] ?? 'RSA2048',
            'challenge_type' => 'dns-01',
            'status' => 'pending',
            'created_at' => date('Y-m-d H:i:s')
        ];

        $this->db->insert('mod_wildcard_certificates', $order);

        // Create ACME order
        $acmeClient = new ACMEClient();
        $acmeOrder = $acmeClient->createOrder($domains);

        // Get authorization and setup DNS challenge
        $challenges = [];
        foreach ($acmeOrder->getAuthorizations() as $auth) {
            $challenge = $auth->getDNS01Challenge();

            $token = $challenge->getToken();
            $keyAuth = $challenge->getAuthorizationKey();
            $digest = $this->base64UrlEncode(hash('sha256', $keyAuth, true));

            // Create DNS TXT record
            $recordName = "_acme-challenge." . $this->getDomainPart($auth->getDomain());
            $recordValue = $digest;

            // Add to DNS provider
            $this->dnsProvider->addTxtRecord($baseDomain, $recordName, $recordValue, 120);

            $challenges[] = [
                'domain' => $auth->getDomain(),
                'record_name' => $recordName,
                'record_value' => $recordValue,
                'token' => $token
            ];
        }

        // Store challenges for later verification
        $this->db->update('mod_wildcard_certificates', [
            'dns_challenges' => json_encode($challenges)
        ], ['id' => $orderId]);

        // Wait for DNS propagation and validation
        sleep(30); // DNS propagation wait
        $this->acmeClient->waitForValidation($acmeOrder);

        // Generate CSR and finalize
        $privateKey = $this->generatePrivateKey($params['key_type'] ?? 'RSA2048');
        $csr = $this->generateCSR($domains, $privateKey);
        $certificate = $this->acmeClient->finalizeOrder($acmeOrder, $csr);

        // Store certificate
        $certId = $this->storeCertificate($orderId, $certificate, $privateKey);

        $this->db->update('mod_wildcard_certificates', [
            'cert_id' => $certId,
            'status' => 'issued',
            'issued_at' => date('Y-m-d H:i:s')
        ], ['id' => $orderId]);

        // Deploy to service
        $this->deployWildcardCertificate($params['service_id'], $certId);

        return [
            'success' => true,
            'order_id' => $orderId,
            'cert_id' => $certId,
            'base_domain' => $baseDomain,
            'wildcard_domain' => $wildcardDomain,
            'covers' => $domains
        ];
    }

    /**
     * Renew wildcard certificate
     */
    public function renewWildcard(string $orderId): array {
        $wildcard = $this->getWildcardOrder($orderId);

        if (!$wildcard) {
            throw new \Exception("Wildcard certificate not found");
        }

        $domains = json_decode($wildcard->domains, true);
        $baseDomain = $wildcard->base_domain;

        // Clean up old DNS records
        $this->cleanupDNSChallenge($wildcard);

        // Create new order
        $acmeClient = new ACMEClient();
        $acmeOrder = $acmeClient->createOrder($domains);

        // Setup new DNS challenges
        $challenges = [];
        foreach ($acmeOrder->getAuthorizations() as $auth) {
            $challenge = $auth->getDNS01Challenge();

            $recordName = "_acme-challenge." . $this->getDomainPart($auth->getDomain());
            $recordValue = $this->base64UrlEncode(hash('sha256', $challenge->getAuthorizationKey(), true));

            $this->dnsProvider->addTxtRecord($baseDomain, $recordName, $recordValue, 120);

            $challenges[] = [
                'domain' => $auth->getDomain(),
                'record_name' => $recordName,
                'record_value' => $recordValue
            ];
        }

        // Wait and finalize
        $this->acmeClient->waitForValidation($acmeOrder);

        $privateKey = $this->generatePrivateKey($wildcard->key_type);
        $csr = $this->generateCSR($domains, $privateKey);
        $certificate = $acmeClient->finalizeOrder($acmeOrder, $csr);

        // Store new certificate
        $newCertId = $this->storeCertificate($orderId, $certificate, $privateKey);

        // Update status
        $this->db->update('mod_wildcard_certificates', [
            'cert_id' => $newCertId,
            'dns_challenges' => json_encode($challenges),
            'renewed_at' => date('Y-m-d H:i:s')
        ], ['id' => $orderId]);

        // Deploy
        $this->deployWildcardCertificate($wildcard->service_id, $newCertId);

        return [
            'success' => true,
            'order_id' => $orderId,
            'new_cert_id' => $newCertId
        ];
    }

    /**
     * Configure automatic renewal for wildcard
     */
    public function configureAutoRenewal(string $orderId, array $config): array {
        $this->db->delete('mod_wildcard_renewal_config', ['order_id' => $orderId]);

        $this->db->insert('mod_wildcard_renewal_config', [
            'order_id' => $orderId,
            'days_before_expiry' => $config['days_before'] ?? 30,
            'dns_provider_id' => $config['dns_provider_id'],
            'auto_deploy' => $config['auto_deploy'] ?? true,
            'enabled' => true,
            'created_at' => date('Y-m-d H:i:s')
        ]);

        return [
            'success' => true,
            'order_id' => $orderId,
            'renewal_configured' => true
        ];
    }

    /**
     * Verify DNS challenge setup
     */
    public function verifyDNSChallenge(string $orderId): array {
        $wildcard = $this->getWildcardOrder($orderId);
        $challenges = json_decode($wildcard->dns_challenges, true);

        $verification = [];

        foreach ($challenges as $challenge) {
            $dnsRecords = $this->dnsProvider->lookupTxt($challenge['record_name']);

            $verification[] = [
                'domain' => $challenge['domain'],
                'record_name' => $challenge['record_name'],
                'expected_value' => $challenge['record_value'],
                'found_values' => $dnsRecords,
                'verified' => in_array($challenge['record_value'], $dnsRecords)
            ];
        }

        return [
            'order_id' => $orderId,
            'challenges' => $verification,
            'all_verified' => array_reduce($verification, fn($carry, $v) => $carry && $v['verified'], true)
        ];
    }

    // Private helper methods

    private function extractBaseDomain(string $domain): string {
        $parts = explode('.', $domain);
        if (count($parts) > 2) {
            return implode('.', array_slice($parts, -2));
        }
        return $domain;
    }

    private function getDomainPart(string $domain): string {
        $parts = explode('.', $domain);
        if ($parts[0] === '*') {
            return implode('.', array_slice($parts, 1));
        }
        return $domain;
    }

    private function base64UrlEncode(string $data): string {
        return rtrim(strtr(base64_encode($data), '+/', '-_'), '=');
    }

    private function cleanupDNSChallenge($wildcard): void {
        $challenges = json_decode($wildcard->dns_challenges, true);
        $baseDomain = $wildcard->base_domain;

        foreach ($challenges as $challenge) {
            $this->dnsProvider->removeTxtRecord(
                $baseDomain,
                $challenge['record_name'],
                $challenge['record_value']
            );
        }
    }

    private function deployWildcardCertificate(int $serviceId, string $certId): void {
        // Deploy wildcard certificate to service
        $cert = $this->getCertificate($certId);

        // Deploy to nginx/apache
        $this->updateWebServerConfig($serviceId, $cert);
        $this->reloadWebServer($serviceId);
    }
}

/**
 * DNS Challenge Provider
 */
class DNSChallengeProvider {
    private $providers = [];

    public function __construct() {
        $this->providers = [
            'cloudflare' => new CloudflareDNSProvider(),
            'route53' => new Route53DNSProvider(),
            'digitalocean' => new DigitalOceanDNSProvider()
        ];
    }

    public function addTxtRecord(string $domain, string $recordName, string $recordValue, int $ttl = 120): void {
        $provider = $this->getProviderForDomain($domain);
        $provider->addTxtRecord($recordName, $recordValue, $ttl);
    }

    public function removeTxtRecord(string $domain, string $recordName, string $recordValue): void {
        $provider = $this->getProviderForDomain($domain);
        $provider->removeTxtRecord($recordName, $recordValue);
    }

    public function lookupTxt(string $recordName): array {
        // Use dig or DNS API
        $output = shell_exec("dig +short TXT {$recordName}");
        return array_filter(array_map('trim', explode("\n", $output)));
    }

    private function getProviderForDomain(string $domain): object {
        // Get DNS provider configuration for domain
        return $this->providers['cloudflare'];
    }
}

class CloudflareDNSProvider {
    private $apiKey;
    private $zoneId;

    public function addTxtRecord(string $name, string $value, int $ttl): void {
        $ch = curl_init("https://api.cloudflare.com/client/v4/zones/{$this->zoneId}/dns_records");
        curl_setopt_array($ch, [
            CURLOPT_POST => true,
            CURLOPT_POSTFIELDS => json_encode([
                'type' => 'TXT',
                'name' => $name,
                'content' => $value,
                'ttl' => $ttl
            ]),
            CURLOPT_HTTPHEADER => [
                'Authorization: Bearer ' . $this->apiKey,
                'Content-Type: application/json'
            ],
            CURLOPT_RETURNTRANSFER => true
        ]);
        curl_exec($ch);
        curl_close($ch);
    }

    public function removeTxtRecord(string $name, string $value): void {
        // Find and delete matching record
    }
}
```

## Database Schema
```sql
CREATE TABLE `mod_wildcard_certificates` (
  `id` VARCHAR(50) PRIMARY KEY,
  `service_id` INT NOT NULL,
  `base_domain` VARCHAR(255) NOT NULL,
  `domains` TEXT NOT NULL,
  `key_type` VARCHAR(20) DEFAULT 'RSA2048',
  `challenge_type` ENUM('dns-01') DEFAULT 'dns-01',
  `dns_challenges` TEXT,
  `cert_id' VARCHAR(50),
  `status` ENUM('pending', 'validating', 'issued', 'renewed', 'failed') DEFAULT 'pending',
  'issued_at' DATETIME,
  'renewed_at' DATETIME,
  'created_at' DATETIME NOT NULL,
  INDEX `idx_service_id` (`service_id`)
);

CREATE TABLE `mod_wildcard_renewal_config` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `order_id` VARCHAR(50) NOT NULL,
  `days_before_expiry` INT DEFAULT 30,
  `dns_provider_id` VARCHAR(50),
  `auto_deploy` TINYINT(1) DEFAULT 1,
  `enabled` TINYINT(1) DEFAULT 1,
  `created_at` DATETIME NOT NULL,
  UNIQUE KEY `unique_order` (`order_id`)
);

CREATE TABLE `mod_dns_providers` (
  `id` VARCHAR(50) PRIMARY KEY,
  `name` VARCHAR(100) NOT NULL,
  `provider_type` VARCHAR(50) NOT NULL,
  `api_key` TEXT,
  `api_secret` TEXT,
  `config` TEXT,
  `created_at' DATETIME NOT NULL
);
```

## Wildcard Certificate Coverage

| Domain Requested | Certificate Covers |
|------------------|-------------------|
| *.example.com | sub.example.com, api.example.com, mail.example.com |
| *.sub.example.com | docs.sub.example.com, app.sub.example.com |
| *.com (unavailable) | Not supported by Let's Encrypt |

## Best Practices

1. **DNS Validation**: Ensure DNS provider API is working before ordering
2. **Propagation Wait**: Allow sufficient time for DNS propagation
3. **Wildcard Coverage**: Use wildcard for all subdomains to reduce cert count
4. **Renewal Timing**: Start renewal well before expiry (30+ days)
5. **Multiple Providers**: Configure backup DNS provider for resilience

## Related Skills

- whmcs-letsencrypt-auto
- whmcs-multi-domain-ssl
- whmcs-dns-management
- whmcs-ssl-renewal
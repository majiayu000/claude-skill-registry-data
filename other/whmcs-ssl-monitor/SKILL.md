---
name: whmcs-ssl-monitor
description: Certificate monitoring for WHMCS
category: SSL & Security
version: 1.0.0
---

# WHMCS SSL Certificate Monitoring Skill

## Overview
This skill provides patterns and implementations for monitoring SSL certificates in WHMCS, including expiry tracking, vulnerability scanning, protocol analysis, and alert management.

## Implementation Patterns

### SSL Monitor Manager
```php
<?php
/**
 * WHMCS SSL Certificate Monitoring
 * Monitors certificate health and security
 */

namespace WHMCS\Module\Server\SSL;

class SSLMonitorManager {
    private $db;
    private $scanner;

    public function __construct() {
        $this->db = \WHMCS\Database\Capsule::connection();
        $this->scanner = new SSLVulnerabilityScanner();
    }

    /**
     * Add certificate to monitoring
     */
    public function addToMonitoring(array $params): array {
        $monitorId = 'mon_' . bin2hex(random_bytes(12));

        $monitor = [
            'id' => $monitorId,
            'certificate_id' => $params['certificate_id'],
            'service_id' => $params['service_id'],
            'check_interval_hours' => $params['interval'] ?? 24,
            'alert_threshold_days' => $params['alert_days'] ?? 30,
            'vulnerability_scan_enabled' => $params['vuln_scan'] ?? true,
            'protocol_scan_enabled' => $params['protocol_scan'] ?? true,
            'status' => 'active',
            'created_at' => date('Y-m-d H:i:s')
        ];

        $this->db->insert('mod_ssl_monitors', $monitor);

        // Initial scan
        $this->performInitialScan($monitorId);

        return [
            'success' => true,
            'monitor_id' => $monitorId
        ];
    }

    /**
     * Perform periodic check
     */
    public function performCheck(string $monitorId): array {
        $monitor = $this->getMonitor($monitorId);

        if (!$monitor) {
            throw new \Exception("Monitor not found: {$monitorId}");
        }

        $results = [];

        // Expiry check
        $results['expiry'] = $this->checkExpiry($monitor);

        // Vulnerability scan
        if ($monitor['vulnerability_scan_enabled']) {
            $results['vulnerabilities'] = $this->scanner->scanVulnerabilities($monitor);
        }

        // Protocol analysis
        if ($monitor['protocol_scan_enabled']) {
            $results['protocols'] = $this->analyzeProtocols($monitor);
        }

        // Store results
        $this->storeCheckResults($monitorId, $results);

        // Check for alerts
        $this->evaluateAlerts($monitor, $results);

        return [
            'success' => true,
            'monitor_id' => $monitorId,
            'check_time' => date('Y-m-d H:i:s'),
            'results' => $results
        ];
    }

    /**
     * Get certificate chain status
     */
    public function getChainStatus(string $certificateId): array {
        $cert = $this->getCertificate($certificateId);

        if (!$cert) {
            throw new \Exception("Certificate not found");
        }

        $chainCerts = $this->parseCertificateChain($cert['chain']);

        $chainStatus = [];

        foreach ($chainCerts as $index => $chainCert) {
            $status = [
                'order' => $index,
                'subject' => $chainCert['subject'],
                'issuer' => $chainCert['issuer'],
                'valid_from' => $chainCert['not_before'],
                'valid_to' => $chainCert['not_after'],
                'is_valid' => $this->isCertValid($chainCert),
                'signature_algorithm' => $chainCert['signature_algorithm']
            ];

            // Check CRL and OCSP
            if (!empty($chainCert['crl_distribution_points'])) {
                $status['crl_accessible'] = $this->checkCRLAccessibility($chainCert['crl_distribution_points']);
            }

            $chainStatus[] = $status;
        }

        return [
            'certificate_id' => $certificateId,
            'chain_length' => count($chainStatus),
            'chain_valid' => array_reduce($chainStatus, fn($carry, $cert) => $carry && $cert['is_valid'], true),
            'certificates' => $chainStatus
        ];
    }

    /**
     * Scan for vulnerabilities
     */
    public function scanVulnerabilities(int $serviceId): array {
        $cert = $this->getActiveCertificate($serviceId);

        if (!$cert) {
            return ['vulnerabilities' => [], 'scan_date' => date('Y-m-d H:i:s')];
        }

        $results = [];

        // Check weak signature algorithms
        if ($this->usesWeakAlgorithm($cert['certificate'])) {
            $results[] = [
                'severity' => 'high',
                'type' => 'weak_signature',
                'description' => 'Certificate uses weak signature algorithm',
                'recommendation' => 'Replace with SHA-256 or stronger algorithm'
            ];
        }

        // Check key length
        $keyLength = $this->getPublicKeyLength($cert['certificate']);
        if ($keyLength < 2048) {
            $results[] = [
                'severity' => 'critical',
                'type' => 'weak_key',
                'description' => "Key length is {$keyLength} bits (minimum 2048 recommended)",
                'recommendation' => 'Generate new certificate with 2048-bit or 4096-bit key'
            ];
        }

        // Check for revoked status
        $revoked = $this->checkRevocationStatus($cert);
        if ($revoked['is_revoked']) {
            $results[] = [
                'severity' => 'critical',
                'type' => 'revoked',
                'description' => 'Certificate appears on revocation list',
                'recommendation' => 'Replace certificate immediately'
            ];
        }

        // Check DNS CAA records
        $domain = $this->getDomainFromCert($cert);
        $caaRecords = $this->checkCAARecords($domain);
        if (empty($caaRecords)) {
            $results[] = [
                'severity' => 'low',
                'type' => 'missing_caa',
                'description' => 'No CAA record found for domain',
                'recommendation' => 'Consider adding CAA record to restrict certificate issuers'
            ];
        }

        // Store scan results
        $this->storeVulnerabilityScan($serviceId, $results);

        return [
            'service_id' => $serviceId,
            'scan_date' => date('Y-m-d H:i:s'),
            'vulnerabilities' => $results,
            'total_issues' => count($results)
        ];
    }

    /**
     * Get monitoring dashboard data
     */
    public function getDashboardData(): array {
        $stats = $this->db->select(
            "SELECT
                COUNT(*) as total_certs,
                SUM(CASE WHEN expiry_date <= DATE_ADD(CURDATE(), INTERVAL 30 DAY) THEN 1 ELSE 0 END) as expiring_soon,
                SUM(CASE WHEN expiry_date <= CURDATE() THEN 1 ELSE 0 END) as expired,
                SUM(CASE WHEN status = 'active' THEN 1 ELSE 0 END) as active
             FROM mod_ssl_certificates"
        )[0];

        $vulnerabilities = $this->db->select(
            "SELECT severity, COUNT(*) as count
             FROM mod_ssl_vulnerabilities
             WHERE resolved = 0 AND created_at > DATE_SUB(NOW(), INTERVAL 30 DAY)
             GROUP BY severity"
        );

        return [
            'total_certificates' => $stats->total_certs,
            'active' => $stats->active,
            'expiring_soon' => $stats->expiring_soon,
            'expired' => $stats->expired,
            'vulnerabilities_by_severity' => array_column($vulnerabilities, 'count', 'severity'),
            'generated_at' => date('Y-m-d H:i:s')
        ];
    }

    // Private helper methods

    private function checkExpiry(array $monitor): array {
        $cert = $this->getCertificate($monitor['certificate_id']);

        $expiryTimestamp = strtotime($cert['expiry_date']);
        $daysUntilExpiry = floor(($expiryTimestamp - time()) / 86400);

        return [
            'expiry_date' => $cert['expiry_date'],
            'days_remaining' => $daysUntilExpiry,
            'is_expired' => $daysUntilExpiry < 0,
            'is_critical' => $daysUntilExpiry <= 7,
            'is_warning' => $daysUntilExpiry <= 30
        ];
    }

    private function analyzeProtocols(array $monitor): array {
        $cert = $this->getCertificate($monitor['certificate_id']);

        // Get supported protocols and ciphers
        $analysis = $this->scanner->analyzeTLSConfiguration($monitor['service_id']);

        $issues = [];

        if (!$analysis['tls_1_2_supported']) {
            $issues[] = [
                'severity' => 'medium',
                'type' => 'old_tls',
                'description' => 'TLS 1.2 not supported'
            ];
        }

        if ($analysis['tls_1_0_supported'] || $analysis['ssl_enabled']) {
            $issues[] = [
                'severity' => 'high',
                'type' => 'deprecated_protocol',
                'description' => 'Deprecated SSL/TLS protocols detected'
            ];
        }

        if ($this->hasWeakCiphers($analysis['ciphers'])) {
            $issues[] = [
                'severity' => 'medium',
                'type' => 'weak_ciphers',
                'description' => 'Weak cipher suites in use'
            ];
        }

        return [
            'tls_1_0' => $analysis['tls_1_0_supported'] ?? false,
            'tls_1_1' => $analysis['tls_1_1_supported'] ?? false,
            'tls_1_2' => $analysis['tls_1_2_supported'] ?? false,
            'tls_1_3' => $analysis['tls_1_3_supported'] ?? false,
            'issues' => $issues
        ];
    }

    private function evaluateAlerts(array $monitor, array $results): void {
        $alerts = [];

        // Expiry alerts
        if ($results['expiry']['is_critical']) {
            $alerts[] = [
                'type' => 'critical_expiry',
                'message' => "Certificate expires in {$results['expiry']['days_remaining']} days",
                'severity' => 'critical'
            ];
        } elseif ($results['expiry']['is_warning']) {
            $alerts[] = [
                'type' => 'warning_expiry',
                'message' => "Certificate expires in {$results['expiry']['days_remaining']} days",
                'severity' => 'warning'
            ];
        }

        // Vulnerability alerts
        if (!empty($results['vulnerabilities'])) {
            foreach ($results['vulnerabilities'] as $vuln) {
                if ($vuln['severity'] === 'critical' || $vuln['severity'] === 'high') {
                    $alerts[] = [
                        'type' => 'vulnerability',
                        'message' => $vuln['description'],
                        'severity' => $vuln['severity']
                    ];
                }
            }
        }

        // Send alerts
        foreach ($alerts as $alert) {
            $this->sendAlert($monitor['service_id'], $alert);
        }
    }

    private function sendAlert(int $serviceId, array $alert): void {
        // Log alert
        $this->db->insert('mod_ssl_alerts', [
            'monitor_id' => $this->getMonitorIdByService($serviceId),
            'service_id' => $serviceId,
            'type' => $alert['type'],
            'message' => $alert['message'],
            'severity' => $alert['severity'],
            'created_at' => date('Y-m-d H:i:s')
        ]);

        // Send email if configured
        if ($this->shouldEmailAlert($alert['severity'])) {
            $this->sendAlertEmail($serviceId, $alert);
        }
    }
}

/**
 * SSL Vulnerability Scanner
 */
class SSLVulnerabilityScanner {
    public function scanVulnerabilities(array $monitor): array {
        // Implement vulnerability scanning
        return [];
    }

    public function analyzeTLSConfiguration(int $serviceId): array {
        $service = $this->getService($serviceId);
        $ip = $service['ip_address'];

        // Use testssl or similar tool
        $output = shell_exec("testssl --json {$ip} 2>&1");

        return json_decode($output, true) ?? [];
    }

    private function hasWeakCiphers(array $ciphers): bool {
        $weakCiphers = ['RC4', 'DES', '3DES', 'MD5', 'SHA1'];
        foreach ($ciphers as $cipher) {
            foreach ($weakCiphers as $weak) {
                if (stripos($cipher, $weak) !== false) {
                    return true;
                }
            }
        }
        return false;
    }
}
```

## Database Schema
```sql
CREATE TABLE `mod_ssl_monitors` (
  `id` VARCHAR(50) PRIMARY KEY,
  `certificate_id` VARCHAR(50) NOT NULL,
  `service_id` INT NOT NULL,
  `check_interval_hours` INT DEFAULT 24,
  `alert_threshold_days` INT DEFAULT 30,
  `vulnerability_scan_enabled` TINYINT(1) DEFAULT 1,
  `protocol_scan_enabled` TINYINT(1) DEFAULT 1,
  `status` ENUM('active', 'paused', 'error') DEFAULT 'active',
  `last_check_at` DATETIME,
  `created_at` DATETIME NOT NULL,
  UNIQUE KEY `unique_service` (`service_id`)
);

CREATE TABLE `mod_ssl_check_results` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `monitor_id` VARCHAR(50) NOT NULL,
  `check_type` VARCHAR(50) NOT NULL,
  `results` TEXT,
  `created_at` DATETIME NOT NULL,
  FOREIGN KEY (`monitor_id`) REFERENCES `mod_ssl_monitors`(`id`)
);

CREATE TABLE `mod_ssl_vulnerabilities` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `service_id` INT NOT NULL,
  `type` VARCHAR(100) NOT NULL,
  `severity` ENUM('low', 'medium', 'high', 'critical') NOT NULL,
  'description' TEXT,
  `recommendation' TEXT,
  'resolved' TINYINT(1) DEFAULT 0,
  `resolved_at` DATETIME,
  `created_at` DATETIME NOT NULL,
  INDEX `idx_service_id` (`service_id`)
);

CREATE TABLE `mod_ssl_alerts` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `monitor_id` VARCHAR(50),
  `service_id` INT NOT NULL,
  `type` VARCHAR(50) NOT NULL,
  `message` TEXT,
  `severity` ENUM('info', 'warning', 'critical') DEFAULT 'warning',
  `acknowledged` TINYINT(1) DEFAULT 0,
  `created_at` DATETIME NOT NULL,
  INDEX `idx_service_severity` (`service_id`, `severity`)
);
```

## Best Practices

1. **Regular Scanning**: Run vulnerability scans at least weekly
2. **Monitor Expiry**: Track all certificates, not just active ones
3. **Alert Tiers**: Different alert levels for different severity
4. **Protocol Analysis**: Check for deprecated protocols regularly
5. **Chain Validation**: Verify complete certificate chain integrity

## Related Skills

- whmcs-letsencrypt-auto
- whmcs-ssl-renewal
- whmcs-ssl-scan-vulnerability
- whmcs-certificate-transparency
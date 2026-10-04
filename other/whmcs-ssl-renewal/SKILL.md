---
name: whmcs-ssl-renewal
description: SSL renewal workflow for WHMCS
category: SSL & Security
version: 1.0.0
---

# WHMCS SSL Renewal Workflow Skill

## Overview
This skill provides patterns and implementations for managing SSL certificate renewal workflows in WHMCS, including scheduling, validation, deployment, and notification systems.

## Implementation Patterns

### SSL Renewal Manager
```php
<?php
/**
 * WHMCS SSL Renewal Workflow
 * Manages certificate renewal lifecycle
 */

namespace WHMCS\Module\Server\SSL;

class SSLRenewalManager {
    private $db;
    private $deploymentManager;

    public function __construct() {
        $this->db = \WHMCS\Database\Capsule::connection();
        $this->deploymentManager = new SSLDeploymentManager();
    }

    /**
     * Schedule certificate renewal
     */
    public function scheduleRenewal(array $params): array {
        $scheduleId = 'ren_' . bin2hex(random_bytes(12));

        $schedule = [
            'id' => $scheduleId,
            'certificate_id' => $params['certificate_id'],
            'renewal_days_before' => $params['days_before'] ?? 30,
            'auto_renew' => $params['auto_renew'] ?? true,
            'notification_enabled' => $params['notify'] ?? true,
            'notification_days' => json_encode($params['notify_days'] ?? [30, 14, 7, 1]),
            'status' => 'active',
            'created_at' => date('Y-m-d H:i:s')
        ];

        $this->db->insert('mod_ssl_renewal_schedules', $schedule);

        // Calculate next renewal date
        $nextRenewal = $this->calculateNextRenewal($params['certificate_id'], $params['days_before'] ?? 30);

        return [
            'success' => true,
            'schedule_id' => $scheduleId,
            'next_renewal' => $nextRenewal
        ];
    }

    /**
     * Process pending renewals
     */
    public function processPendingRenewals(): array {
        $dueRenewals = $this->db->select(
            "SELECT rs.*, c.service_id, c.common_name, c.expiry_date
             FROM mod_ssl_renewal_schedules rs
             JOIN mod_ssl_certificates c ON rs.certificate_id = c.id
             WHERE rs.auto_renew = 1
             AND rs.status = 'active'
             AND c.status = 'active'
             AND c.expiry_date <= DATE_ADD(CURDATE(), INTERVAL rs.renewal_days_before DAY)"
        );

        $results = [];

        foreach ($dueRenewals as $renewal) {
            try {
                $result = $this->executeRenewal($renewal);
                $results[] = array_merge(['success' => true], $result);
            } catch (\Exception $e) {
                $results[] = [
                    'success' => false,
                    'schedule_id' => $renewal->id,
                    'error' => $e->getMessage()
                ];

                $this->logRenewalFailure($renewal, $e->getMessage());
            }
        }

        return [
            'processed' => count($results),
            'successful' => count(array_filter($results, fn($r) => $r['success'])),
            'failed' => count(array_filter($results, fn($r) => !$r['success'])),
            'details' => $results
        ];
    }

    /**
     * Execute renewal
     */
    private function executeRenewal($schedule): array {
        $certificate = $this->getCertificate($schedule->certificate_id);

        // Check if already being renewed
        if ($certificate->status === 'renewing') {
            throw new \Exception("Renewal already in progress");
        }

        // Update status
        $this->db->update('mod_ssl_certificates', [
            'status' => 'renewing'
        ], ['id' => $schedule->certificate_id]);

        // Create new order
        $letsEncrypt = new LetsEncryptManager();
        $domains = array_filter(array_merge([$certificate->common_name], explode(',', $certificate->sans)));

        $newCert = $letsEncrypt->requestCertificate([
            'service_id' => $schedule->service_id,
            'domains' => $domains,
            'challenge_type' => $certificate->challenge_type ?? 'http'
        ]);

        // Deploy new certificate
        $this->deploymentManager->deployToService($schedule->service_id, $newCert['certificate_id']);

        // Update old certificate status
        $this->db->update('mod_ssl_certificates', [
            'status' => 'replaced',
            'replaced_by' => $newCert['certificate_id']
        ], ['id' => $schedule->certificate_id]);

        // Update schedule
        $nextRenewal = $this->calculateNextRenewal($newCert['certificate_id'], $schedule->renewal_days_before);

        $this->db->update('mod_ssl_renewal_schedules', [
            'certificate_id' => $newCert['certificate_id'],
            'last_renewal_at' => date('Y-m-d H:i:s'),
            'next_renewal_at' => $nextRenewal
        ], ['id' => $schedule->id]);

        // Send notification
        $this->sendRenewalNotification($schedule, true);

        return [
            'schedule_id' => $schedule->id,
            'old_cert_id' => $schedule->certificate_id,
            'new_cert_id' => $newCert['certificate_id'],
            'next_renewal' => $nextRenewal
        ];
    }

    /**
     * Manual renewal trigger
     */
    public function triggerManualRenewal(string $scheduleId): array {
        $schedule = $this->getSchedule($scheduleId);

        if (!$schedule) {
            throw new \Exception("Renewal schedule not found");
        }

        return $this->executeRenewal($schedule);
    }

    /**
     * Calculate next renewal date
     */
    private function calculateNextRenewal(string $certificateId, int $daysBefore): string {
        $certificate = $this->getCertificate($certificateId);
        $expiry = strtotime($certificate->expiry_date);

        return date('Y-m-d', $expiry - ($daysBefore * 86400));
    }

    /**
     * Send renewal notifications
     */
    public function sendRenewalNotifications(): array {
        $today = date('Y-m-d');

        // Get notifications due today
        $schedules = $this->db->select(
            "SELECT rs.*, c.common_name, c.expiry_date, c.service_id
             FROM mod_ssl_renewal_schedules rs
             JOIN mod_ssl_certificates c ON rs.certificate_id = c.id
             WHERE rs.notification_enabled = 1
             AND c.status = 'active'"
        );

        $sent = [];

        foreach ($schedules as $schedule) {
            $notifyDays = json_decode($schedule->notification_days, true);
            $daysUntilExpiry = (strtotime($schedule->expiry_date) - time()) / 86400;

            if (in_array((int) $daysUntilExpiry, $notifyDays)) {
                $this->sendExpiryWarning($schedule, (int) $daysUntilExpiry);
                $sent[] = $schedule->id;
            }
        }

        return ['notifications_sent' => count($sent)];
    }

    private function sendExpiryWarning($schedule, int $daysRemaining): void {
        $service = $this->db->select(
            "SELECT h.*, c.email, c.firstname, c.lastname
             FROM tblhosting h
             JOIN tblclients c ON h.userid = c.id
             WHERE h.id = ?",
            [$schedule->service_id]
        )[0];

        if (!$service) return;

        send_email($service->email, 'ssl-expiry-warning', [
            'client_name' => $service->firstname . ' ' . $service->lastname,
            'domain' => $schedule->common_name,
            'days_remaining' => $daysRemaining,
            'expiry_date' => $schedule->expiry_date
        ]);
    }

    private function logRenewalFailure($schedule, string $error): void {
        $this->db->insert('mod_ssl_renewal_logs', [
            'schedule_id' => $schedule->id,
            'action' => 'renewal_failed',
            'error_message' => $error,
            'created_at' => date('Y-m-d H:i:s')
        ]);
    }
}

/**
 * SSL Deployment Manager
 */
class SSLDeploymentManager {
    public function deployToService(int $serviceId, string $certId): void {
        $cert = $this->getCertificate($certId);

        // Deploy based on service type
        switch ($this->getServiceType($serviceId)) {
            case 'apache':
                $this->deployToApache($cert);
                break;
            case 'nginx':
                $this->deployToNginx($cert);
                break;
            case 'cpanel':
                $this->deployToCpanel($cert);
                break;
            case 'plesk':
                $this->deployToPlesk($cert);
                break;
        }

        // Reload web server
        $this->reloadWebServer($serviceId);
    }

    private function deployToApache(array $cert): void {
        $vhostPath = "/etc/apache2/sites-enabled/{$cert['common_name']}.conf";

        $config = <<<CONFIG
<VirtualHost *:443>
    ServerName {$cert['common_name']}
    DocumentRoot /var/www/html

    SSLEngine on
    SSLCertificateFile /etc/ssl/certs/{$cert['id']}.crt
    SSLCertificateKeyFile /etc/ssl/private/{$cert['id']}.key
    SSLCertificateChainFile /etc/ssl/certs/{$cert['id']}.chain
</VirtualHost>
CONFIG;

        file_put_contents($vhostPath, $config);
    }

    private function deployToNginx(array $cert): void {
        $vhostPath = "/etc/nginx/sites-enabled/{$cert['common_name']}.conf";

        $config = <<<CONFIG
server {
    listen 443 ssl;
    server_name {$cert['common_name']};

    ssl_certificate /etc/ssl/certs/{$cert['id']}.crt;
    ssl_certificate_key /etc/ssl/private/{$cert['id']}.key;
    ssl_trusted_certificate /etc/ssl/certs/{$cert['id']}.chain;

    # SSL configuration
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
}
CONFIG;

        file_put_contents($vhostPath, $config);
    }
}
```

## Database Schema
```sql
CREATE TABLE `mod_ssl_renewal_schedules` (
  `id` VARCHAR(50) PRIMARY KEY,
  `certificate_id` VARCHAR(50) NOT NULL,
  `renewal_days_before` INT DEFAULT 30,
  `auto_renew` TINYINT(1) DEFAULT 1,
  `notification_enabled` TINYINT(1) DEFAULT 1,
  `notification_days` TEXT,
  `status` ENUM('active', 'paused', 'cancelled') DEFAULT 'active',
  `last_renewal_at` DATETIME,
  `next_renewal_at` DATETIME,
  `created_at` DATETIME NOT NULL
);

CREATE TABLE `mod_ssl_renewal_logs` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `schedule_id` VARCHAR(50) NOT NULL,
  `action` VARCHAR(50) NOT NULL,
  `error_message` TEXT,
  `created_at` DATETIME NOT NULL,
  FOREIGN KEY (`schedule_id`) REFERENCES `mod_ssl_renewal_schedules`(`id`)
);
```

## Renewal Workflow Timeline

```
┌─────────────────────────────────────────────────────────────────┐
│                    SSL Renewal Timeline                          │
├─────────────────────────────────────────────────────────────────┤
│  90 days: Certificate issued                                    │
│     │                                                         │
│  60 days: First warning notification (if configured)           │
│     │                                                         │
│  30 days: Auto-renewal check begins                            │
│     │                                                         │
│  30 days: Renewal scheduled if auto_renew enabled              │
│     │                                                         │
│  14 days: Second warning notification                          │
│     │                                                         │
│  7 days: Final warning before expiry                           │
│     │                                                         │
│  1 day: Last chance renewal notification                       │
│     │                                                         │
│  0 days: Certificate expires - service may be affected         │
└─────────────────────────────────────────────────────────────────┘
```

## Best Practices

1. **Early Detection**: Monitor certificate expiry dates regularly
2. **Automated Renewal**: Enable auto-renewal whenever possible
3. **Testing**: Test renewal process in staging environment
4. **Notifications**: Send multiple reminders at different intervals
5. **Fallback**: Have backup certificates available

## Related Skills

- whmcs-letsencrypt-auto
- whmcs-ssl-monitor
- whmcs-certificate-transparency
- whmcs-ocsp-stapling
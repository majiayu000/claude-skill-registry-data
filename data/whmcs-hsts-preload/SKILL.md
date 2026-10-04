---
name: whmcs-hsts-preload
description: HSTS preload list for WHMCS
category: SSL & Security
version: 1.0.0
---

# WHMCS HSTS Preload List Skill

## Overview
This skill provides patterns and implementations for HSTS preload list submission and management in WHMCS, including eligibility verification and submission workflow.

## Implementation Patterns

### HSTS Preload Manager
```php
<?php
/**
 * WHMCS HSTS Preload List Management
 * Handles HSTS preload submission
 */

namespace WHMCS\Module\Server\Security;

class HSTSPreloadManager {
    private $db;

    public function __construct() {
        $this->db = \WHMCS\Database\Capsule::connection();
    }

    /**
     * Check preload eligibility
     */
    public function checkEligibility(int $serviceId): array {
        $requirements = [
            'max_age' => ['required' => 31536000, 'description' => 'min 1 year'],
            'include_subdomains' => ['required' => true, 'description' => 'must include all subdomains'],
            'preload_directive' => ['required' => true, 'description' => 'must have preload directive'],
            'https_only' => ['required' => true, 'description' => 'all traffic must be HTTPS'],
            'no_cookie_flags' => ['description' => 'cookies should be secure'],
            'no_critical_issues' => ['description' => 'no mixed content']
        ];

        $domain = $this->getServiceDomain($serviceId);
        $checks = [];

        // Check max-age
        $hstsConfig = $this->db->select(
            "SELECT hsts_config FROM mod_service_security WHERE service_id = ?",
            [$serviceId]
        )[0];

        if ($hstsConfig && $hstsConfig->hsts_config) {
            $config = json_decode($hstsConfig->hsts_config, true);
            $checks['max_age'] = [
                'passed' => ($config['max_age'] ?? 0) >= 31536000,
                'current' => $config['max_age'] ?? 0
            ];

            $checks['include_subdomains'] = [
                'passed' => $config['include_subdomains'] ?? false
            ];

            $checks['preload_directive'] = [
                'passed' => $config['preload'] ?? false
            ];
        } else {
            $checks['max_age'] = ['passed' => false, 'current' => 0];
            $checks['include_subdomains'] = ['passed' => false];
            $checks['preload_directive'] = ['passed' => false];
        }

        // Check HTTPS enforcement
        $checks['https_only'] = ['passed' => $this->checkHTTPSEnforcement($domain)];

        // Check for mixed content
        $checks['no_mixed_content'] = ['passed' => $this->checkNoMixedContent($domain)];

        // Calculate overall eligibility
        $eligible = array_reduce($checks, fn($carry, $check) => $carry && $check['passed'], true);

        return [
            'service_id' => $serviceId,
            'domain' => $domain,
            'eligible' => $eligible,
            'checks' => $checks,
            'requirements' => $requirements
        ];
    }

    /**
     * Submit to HSTS preload list
     */
    public function submitToPreloadList(int $serviceId): array {
        $eligibility = $this->checkEligibility($serviceId);

        if (!$eligibility['eligible']) {
            throw new \Exception("Service does not meet preload eligibility requirements");
        }

        $domain = $eligibility['domain'];

        // Create submission payload
        $submission = [
            'domain' => $domain,
            'include_subdomains' => true,
            'policy' => 'max-age=31536000; includeSubDomains; preload',
            'submitter' => 'whmcs',
            'submitter_contact' => $this->getSubmitterContact()
        ];

        // Submit to hstspreload.org
        $response = $this->submitToHSTSPS($submission);

        // Update status
        $this->db->update('mod_service_security', [
            'preload_submitted' => true,
            'preload_submitted_at' => date('Y-m-d H:i:s'),
            'preload_status' => $response['status'] ?? 'pending'
        ], ['service_id' => $serviceId]);

        // Log submission
        $this->logPreloadSubmission($serviceId, $submission, $response);

        return [
            'success' => true,
            'service_id' => $serviceId,
            'domain' => $domain,
            'status' => $response['status'] ?? 'submitted',
            'estimated_inclusion' => $this->estimateInclusionTime()
        ];
    }

    /**
     * Check preload removal status
     */
    public function checkRemovalStatus(int $serviceId): array {
        $domain = $this->getServiceDomain($serviceId);

        // Check if domain is in preload list
        $inList = $this->checkPreloadListInclusion($domain);

        if (!$inList) {
            return [
                'in_preload_list' => false,
                'message' => 'Domain not currently in preload list'
            ];
        }

        // Check removal request status if any
        $removal = $this->db->select(
            "SELECT * FROM mod_hsts_preload_removals WHERE service_id = ? ORDER BY created_at DESC LIMIT 1",
            [$serviceId]
        )[0];

        return [
            'in_preload_list' => true,
            'domain' => $domain,
            'removal_requested' => $removal ? true : false,
            'removal_status' => $removal->status ?? null,
            'estimated_removal' => $removal ? $this->estimateRemovalTime() : null
        ];
    }

    /**
     * Request removal from preload list
     */
    public function requestRemoval(int $serviceId): array {
        $domain = $this->getServiceDomain($serviceId);

        $this->db->insert('mod_hsts_preload_removals', [
            'service_id' => $serviceId,
            'domain' => $domain,
            'status' => 'pending',
            'requested_at' => date('Y-m-d H:i:s')
        ]);

        // Submit removal request
        $this->submitRemovalRequest($domain);

        return [
            'success' => true,
            'service_id' => $serviceId,
            'domain' => $domain,
            'status' => 'pending_removal',
            'note' => 'Removal from preload list takes 2-3 months'
        ];
    }

    // Private helper methods

    private function checkHTTPSEnforcement(string $domain): bool {
        $ch = curl_init("https://{$domain}/");
        curl_setopt_array($ch, [
            CURLOPT_RETURNTRANSFER => true,
            CURLOPT_NOBODY => true
        ]);
        curl_exec($ch);
        $code = curl_getinfo($ch, CURLINFO_HTTP_CODE);
        curl_close($ch);

        return $code > 0;
    }

    private function checkNoMixedContent(string $domain): bool {
        // Check for mixed content issues
        $html = @file_get_contents("https://{$domain}/");

        if (!$html) return false;

        // Check for http:// resources
        $hasMixedContent = preg_match('/src=["\']http:\/\//i', $html);

        return !$hasMixedContent;
    }

    private function submitToHSTSPS(array $submission): array {
        // Submit to hstspreload.org
        $ch = curl_init('https://hstspreload.org/api/v1/domains/');
        curl_setopt_array($ch, [
            CURLOPT_POST => true,
            CURLOPT_POSTFIELDS => http_build_query($submission),
            CURLOPT_RETURNTRANSFER => true
        ]);

        $response = curl_exec($ch);
        curl_close($ch);

        return json_decode($response, true) ?? ['status' => 'unknown'];
    }

    private function submitRemovalRequest(string $domain): void {
        // Submit removal request
        $ch = curl_init("https://hstspreload.org/api/v1/domains/{$domain}/");
        curl_setopt_array($ch, [
            CURLOPT_CUSTOMREQUEST => 'DELETE',
            CURLOPT_RETURNTRANSFER => true
        ]);
        curl_exec($ch);
        curl_close($ch);
    }

    private function estimateInclusionTime(): string {
        // Chrome updates preload list approximately every 6 weeks
        return date('Y-m-d', strtotime('+6 weeks'));
    }

    private function estimateRemovalTime(): string {
        // Browser vendors update preload list approximately every 6 weeks
        return date('Y-m-d', strtotime('+8 weeks'));
    }
}
```

## Preload Requirements Checklist

| Requirement | Minimum Value | WHMCS Implementation |
|-------------|--------------|---------------------|
| max-age | 31536000 seconds (1 year) | Configured in HSTS settings |
| includeSubDomains | Required | Automatic |
| preload | Required | Automatic |
| HTTPS Only | All traffic HTTPS | Enforced via redirect |
| No Mixed Content | All resources HTTPS | CSP and content checks |

## Database Schema
```sql
CREATE TABLE `mod_hsts_preload_submissions` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `service_id` INT NOT NULL,
  `domain` VARCHAR(255) NOT NULL,
  `policy` VARCHAR(500),
  `status` ENUM('pending', 'approved', 'rejected') DEFAULT 'pending',
  `submitted_at` DATETIME NOT NULL,
  `approved_at` DATETIME,
  INDEX `idx_service_id` (`service_id`)
);

CREATE TABLE `mod_hsts_preload_removals` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `service_id` INT NOT NULL,
  `domain` VARCHAR(255) NOT NULL,
  `status` ENUM('pending', 'requested', 'removed') DEFAULT 'pending',
  `requested_at` DATETIME NOT NULL,
  `removed_at` DATETIME
);
```

## Best Practices

1. **Test Thoroughly**: Ensure all subdomains work with HTTPS before submission
2. **Plan for Duration**: Once submitted, removal takes 2-3 months minimum
3. **Document Changes**: Keep records of all HSTS-related changes
4. **Monitor Status**: Track inclusion in preload lists
5. **Consider Implications**: Subdomain lock-in means all subdomains must use HTTPS

## Related Skills

- whmcs-certificate-pinning
- whmcs-security-headers
- whmcs-tls-configuration
- whmcs-ssl-renewal
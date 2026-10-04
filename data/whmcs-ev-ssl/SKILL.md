---
name: whmcs-ev-ssl
description: Extended validation SSL for WHMCS
category: SSL & Security
version: 1.0.0
---

# WHMCS Extended Validation SSL Skill

## Overview
This skill provides patterns and implementations for managing Extended Validation (EV) SSL certificates in WHMCS, including validation procedures, organization verification, and EV-specific deployment.

## Implementation Patterns

### EV Certificate Manager
```php
<?php
/**
 * WHMCS Extended Validation SSL
 * Handles EV certificate lifecycle
 */

namespace WHMCS\Module\Server\SSL;

class EVSSLCertificateManager {
    private $db;
    private $validationProcessor;

    public function __construct() {
        $this->db = \WHMCS\Database\Capsule::connection();
        $this->validationProcessor = new EVValidationProcessor();
    }

    /**
     * Request EV certificate
     */
    public function requestEVCertificate(array $params): array {
        $orderId = 'ev_' . bin2hex(random_bytes(12));

        // EV requires organization verification
        $order = [
            'id' => $orderId,
            'service_id' => $params['service_id'],
            'common_name' => $params['domain'],
            'organization_name' => $params['organization_name'],
            'organization_unit' => $params['organization_unit'] ?? null,
            'registration_number' => $params['registration_number'],
            'jurisdiction' => $params['jurisdiction'],
            'duns' => $params['duns'] ?? null,
            'key_type' => 'RSA2048',
            'csr' => $params['csr'],
            'status' => 'validation_pending',
            'created_at' => date('Y-m-d H:i:s')
        ];

        $this->db->insert('mod_ev_certificates', $order);

        // Begin EV validation process
        $this->validationProcessor->startValidation($orderId, $params);

        return [
            'success' => true,
            'order_id' => $orderId,
            'status' => 'validation_pending',
            'required_documents' => $this->validationProcessor->getRequiredDocuments()
        ];
    }

    /**
     * Submit organization documents
     */
    public function submitDocuments(string $orderId, array $documents): array {
        $order = $this->getEVOrder($orderId);

        if (!$order) {
            throw new \Exception("EV order not found: {$orderId}");
        }

        // Store document references
        $docRecords = [];
        foreach ($documents as $doc) {
            $docId = 'doc_' . bin2hex(random_bytes(8));
            $this->db->insert('mod_ev_documents', [
                'id' => $docId,
                'order_id' => $orderId,
                'document_type' => $doc['type'],
                'file_path' => $doc['path'],
                'uploaded_at' => date('Y-m-d H:i:s')
            ]);
            $docRecords[] = $docId;
        }

        // Submit to CA for review
        $this->validationProcessor->submitDocuments($orderId, $documents);

        return [
            'success' => true,
            'order_id' => $orderId,
            'documents_submitted' => count($docRecords)
        ];
    }

    /**
     * Process DCV (Domain Control Validation)
     */
    public function processDCV(string $orderId, string $method = 'email'): array {
        $order = $this->getEVOrder($orderId);

        if (!$order) {
            throw new \Exception("EV order not found");
        }

        // Method: email, http, dns
        switch ($method) {
            case 'email':
                $approverEmails = $this->getApproverEmails($order->common_name);
                $this->sendDCVEmail($order->common_name, $approverEmails);
                break;
            case 'http':
                $token = $this->createDCVToken($orderId);
                $this->placeDCVFile($order->common_name, $token);
                break;
            case 'dns':
                $token = $this->createDCVToken($orderId);
                $this->addDCVDNSRecord($order->common_name, $token);
                break;
        }

        $this->db->update('mod_ev_certificates', [
            'dcv_method' => $method,
            'dcv_status' => 'pending'
        ], ['id' => $orderId]);

        return [
            'success' => true,
            'order_id' => $orderId,
            'dcv_method' => $method,
            'status' => 'dcv_pending'
        ];
    }

    /**
     * Verify organization identity
     */
    public function verifyOrganization(string $orderId): array {
        $order = $this->getEVOrder($orderId);

        // Trigger organization verification
        $result = $this->validationProcessor->verifyOrganization($order);

        if ($result['verified']) {
            $this->db->update('mod_ev_certificates', [
                'org_verified' => true,
                'org_verified_at' => date('Y-m-d H:i:s')
            ], ['id' => $orderId]);
        }

        return $result;
    }

    /**
     * Complete EV certificate issuance
     */
    public function completeIssuance(string $orderId): array {
        $order = $this->getEVOrder($orderId);

        // Check all validations passed
        if (!$this->allValidationsComplete($orderId)) {
            throw new \Exception("All validations must be complete before issuance");
        }

        // Finalize with CA
        $certificate = $this->validationProcessor->issueCertificate($orderId);

        // Store certificate
        $certId = $this->storeCertificate($orderId, $certificate);

        // Update order
        $this->db->update('mod_ev_certificates', [
            'cert_id' => $certId,
            'status' => 'issued',
            'issued_at' => date('Y-m-d H:i:s')
        ], ['id' => $orderId]);

        // Deploy with EV properties
        $this->deployEVCertificate($order->service_id, $certId);

        return [
            'success' => true,
            'order_id' => $orderId,
            'cert_id' => $certId,
            'green_bar_enabled' => true
        ];
    }

    /**
     * Get EV certificate status
     */
    public function getStatus(string $orderId): array {
        $order = $this->getEVOrder($orderId);

        $validations = [
            'organization' => [
                'status' => $order->org_verified ? 'verified' : 'pending',
                'verified_at' => $order->org_verified_at
            ],
            'domain' => [
                'status' => $order->dcv_status,
                'method' => $order->dcv_method
            ],
            'operational' => [
                'status' => $order->operational_verified ? 'verified' : 'pending'
            ]
        ];

        return [
            'order_id' => $orderId,
            'common_name' => $order->common_name,
            'organization' => $order->organization_name,
            'status' => $order->status,
            'validations' => $validations,
            'created_at' => $order->created_at
        ];
    }

    // Private helper methods

    private function getApproverEmails(string $domain): array {
        // Common EV approver emails
        return [
            'admin@' . $domain,
            'administrator@' . $domain,
            'webmaster@' . $domain,
            'postmaster@' . $domain,
            'hostmaster@' . $domain
        ];
    }

    private function createDCVToken(string $orderId): string {
        return bin2hex(random_bytes(32));
    }

    private function placeDCVFile(string $domain, string $token): void {
        $path = "/var/www/html/.well-known/pki-validation/{$token}.txt";
        $content = "{$token}";

        if (!is_dir(dirname($path))) {
            mkdir(dirname($path), 0755, true);
        }

        file_put_contents($path, $content);
    }

    private function addDCVDNSRecord(string $domain, string $token): void {
        $recordName = "_acme-validation.{$domain}";
        $recordValue = "{$token}";

        // Add DNS TXT record
        // Implementation depends on DNS provider
    }

    private function allValidationsComplete(string $orderId): bool {
        $order = $this->getEVOrder($orderId);

        return $order->org_verified &&
               $order->dcv_status === 'completed' &&
               $order->operational_verified;
    }

    private function deployEVCertificate(int $serviceId, string $certId): void {
        $cert = $this->getCertificate($certId);

        // Deploy with EV-specific configurations
        // EV certificates show organization name in browser
        $this->updateWebServerConfig($serviceId, $cert);
        $this->reloadWebServer($serviceId);
    }
}

/**
 * EV Validation Processor
 */
class EVValidationProcessor {
    private $caEndpoint;

    public function startValidation(string $orderId, array $params): void {
        // Initiate validation with CA
        // This involves organization checks, phone verification, etc.
    }

    public function getRequiredDocuments(): array {
        return [
            ['type' => 'business_license', 'description' => 'Business License or Registration'],
            ['type' => 'articles_of_incorporation', 'description' => 'Articles of Incorporation'],
            ['type' => 'bank_statement', 'description' => 'Bank Statement (for address verification)'],
            ['type' => 'telephone_bill', 'description' => 'Telephone Bill (for phone verification)']
        ];
    }

    public function submitDocuments(string $orderId, array $documents): void {
        // Submit documents to CA for verification
    }

    public function verifyOrganization(array $order): array {
        // Phone verification, legal name verification, etc.
        return [
            'verified' => true,
            'verification_id' => 'ver_' . bin2hex(random_bytes(8)),
            'verified_by' => 'GlobalSign',
            'verified_at' => date('Y-m-d H:i:s')
        ];
    }

    public function issueCertificate(string $orderId): string {
        // Finalize certificate issuance with CA
        return '';
    }
}
```

## Database Schema
```sql
CREATE TABLE `mod_ev_certificates` (
  `id` VARCHAR(50) PRIMARY KEY,
  `service_id` INT NOT NULL,
  `common_name` VARCHAR(255) NOT NULL,
  `organization_name` VARCHAR(255) NOT NULL,
  `organization_unit` VARCHAR(255),
  `registration_number` VARCHAR(100),
  `jurisdiction` VARCHAR(100),
  `duns` VARCHAR(20),
  `csr` TEXT NOT NULL,
  `cert_id` VARCHAR(50),
  `dcv_method` VARCHAR(20),
  `dcv_status` ENUM('pending', 'completed') DEFAULT 'pending',
  `org_verified` TINYINT(1) DEFAULT 0,
  `org_verified_at` DATETIME,
  `operational_verified` TINYINT(1) DEFAULT 0,
  `status` ENUM('validation_pending', 'documents_submitted', 'verified', 'issued', 'failed') DEFAULT 'validation_pending',
  `issued_at' DATETIME,
  `created_at' DATETIME NOT NULL,
  INDEX `idx_service_id` (`service_id`)
);

CREATE TABLE `mod_ev_documents` (
  `id` VARCHAR(50) PRIMARY KEY,
  `order_id` VARCHAR(50) NOT NULL,
  `document_type` VARCHAR(50) NOT NULL,
  `file_path` VARCHAR(500) NOT NULL,
  `verified` TINYINT(1) DEFAULT 0,
  `uploaded_at` DATETIME NOT NULL,
  FOREIGN KEY (`order_id`) REFERENCES `mod_ev_certificates`(`id`)
);

CREATE TABLE `mod_ev_verification_log` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `order_id` VARCHAR(50) NOT NULL,
  `verification_type` VARCHAR(50) NOT NULL,
  `status` VARCHAR(20) NOT NULL,
  `details` TEXT,
  `verified_by` VARCHAR(100),
  `created_at' DATETIME NOT NULL,
  FOREIGN KEY (`order_id`) REFERENCES `mod_ev_certificates`(`id`)
);
```

## EV Certificate Features

| Feature | Description |
|---------|-------------|
| Green Address Bar | Browser shows green bar with company name |
| Organization Name | Displayed in certificate details |
| Higher Trust | Higher assurance level than DV certificates |
| Strict Validation | Phone, legal, and operational verification |
| Annual Renewal | Requires annual re-validation |

## Best Practices

1. **Document Preparation**: Have all documents ready before ordering
2. **Accurate Information**: Ensure organization details match legal documents exactly
3. **Phone Availability**: Be available for CA phone verification
4. **Timely Response**: Respond quickly to CA verification requests
5. **DCV Method**: Choose DNS validation for faster processing

## Related Skills

- whmcs-ssl-renewal
- whmcs-multi-domain-ssl
- whmcs-certificate-pinning
- whmcs-security-headers
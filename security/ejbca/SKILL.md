---
name: ejbca
description: "Expert agent for Keyfactor EJBCA enterprise PKI platform. Covers CA hierarchy setup, ACME/EST/CMP/SCEP/OCSP protocols, Registration Authority (RA), HSM integration, Common Criteria EAL4+ certification, Kubernetes deployment, and REST/WS APIs. WHEN: \"EJBCA\", \"Keyfactor EJBCA\", \"enterprise PKI\", \"EJBCA ACME\", \"EJBCA EST\", \"EJBCA CMP\", \"EJBCA SCEP\", \"registration authority\", \"EJBCA Kubernetes\", \"Common Criteria PKI\"."
license: MIT
---

# Keyfactor EJBCA

This skill covers EJBCA (formerly PrimeKey, now Keyfactor EJBCA), the open-source and enterprise PKI platform. It has deep knowledge of EJBCA architecture, CA management, enrollment protocols, HSM integration, and enterprise deployments.

## How to Approach Tasks

1. **Identify edition**: Community (LGPL, free), Enterprise (commercial), or Keyfactor Command (cloud-managed).
2. **Classify the request**: CA setup, enrollment protocol, RA configuration, protocol integration, HSM, or Kubernetes deployment.
3. **Identify enrollment protocol**: ACME, EST, CMP, SCEP, REST, WS (Web Services), or EJBCA RA UI.

## EJBCA Overview

EJBCA is a full-featured, open-source (Java EE) PKI platform with:
- **Common Criteria EAL4+ certified** (Enterprise edition)
- **Multiple enrollment protocols**: ACME, EST, CMP, SCEP, REST, Web Services
- **Multi-CA**: Run hundreds of CAs in a single instance
- **HSM integration**: PKCS#11 (Thales, nCipher, Utimaco, AWS CloudHSM, etc.)
- **RA (Registration Authority)**: Delegate enrollment without giving CA access
- **Role-based administration**: Granular access control
- **High availability**: Clustered, database-backed

---

## Architecture

```
EJBCA Cluster
├── CA Service (cryptographic operations)
│   ├── Root CA (offline recommended)
│   ├── Intermediate/Issuing CA (online)
│   └── OCSP Responder CA
│
├── VA (Validation Authority) — OCSP/CRL publishing
│
├── RA (Registration Authority) — enrollment front-end
│   ├── ACME protocol endpoint
│   ├── EST protocol endpoint
│   ├── CMP protocol endpoint
│   ├── SCEP protocol endpoint
│   └── REST API endpoint
│
├── Database (PostgreSQL, MySQL, MariaDB)
└── HSM (PKCS#11, optional but recommended for production)
```

---

## CA Hierarchy Setup

### Creating a Root CA

```
EJBCA Admin UI → CA Functions → Create new CA

Name: Root CA 2025
Subject DN: CN=Root CA 2025,O=Example Corp,C=US
CA Type: X509
Certificate Profile: RootCA
Validity: 30 years
Key Algorithm: RSA 4096 (or P-384 EC)
Signing Algorithm: SHA256WithRSA (or SHA384WithECDSA)
PKCS#11 HSM: select HSM token and key alias

For offline Root CA:
  Status: Initial (active for signing, but keep offline)
  Sign with: Self-signed
```

### Creating an Intermediate CA

```
EJBCA Admin UI → CA Functions → Create new CA

Name: Issuing CA 2025
Subject DN: CN=Issuing CA 2025,O=Example Corp,C=US
CA Type: X509
Certificate Profile: SubCA
Validity: 10 years
Signed by: Root CA 2025

For online operation:
  Status: Active
  CRL Generation: Enabled (24h period)
  OCSP: Enabled
  CRL Distribution Points: http://ejbca.example.com/ejbca/publicweb/webdist/certdist?cmd=crl&issuer=CN%3DIssuing+CA+2025...
  AIA: http://ejbca.example.com/ejbca/publicweb/webdist/certdist?cmd=cacert&issuer=...
```

---

## Certificate Profiles and End Entity Profiles

### Certificate Profile

Defines the X.509 fields and constraints for issued certificates:

```
Certificate Profile: TLS-Server-90Day
  Key Usage:
    Digital Signature: checked
    Key Encipherment: checked (RSA) / unchecked (ECDSA)
  Extended Key Usage:
    Server Authentication: checked
    Client Authentication: unchecked
  Basic Constraints:
    Critical: checked
    Is CA: NO
  Subject Alternative Names:
    DNS Name: allowed
    IP Address: allowed
  Validity:
    Certificate Validity: 90 days
    Allow Validity Override: No
  Signature Algorithm: SHA256WithRSA or SHA256WithECDSA
  OCSP No Check: unchecked
  CT Logging: enabled (for public CAs)
```

### End Entity Profile

Defines what information must be provided when enrolling:

```
End Entity Profile: Web-Service-Enrollment
  Subject DN Fields:
    Common Name: required
    Organization: required, default value: "Example Corp"
    Country: required, default value: "US"
  Subject Alternative Names:
    DNS Name: required
    IP Address: optional
  Certificate Profile: TLS-Server-90Day
  Default CA: Issuing CA 2025
  Available CAs: [Issuing CA 2025]
```

---

## Enrollment Protocols

### ACME (RFC 8555)

```bash
# EJBCA ACME directory URL
https://ejbca.example.com/ejbca/acme/directory

# certbot with EJBCA
certbot certonly \
    --server https://ejbca.example.com/ejbca/acme/directory \
    --email admin@example.com \
    --agree-tos \
    --standalone \
    -d myservice.example.com

# cert-manager ClusterIssuer with EJBCA ACME
```

```yaml
apiVersion: cert-manager.io/v1
kind: ClusterIssuer
metadata:
  name: ejbca-acme
spec:
  acme:
    server: https://ejbca.example.com/ejbca/acme/directory
    email: admin@example.com
    privateKeySecretRef:
      name: ejbca-acme-account-key
    solvers:
    - dns01:
        webhook:
          groupName: acme.ejbca.example.com
          solverName: ejbca-dns
```

**EJBCA ACME configuration**:
```
EJBCA Admin → RA Functions → ACME Configuration
  Alias: default
  End Entity Profile: Web-Service-Enrollment
  Certificate Profile: TLS-Server-90Day
  Pre-Authorization: HTTP-01, DNS-01
  Require Pre-Authorization: Yes
```

### EST (RFC 7030)

EST (Enrollment over Secure Transport) is a TLS-based certificate enrollment protocol, commonly used for IoT and network devices:

```
Endpoints:
  /cacerts         — Get CA certificates
  /simpleenroll    — Enroll (PKCS#10 CSR → certificate)
  /simplereenroll  — Re-enroll (renew existing certificate)
  /fullcmc         — Full CMC request
  
Authentication:
  Certificate-based (mTLS)
  Username/password (HTTP Basic over TLS)
  SRP (Secure Remote Password)
```

```bash
# EST enrollment with openssl
# 1. Generate key and CSR
openssl req -newkey rsa:2048 -nodes -keyout device.key \
    -subj "/CN=device-001/O=Example Corp" -out device.csr

# 2. EST simpleenroll
curl -X POST https://ejbca.example.com/.well-known/est/simpleenroll \
    -H "Content-Type: application/pkcs10" \
    --data-binary @device.csr \
    --user enrolluser:password \
    --cacert ca-chain.pem \
    -o device.p7

# 3. Convert PKCS#7 to PEM
openssl pkcs7 -in device.p7 -print_certs -out device.crt
```

### CMP (RFC 4210 / RFC 4211)

CMP is used by network devices (routers, switches, PKI clients for automated renewal):

```bash
# CMP enrollment via OpenSSL
openssl cmp -cmd ir \
    -server ejbca.example.com:443/ejbca/publicweb/cmp/alias \
    -path /ejbca/publicweb/cmp/alias \
    -ref myref \
    -secret pass:password \
    -newkey device.key \
    -subject "/CN=device-001/O=Example Corp" \
    -cert device.crt \
    -certout newdevice.crt
```

### SCEP (Simple Certificate Enrollment Protocol)

Commonly used by network devices (Cisco, Juniper) and MDM solutions:

```
SCEP URL: https://ejbca.example.com/ejbca/publicweb/apply/scep/alias/pkiclient.exe

Operations:
  GetCACaps  — Query CA capabilities
  GetCACert  — Download CA certificate
  PKIOperation (GetCertInitial, GetCert, GetCRL, PKCSReq, CertPoll)
```

### REST API

EJBCA REST API (v1):

```bash
# Enroll via REST API
curl -X POST https://ejbca.example.com/ejbca/ejbca-rest-api/v1/certificate/enrollkeystore \
    -H "Authorization: Bearer <token>" \
    -H "Content-Type: application/json" \
    -d '{
        "username": "my-service-001",
        "password": "enrollment-password",
        "include_chain": true,
        "certificate_profile_name": "TLS-Server-90Day",
        "end_entity_profile_name": "Web-Service-Enrollment",
        "certificate_authority_name": "Issuing CA 2025"
    }'

# Search for certificates
curl -X POST https://ejbca.example.com/ejbca/ejbca-rest-api/v1/certificate/search \
    -H "Authorization: Bearer <token>" \
    -d '{
        "max_number_of_results": 100,
        "criteria": [
            {"property": "STATUS", "value": "CERT_ACTIVE", "operation": "EQUAL"},
            {"property": "QUERY", "value": "CN=api.example.com"}
        ]
    }'
```

---

## HSM Integration

```
EJBCA Admin → CA Functions → Crypto Tokens → Create new Crypto Token

Name: Production HSM Token
Token Type: PKCS#11 NG
PKCS#11 Library: /usr/lib/pkcs11/libpkcs11.so  (HSM vendor library)
Slot: 0  (or slot label)
PIN: (HSM partition PIN)

Generate key pair on HSM:
  Alias: RootCAKey2025
  Key Algorithm: RSA 4096 (or EC secp384r1)
  → Keys generated inside HSM, private key never exported
```

Supported HSMs:
- Thales Luna Network HSM (nCipher HSM)
- Utimaco HSM
- AWS CloudHSM (via PKCS#11 library)
- Azure Managed HSM (via PKCS#11)
- SoftHSM2 (software HSM for testing)

---

## Kubernetes Deployment

```bash
# Install EJBCA via Helm
helm repo add keyfactor https://keyfactor.github.io/ejbca-helm-charts
helm install ejbca keyfactor/ejbca \
    --namespace ejbca \
    --create-namespace \
    --set ejbca.image.repository=keyfactor/ejbca-ce \
    --set database.host=postgres.example.com \
    --set database.name=ejbca \
    --set database.user=ejbca \
    --set database.password=ejbca-password

# Or EJBCA Community Docker image
docker run -d \
    -p 8080:8080 -p 8443:8443 \
    -e DATABASE_JDBC_URL=jdbc:mariadb://db:3306/ejbca \
    -e DATABASE_USER=ejbca \
    -e DATABASE_PASSWORD=ejbca \
    keyfactor/ejbca-ce:latest
```

---

## EJBCA in Kubernetes PKI Patterns

EJBCA as a cert-manager external issuer:

```yaml
# Using the EJBCA cert-manager external issuer
# (community project: github.com/Keyfactor/ejbca-cert-manager-issuer)
apiVersion: ejbca-issuer.keyfactor.com/v1alpha1
kind: ClusterIssuer
metadata:
  name: ejbca-cluster-issuer
spec:
  hostname: ejbca.example.com
  ejbcaCredentialsRef:
    name: ejbca-credentials  # Secret with client cert/key for EJBCA auth
  certificateProfileName: TLS-Server-90Day
  endEntityProfileName: Web-Service-Enrollment
  certificateAuthorityName: Issuing CA 2025
```

---

## Compliance Features

- **Common Criteria EAL4+**: Enterprise edition certified; required for government PKI and some financial sector deployments
- **FIPS 140-3**: Via HSM integration; EJBCA itself is cryptographically agnostic (uses HSM for key operations)
- **Audit logging**: All CA operations logged with operator identity, timestamp, and outcome; exportable to SIEM
- **Role separation**: Separate CA Admin, RA Officer, Auditor, and Supervisor roles
- **Dual control**: Require two-person authorization for sensitive CA operations (key generation, revocation of CA)
- **ETSI/eIDAS**: Supports qualified certificate profiles for eIDAS-compliant TSPs

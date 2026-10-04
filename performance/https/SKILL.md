---
name: https
description: HTTPS and TLS security
license: MIT
compatibility: opencode
metadata:
  audience: web-developers
  category: networking
---

## What I do

- Implement HTTPS/TLS for web applications
- Configure SSL/TLS certificates
- Enable HTTP Strict Transport Security (HSTS)
- Set up certificate pinning
- Optimize TLS handshake performance
- Implement modern cipher suites
- Handle mixed content issues

## When to use me

Use me when:
- Securing web application communications
- Configuring web servers for HTTPS
- Implementing certificate management
- Fixing mixed content warnings
- Setting up modern TLS configurations
- Protecting against man-in-the-middle attacks

## Key Concepts

### TLS Handshake Process
```
Client                        Server
  │                              │
  │──── ClientHello ────────────▶│
  │                              │
  │◀─── ServerHello + Cert ──────│
  │◀─── ServerKeyExchange ───────│
  │◀─── CertificateRequest ─────│
  │                              │
  │──── ClientKeyExchange ──────▶│
  │──── CertificateVerify ──────▶│
  │──── ChangeCipherSpec ────────▶│
  │──── Finished ───────────────▶│
  │                              │
  │◀─── ChangeCipherSpec ────────│
  │◀─── Finished ────────────────│
  │                              │
  │════════ Encrypted Data ═════│
```

### Certificate Types
- **DV**: Domain Validation (basic)
- **OV**: Organization Validation
- **EV**: Extended Validation (green bar)
- **Let's Encrypt**: Free, automated DV

### Modern TLS Configuration
```nginx
# Nginx TLS configuration
server {
    listen 443 ssl http2;
    
    ssl_certificate /etc/ssl/certs/server.crt;
    ssl_certificate_key /etc/ssl/private/server.key;
    
    # Modern TLS
    ssl_protocols TLSv1.3;
    ssl_ciphers ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256;
    ssl_prefer_server_ciphers on;
    
    # HSTS
    add_header Strict-Transport-Security "max-age=63072000" always;
    
    # OCSP Stapling
    ssl_stapling on;
    ssl_stapling_verify on;
}
```

### Security Headers
- HSTS: Forces HTTPS connections
- CSP: Content Security Policy
- Certificate Pinning: Prevents MITM

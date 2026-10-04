---
type: skill
name: curl
description: curl command-line HTTP client for making requests, testing APIs, debugging web services, handling authentication, uploading/downloading files, and automating web interactions. Use when interacting with REST APIs.
last_updated: "2026-01-07"
documentation: https://curl.se/docs/manpage.html
---

# curl is a command-line utility for testing and automating web requests with APIs, authentication, and downloading/uploading files with web servers.

# Table of contents 
- [Core Concepts](#core-concepts)
- [Basic Requests](#basic-requests)
- [HTTP Methods](#http-methods)
- [Headers & Authentication](#headers--authentication)
- [Sending Data](#sending-data)
- [File Uploads & Downloads](#file-uploads--downloads)
- [Cookies & Sessions](#cookies--sessions)
- [Debugging & Verbose Output](#debugging--verbose-output)
- [TLS & Certificates](#tls--certificates)
- [Automation & Scripting](#automation--scripting)
- [Common API Workflows](#common-api-workflows)
- [Troubleshooting](#troubleshooting)
- [Best Practices](#best-practices)
- [References](#references)

---

# Core Concepts

| Concept | Description |
|----------|-------------|
| **URL** | Target endpoint |
| **Method** | HTTP verb (GET, POST, PUT, DELETE, PATCH, HEAD, OPTIONS) |
| **Headers** | Metadata sent with request |
| **Body** | Data payload |
| **Status Code** | Server response indicator |
| **Response Headers** | Metadata returned by server |

---

# Basic Requests

## Simple GET Request

```bash
curl https://example.com
```

Follow redirects:

```bash
curl -L https://example.com
```

Save output to file:

```bash
curl -o output.html https://example.com
```

---

# HTTP Methods

## POST

```bash
curl -X POST https://api.example.com
```

## PUT

```bash
curl -X PUT https://api.example.com/resource/1
```

## DELETE

```bash
curl -X DELETE https://api.example.com/resource/1
```

## Custom Method

```bash
curl -X PATCH https://api.example.com/resource/1
```

---

# Headers & Authentication

## Add Headers

```bash
curl -H "Content-Type: application/json" https://api.example.com
```

Multiple headers:

```bash
curl \
  -H "Authorization: Bearer TOKEN" \
  -H "Accept: application/json" \
  https://api.example.com
```

---

## Basic Auth

```bash
curl -u username:password https://example.com
```

---

## Bearer Token

```bash
curl -H "Authorization: Bearer YOUR_TOKEN" https://api.example.com
```

---

## API Key Header

```bash
curl -H "x-api-key: YOUR_API_KEY" https://api.example.com
```

---

# Sending Data

## JSON POST

```bash
curl -X POST https://api.example.com/users \
  -H "Content-Type: application/json" \
  -d '{"name":"John","email":"john@example.com"}'
```

---

## Form Data

```bash
curl -X POST https://example.com/login \
  -d "username=admin&password=pass123"
```

---

## Multipart Form (File Upload)

```bash
curl -F "file=@report.pdf" https://example.com/upload
```

---

# File Uploads & Downloads

## Download File

```bash
curl -O https://example.com/file.zip
```

Custom filename:

```bash
curl -o myfile.zip https://example.com/file.zip
```

---

## Resume Download

```bash
curl -C - -O https://example.com/file.zip
```

---

# Cookies & Sessions

## Send Cookie

```bash
curl -b "sessionid=abc123" https://example.com
```

---

## Store Cookies

```bash
curl -c cookies.txt https://example.com
```

---

## Use Stored Cookies

```bash
curl -b cookies.txt https://example.com/dashboard
```

---

# Debugging & Verbose Output

## Verbose Mode

```bash
curl -v https://example.com
```

## Show Headers Only

```bash
curl -I https://example.com
```

## Include Response Headers in Output

```bash
curl -i https://example.com
```

## Trace Full Request

```bash
curl --trace-ascii debug.txt https://example.com
```

---

# TLS & Certificates

## Ignore Certificate Errors

```bash
curl -k https://example.com
```

## Specify Certificate

```bash
curl --cert client.pem https://secure.example.com
```

## Force TLS Version

```bash
curl --tlsv1.2 https://example.com
```

---

# Automation & Scripting

## Silent Mode

```bash
curl -s https://api.example.com
```

---

## Return Only HTTP Status Code

```bash
curl -s -o /dev/null -w "%{http_code}" https://example.com
```

---

## Timeout

```bash
curl --max-time 10 https://example.com
```

---

## Retry on Failure

```bash
curl --retry 5 https://example.com
```

---

## Pipe to jq (JSON parsing)

```bash
curl -s https://api.example.com/users | jq '.'
```

---

# Common API Workflows

## Auth → Token → Request

```bash
TOKEN=$(curl -s -X POST https://api.example.com/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"pass"}' | jq -r '.token')

curl -H "Authorization: Bearer $TOKEN" https://api.example.com/profile
```

---

## Health Check

```bash
curl -f https://api.example.com/health || echo "Service down"
```

---

## REST Resource Creation

```bash
curl -X POST https://api.example.com/items \
  -H "Content-Type: application/json" \
  -d '{"name":"item1"}'
```

---

# Troubleshooting

## 403 Forbidden

- Missing authentication header
- Invalid API key
- IP blocked

---

## 415 Unsupported Media Type

Ensure:

```bash
-H "Content-Type: application/json"
```

---

## Connection Refused

- Server not running
- Wrong port
- Firewall blocking

---

## SSL Errors

Try:

```bash
curl -k https://example.com
```

Or verify certificate chain.

---

# Best Practices

- Always specify `Content-Type` for JSON
- Use `-s` in automation scripts
- Use `-f` to fail on HTTP errors
- Avoid exposing tokens in shell history
- Store secrets in environment variables
- Combine with `jq` for structured parsing
- Log response codes in automation workflows

---

# Safe Usage

- Do not send credentials over HTTP (use HTTPS)
- Avoid logging sensitive headers
- Protect API tokens
- Validate responses before processing in automation

---

# AWS Integration

## Feedback Loop Integration

curl is used to run external probes — with no AWS credentials — directly against AWS endpoints. Under the External Probe path, curl results bypass the pipeline and return directly. While AWS CLI checks verify *configuration*, curl verifies *actual reachability* from outside the account.

Probe commands per service are in `skills/validation-rules/probes.md`. Service-specific endpoint discovery is in each service skill (e.g., `skills/s3/SKILL.md`, `skills/rds/SKILL.md`).

### Common AWS Validation Requests

Verify S3 bucket is publicly accessible:

```bash
curl -s -o /dev/null -w "%{http_code}" https://s3.amazonaws.com/BUCKET_NAME
```

Check if an ALB/CloudFront endpoint enforces HTTPS redirect:

```bash
curl -s -o /dev/null -w "%{http_code}" -L http://ENDPOINT
```

Test EC2 metadata endpoint (from within an instance):

```bash
curl -s -H "X-aws-ec2-metadata-token-ttl-seconds: 21600" -X PUT http://169.254.169.254/latest/api/token
```

Verify API Gateway returns 403 without auth:

```bash
curl -s -o /dev/null -w "%{http_code}" https://API_ID.execute-api.REGION.amazonaws.com/STAGE/
```

Check if a public RDS/ElastiCache endpoint responds (should timeout if properly secured):

```bash
curl -s --max-time 5 -o /dev/null -w "%{http_code}" http://ENDPOINT:PORT || echo "Connection refused/timed out"
```

For Critic scoring of curl probe results, see the Scoring Rubric and Service exceptions in `agents/roles.md`.

---

# References

- https://curl.se/docs/
- https://curl.se/docs/manpage.html
- https://everything.curl.dev/

---

# End of Skill
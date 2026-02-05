---
name: "IP Geolocation"
description: "Geolocate IP addresses and analyze network information"
allowed-tools:
  - src.tools.ip_geolocation
---

# IP Geolocation

## Purpose

Determine geographic location, ISP information, and network details for IP addresses to support fraud investigation, security analysis, and compliance screening.

## When to Use

- Fraud detection and prevention analysis
- Investigation of suspicious login activities
- Geolocation verification for compliance purposes
- Cybersecurity incident response and threat analysis
- Network traffic analysis and attribution
- Verification of claimed business locations
- Investigation of VPN and proxy usage
- Risk assessment for online transactions

## How to Use

The IP geolocation tool provides comprehensive network intelligence:

- **Geographic Location**: Country, region, city, latitude/longitude coordinates
- **ISP Information**: Internet service provider, organization, network name
- **Network Details**: ASN (Autonomous System Number), IP range, routing info
- **Connection Type**: Residential, business, mobile, hosting, VPN/proxy
- **Risk Assessment**: Known malicious IPs, proxy detection, anonymization services
- **Timezone**: Local timezone for the IP location

## Examples

**Fraud investigation:**
```
Login IP: 203.0.113.45 from claimed US user
Analysis: IP resolves to Eastern Europe, known VPN service
Red flags: Geographic mismatch, anonymization service usage
Assessment: High fraud risk - investigate account compromise
```

**Transaction verification:**
```
Purchase IP: 198.51.100.10 for international wire transfer
Location: New York City, business ISP, matches claimed location
Network: Legitimate financial district business connection
Assessment: Low risk - geographic consistency with transaction
```

**Cybersecurity incident:**
```
Attack IP: 192.0.2.150 in security breach
Investigation: Hosting provider in country with weak cybercrime laws
Network: Known bulletproof hosting service, high-risk ASN
Intelligence: Add to threat indicators for blocking
```

**Compliance screening:**
```
User IP: 172.16.254.1 accessing regulated service
Location: Sanctioned country, government ISP
Compliance: Block access due to sanctions restrictions
Documentation: Record for regulatory compliance audit
```

## Important Notes

- IP geolocation accuracy varies (city-level ~70-80% accurate)
- VPN and proxy services can mask true user location
- Mobile IPs may show carrier headquarters rather than user location
- Consider timezone correlation with claimed user location
- Some ISPs use dynamic IP allocation affecting accuracy
- Corporate networks may route through different geographic locations
- IPv6 adoption may affect traditional geolocation methods
- Cross-reference IP data with other geographic indicators
- Be aware of privacy implications when collecting IP intelligence
---
name: cert-manager
description: >
  cert-manager TLS certificate management: internal CA for cluster.home,
  ClusterIssuer, Certificate resources, Gateway API TLS integration, and
  macOS Keychain trust. No Let's Encrypt — internal CA only.
license: MIT
compatibility:
  - opencode
metadata:
  author: dotfiles
  tags: [kubernetes, cert-manager, tls, certificates, pki, gateway-api]
---

# cert-manager Skill

## Cluster Context

cert-manager manages TLS certificates for the `cluster.home` internal domain.
Since `cluster.home` is a private/invented domain, Let's Encrypt cannot be used
(no public DNS validation). Strategy: **internal CA signed by cert-manager**.

Helm release: `cert-manager` in namespace `cert-manager`
Chart version pinned in: `roles/install-cert-manager/defaults/main.yml`

Domain: `cluster.home`
CA Secret: `cluster-home-ca` in namespace `cert-manager`
ClusterIssuer: `cluster-home-ca-issuer`

---

## How It Works

```
Ansible (community.crypto)
  → generates CA keypair (once, stored in infra repo as encrypted vault)
  → creates Secret cluster-home-ca in cert-manager namespace

cert-manager ClusterIssuer (type: CA)
  → references Secret cluster-home-ca
  → signs Certificate resources for *.cluster.home

Gateway listener (port 443)
  → references Secret produced by Certificate resource
  → terminates TLS for all HTTPRoutes

macOS Keychain (via Ansible shell role)
  → trusts the CA cert → browsers accept *.cluster.home without warnings
```

---

## CA Generation (Ansible)

The CA is generated once by Ansible using `community.crypto.x509_certificate`
and stored as a Kubernetes Secret. It is NOT regenerated on re-runs (idempotent).

```yaml
# roles/install-cert-manager/tasks/main.yml (excerpt)
- name: Generate CA private key
  community.crypto.openssl_privatekey:
    path: /tmp/cluster-home-ca.key
    size: 4096

- name: Generate CA certificate (self-signed root)
  community.crypto.x509_certificate:
    path: /tmp/cluster-home-ca.crt
    privatekey_path: /tmp/cluster-home-ca.key
    provider: selfsigned
    selfsigned_not_after: "+3650d"   # 10 years
    subject:
      CN: "cluster.home CA"

- name: Create CA secret in cert-manager namespace
  kubernetes.core.k8s:
    state: present
    definition:
      apiVersion: v1
      kind: Secret
      metadata:
        name: cluster-home-ca
        namespace: cert-manager
      data:
        tls.crt: "{{ ca_cert_b64 }}"
        tls.key: "{{ ca_key_b64 }}"
      type: kubernetes.io/tls
```

---

## ClusterIssuer

```yaml
apiVersion: cert-manager.io/v1
kind: ClusterIssuer
metadata:
  name: cluster-home-ca-issuer
spec:
  ca:
    secretName: cluster-home-ca
```

---

## Certificate for Gateway TLS

cert-manager issues a wildcard cert for the Gateway's HTTPS listener:

```yaml
apiVersion: cert-manager.io/v1
kind: Certificate
metadata:
  name: cluster-home-wildcard
  namespace: infra-gateway         # must be same namespace as Gateway
spec:
  secretName: cluster-home-wildcard-tls
  issuerRef:
    name: cluster-home-ca-issuer
    kind: ClusterIssuer
  dnsNames:
    - "*.cluster.home"
    - "cluster.home"
```

The `Gateway` listener references `cluster-home-wildcard-tls` for HTTPS.

---

## macOS Keychain Trust (Ansible)

The CA cert is exported and trusted on the Mac so browsers accept `*.cluster.home`
without security warnings. This is applied by the `shell` role (macOS only):

```bash
# What Ansible runs (once):
sudo security add-trusted-cert -d -r trustRoot \
  -k /Library/Keychains/System.keychain /tmp/cluster-home-ca.crt
```

After this, Chrome/Safari/curl all trust `*.cluster.home` certificates automatically.
No per-certificate action needed — trust the CA once, all future certs are accepted.

---

## Integration with Cilium Ingress Controller

Once cert-manager is deployed, flip in `roles/install-cilium/defaults/main.yml`:

```yaml
cilium_ingress_enforce_https: true   # was false during initial setup
```

This enables HTTP → HTTPS redirect (308) for Ingress resources with TLS configured.

---

## BackendTLSPolicy — NOT supported by Cilium

`BackendTLSPolicy` (mTLS between Gateway and backend Service) is in the ArgoCD
Helm chart as an option but **Cilium does not support it yet**. Do not enable it.
TLS terminates at the Gateway; backends receive plain HTTP internally.

---

## Upgrade Procedure

1. Update `cert_manager_version` in `roles/install-cert-manager/defaults/main.yml`
2. Check release notes: https://github.com/cert-manager/cert-manager/releases
3. Re-run:
   ```bash
   ansible-playbook playbooks/bootstrap.yml -i inventory/hosts.ini \
     --start-at-task "Add cert-manager Helm repository"
   ```
4. Verify: `kubectl get pods -n cert-manager`

---

## Health Checks

```bash
# All cert-manager pods
kubectl get pods -n cert-manager

# ClusterIssuer status
kubectl get clusterissuer cluster-home-ca-issuer -o yaml

# All certificates and their status
kubectl get certificate -A

# Certificate details (check Ready=True)
kubectl describe certificate cluster-home-wildcard -n infra-gateway

# Check cert-manager controller logs
kubectl logs -n cert-manager -l app=cert-manager --tail=50
```

---

## Troubleshooting

### Certificate stuck `Ready: False`
```bash
kubectl describe certificate <name> -n <namespace>
kubectl describe certificaterequest -n <namespace>
kubectl describe order -n <namespace>    # for ACME (not used here)
kubectl logs -n cert-manager -l app=cert-manager --tail=100
```
Common causes:
- ClusterIssuer CA Secret missing or wrong key/cert format
- Certificate namespace doesn't match Gateway namespace
- cert-manager webhook not yet ready after fresh install

### cert-manager webhook not ready (fresh install)
```bash
# Wait for webhook deployment
kubectl rollout status deploy/cert-manager-webhook -n cert-manager
```
The `install-cert-manager` role includes an explicit wait task.

### CA cert not trusted in browser
- Verify Ansible ran the `security add-trusted-cert` task (shell role, macOS)
- Check Keychain: `security find-certificate -c "cluster.home CA" -p`
- Restart browser after adding CA to Keychain

### Renewing the CA (after 10 years or if compromised)
1. Delete Secret `cluster-home-ca` in `cert-manager` namespace
2. Re-run bootstrap — Ansible regenerates the CA
3. Re-run shell role on Mac to update Keychain trust
4. All Certificates are automatically reissued by cert-manager

---

## Useful Commands

```bash
# List all CertificateRequests
kubectl get certificaterequest -A

# Force certificate renewal
kubectl annotate certificate <name> -n <namespace> \
  cert-manager.io/issue-temporary-certificate=true --overwrite

# Inspect issued certificate
kubectl get secret <secret-name> -n <namespace> -o jsonpath='{.data.tls\.crt}' \
  | base64 -d | openssl x509 -text -noout

# Helm values
helm get values cert-manager -n cert-manager
```

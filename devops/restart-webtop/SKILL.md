---
name: restart-webtop
description: 設定、重啟並驗證 Webtop AMD 的 host backend、Docker frontend 與 Tailscale Serve sidecar。當使用者說「重啟 webtop」、「restart webtop」、Webtop 網頁或 API 無法開啟、GPU/程序資料停止更新、Docker/Tailscale 失效，或輸入 /restart-webtop 時使用。包含首次環境設定、Tailscale 授權、正確重建順序與完整健康檢查。
license: MIT
metadata:
  hermes:
    tags: [webtop, amdgpu, docker, tailscale, restart, systemd, monitoring]
---

# Restart Webtop AMD

## 直接重啟

```bash
bash ~/.pi/agent/skills/restart-webtop/scripts/restart.sh
```

腳本會先跑測試、typecheck 與 production build，再重啟 host backend，依正確順序重建 Docker frontend 與 Tailscale sidecar，最後驗證本機 API、容器健康、Tailscale Serve 與 tailnet HTTPS。成功前不得只憑 `docker ps` 判定完成。

可選環境覆寫：

```bash
WEBTOP_PROJECT_DIR=/home/chihmin/src/webtop-amd \
WEBTOP_ENV_FILE=/home/chihmin/.config/webtop-amd/env \
WEBTOP_FQDN=webtop-amd.crayfish-monitor.ts.net \
bash ~/.pi/agent/skills/restart-webtop/scripts/restart.sh
```

## Live architecture

| 元件 | 角色 | 管理方式 |
|---|---|---|
| `webtop-amd.service` | 直接讀 host `/proc`、執行 `amdgpu_top`、管理程序的 Node API (`127.0.0.1:8787`) | systemd user service |
| `webtop-amd-frontend` | Nginx + React UI；本機 `8788:80`，將 `/api` proxy 到 host backend | Docker Compose `frontend` |
| `webtop-amd-ts` | 私有 HTTPS 與 MagicDNS 節點 `webtop-amd` | Docker Compose `tailscale` |

專案位於 `/home/chihmin/src/webtop-amd`。Tailscale sidecar 使用 `network_mode: service:frontend`，Serve 將 `https://webtop-amd.crayfish-monitor.ts.net` proxy 到同一 network namespace 的 `http://127.0.0.1:80`。目前啟用公開 Funnel；整個 dashboard 以密碼登入保護，登入後使用簽章 HttpOnly cookie。

## 首次環境設定

### 1. 系統需求

確認 Linux host 已有：

```bash
node --version          # Node.js 22+
docker compose version
amdgpu_top --version
command -v taskset jq curl openssl
```

Backend 必須直接跑在 host，不可搬入 Docker；否則看不到正確的 host `/proc`，也無法依 Unix 權限執行 signal、renice 與 CPU affinity。

### 2. 安裝與建置

```bash
cd /home/chihmin/src/webtop-amd
npm ci
npm test
npm run typecheck
npm run build
```

### 3. Backend 環境

正式環境檔是 `~/.config/webtop-amd/env`，權限必須為 `600`：

```bash
mkdir -p ~/.config/webtop-amd
SECRET="$(openssl rand -hex 32)"
printf 'WEBTOP_PASSWORD=2169\nWEBTOP_SESSION_SECRET=%s\nWEBTOP_HOST=0.0.0.0\nWEBTOP_PORT=8787\n' "$SECRET" \
  > ~/.config/webtop-amd/env
chmod 600 ~/.config/webtop-amd/env
```

- `WEBTOP_PASSWORD=2169` 是 dashboard 登入密碼。
- `WEBTOP_SESSION_SECRET` 簽署 30 天 HttpOnly session cookie，不可提交到 Git。
- `WEBTOP_HOST=0.0.0.0` 讓 Docker Nginx 可透過 `host.docker.internal:8787` 存取。
- `WEBTOP_PORT=8787` 必須與 Nginx upstream 和健康檢查一致。

### 4. 安裝 host systemd service

```bash
mkdir -p ~/.config/systemd/user
cp /home/chihmin/src/webtop-amd/deploy/webtop-amd.service ~/.config/systemd/user/
systemctl --user daemon-reload
systemctl --user enable --now webtop-amd.service
```

若登出後仍需服務常駐，可由具權限的管理者執行：

```bash
loginctl enable-linger chihmin
```

### 5. Docker 與首次 Tailscale 授權

```bash
cd /home/chihmin/src/webtop-amd
TS_AUTHKEY=tskey-auth-... docker compose up -d --build
```

`TS_AUTHKEY` 僅首次註冊需要；授權後 identity 持久化於 `tailscale/state/`，不要把 key 寫入版控。也可不用 key，從 `docker compose logs tailscale` 開啟登入網址。

注意：官方 `containerboot` 的互動式 `tailscale up` 約有 **60 秒** timeout。若瀏覽器授權來不及，容器會重啟並產生新 URL，舊 URL 失效。最可靠方式是一次性 `TS_AUTHKEY`；或暫時直接啟動 `tailscaled` 完成授權後再切回 Compose。不要複製其他服務的 Tailscale state，否則會造成重複 node identity。

## 正確重啟順序

1. 驗證工具與 `~/.config/webtop-amd/env`。
2. `npm test`、typecheck、build。
3. 更新 user unit，daemon-reload，restart `webtop-amd.service`。
4. `docker compose up -d --build --force-recreate frontend`。
5. **之後** `docker compose up -d --force-recreate tailscale`。
6. 驗證 backend、frontend、Tailscale state、Serve proxy、HTTPS API；若設定啟用 Funnel，再透過 public DNS 固定 ingress IP 驗證真正的公開路徑。

順序不能交換。因為 sidecar 綁定 frontend 的 network namespace；frontend 被 recreate 後，舊 sidecar 可能仍停在 **stale network namespace**。此時兩個容器看似都 running，但 HTTPS 會 502。單純 `docker restart webtop-amd-ts` 不足以修復，必須在 frontend 之後 force-recreate sidecar。

## 驗證與診斷

```bash
systemctl --user status webtop-amd.service
a=$(curl -fsS http://127.0.0.1:8787/api/health); echo "$a"
docker compose -f /home/chihmin/src/webtop-amd/compose.yaml ps
docker exec webtop-amd-ts tailscale status
docker exec webtop-amd-ts tailscale serve status
docker exec webtop-amd-ts wget -qO- http://127.0.0.1/healthz
curl -fsS https://webtop-amd.crayfish-monitor.ts.net/api/health
```

查看日誌：

```bash
journalctl --user -u webtop-amd.service -n 100 --no-pager
docker compose -f /home/chihmin/src/webtop-amd/compose.yaml logs --tail=100 frontend tailscale
```

常見問題：

- Backend 無 GPU：確認 systemd user 的 `PATH` 找得到 `amdgpu_top`，並檢查 `/dev/dri` 權限。
- 程序擁有者變成 `nobody`：不可加入會建立 mount/user namespace 的 systemd hardening；會扭曲其他 UID 的 `/proc` 資訊。
- Fastify 顯示 interface error：unit 的 `RestrictAddressFamilies` 必須保留 `AF_NETLINK`。
- HTTPS 502、local 8788 正常：優先重建 Tailscale sidecar，檢查 stale network namespace。
- Tailscale `NeedsLogin`：state 未授權或失效，重新完成首次授權，不要刪除仍有效的 state 當作例行修復。
- 公開 Funnel 只公開登入頁；telemetry、process details 與 signal、renice、affinity 都必須先以 `WEBTOP_PASSWORD` 登入取得 session cookie。普通 `curl` 在 tailnet host 上會走 MagicDNS `100.x`，不能證明 Funnel 正常；需用 `dig @1.1.1.1` 搭配 `curl --resolve` 驗證 public ingress。

## Skill 自我測試

```bash
bash ~/.pi/agent/skills/restart-webtop/tests/run-tests.sh
```

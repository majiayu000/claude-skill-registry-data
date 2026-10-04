---
name: pre-deploy-validator
description: Use ANTES de qualquer deploy em produção. Roda checklist de 23 validações baseadas em falhas reais detectadas em projetos anteriores (CRM_OS, Valesa, etc). Detecta env vars hardcoded errado, CSP/CORS misconfig, JWT claims mismatch, migrations slot conflict, rotas Hono não montadas, RBAC lazy, mocks em prod, e mais. Invocável com `/pre-deploy-check` ou automaticamente quando o usuário menciona deploy/release.
---

# Pre-Deploy Validator

Checklist de validações que DEVE rodar antes de qualquer `gcloud run deploy`, `terraform apply` em prod, ou tag de release. Baseada em falhas reais.

## Quando invocar

- Antes de `docker buildx build --push` pra image de prod
- Antes de `gcloud run deploy` pra service em prod
- Antes de tagear release (v1.0.0+)
- Quando user fala "deploy", "subir em prod", "release"

## Checklist (23 items)

### 🔴 P0 — Bloqueia deploy

**1. Env vars Vite no build apontam pro DOMÍNIO PÚBLICO, não run.app interno**

```bash
# ANTES de docker buildx, confirmar:
echo "VITE_SERVER_URL=https://meudominio.com"  # NÃO https://servico-xxxx.run.app
echo "VITE_AUTH_URL=https://meudominio.com"
```

Por quê: CSP `connect-src 'self'` bloqueia chamadas pro run.app. Browser entra em retry infinito → `ERR_INSUFFICIENT_RESOURCES`.

**2. CSP `connect-src` inclui o domínio do backend**

Inspecionar `apps/web/nginx.conf` ou middleware CSP:
```
connect-src 'self' https://meudominio.com
```

**3. CSP nonce placeholder substituído ou removido**

```bash
grep -rn "%%CSP_NONCE%%" apps/web/dist apps/web/index.html
# Deve retornar 0 matches (ou remover o placeholder)
```

**4. Migrations slot livre (sem colisão entre PRs)**

```bash
# Confirmar próximo slot:
ls packages/db/migrations/*.sql | tail -3
# Pegar último N, usar N+1 na nova migration
# Verificar _journal.json sincronizado com files
```

**5. Rotas Hono novas estão MONTADAS em index.ts**

```bash
# Pra cada novo arquivo em apps/server/src/routes/, confirmar:
grep "novoArquivo" apps/server/src/index.ts
# Se não tem, é 404 silencioso em prod
```

**6. Paths internos não duplicam o segmento do mount**

```ts
// BUG: router.get('/deals/:id') montado em app.route('/api/deals') = /api/deals/deals/:id
// CORRETO: router.get('/:id') montado em app.route('/api/deals') = /api/deals/:id
```

Comando de verificação:
```bash
for f in apps/server/src/routes/*.ts; do
  recurso=$(basename $f .ts | sed 's/-.*//')
  grep -q "router\.\(get\|post\|patch\|delete\)('/$recurso" "$f" && echo "BUG: $f duplica /$recurso"
done
```

**7. Cloud Run traffic apontado pra LATEST após deploy**

```bash
gcloud run services update-traffic <service> --to-latest --region=<region> --project=<project>
# Sem isso, deploy cria rev nova mas tráfego fica na anterior
```

### 🟡 P1 — Investigar antes

**8. JWT claims que código backend espera estão sendo emitidos**

```ts
// Decodar JWT real do user e verificar claims:
const decoded = jwt.decode(token);
// Se backend espera org_id mas JWT só tem app_metadata.org_id, ou vice-versa,
// é bug. GoTrue auto-hospedado precisa Custom Access Token Hook pra injetar claims.
```

**9. RBAC Guard é SÍNCRONO (não lazy/toast-then-redirect)**

```tsx
// BUG: renderiza componente, dispara toast, redireciona depois → flash conteúdo sensível
// CORRETO: redirect imediato ANTES de render
if (role && !allow.includes(role)) return <Navigate to="/dashboard" replace />;
if (!role) return <Skeleton />;  // loading
```

**10. Mocks/placeholders foram removidos**

```bash
grep -rn "MOCK_\|FAKE_\|hardcoded\|TODO.*mock\|Ana Lima\|Carlos Mendes\|R\$ 297" apps/web/src
# Esperado: zero matches em prod
```

**11. Rate limit é DISTRIBUÍDO (Redis), não in-memory**

```bash
grep -rn "new Map()" apps/server/src/middleware/rate-limit*
# Se aparecer Map(), não escala entre instâncias Cloud Run
```

**12. Dev secrets com `fail-fast` em produção**

```ts
// BUG: process.env['SECRET'] ?? 'dev-fallback-min-32-chars'
// CORRETO:
function requireEnv(name: string): string {
  const v = process.env[name];
  if (!v && process.env['NODE_ENV'] === 'production') {
    throw new Error(`Missing required env var: ${name}`);
  }
  return v || `dev-fallback-${name.toLowerCase()}`;
}
```

**13. CORS allowlist explícita, sem `*` com credentials**

Backend Hono `cors()`:
```ts
cors({ origin: ['https://meudominio.com'], credentials: true })
```

**14. Security headers HSTS+CSP+XFO+nosniff+Referrer**

```bash
curl -sI https://meudominio.com/ | grep -iE "strict-transport|x-frame|content-security|x-content|referrer"
# Esperado: 5 headers presentes
```

**15. PostgREST/serviços internos NÃO expostos publicamente**

Verificar URL Map / Cloud Armor — `/rest/v1/*` deve estar bloqueado ou autenticado.

### ⚪ P2 — Polish

**16. Frontmatter `status: implemented` tem código real**

```bash
# Pra spec com status: implemented, grep palavras-chave do nome:
grep -rn "<slug-keyword>" apps/server/src apps/web/src packages/
# Se zero matches, frontmatter mente
```

**17. Worktrees git órfãos limpados**

```bash
git worktree list | grep -v "$(pwd)"
du -sh ../proj-*  # Cada worktree ~500MB
```

**18. Branches mergeadas deletadas**

```bash
gh pr list --state merged --limit 50 --json headRefName -q '.[].headRefName' | while read b; do
  gh api repos/OWNER/REPO/branches/$b >/dev/null 2>&1 && echo "$b ainda existe"
done
```

**19. PostgREST schema cache atualizado após mudança DB**

```sql
NOTIFY pgrst, 'reload schema';
-- OU redeploy do service postgrest
```

**20. Maestri agents não ficam idle aguardando "GO"**

Briefings devem ter "GO autoridade total modo overnight, decide+implementa+valida". Caso contrário agent fica esperando confirmação.

**21. Smoke E2E REAL via browser (não só curl)**

Playwright headless executa o JS bundle. Curl só testa HTTP path — pode dar false positive enquanto bundle JS crasha em runtime.

**22. Cloud SQL Private IP + VPC Connector (não 0.0.0.0/0)**

```bash
gcloud sql instances describe <inst> --format='value(ipAddresses[].type)'
# Esperado: ['PRIVATE'] (sem PUBLIC/PRIMARY)
```

**23. Backup automatizado configurado**

Cloud SQL → automated backups daily + PITR ≥7d.

## Output

Reporta cada item ✅ ou ❌, com fix sugerido pra cada ❌. Se algum P0 falha, **BLOQUEAR DEPLOY**.

## Lições adicionais

- **Validar build args ANTES do push**: rodar `docker run --rm <image> grep -r "run.app" /usr/share/nginx/html` pra detectar URL interna vazada
- **CDN/LB cache**: após deploy, fazer hard refresh + cache_bust query string pra validar bundle novo
- **`--to-latest` é obrigatório**: Cloud Run não promove tráfego automaticamente, mesmo com `--platform=managed`
- **`gh pr merge` sem `--delete-branch`**: deixa branches acumulando — sempre usar
- **Múltiplos PRs paralelos com mesma migration slot**: precisam rebasear sequencialmente, não simultâneo
- **Buildx cache do runner stage:** quando `Dockerfile` é multi-stage (`builder` + `runner`), `buildx` com driver `docker-container` **cacheia o runner stage** mesmo quando o builder produz dist nova com hash de conteúdo igual. Bundle antigo pode ser servido apesar de `--no-cache` no buildx. **Mitigação obrigatória:** adicionar `ARG CACHEBUST=1` no Dockerfile antes do `COPY --from=builder ...`, e passar `--build-arg CACHEBUST=$(date +%s)` em TODO build de prod. Sem isso, prod pode servir bundle com env vars ou código de PRs anteriores. (Descoberto em CRM_OS web:v23 — bundle antigo persistiu mesmo após PR mergeado com fix.)
- **Cloud Armor URL Map removal NÃO basta:** se o path matcher é apenas removido do URL Map, o tráfego cai no `defaultService` (frontend SPA). Pra bloqueio explícito 403, adicionar regra Cloud Armor `deny-403` no path. Defense in depth.
- **PoC de security audit pode deixar resíduo no DB:** agents de pentest fazem INSERT/UPDATE pra provar exploit. Sempre exigir que o agent REVERTA cada mudança ao final + logue PoC com timestamp pra cleanup posterior.
- **State de auth descentralizado = dessincronia visual:** se múltiplos hooks consomem `session` por caminhos diferentes (auth-context vs cache singleton vs localStorage direto), eles ficam dessincronizados no primeiro render. Sintoma típico: sidebar mostra org/user, dashboard mostra "Selecione organização". Regra: **único source of truth via auth-context React; todos os hooks DERIVAM dele**. Cache singleton em módulo só serve pra memoização secundária após session estabilizada, nunca como primeiro source.
- **Cloud Armor rule com expression vazio bloqueia TUDO:** ao criar rule via `gcloud compute security-policies rules create` se o flag `--expression` for omitido ou aceito vazio, a rule fica `match: { expr: { expression: '' }}` que matcha tudo. Validar SEMPRE após criar: `gcloud compute security-policies rules describe <priority> --format='value(match.expr.expression)'` — não pode estar vazio.
- **`??` não trata string vazia como falsy:** `const X = import.meta.env.VITE_FOO ?? 'fallback'` falha quando Vite injeta `''` (de `--build-arg VITE_FOO=` sem valor). `??` só faz fallback em null/undefined. Use `(env as string \| undefined)?.trim() \|\| 'fallback'`. Validar bundle pós-build: `curl bundle.js \| grep -oE 'https://[^"]*'` deve listar URLs absolutas esperadas. Bug encontrado em CRM_OS web:v29 (login quebrado) — fix em PR #116.
- **Fix de Zod schema sem atualizar consumers do parsed value:** ao trocar tipo de validação (ex: `z.string().date()` → `z.string().datetime()`), buscar TODOS os call sites que consomem o valor parseado — formato muda. Em CRM_OS PR #117 corrigiu schema de `/api/admin/audit-log` de `date` (YYYY-MM-DD) pra `datetime` (ISO completo), mas `buildFilters()` continuou fazendo `new Date(\`\${from}T00:00:00.000Z\`)` (concatenava sufixo presumindo formato date) — virou `Date(NaN)`, drizzle quebrava com RangeError, endpoint passou de 400 pra 500. Fix completo em PR #118. **Regra:** após mudar schema, `grep` o nome do campo no arquivo todo + buscar consumers que assumem formato antigo. Pre-deploy: rodar a request real com payload do frontend antes de declarar pronto.

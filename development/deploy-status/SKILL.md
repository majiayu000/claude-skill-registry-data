---
name: deploy-status
description: Confere se o frontend e o backend em produção estão de pé e se comunicando direito (Cloud Run, Cloudflare Pages, Neon) e mostra a última execução do workflow de deploy. Use quando pedirem "confere o deploy", "o site está no ar?", "por que o /ocr não está funcionando" ou antes de investigar um problema em produção.
---

# deploy-status

Verificação rápida do ambiente de produção deste projeto — ver a seção "Deploy (produção)" do
`CLAUDE.md` da raiz para as URLs e a arquitetura completa. Não altera nada, só lê.

## Passo a passo

1. **Última execução do deploy**:

   ```bash
   gh run list --workflow=deploy.yml --limit 3
   ```

   Se o mais recente estiver `failure`, veja qual job falhou:

   ```bash
   gh run view --log-failed <run-id>
   ```

2. **Backend (Cloud Run)** — saúde e banco:

   ```bash
   curl -s -o /dev/null -w "%{http_code}\n" https://ocr-placas-backend-6yjkqvbuoq-rj.a.run.app/health
   curl -s https://ocr-placas-backend-6yjkqvbuoq-rj.a.run.app/health/db
   ```

   Both devem responder `200`. Se vier `403 Forbidden`, é o acesso público que caiu — veja
   "Armadilhas já resolvidas" no `CLAUDE.md` (política `iam.allowedPolicyMemberDomains`) antes
   de supor que é bug no código.

3. **Frontend (Cloudflare Pages)** — no ar e apontando pro backend certo:

   ```bash
   curl -s -o /dev/null -w "%{http_code}\n" https://ocr-placas.pages.dev
   JS_FILE=$(curl -s https://ocr-placas.pages.dev/ | grep -oE '/assets/index-[^"]+\.js' | head -1)
   curl -s "https://ocr-placas.pages.dev$JS_FILE" | grep -o "ocr-placas-backend-[a-zA-Z0-9.-]*" | head -1
   ```

   Se o segundo comando não retornar nada, o build do frontend não embutiu a URL do backend
   (veja a armadilha do `VITE_API_BASE` no `CLAUDE.md`) — o site carrega, mas o upload de placa
   não funciona.

4. **Ponta a ponta de verdade** (opcional, quando os passos acima não explicam o problema):
   simula uma requisição real com a origem do frontend, provando CORS + OCR juntos:

   ```bash
   curl -s -D - -X POST https://ocr-placas-backend-6yjkqvbuoq-rj.a.run.app/ocr/upload \
     -H "Origin: https://ocr-placas.pages.dev" \
     -F "file=@caminho/para/uma-imagem.png;type=image/png"
   ```

   Espera `200` com `access-control-allow-origin: https://ocr-placas.pages.dev` no header.

5. **Reportar**: resume pro usuário o que está no ar, o que não está, e — se achar a causa —
   aponta pra seção correspondente do `CLAUDE.md` ou sugere rodar `/redeploy`.

## O que não fazer

- Não mexer em IAM, política de organização ou secrets a partir daqui — isso é o skill
  `/redeploy` (ou intervenção manual), não este, que é só leitura/diagnóstico.

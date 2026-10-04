---
name: redeploy
description: Dispara manualmente o deploy de produção (Cloud Run + Cloudflare Pages) sem precisar de um commit novo, e acompanha até o fim. Use quando pedirem "redeploy", "sobe de novo", "só trocou um secret, precisa publicar de novo" ou depois de corrigir um secret/config que não muda código.
---

# redeploy

O `.github/workflows/deploy.yml` normalmente só dispara sozinho depois que o CI passa num push
na `main` (ver "Deploy (produção)" no `CLAUDE.md`). Este skill usa o gatilho manual
(`workflow_dispatch`) já configurado nele, para os casos em que nada mudou no código — só um
secret, uma variável de ambiente ou uma config na nuvem — mas é preciso publicar de novo.

## Pré-condições

- Não use isto para publicar uma mudança de código ainda não mergeada — isso é o fluxo normal
  (`/prepare-pr`, PR, merge). Este skill é só para re-rodar o deploy do estado atual da `main`.
- `gh` autenticado com acesso de escrita ao repositório (`gh auth status`).

## Passo a passo

1. **Dispara o workflow**:

   ```bash
   gh workflow run deploy.yml
   ```

2. **Acompanha até terminar** (pode levar alguns minutos, o backend builda e sobe uma imagem
   de ~2 GB):

   ```bash
   sleep 15
   gh run list --workflow=deploy.yml --limit 1
   ```

   Repete o `gh run list` a cada 30-60s até o status virar `completed`. Se preferir, use
   `gh run watch <run-id>` para acompanhar ao vivo.

3. **Se falhar**, rode `gh run view --log-failed <run-id>` e trate a causa — não insista em
   disparar de novo sem entender o que quebrou. Erros de permissão (IAM, política de
   organização) não se resolvem re-rodando; veja "Armadilhas já resolvidas" no `CLAUDE.md`.

4. **Depois que passar**, confirme que os dois lados subiram de verdade com o skill
   `/deploy-status` — um workflow verde não garante que o site está funcionando de ponta a
   ponta (ex: o bug do `VITE_API_BASE` passou no CI e no deploy, e mesmo assim quebrava a
   chamada real da API).

## O que não fazer

- Não use este skill para contornar o CI (ex: código que falhou no `/prepare-pr`) — ele só
  redisponibiliza o que já está na `main`, não pula nenhum teste.
- Se o problema for de infraestrutura (IAM, política de organização, secret errado), corrija a
  causa antes de re-rodar; disparar de novo sem corrigir só repete a mesma falha.

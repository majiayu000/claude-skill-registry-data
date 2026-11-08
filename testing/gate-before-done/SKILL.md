---
name: gate-before-done
description: >
  Run the repository gate and read its real output before claiming any work is
  done, fixed, or passing. Use before saying "pronto", before committing, before
  opening a PR, and whenever a check goes red and you need to classify the
  failure instead of guessing.
---

# gate-before-done

"Verifiquei" é um comando, não uma impressão.

```sh
npx pnpm@11.18.0 gate          # lint -> typecheck -> test -> secrets; para no primeiro vermelho
npx pnpm@11.18.0 gate --fast   # lint + typecheck; loop de edição
```

`pnpm` não está no PATH da máquina de dev — sempre `npx pnpm@11.18.0`.

## Três regras

1. **`--fast` não autoriza declarar pronto.** Ele não roda teste nenhum.
2. **Leia a saída.** "Deve estar passando" não é evidência; a saída lida é.
3. **Exit 0 ou não passou.** Não existe amarelo.

## Vermelho: classifique antes de consertar

Antes de atribuir a falha ao seu diff, confirme que ela reproduz num estado limpo.
Três armadilhas conhecidas deste repo se parecem exatamente com regressão real:

- **Perfil fantasma "Visual Capture"** — dev server ou captura visual entre `db:reset` e
  `test:db` quebra seis asserts de pgTAP (`locality-profile-access`, `authz-*-matrix`,
  `full-regression`). `.visual/` é gitignored, então grep no repo não acha nada.
  **Correção:** `db:reset` de novo, sem dev server e sem captura, depois `test:db`.
- **`dev-server.pid` / `dev-server.log` velhos** — apague e tente de novo.
- **Docker parado** — comando Supabase exige `supabase start` antes.

Classifique toda falha como: **causada pelo meu diff / pré-existente / armadilha conhecida**.
Consertar o que não está quebrado é o modo de falha mais caro de um agente autônomo.

## O que o gate não cobre

`test:db`, `test:e2e` e o loop visual **não** estão no gate (exigem Docker, banco em estado
específico, browser). Se o contrato pede prova de banco ou de tela, o gate verde é
necessário e insuficiente — veja a skill `runtime-proof`.

---
name: commit-smart
description: Analisa alterações staged/unstaged e cria commits convencionais semânticos com contexto sobre POR QUÊ, não apenas O QUÊ. Detecta automaticamente tipo e escopo do commit a partir do diff. Suporta argumentos opcionais de tipo/escopo. Uso - /commit-smart, /commit-smart fix, /commit-smart refactor api
---

# Smart Commit

Crie commits convencionais significativos analisando suas alterações reais.

## Fluxo de trabalho

### Etapa 1: Avalie a árvore de trabalho

Execute estes comandos para entender o estado atual:

```bash
git status
git diff --stat
git diff --cached --stat
```

### Etapa 2: Lidar com alterações unstaged

Se nada estiver staged (`git diff --cached` está vazio):

1. Mostre ao usuário quais arquivos foram alterados
2. Sugira o que fazer stage com base em agrupamento lógico (ex: "estes 3 arquivos estão todos relacionados ao refactor de auth")
3. Pergunte se quer fazer stage de tudo, ou selecionar arquivos específicos
4. Faça stage dos arquivos aprovados com `git add <files>`

Se as alterações já estão staged, prossiga para a análise.

### Etapa 3: Analise o diff

Leia o diff staged completo:

```bash
git diff --cached
```

Determine o tipo de commit a partir das alterações:

| Sinal | Tipo |
|--------|------|
| Novos arquivos com nova funcionalidade | `feat` |
| Novos arquivos de teste ou adições de teste | `test` |
| Alterações em lógica existente corrigindo comportamento incorreto | `fix` |
| Alterações estruturais sem mudança de comportamento | `refactor` |
| Alterações em package.json, tsconfig, CI config | `chore` |
| Alterações em config de build/bundler | `build` |
| README, docs, comentários apenas | `docs` |
| Formatação, espaçamento, ponto-e-vírgula apenas | `style` |
| Melhorias de desempenho | `perf` |

Determine o escopo a partir do diretório principal ou módulo afetado:
- `src/api/` -> `api`
- `src/components/auth/` -> `auth`
- `tests/` -> `tests`
- Arquivos de config na raiz -> omita escopo
- Múltiplas áreas não relacionadas -> omita escopo

### Etapa 4: Verifique sobreposições do usuário

Se o usuário forneceu argumentos via `$ARGUMENTS`:
- Uma palavra (ex: `fix`) -> use como tipo de commit
- Duas palavras (ex: `refactor api`) -> use como tipo e escopo
- Caso contrário -> use valores detectados automaticamente

### Etapa 5: Componha a mensagem de commit

Formato: `type(scope): descrição breve no modo imperativo`

Regras:
- Linha de assunto máximo 72 caracteres
- Use modo imperativo ("add", "fix", "refactor", não "added", "fixes")
- Não termine com ponto
- O corpo explica **POR QUÊ** a mudança foi feita, não o que mudou (o diff mostra o quê)
- Se as alterações forem triviais (correção de typo, formatação), pule o corpo

Exemplo:
```
feat(auth): add JWT refresh token rotation

Tokens estavam expirando no meio da sessão para usuários com conexões lentas.
Rotacionar refresh tokens estende a sessão sem comprometer segurança,
já que cada refresh token pode ser usado apenas uma vez.
```

### Etapa 6: Confirme e faça commit

Mostre ao usuário a mensagem de commit proposta e peça confirmação.

Se confirmado, execute:
```bash
git commit -m "<message>"
```

Depois verifique com:
```bash
git log --oneline -1
```

Mostre o hash e a mensagem do commit realizado.

## Dicas

- Execute após completar uma unidade lógica de trabalho, não após cada alteração de arquivo
- Se o diff for muito grande para um commit, sugira dividir em múltiplos commits
- Para breaking changes, adicione `!` após o escopo: `feat(api)!: change response format`
- O corpo deve responder "se alguém ler este commit em 6 meses, compreenderá POR QUÊ?"
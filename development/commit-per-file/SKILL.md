---
name: commit-per-file
description: Analisa os arquivos alterados no repositório e cria um commit semântico individual para cada um, seguindo as regras de docs/commits.md (tipo, emoji e apenas a mensagem principal).
---

# Commit por arquivo

Cria um commit separado para cada arquivo alterado no repositório, classificando cada mudança de acordo com as regras de commits semânticos definidas em `docs/commits.md`.

## Passos

1. Leia `docs/commits.md` na raiz do projeto para obter a tabela atual de tipos, emojis e palavras-chave, além das recomendações de formatação. Releia sempre — não presuma que uma versão vista anteriormente na conversa ainda é a atual.
2. Rode `git status --porcelain` para listar todos os arquivos com mudanças (staged, unstaged e untracked).
3. Para cada arquivo alterado, processe individualmente, um de cada vez:
   a. Rode `git diff -- <arquivo>` (ou `git diff --cached -- <arquivo>` se já estiver staged; leia o conteúdo se for um arquivo novo/untracked) para entender exatamente o que mudou.
   b. Classifique a mudança em um dos tipos da tabela do documento (`feat`, `fix`, `docs`, `test`, `build`, `perf`, `style`, `refactor`, `chore`, `ci`, `raw`, `cleanup`, `remove`) com base no que a mudança realmente faz, não no nome do arquivo.
   c. Escreva a mensagem do commit em português, no formato `:emoji: tipo: descrição curta`, seguindo as recomendações do documento (descrição idealmente com até ~4 palavras, consistente com o tipo escolhido). Use apenas a mensagem principal — sem corpo nem rodapé — a menos que o usuário peça explicitamente mais detalhes.
   d. Rode `git add -- <arquivo>` e `git commit -m "<mensagem>"` contendo somente esse arquivo.
4. Ao final, rode `git log --oneline -n <quantidade de arquivos commitados>` e mostre ao usuário a lista de commits criados.

## Regras importantes

- Um commit por arquivo — nunca agrupe múltiplos arquivos no mesmo commit, mesmo que pareçam parte da mesma mudança lógica. Se o usuário quiser agrupar arquivos, ele pedirá isso explicitamente.
- Se um único arquivo misturar tipos diferentes de mudança (ex.: um bugfix e uma refatoração), escolha o tipo predominante; não tente dividir o mesmo arquivo em múltiplos commits sem que o usuário peça.
- Nunca faça `git push` automaticamente.
- Nunca use `--no-verify` ou outras flags que pulem hooks/verificações.
- Se não houver arquivos alterados, informe o usuário e não crie nenhum commit.
- Siga a ordem em que os arquivos aparecem em `git status --porcelain`, salvo alguma razão clara para priorizar um arquivo específico.

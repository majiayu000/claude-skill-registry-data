---
name: verificar-fila
description: Roda o verificador oficial da regra de ouro sobre um fila_priorizada.csv e explica o resultado. Use sempre que a ordenação da fila mudar ou antes de commitar/entregar a fila.
argument-hint: [caminho/para/fila_priorizada.csv]
allowed-tools: Bash(python src/verificar_fila_priorizada.py *) Bash(python3 src/verificar_fila_priorizada.py *)
---

Verifique a fila priorizada.

1. Arquivo alvo: `$ARGUMENTS`. Se vazio, procure `fila_priorizada.csv` no repositório (raiz, `data/processed/`, `output/`, `backend/`), e se houver mais de um, pergunte qual.
2. Rode a partir da raiz do repositório:
   `python src/verificar_fila_priorizada.py <arquivo>`
3. Responda em português, curto:
   - **Resultado:** OK ou número de erros.
   - **Regra de ouro:** se violada, liste os oncológicos mal posicionados e a posição do primeiro paciente "sem urgência".
   - **Avisos:** solicitações fora do arquivo (confira se estão justificadas no `DECISOES.md`) e linhas sem justificativa.
   - **Indicadores:** posição mediana dos oncológicos, % de pacientes com PS/internação recente na primeira metade, % de sem urgência no último terço.
4. Se falhou, diga a causa provável no código (ex.: trava C-11 não aplicada, CID não normalizado, uso da flag em vez do CID) e proponha a correção. **Não** edite o verificador nem os CSVs oficiais.

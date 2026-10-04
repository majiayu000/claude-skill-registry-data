---
name: readme-manutencao
description: Skill para manter os READMEs do projeto sincronizados em PT-BR, EN e ZH. Use quando precisar atualizar documentação após implementações ou mudanças no projeto.
---

# Skill: Manutenção de README

Mantém os três READMEs do projeto (PT-BR, EN, ZH) sincronizados e atualizados.

## Arquivos Gerenciados

| Arquivo | Idioma | Público |
|---------|--------|---------|
| `README.md` | 🇧🇷 Português | Principal |
| `README-en.md` | 🇺🇸 English | Internacional |
| `README-zh.md` | 🇨🇳 中文 | Chinês |

## Quando Usar

- Após adicionar uma nova funcionalidade ao projeto
- Após criar novos agentes, skills ou prompts
- Quando o README está desatualizado em relação ao código
- Quando o usuário pede para "atualizar a documentação"

## Regras de Sincronização

### Conteúdo Obrigatório (todos os idiomas)
1. Título e tagline do projeto
2. Badges (License, GnuCOBOL, Copilot, PRs)
3. Links de navegação entre idiomas
4. Seção "O que é" / "What is" / "这是什么"
5. Seção de funcionalidades/features
6. Instruções de instalação (GnuCOBOL)
7. Como usar (compilar + executar)
8. Estrutura do projeto
9. Como contribuir (link para CONTRIBUTING)

### Regras de Tradução

**PT-BR → EN:**
- Manter tom casual e didático
- "Vibe Coding é programar sem entender o código" → "Vibe Coding is programming without understanding the code"
- Manter emojis idênticos

**PT-BR → ZH (中文):**
- Manter tom técnico mas acessível
- "Vibe Coding é programar sem entender o código" → "氛围编程就是在不理解代码的情况下编程"
- Adaptar culturalmente (não tradução literal)

### Formato de Badges
```markdown
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](./LICENSE)
[![GnuCOBOL](https://img.shields.io/badge/COBOL-GnuCOBOL-blue)](https://gnucobol.sourceforge.io/)
[![GitHub Copilot](https://img.shields.io/badge/GitHub-Copilot%20Agent%20Mode-8A2BE2)](https://github.com/features/copilot)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](./CONTRIBUTING.md)
```

### Navegação Entre Idiomas

**Em README.md:**
```markdown
🇧🇷 Português | [🇺🇸 English](./README-en.md) | [🇨🇳 中文](./README-zh.md)
```

**Em README-en.md:**
```markdown
[🇧🇷 Português](./README.md) | 🇺🇸 English | [🇨🇳 中文](./README-zh.md)
```

**Em README-zh.md:**
```markdown
[🇧🇷 Português](./README.md) | [🇺🇸 English](./README-en.md) | 🇨🇳 中文
```

## Sincronização de Exemplos de Código

Os READMEs podem conter blocos de código COBOL para ilustrar funcionalidades.
Esses blocos devem sempre refletir o código real em `src/CALCULADORA.cbl`.

### Quando Verificar

- Sempre que o COBOL Coder modificar `src/CALCULADORA.cbl`
- Quando novos parágrafos ou operações forem adicionados
- Quando nomes de variáveis forem alterados

### Como Sincronizar

1. **Leia** `src/CALCULADORA.cbl` por completo
2. **Identifique** todos os blocos ` ```cobol ` nos três READMEs
3. **Compare** cada bloco com o código real:
   - Nomes de variáveis (ex: `WS-NUMERO-1`, `WS-RESULTADO`)
   - Nomes de parágrafos (ex: `INICIO`, `PROCESSAR`)
   - Operações implementadas (ex: `ADD`, `SUBTRACT`)
4. **Atualize** os blocos desatualizados nos três idiomas simultaneamente
5. **Nunca** invente código que não existe no arquivo `.cbl`
6. **Prefira** recortes reais do arquivo a exemplos genéricos

### Exemplo de Verificação

Se o README mostra:
```cobol
ADD WS-NUMERO-1 TO WS-NUMERO-2 GIVING WS-RESULTADO.
```
E o arquivo `.cbl` foi alterado para incluir subtração, adicione também:
```cobol
SUBTRACT WS-NUMERO-2 FROM WS-NUMERO-1 GIVING WS-RESULTADO.
```

## Processo de Atualização

1. **Leia** `src/CALCULADORA.cbl` — é a fonte da verdade do código
2. **Leia** o `README.md` (PT-BR) atual — é a fonte da verdade da documentação
3. **Identifique** o que mudou no projeto (novos arquivos, features, estrutura, código)
4. **Atualize** os exemplos de código COBOL nos READMEs para refletir o `.cbl` atual
5. **Atualize** o `README.md` primeiro
6. **Traduza** as mudanças para `README-en.md`
7. **Traduza** as mudanças para `README-zh.md`
8. **Verifique** que os links entre os arquivos funcionam

## Checklist de Qualidade

- [ ] Os três arquivos têm o mesmo conteúdo (adaptado ao idioma)
- [ ] Links de navegação entre idiomas funcionam
- [ ] Badges estão corretos e atualizados
- [ ] Estrutura do projeto reflete o estado atual
- [ ] Instruções de uso estão corretas
- [ ] Nenhum conteúdo PT-BR ficou no EN ou ZH
- [ ] Todos os blocos `\`\`\`cobol` nos READMEs refletem o código real de `src/CALCULADORA.cbl`
- [ ] Nomes de variáveis e parágrafos nos exemplos estão corretos e atualizados

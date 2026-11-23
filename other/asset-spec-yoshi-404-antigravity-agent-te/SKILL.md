---
name: asset-spec
description: Modelo de especificação de assets de arte e áudio (descrição, formato, uso, licença).
---

# Skill: asset-spec

Uma entrada por asset, em `docs/arte/assets/` ou `docs/audio/`.

## Campos
- **ID e nome do arquivo** (convenção: `tipo_nome_variante`, minúsculas, sem espaços)
- **Tipo**: sprite, modelo 3D, textura, UI, música, efeito, voz
- **Uso**: onde e quando aparece no jogo
- **Descrição**: forma, cores (da paleta), estado, expressão
- **Formato técnico**: dimensões, proporção, formato de arquivo, taxa de amostragem/canais para áudio, duração
- **Variantes e estados**: ex.: parado, andando, dano
- **Referências**: em palavras e em fontes que o projeto tenha direito de usar
- **Origem**: feito por artista, gerado por ferramenta, ou licenciado
- **Licença**: autor, link, termos (obrigatório se não for original)
- **Status**: especificado | em produção | entregue | integrado

## Regras
- Especificar não é produzir: o asset é feito fora do agente.
- Não referencie obras protegidas como "copie isto".

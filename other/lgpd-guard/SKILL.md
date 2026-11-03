---
name: LGPD Compliance Guard
description: Garante que novas funcionalidades de coleta de dados respeitem a soberania e privacidade da LGPD.
---

# LGPD Compliance Guard

Guardião da privacidade e soberania de dados no ecossistema Áquila Pro.

## Instruções de Uso
Ativar sempre que criar novas tabelas no SQLite, novos fluxos de captura de imagem/voz ou extração de documentos.

## Capacidades
- **Edge Anonymization**: Geração de vetores biométricos na borda com descarte imediato de imagens cruas.
- **RBAC Verification**: Validação de acesso baseada na matriz de permissões.
- **Hardware Encryption**: Uso de AES-256 via hardware no Áquila Edge.

## Regras Invioláveis (Zero-Bypass)
1. **Zero Storage of Raw Faces**: Proibido armazenar rostos de alunos em formato identificável sem criptografia quântica.
2. **Audit Logging**: Toda verificação de conformidade deve ser registrada em `c:\aquila\.aquila_brain\40_Legal_LGPD\LGPD_Compliance.md`.
3. **No External Sync**: Dados sob custódia LGPD nunca devem ser sincronizados com nuvens públicas.

## Exemplos
"Verifique se o novo fluxo de presença por voz está em conformidade com a LGPD."

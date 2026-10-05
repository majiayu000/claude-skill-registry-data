---
name: specsfy-specialist-debugging
description: Diagnosticar bugs, regressões, falhas intermitentes e problemas de performance por reprodução, minimização, hipótese e instrumentação. Use quando o usuário pedir diagnóstico ou relatar algo quebrado; não implementar correção quando o pedido for somente diagnóstico.
---

# Diagnóstico

## Fluxo

1. Capturar comportamento esperado, observado, ambiente e última ocorrência.
2. Construir reprodução confiável ou sinal observável.
3. Reduzir input, componentes e tempo até o menor caso.
4. Formular hipóteses falsificáveis e ordená-las.
5. Instrumentar o boundary mais discriminante.
6. Identificar causa, extensão e mecanismo.
7. Se autorizado, corrigir e adicionar teste de regressão.

## Padrões

- Não alterar várias causas possíveis ao mesmo tempo.
- Separar correlação temporal de causalidade.
- Preservar evidência antes de reiniciar ou limpar estado.
- Comparar ambiente bom e ruim sistematicamente.
- Tratar flakiness como concorrência, tempo, estado ou dependência até prova.
- Remover instrumentação sensível ou ruidosa ao concluir.
- Descrever causa no nível do mecanismo, não do sintoma.

## Validação

- Reprodução falha antes e passa após a correção.
- Teste de regressão falha pelo motivo correto.
- Verificação de cenários adjacentes e impacto.
- Registro conciso de causa, evidência e prevenção.

Leia [references/standards.md](references/standards.md) para técnicas de
reprodução, concorrência, performance e incidentes.

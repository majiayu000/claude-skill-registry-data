---
name: adaptyv
description: Plataforma de laboratório em nuvem para testes e validação automatizados de proteínas. Use ao projetar proteínas e precisar de validação experimental incluindo ensaios de ligação, testes de expressão, medições de estabilidade térmica, ensaios de atividade enzimática ou otimização de sequências de proteínas. Use também para submeter experimentos via API, rastrear status de experimentos, baixar resultados, otimizar sequências de proteínas para melhor expressão usando ferramentas computacionais (NetSolP, SoluProt, SolubleMPNN, ESM), ou gerenciar workflows de design de proteínas com validação em laboratório úmido.
---

# Adaptyv

Adaptyv é uma plataforma de laboratório em nuvem que oferece serviços automatizados de testes e validação de proteínas. Envie sequências de proteínas via API ou interface web e receba resultados experimentais em aproximadamente 21 dias.

## Início Rápido

### Configuração de Autenticação

Adaptyv requer autenticação via API. Configure suas credenciais:

1. Entre em contato com support@adaptyvbio.com para solicitar acesso à API (a plataforma está em fase alfa/beta)
2. Receba seu token de acesso à API
3. Configure a variável de ambiente:

```bash
export ADAPTYV_API_KEY="your_api_key_here"
```

Ou crie um arquivo `.env`:

```
ADAPTYV_API_KEY=your_api_key_here
```

### Instalação

Instale o pacote necessário usando uv:

```bash
uv pip install requests python-dotenv
```

### Uso Básico

Envie sequências de proteínas para testes:

```python
import os
import requests
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("ADAPTYV_API_KEY")
base_url = "https://kq5jp7qj7wdqklhsxmovkzn4l40obksv.lambda-url.eu-central-1.on.aws"

headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

# Submit experiment
response = requests.post(
    f"{base_url}/experiments",
    headers=headers,
    json={
        "sequences": ">protein1\nMKVLWALLGLLGAA...",
        "experiment_type": "binding",
        "webhook_url": "https://your-webhook.com/callback"
    }
)

experiment_id = response.json()["experiment_id"]
```

## Tipos de Experimentos Disponíveis

Adaptyv oferece suporte a múltiplos tipos de ensaios:

- **Ensaios de ligação** - Teste interações proteína-alvo usando interferometria de biolayer
- **Testes de expressão** - Meça os níveis de expressão de proteínas
- **Estabilidade térmica** - Caracterize a estabilidade térmica da proteína
- **Atividade enzimática** - Avalie a função enzimática

Consulte `reference/experiments.md` para informações detalhadas sobre cada tipo de experimento e workflows.

## Otimização de Sequências de Proteínas

Antes de enviar sequências, otimize-as para melhor expressão e estabilidade:

**Problemas comuns a serem abordados:**
- Cisteínas não pareadas que criam dissulfetos indesejados
- Regiões excessivamente hidrofóbicas causando agregação
- Predições pobres de solubilidade

**Ferramentas recomendadas:**
- NetSolP / SoluProt - Filtragem inicial de solubilidade
- SolubleMPNN - Redesenho de sequência para solubilidade melhorada
- ESM - Pontuação de probabilidade de sequência
- ipTM - Avaliação de estabilidade de interface
- pSAE - Quantificação de exposição hidrofóbica

Consulte `reference/protein_optimization.md` para workflows detalhados de otimização e uso de ferramentas.

## Referência de API

Para documentação completa de API incluindo todos os endpoints, formatos de requisição/resposta e detalhes de autenticação, consulte `reference/api_reference.md`.

## Exemplos

Para exemplos de código concretos cobrindo casos de uso comuns (submissão de experimentos, rastreamento de status, recuperação de resultados, processamento em lote), consulte `reference/examples.md`.

## Notas Importantes

- A plataforma está atualmente em fase alfa/beta com recursos sujeitos a alterações
- Nem todos os recursos da plataforma estão disponíveis via API ainda
- Resultados geralmente entregues em ~21 dias
- Entre em contato com support@adaptyvbio.com para solicitações de acesso ou dúvidas
- Adequada para workflows de design de proteínas impulsionados por IA de alto rendimento
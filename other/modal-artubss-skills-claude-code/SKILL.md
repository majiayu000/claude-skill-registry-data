---
name: modal
description: Execute código Python na nuvem com contêineres serverless, GPUs e autoscaling. Use ao fazer deploy de modelos de ML, executar jobs de processamento em lote, agendar tarefas compute-intensivas ou servir APIs que exigem aceleração GPU ou scaling dinâmico.
---

# Modal

## Visão Geral

Modal é uma plataforma serverless para executar código Python na nuvem com configuração mínima. Execute funções em GPUs poderosas, escale automaticamente para milhares de contêineres e pague apenas pelo compute utilizado.

Modal é particularmente adequado para workloads de IA/ML, processamento em lote de alto desempenho, jobs agendados, inferência GPU e APIs serverless. Cadastre-se gratuitamente em https://modal.com e receba $30/mês em créditos.

## Quando Usar Esta Skill

Use Modal para:
- Fazer deploy e servir modelos de ML (LLMs, geração de imagens, modelos de embedding)
- Executar computação acelerada por GPU (treinamento, inferência, renderização)
- Processar em lote grandes conjuntos de dados em paralelo
- Agendar jobs compute-intensivos (processamento diário de dados, treinamento de modelos)
- Construir APIs serverless que necessitam escalabilidade automática
- Computação científica que exige compute distribuído ou hardware especializado

## Autenticação e Setup

Modal requer autenticação via token de API.

### Setup Inicial

```bash
# Instalar Modal
uv pip install modal

# Autenticar (abre navegador para login)
modal token new
```

Isso cria um token armazenado em `~/.modal.toml`. O token autentica todas as operações Modal.

### Verificar Setup

```python
import modal

app = modal.App("test-app")

@app.function()
def hello():
    print("Modal is working!")
```

Execute com: `modal run script.py`

## Capacidades Principais

Modal oferece execução Python serverless através de Functions que executam em contêineres. Defina requisitos de compute, dependências e comportamento de scaling de forma declarativa.

### 1. Definir Imagens de Contêiner

Especifique dependências e ambiente para funções usando Modal Images.

```python
import modal

# Imagem básica com pacotes Python
image = (
    modal.Image.debian_slim(python_version="3.12")
    .uv_pip_install("torch", "transformers", "numpy")
)

app = modal.App("ml-app", image=image)
```

**Padrões comuns:**
- Instalar pacotes Python: `.uv_pip_install("pandas", "scikit-learn")`
- Instalar pacotes do sistema: `.apt_install("ffmpeg", "git")`
- Usar imagens Docker existentes: `modal.Image.from_registry("nvidia/cuda:12.1.0-base")`
- Adicionar código local: `.add_local_python_source("my_module")`

Veja `references/images.md` para documentação abrangente de construção de imagens.

### 2. Criar Functions

Defina funções que executam na nuvem com o decorator `@app.function()`.

```python
@app.function()
def process_data(file_path: str):
    import pandas as pd
    df = pd.read_csv(file_path)
    return df.describe()
```

**Chamar funções:**
```python
# Do entrypoint local
@app.local_entrypoint()
def main():
    result = process_data.remote("data.csv")
    print(result)
```

Execute com: `modal run script.py`

Veja `references/functions.md` para padrões de função, deploy e manipulação de parâmetros.

### 3. Solicitar GPUs

Anexe GPUs a funções para computação acelerada.

```python
@app.function(gpu="H100")
def train_model():
    import torch
    assert torch.cuda.is_available()
    # Código acelerado por GPU aqui
```

**Tipos de GPU disponíveis:**
- `T4`, `L4` - Inferência econômica
- `A10`, `A100`, `A100-80GB` - Treinamento/inferência padrão
- `L40S` - Excelente relação custo/desempenho (48GB)
- `H100`, `H200` - Treinamento de alto desempenho
- `B200` - Desempenho flagship (mais poderosa)

**Solicitar múltiplas GPUs:**
```python
@app.function(gpu="H100:8")  # 8x GPUs H100
def train_large_model():
    pass
```

Veja `references/gpu.md` para orientação de seleção de GPU, setup CUDA e configuração multi-GPU.

### 4. Configurar Recursos

Solicite CPU cores, memória e disco para funções.

```python
@app.function(
    cpu=8.0,           # 8 núcleos físicos
    memory=32768,      # 32 GiB RAM
    ephemeral_disk=10240  # 10 GiB disco
)
def memory_intensive_task():
    pass
```

Alocação padrão: 0,125 CPU cores, 128 MiB memória. Billing baseado em reserva ou uso real, o que for maior.

Veja `references/resources.md` para limites de recursos e detalhes de billing.

### 5. Escalar Automaticamente

Modal autoscale funções de zero a milhares de contêineres baseado na demanda.

**Processar inputs em paralelo:**
```python
@app.function()
def analyze_sample(sample_id: int):
    # Processar amostra única
    return result

@app.local_entrypoint()
def main():
    sample_ids = range(1000)
    # Automaticamente paralelizado entre contêineres
    results = list(analyze_sample.map(sample_ids))
```

**Configurar autoscaling:**
```python
@app.function(
    max_containers=100,      # Limite superior
    min_containers=2,        # Manter aquecido
    buffer_containers=5      # Buffer ocioso para picos
)
def inference():
    pass
```

Veja `references/scaling.md` para configuração de autoscaling, concorrência e limites de scaling.

### 6. Armazenar Dados Persistentemente

Use Volumes para armazenamento persistente entre invocações de função.

```python
volume = modal.Volume.from_name("my-data", create_if_missing=True)

@app.function(volumes={"/data": volume})
def save_results(data):
    with open("/data/results.txt", "w") as f:
        f.write(data)
    volume.commit()  # Persistir mudanças
```

Volumes persistem dados entre execuções, armazenam pesos de modelos, fazem cache de datasets e compartilham dados entre funções.

Veja `references/volumes.md` para gerenciamento de volumes, commits e padrões de caching.

### 7. Gerenciar Secrets

Armazene chaves de API e credenciais com segurança usando Modal Secrets.

```python
@app.function(secrets=[modal.Secret.from_name("huggingface")])
def download_model():
    import os
    token = os.environ["HF_TOKEN"]
    # Usar token para autenticação
```

**Criar secrets no dashboard Modal ou via CLI:**
```bash
modal secret create my-secret KEY=value API_TOKEN=xyz
```

Veja `references/secrets.md` para gerenciamento de secrets e padrões de autenticação.

### 8. Fazer Deploy de Web Endpoints

Sirva endpoints HTTP, APIs e webhooks com `@modal.web_endpoint()`.

```python
@app.function()
@modal.web_endpoint(method="POST")
def predict(data: dict):
    # Processar requisição
    result = model.predict(data["input"])
    return {"prediction": result}
```

**Fazer deploy com:**
```bash
modal deploy script.py
```

Modal fornece URL HTTPS para o endpoint.

Veja `references/web-endpoints.md` para integração FastAPI, streaming, autenticação e suporte WebSocket.

### 9. Agendar Jobs

Execute funções em um schedule com expressões cron.

```python
@app.function(schedule=modal.Cron("0 2 * * *"))  # Diariamente às 2 AM
def daily_backup():
    # Fazer backup de dados
    pass

@app.function(schedule=modal.Period(hours=4))  # A cada 4 horas
def refresh_cache():
    # Atualizar cache
    pass
```

Funções agendadas executam automaticamente sem invocação manual.

Veja `references/scheduled-jobs.md` para sintaxe cron, configuração de timezone e monitoramento.

## Workflows Comuns

### Fazer Deploy de Modelo de ML para Inferência

```python
import modal

# Definir dependências
image = modal.Image.debian_slim().uv_pip_install("torch", "transformers")
app = modal.App("llm-inference", image=image)

# Baixar modelo no tempo de build
@app.function()
def download_model():
    from transformers import AutoModel
    AutoModel.from_pretrained("bert-base-uncased")

# Servir modelo
@app.cls(gpu="L40S")
class Model:
    @modal.enter()
    def load_model(self):
        from transformers import pipeline
        self.pipe = pipeline("text-classification", device="cuda")

    @modal.method()
    def predict(self, text: str):
        return self.pipe(text)

@app.local_entrypoint()
def main():
    model = Model()
    result = model.predict.remote("Modal is great!")
    print(result)
```

### Processar em Lote Grande Conjunto de Dados

```python
@app.function(cpu=2.0, memory=4096)
def process_file(file_path: str):
    import pandas as pd
    df = pd.read_csv(file_path)
    # Processar dados
    return df.shape[0]

@app.local_entrypoint()
def main():
    files = ["file1.csv", "file2.csv", ...]  # Milhares de arquivos
    # Automaticamente paralelizado entre contêineres
    for count in process_file.map(files):
        print(f"Processed {count} rows")
```

### Treinar Modelo em GPU

```python
@app.function(
    gpu="A100:2",      # 2x GPUs A100
    timeout=3600       # 1 hora timeout
)
def train_model(config: dict):
    import torch
    # Código de treinamento multi-GPU
    model = create_model(config)
    train(model)
    return metrics
```

## Documentação de Referência

Documentação detalhada para recursos específicos:

- **`references/getting-started.md`** - Autenticação, setup, conceitos básicos
- **`references/images.md`** - Construção de imagens, dependências, Dockerfiles
- **`references/functions.md`** - Padrões de função, deploy, parâmetros
- **`references/gpu.md`** - Tipos de GPU, CUDA, configuração multi-GPU
- **`references/resources.md`** - Gerenciamento de CPU, memória, disco
- **`references/scaling.md`** - Autoscaling, execução paralela, concorrência
- **`references/volumes.md`** - Armazenamento persistente, gerenciamento de dados
- **`references/secrets.md`** - Variáveis de ambiente, autenticação
- **`references/web-endpoints.md`** - APIs, webhooks, endpoints
- **`references/scheduled-jobs.md`** - Jobs cron, tarefas periódicas
- **`references/examples.md`** - Padrões comuns para computação científica

## Melhores Práticas

1. **Fixe dependências** em `.uv_pip_install()` para builds reproduzíveis
2. **Use tipos de GPU apropriados** - L40S para inferência, H100/A100 para treinamento
3. **Aproveite o caching** - Use Volumes para pesos de modelos e datasets
4. **Configure autoscaling** - Defina `max_containers` e `min_containers` baseado na carga de trabalho
5. **Importe pacotes no corpo da função** se não disponíveis localmente
6. **Use `.map()` para processamento paralelo** em vez de loops sequenciais
7. **Armazene secrets com segurança** - Nunca faça hardcode de chaves de API
8. **Monitore custos** - Verifique o dashboard Modal para uso e billing

## Solução de Problemas

**Erros "Module not found":**
- Adicione pacotes à imagem com `.uv_pip_install("package-name")`
- Importe pacotes dentro do corpo da função se não disponíveis localmente

**GPU não detectada:**
- Verifique especificação de GPU: `@app.function(gpu="A100")`
- Verifique disponibilidade CUDA: `torch.cuda.is_available()`

**Função com timeout:**
- Aumente timeout: `@app.function(timeout=3600)`
- O timeout padrão é 5 minutos

**Mudanças de Volume não persisting:**
- Chame `volume.commit()` após escrever arquivos
- Verifique se volume está montado corretamente no decorator da função

Para ajuda adicional, veja documentação Modal em https://modal.com/docs ou participe da comunidade Slack Modal.
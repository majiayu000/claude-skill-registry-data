---
name: shap
description: Interpretabilidade e explicabilidade de modelos usando SHAP (SHapley Additive exPlanations). Use essa skill ao explicar predições de modelos de machine learning, computar importância de features, gerar plots SHAP (waterfall, beeswarm, bar, scatter, force, heatmap), depurar modelos, analisar vieses ou justiça de modelos, comparar modelos ou implementar IA explicável. Funciona com modelos baseados em árvores (XGBoost, LightGBM, Random Forest), deep learning (TensorFlow, PyTorch), modelos lineares e qualquer modelo black-box.
---

# SHAP (SHapley Additive exPlanations)

## Visão Geral

SHAP é uma abordagem unificada para explicar saídas de modelos de machine learning usando valores de Shapley da teoria dos jogos cooperativos. Essa skill oferece orientação abrangente para:

- Computar valores SHAP para qualquer tipo de modelo
- Criar visualizações para entender importância de features
- Depurar e validar comportamento de modelos
- Analisar justiça e vieses
- Implementar IA explicável em produção

SHAP funciona com todos os tipos de modelos: modelos baseados em árvores (XGBoost, LightGBM, CatBoost, Random Forest), modelos de deep learning (TensorFlow, PyTorch, Keras), modelos lineares e modelos black-box.

## Quando Usar Essa Skill

**Ative essa skill quando usuários perguntarem sobre**:
- "Explique quais features são mais importantes no meu modelo"
- "Gere plots SHAP" (waterfall, beeswarm, bar, scatter, force, heatmap, etc.)
- "Por que meu modelo fez essa predição?"
- "Calcule valores SHAP para meu modelo"
- "Visualize importância de features usando SHAP"
- "Depure o comportamento do meu modelo" ou "valide meu modelo"
- "Verifique vieses no meu modelo" ou "analise justiça"
- "Compare importância de features entre modelos"
- "Implemente IA explicável" ou "adicione explicações ao meu modelo"
- "Entenda interações de features"
- "Crie dashboard de interpretação de modelos"

## Guia de Início Rápido

### Passo 1: Selecione o Explainer Correto

**Árvore de Decisão**:

1. **Modelo baseado em árvores?** (XGBoost, LightGBM, CatBoost, Random Forest, Gradient Boosting)
   - Use `shap.TreeExplainer` (rápido, exato)

2. **Rede neural profunda?** (TensorFlow, PyTorch, Keras, CNNs, RNNs, Transformers)
   - Use `shap.DeepExplainer` ou `shap.GradientExplainer`

3. **Modelo linear?** (Linear/Logistic Regression, GLMs)
   - Use `shap.LinearExplainer` (extremamente rápido)

4. **Qualquer outro modelo?** (SVMs, funções customizadas, modelos black-box)
   - Use `shap.KernelExplainer` (agnóstico de modelo, mas mais lento)

5. **Incerto?**
   - Use `shap.Explainer` (seleciona automaticamente o melhor algoritmo)

**Veja `references/explainers.md` para informações detalhadas sobre todos os tipos de explainers.**

### Passo 2: Compute Valores SHAP

```python
import shap

# Exemplo com modelo baseado em árvores (XGBoost)
import xgboost as xgb

# Treine o modelo
model = xgb.XGBClassifier().fit(X_train, y_train)

# Crie o explainer
explainer = shap.TreeExplainer(model)

# Compute valores SHAP
shap_values = explainer(X_test)

# O objeto shap_values contém:
# - values: valores SHAP (atribuições de features)
# - base_values: saída esperada do modelo (baseline)
# - data: valores originais das features
```

### Passo 3: Visualize Resultados

**Para Entendimento Global** (dataset inteiro):
```python
# Plot beeswarm - mostra importância de features com distribuições de valores
shap.plots.beeswarm(shap_values, max_display=15)

# Plot bar - resumo limpo de importância de features
shap.plots.bar(shap_values)
```

**Para Predições Individuais**:
```python
# Plot waterfall - decomposição detalhada de uma predição
shap.plots.waterfall(shap_values[0])

# Plot force - visualização de força aditiva
shap.plots.force(shap_values[0])
```

**Para Relações de Features**:
```python
# Plot scatter - relação feature-predição
shap.plots.scatter(shap_values[:, "Feature_Name"])

# Colorido por outra feature para mostrar interações
shap.plots.scatter(shap_values[:, "Age"], color=shap_values[:, "Education"])
```

**Veja `references/plots.md` para guia abrangente sobre todos os tipos de plots.**

## Workflows Principais

Essa skill suporta vários workflows comuns. Escolha o workflow que corresponde à tarefa atual.

### Workflow 1: Explicação Básica de Modelo

**Objetivo**: Entender o que direciona predições de modelo

**Passos**:
1. Treine modelo e crie explainer apropriado
2. Compute valores SHAP para conjunto de teste
3. Gere plots de importância global (beeswarm ou bar)
4. Examine relações das top features (scatter plots)
5. Explique predições específicas (waterfall plots)

**Exemplo**:
```python
# Passos 1-2: Setup
explainer = shap.TreeExplainer(model)
shap_values = explainer(X_test)

# Passo 3: Importância global
shap.plots.beeswarm(shap_values)

# Passo 4: Relações de features
shap.plots.scatter(shap_values[:, "Most_Important_Feature"])

# Passo 5: Explicação individual
shap.plots.waterfall(shap_values[0])
```

### Workflow 2: Depuração de Modelo

**Objetivo**: Identificar e corrigir problemas de modelo

**Passos**:
1. Compute valores SHAP
2. Identifique erros de predição
3. Explique amostras mal classificadas
4. Verifique importância de features inesperada (vazamento de dados)
5. Valide se relações de features fazem sentido
6. Verifique interações de features

**Veja `references/workflows.md` para workflow de depuração detalhado.**

### Workflow 3: Engenharia de Features

**Objetivo**: Use insights SHAP para melhorar features

**Passos**:
1. Compute valores SHAP para modelo base
2. Identifique relações não-lineares (candidatas para transformação)
3. Identifique interações de features (candidatas para termos de interação)
4. Engenharie novas features
5. Retreine e compare valores SHAP
6. Valide melhorias

**Veja `references/workflows.md` para workflow de engenharia de features detalhado.**

### Workflow 4: Comparação de Modelos

**Objetivo**: Compare múltiplos modelos para selecionar a melhor opção interpretável

**Passos**:
1. Treine múltiplos modelos
2. Compute valores SHAP para cada um
3. Compare importância global de features
4. Verifique consistência de rankings de features
5. Analise predições específicas entre modelos
6. Selecione com base em acurácia, interpretabilidade e consistência

**Veja `references/workflows.md` para workflow de comparação de modelos detalhado.**

### Workflow 5: Análise de Justiça e Viés

**Objetivo**: Detecte e analise vieses de modelo entre grupos demográficos

**Passos**:
1. Identifique atributos protegidos (gênero, raça, idade, etc.)
2. Compute valores SHAP
3. Compare importância de features entre grupos
4. Verifique importância SHAP de atributos protegidos
5. Identifique features proxy
6. Implemente estratégias de mitigação se viés encontrado

**Veja `references/workflows.md` para workflow de análise de justiça detalhado.**

### Workflow 6: Deployment em Produção

**Objetivo**: Integre explicações SHAP em sistemas em produção

**Passos**:
1. Treine e salve modelo
2. Crie e salve explainer
3. Construa serviço de explicação
4. Crie endpoints de API para predições com explicações
5. Implemente cache e otimização
6. Monitore qualidade de explicações

**Veja `references/workflows.md` para workflow de deployment em produção detalhado.**

## Conceitos-Chave

### Valores SHAP

**Definição**: Valores SHAP quantificam a contribuição de cada feature para uma predição, medida como desvio da saída esperada do modelo (baseline).

**Propriedades**:
- **Aditividade**: Valores SHAP somam à diferença entre predição e baseline
- **Justiça**: Baseado em valores de Shapley da teoria dos jogos
- **Consistência**: Se uma feature fica mais importante, seu valor SHAP aumenta

**Interpretação**:
- Valor SHAP positivo → Feature empurra predição para cima
- Valor SHAP negativo → Feature empurra predição para baixo
- Magnitude → Força do impacto da feature
- Soma de valores SHAP → Mudança total de predição a partir do baseline

**Exemplo**:
```
Baseline (valor esperado): 0.30
Contribuições de features (valores SHAP):
  Age: +0.15
  Income: +0.10
  Education: -0.05
Predição final: 0.30 + 0.15 + 0.10 - 0.05 = 0.50
```

### Background Data / Baseline

**Propósito**: Representa entrada "típica" para estabelecer expectativas baseline

**Seleção**:
- Amostra aleatória dos dados de treinamento (50-1000 amostras)
- Ou use kmeans para selecionar amostras representativas
- Para DeepExplainer/KernelExplainer: 100-1000 amostras equilibra acurácia e velocidade

**Impacto**: Baseline afeta magnitudes de valores SHAP, mas não importância relativa

### Tipos de Saída de Modelo

**Consideração Crítica**: Entenda o que seu modelo produz

- **Saída bruta**: Para regressão ou tree margins
- **Probabilidade**: Para probabilidade de classificação
- **Log-odds**: Para regressão logística (antes de sigmoid)

**Exemplo**: Classificadores XGBoost explicam saída de margin (log-odds) por padrão. Para explicar probabilidades, use `model_output="probability"` em TreeExplainer.

## Padrões Comuns

### Padrão 1: Análise Completa de Modelo

```python
# 1. Setup
explainer = shap.TreeExplainer(model)
shap_values = explainer(X_test)

# 2. Importância global
shap.plots.beeswarm(shap_values)
shap.plots.bar(shap_values)

# 3. Relações das top features
top_features = X_test.columns[np.abs(shap_values.values).mean(0).argsort()[-5:]]
for feature in top_features:
    shap.plots.scatter(shap_values[:, feature])

# 4. Predições de exemplo
for i in range(5):
    shap.plots.waterfall(shap_values[i])
```

### Padrão 2: Comparação de Coortes

```python
# Defina coortes
cohort1_mask = X_test['Group'] == 'A'
cohort2_mask = X_test['Group'] == 'B'

# Compare importância de features
shap.plots.bar({
    "Group A": shap_values[cohort1_mask],
    "Group B": shap_values[cohort2_mask]
})
```

### Padrão 3: Depurando Erros

```python
# Encontre erros
errors = model.predict(X_test) != y_test
error_indices = np.where(errors)[0]

# Explique erros
for idx in error_indices[:5]:
    print(f"Amostra {idx}:")
    shap.plots.waterfall(shap_values[idx])

    # Investigue features suspeitas
    shap.plots.scatter(shap_values[:, "Suspicious_Feature"])
```

## Otimização de Performance

### Considerações de Velocidade

**Velocidade de Explainer** (mais rápido para mais lento):
1. `LinearExplainer` - Quase instantâneo
2. `TreeExplainer` - Muito rápido
3. `DeepExplainer` - Rápido para redes neurais
4. `GradientExplainer` - Rápido para redes neurais
5. `KernelExplainer` - Lento (use apenas quando necessário)
6. `PermutationExplainer` - Muito lento mas acurado

### Estratégias de Otimização

**Para Datasets Grandes**:
```python
# Compute SHAP para subset
shap_values = explainer(X_test[:1000])

# Ou use batching
batch_size = 100
all_shap_values = []
for i in range(0, len(X_test), batch_size):
    batch_shap = explainer(X_test[i:i+batch_size])
    all_shap_values.append(batch_shap)
```

**Para Visualizações**:
```python
# Amostra subset para plots
shap.plots.beeswarm(shap_values[:1000])

# Ajuste transparência para plots densos
shap.plots.scatter(shap_values[:, "Feature"], alpha=0.3)
```

**Para Produção**:
```python
# Cache explainer
import joblib
joblib.dump(explainer, 'explainer.pkl')
explainer = joblib.load('explainer.pkl')

# Pre-compute para predições em batch
# Compute apenas top N features para respostas de API
```

## Troubleshooting

### Problema: Escolha errada de explainer
**Problema**: Usar KernelExplainer para modelos de árvore (lento e desnecessário)
**Solução**: Sempre use TreeExplainer para modelos baseados em árvores

### Problema: Background data insuficiente
**Problema**: DeepExplainer/KernelExplainer com pouquíssimas amostras de background
**Solução**: Use 100-1000 amostras representativas

### Problema: Unidades confusas
**Problema**: Interpretar log-odds como probabilidades
**Solução**: Verifique tipo de saída do modelo; entenda se valores são probabilidades, log-odds ou saídas brutas

### Problema: Plots não aparecem
**Problema**: Problemas de backend Matplotlib
**Solução**: Garanta que backend está configurado corretamente; use `plt.show()` se necessário

### Problema: Muitas features poluindo plots
**Problema**: `max_display=10` padrão pode ser muito ou pouco
**Solução**: Ajuste parâmetro `max_display` ou use clustering de features

### Problema: Computação lenta
**Problema**: Computar SHAP para datasets muito grandes
**Solução**: Amostra subset, use batching ou garanta uso de explainer especializado (não KernelExplainer)

## Integração com Outras Ferramentas

### Jupyter Notebooks
- Plots force interativos funcionam perfeitamente
- Exibição inline de plots com `show=True` (padrão)
- Combine com markdown para explicações narrativas

### MLflow / Experiment Tracking
```python
import mlflow

with mlflow.start_run():
    # Treine modelo
    model = train_model(X_train, y_train)

    # Compute SHAP
    explainer = shap.TreeExplainer(model)
    shap_values = explainer(X_test)

    # Log plots
    shap.plots.beeswarm(shap_values, show=False)
    mlflow.log_figure(plt.gcf(), "shap_beeswarm.png")
    plt.close()

    # Log métricas de importância de features
    mean_abs_shap = np.abs(shap_values.values).mean(axis=0)
    for feature, importance in zip(X_test.columns, mean_abs_shap):
        mlflow.log_metric(f"shap_{feature}", importance)
```

### Production APIs
```python
class ExplanationService:
    def __init__(self, model_path, explainer_path):
        self.model = joblib.load(model_path)
        self.explainer = joblib.load(explainer_path)

    def predict_with_explanation(self, X):
        prediction = self.model.predict(X)
        shap_values = self.explainer(X)

        return {
            'prediction': prediction[0],
            'base_value': shap_values.base_values[0],
            'feature_contributions': dict(zip(X.columns, shap_values.values[0]))
        }
```

## Documentação de Referência

Essa skill inclui documentação de referência abrangente organizada por tópico:

### references/explainers.md
Guia completo sobre todas as classes de explainer:
- `TreeExplainer` - Explicações rápidas e exatas para modelos baseados em árvores
- `DeepExplainer` - Modelos de deep learning (TensorFlow, PyTorch)
- `KernelExplainer` - Agnóstico de modelo (funciona com qualquer modelo)
- `LinearExplainer` - Explicações rápidas para modelos lineares
- `GradientExplainer` - Baseado em gradientes para redes neurais
- `PermutationExplainer` - Exato mas lento para qualquer modelo

Inclui: Parâmetros de construtor, métodos, modelos suportados, quando usar, exemplos, considerações de performance.

### references/plots.md
Guia de visualização abrangente:
- **Waterfall plots** - Decomposições de predições individuais
- **Beeswarm plots** - Importância global com distribuições de valores
- **Bar plots** - Resumos limpos de importância de features
- **Scatter plots** - Relações feature-predição e interações
- **Force plots** - Visualizações de força aditiva interativas
- **Heatmap plots** - Grades de comparação multi-amostra
- **Violin plots** - Alternativas focadas em distribuição
- **Decision plots** - Caminhos de predição multiclass

Inclui: Parâmetros, casos de uso, exemplos, boas práticas, guia de seleção de plots.

### references/workflows.md
Workflows detalhados e boas práticas:
- Workflow de explicação básica de modelo
- Depuração e validação de modelo
- Orientação de engenharia de features
- Comparação e seleção de modelos
- Análise de justiça e viés
- Explicação de modelos de deep learning
- Deployment em produção
- Explicação de modelos de série temporal
- Armadilhas comuns e soluções
- Técnicas avançadas
- Integração com MLOps

Inclui: Instruções passo a passo, exemplos de código, critérios de decisão, troubleshooting.

### references/theory.md
Fundações teóricas:
- Valores de Shapley da teoria dos jogos
- Fórmulas matemáticas e propriedades
- Conexão com outros métodos de explicação (LIME, DeepLIFT, etc.)
- Algoritmos de computação SHAP (Tree SHAP, Kernel SHAP, etc.)
- Expectativas condicionais e seleção de baseline
- Interpretando valores SHAP
- Valores de interação
- Limitações teóricas e considerações

Inclui: Fundações matemáticas, provas, comparações, tópicos avançados.

## Diretrizes de Uso

**Quando carregar arquivos de referência**:
- Carregue `explainers.md` quando usuário precisar de informações detalhadas sobre tipos específicos de explainers ou parâmetros
- Carregue `plots.md` quando usuário precisar de orientação detalhada de visualização ou exploração de opções de plots
- Carregue `workflows.md` quando usuário tiver tarefas complexas multi-etapa (depuração, análise de justiça, deployment em produção)
- Carregue `theory.md` quando usuário perguntar sobre fundações teóricas, valores de Shapley ou detalhes matemáticos

**Abordagem padrão** (sem carregar referências):
- Use esse SKILL.md para explicações básicas e início rápido
- Forneça workflows padrão e padrões comuns
- Arquivos de referência estão disponíveis se mais detalhe for necessário

**Carregando referências**:
```python
# Para carregar arquivos de referência, use a ferramenta Read com caminho apropriado:
# /path/to/shap/references/explainers.md
# /path/to/shap/references/plots.md
# /path/to/shap/references/workflows.md
# /path/to/shap/references/theory.md
```

## Resumo de Boas Práticas

1. **Escolha o explainer correto**: Use explainers especializados (TreeExplainer, DeepExplainer, LinearExplainer) quando possível; evite KernelExplainer a menos que necessário

2. **Comece global, depois vá local**: Comece com plots beeswarm/bar para entendimento geral, depois mergulhe em plots waterfall/scatter para detalhes

3. **Use múltiplas visualizações**: Diferentes plots revelam diferentes insights; combine vistas global (beeswarm) + local (waterfall) + relação (scatter)

4. **Selecione background data apropriado**: Use 50-1000 amostras representativas dos dados de treinamento

5. **Entenda unidades de saída de modelo**: Saiba se explicando probabilidades, log-odds ou saídas brutas

6. **Valide com conhecimento de domínio**: SHAP mostra comportamento de modelo; use expertise de domínio para interpretar e validar

7. **Otimize para performance**: Amostra subsets para visualização, batch para datasets grandes, cache explainers em produção

8. **Verifique vazamento de dados**: Importância de features inesperadamente alta pode indicar problemas de qualidade de dados

9. **Considere correlações de features**: Use opções cientes de correlação de TreeExplainer ou clustering de features para features redundantes

10. **Lembre que SHAP mostra associação, não causalidade**: Use conhecimento de domínio para interpretação causal

## Instalação

```bash
# Instalação básica
uv pip install shap

# Com dependências de visualização
uv pip install shap matplotlib

# Versão mais recente
uv pip install -U shap
```

**Dependências**: numpy, pandas, scikit-learn, matplotlib, scipy

**Opcional**: xgboost, lightgbm, tensorflow, torch (dependendo dos tipos de modelo)

## Recursos Adicionais

- **Documentação Oficial**: https://shap.readthedocs.io/
- **Repositório GitHub**: https://github.com/slundberg/shap
- **Paper Original**: Lundberg & Lee (2017) - "A Unified Approach to Interpreting Model Predictions"
- **Paper Nature MI**: Lundberg et al. (2020) - "From local explanations to global understanding with explainable AI for trees"

Essa skill oferece cobertura abrangente de SHAP para interpretabilidade de modelos em todos os casos de uso e tipos de modelo.
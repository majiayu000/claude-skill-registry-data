---
name: pymc-bayesian-modeling
description: "Modelagem Bayesiana com PyMC. Construa modelos hierárquicos, MCMC (NUTS), inferência variacional, comparação LOO/WAIC, verificações posteriores, para programação probabilística e inferência."
---

# Modelagem Bayesiana com PyMC

## Visão Geral

PyMC é uma biblioteca Python para modelagem Bayesiana e programação probabilística. Construa, ajuste, valide e compare modelos Bayesianos usando a API moderna do PyMC (versão 5.x+), incluindo modelos hierárquicos, amostragem MCMC (NUTS), inferência variacional e comparação de modelos (LOO, WAIC).

## Quando Usar Esta Habilidade

Esta habilidade deve ser usada quando:
- Construir modelos Bayesianos (regressão linear/logística, modelos hierárquicos, séries temporais, etc.)
- Realizar amostragem MCMC ou inferência variacional
- Conduzir verificações preditivas anteriores/posteriores
- Diagnosticar problemas de amostragem (divergências, convergência, ESS)
- Comparar múltiplos modelos usando critérios de informação (LOO, WAIC)
- Implementar quantificação de incerteza através de métodos Bayesianos
- Trabalhar com estruturas de dados hierárquicas/multinível
- Lidar com dados faltantes ou erro de medição de forma principiada

## Fluxo de Trabalho Bayesiano Padrão

Siga este fluxo de trabalho para construir e validar modelos Bayesianos:

### 1. Preparação de Dados

```python
import pymc as pm
import arviz as az
import numpy as np

# Carregar e preparar dados
X = ...  # Preditores
y = ...  # Resultados

# Padronizar preditores para melhor amostragem
X_mean = X.mean(axis=0)
X_std = X.std(axis=0)
X_scaled = (X - X_mean) / X_std
```

**Práticas principais:**
- Padronizar preditores contínuos (melhora eficiência de amostragem)
- Centralizar resultados quando possível
- Lidar explicitamente com dados faltantes (tratar como parâmetros)
- Usar dimensões nomeadas com `coords` para clareza

### 2. Construção do Modelo

```python
coords = {
    'predictors': ['var1', 'var2', 'var3'],
    'obs_id': np.arange(len(y))
}

with pm.Model(coords=coords) as model:
    # Priors
    alpha = pm.Normal('alpha', mu=0, sigma=1)
    beta = pm.Normal('beta', mu=0, sigma=1, dims='predictors')
    sigma = pm.HalfNormal('sigma', sigma=1)

    # Preditor linear
    mu = alpha + pm.math.dot(X_scaled, beta)

    # Verossimilhança
    y_obs = pm.Normal('y_obs', mu=mu, sigma=sigma, observed=y, dims='obs_id')
```

**Práticas principais:**
- Usar priors fracamente informativos (não priors planos)
- Usar `HalfNormal` ou `Exponential` para parâmetros de escala
- Usar dimensões nomeadas (`dims`) em vez de `shape` quando possível
- Usar `pm.Data()` para valores que serão atualizados para previsões

### 3. Verificação Preditiva Anterior

**Sempre valide priors antes de ajustar:**

```python
with model:
    prior_pred = pm.sample_prior_predictive(samples=1000, random_seed=42)

# Visualizar
az.plot_ppc(prior_pred, group='prior')
```

**Verifique:**
- As previsões anteriores cobrem valores razoáveis?
- Valores extremos são plausíveis dado o conhecimento do domínio?
- Se priors geram dados implausíveis, ajuste e re-verifique

### 4. Ajustar Modelo

```python
with model:
    # Opcional: Exploração rápida com ADVI
    # approx = pm.fit(n=20000)

    # Inferência MCMC completa
    idata = pm.sample(
        draws=2000,
        tune=1000,
        chains=4,
        target_accept=0.9,
        random_seed=42,
        idata_kwargs={'log_likelihood': True}  # Para comparação de modelos
    )
```

**Parâmetros principais:**
- `draws=2000`: Número de amostras por cadeia
- `tune=1000`: Amostras de aquecimento (descartadas)
- `chains=4`: Executar 4 cadeias para verificação de convergência
- `target_accept=0.9`: Maior para posteriores difíceis (0.95-0.99)
- Inclua `log_likelihood=True` para comparação de modelos

### 5. Verificar Diagnósticos

**Use o script de diagnóstico:**

```python
from scripts.model_diagnostics import check_diagnostics

results = check_diagnostics(idata, var_names=['alpha', 'beta', 'sigma'])
```

**Verifique:**
- **R-hat < 1.01**: Cadeias convergiram
- **ESS > 400**: Amostras efetivas suficientes
- **Sem divergências**: NUTS amostrou com sucesso
- **Gráficos de traço**: Cadeias devem se misturar bem (caterpillar fuzzy)

**Se problemas surgirem:**
- Divergências → Aumente `target_accept=0.95`, use parametrização não-centrada
- ESS baixo → Amostre mais, reparametrize para reduzir correlação
- R-hat alto → Execute por mais tempo, verifique multimodalidade

### 6. Verificação Preditiva Posterior

**Valide o ajuste do modelo:**

```python
with model:
    pm.sample_posterior_predictive(idata, extend_inferencedata=True, random_seed=42)

# Visualizar
az.plot_ppc(idata)
```

**Verifique:**
- As previsões posteriores capturam padrões de dados observados?
- Desvios sistemáticos são evidentes (especificação errada do modelo)?
- Considere modelos alternativos se o ajuste for ruim

### 7. Analisar Resultados

```python
# Estatísticas resumidas
print(az.summary(idata, var_names=['alpha', 'beta', 'sigma']))

# Distribuições posteriores
az.plot_posterior(idata, var_names=['alpha', 'beta', 'sigma'])

# Estimativas de coeficientes
az.plot_forest(idata, var_names=['beta'], combined=True)
```

### 8. Fazer Previsões

```python
X_new = ...  # Novos valores de preditores
X_new_scaled = (X_new - X_mean) / X_std

with model:
    pm.set_data({'X_scaled': X_new_scaled})
    post_pred = pm.sample_posterior_predictive(
        idata.posterior,
        var_names=['y_obs'],
        random_seed=42
    )

# Extrair intervalos de previsão
y_pred_mean = post_pred.posterior_predictive['y_obs'].mean(dim=['chain', 'draw'])
y_pred_hdi = az.hdi(post_pred.posterior_predictive, var_names=['y_obs'])
```

## Padrões de Modelo Comuns

### Regressão Linear

Para resultados contínuos com relacionamentos lineares:

```python
with pm.Model() as linear_model:
    alpha = pm.Normal('alpha', mu=0, sigma=10)
    beta = pm.Normal('beta', mu=0, sigma=10, shape=n_predictors)
    sigma = pm.HalfNormal('sigma', sigma=1)

    mu = alpha + pm.math.dot(X, beta)
    y = pm.Normal('y', mu=mu, sigma=sigma, observed=y_obs)
```

**Use template:** `assets/linear_regression_template.py`

### Regressão Logística

Para resultados binários:

```python
with pm.Model() as logistic_model:
    alpha = pm.Normal('alpha', mu=0, sigma=10)
    beta = pm.Normal('beta', mu=0, sigma=10, shape=n_predictors)

    logit_p = alpha + pm.math.dot(X, beta)
    y = pm.Bernoulli('y', logit_p=logit_p, observed=y_obs)
```

### Modelos Hierárquicos

Para dados agrupados (use parametrização não-centrada):

```python
with pm.Model(coords={'groups': group_names}) as hierarchical_model:
    # Hiperpriors
    mu_alpha = pm.Normal('mu_alpha', mu=0, sigma=10)
    sigma_alpha = pm.HalfNormal('sigma_alpha', sigma=1)

    # Nível de grupo (não-centrado)
    alpha_offset = pm.Normal('alpha_offset', mu=0, sigma=1, dims='groups')
    alpha = pm.Deterministic('alpha', mu_alpha + sigma_alpha * alpha_offset, dims='groups')

    # Nível de observação
    mu = alpha[group_idx]
    sigma = pm.HalfNormal('sigma', sigma=1)
    y = pm.Normal('y', mu=mu, sigma=sigma, observed=y_obs)
```

**Use template:** `assets/hierarchical_model_template.py`

**Crítico:** Sempre use parametrização não-centrada para modelos hierárquicos para evitar divergências.

### Regressão de Poisson

Para dados de contagem:

```python
with pm.Model() as poisson_model:
    alpha = pm.Normal('alpha', mu=0, sigma=10)
    beta = pm.Normal('beta', mu=0, sigma=10, shape=n_predictors)

    log_lambda = alpha + pm.math.dot(X, beta)
    y = pm.Poisson('y', mu=pm.math.exp(log_lambda), observed=y_obs)
```

Para contagens sobredispersas, use `NegativeBinomial` em vez disso.

### Séries Temporais

Para processos autorregressivos:

```python
with pm.Model() as ar_model:
    sigma = pm.HalfNormal('sigma', sigma=1)
    rho = pm.Normal('rho', mu=0, sigma=0.5, shape=ar_order)
    init_dist = pm.Normal.dist(mu=0, sigma=sigma)

    y = pm.AR('y', rho=rho, sigma=sigma, init_dist=init_dist, observed=y_obs)
```

## Comparação de Modelos

### Comparando Modelos

Use LOO ou WAIC para comparação de modelos:

```python
from scripts.model_comparison import compare_models, check_loo_reliability

# Ajustar modelos com log_likelihood
models = {
    'Model1': idata1,
    'Model2': idata2,
    'Model3': idata3
}

# Comparar usando LOO
comparison = compare_models(models, ic='loo')

# Verificar confiabilidade
check_loo_reliability(models)
```

**Interpretação:**
- **Δloo < 2**: Modelos são similares, escolha modelo mais simples
- **2 < Δloo < 4**: Evidência fraca para modelo melhor
- **4 < Δloo < 10**: Evidência moderada
- **Δloo > 10**: Evidência forte para modelo melhor

**Verifique valores de Pareto-k:**
- k < 0.7: LOO confiável
- k > 0.7: Considere WAIC ou validação cruzada k-fold

### Média de Modelos

Quando modelos são similares, calcule média das previsões:

```python
from scripts.model_comparison import model_averaging

averaged_pred, weights = model_averaging(models, var_name='y_obs')
```

## Guia de Seleção de Distribuição

### Para Priors

**Parâmetros de escala** (σ, τ):
- `pm.HalfNormal('sigma', sigma=1)` - Escolha padrão
- `pm.Exponential('sigma', lam=1)` - Alternativa
- `pm.Gamma('sigma', alpha=2, beta=1)` - Mais informativo

**Parâmetros sem restrição**:
- `pm.Normal('theta', mu=0, sigma=1)` - Para dados padronizados
- `pm.StudentT('theta', nu=3, mu=0, sigma=1)` - Robusto para outliers

**Parâmetros positivos**:
- `pm.LogNormal('theta', mu=0, sigma=1)`
- `pm.Gamma('theta', alpha=2, beta=1)`

**Probabilidades**:
- `pm.Beta('p', alpha=2, beta=2)` - Fracamente informativo
- `pm.Uniform('p', lower=0, upper=1)` - Não-informativo (use com moderação)

**Matrizes de correlação**:
- `pm.LKJCorr('corr', n=n_vars, eta=2)` - eta=1 uniforme, eta>1 prefere identidade

### Para Verossimilhanças

**Resultados contínuos**:
- `pm.Normal('y', mu=mu, sigma=sigma)` - Padrão para dados contínuos
- `pm.StudentT('y', nu=nu, mu=mu, sigma=sigma)` - Robusto para outliers

**Dados de contagem**:
- `pm.Poisson('y', mu=lambda)` - Contagens equidispersas
- `pm.NegativeBinomial('y', mu=mu, alpha=alpha)` - Contagens sobredispersas
- `pm.ZeroInflatedPoisson('y', psi=psi, mu=mu)` - Zeros em excesso

**Resultados binários**:
- `pm.Bernoulli('y', p=p)` ou `pm.Bernoulli('y', logit_p=logit_p)`

**Resultados categóricos**:
- `pm.Categorical('y', p=probs)`

**Veja:** `references/distributions.md` para referência abrangente de distribuições

## Amostragem e Inferência

### MCMC com NUTS

Padrão e recomendado para maioria dos modelos:

```python
idata = pm.sample(
    draws=2000,
    tune=1000,
    chains=4,
    target_accept=0.9,
    random_seed=42
)
```

**Ajuste quando necessário:**
- Divergências → `target_accept=0.95` ou maior
- Amostragem lenta → Use ADVI para inicialização
- Parâmetros discretos → Use `pm.Metropolis()` para variáveis discretas

### Inferência Variacional

Aproximação rápida para exploração ou inicialização:

```python
with model:
    approx = pm.fit(n=20000, method='advi')

    # Usar para inicialização
    start = approx.sample(return_inferencedata=False)[0]
    idata = pm.sample(start=start)
```

**Trade-offs:**
- Muito mais rápido que MCMC
- Aproximado (pode subestimar incerteza)
- Bom para modelos grandes ou exploração rápida

**Veja:** `references/sampling_inference.md` para guia detalhado de amostragem

## Scripts de Diagnóstico

### Diagnósticos Abrangentes

```python
from scripts.model_diagnostics import create_diagnostic_report

create_diagnostic_report(
    idata,
    var_names=['alpha', 'beta', 'sigma'],
    output_dir='diagnostics/'
)
```

Cria:
- Gráficos de traço
- Gráficos de classificação (verificação de mistura)
- Gráficos de autocorrelação
- Gráficos de energia
- Evolução de ESS
- CSV com estatísticas resumidas

### Verificação Rápida de Diagnóstico

```python
from scripts.model_diagnostics import check_diagnostics

results = check_diagnostics(idata)
```

Verifica R-hat, ESS, divergências e profundidade da árvore.

## Problemas Comuns e Soluções

### Divergências

**Sintoma:** `idata.sample_stats.diverging.sum() > 0`

**Soluções:**
1. Aumente `target_accept=0.95` ou `0.99`
2. Use parametrização não-centrada (modelos hierárquicos)
3. Adicione priors mais fortes para restringir parâmetros
4. Verifique especificação errada do modelo

### Tamanho Efetivo de Amostra Baixo

**Sintoma:** `ESS < 400`

**Soluções:**
1. Amostre mais: `draws=5000`
2. Reparametrize para reduzir correlação posterior
3. Use decomposição QR para regressão com preditores correlacionados

### R-hat Alto

**Sintoma:** `R-hat > 1.01`

**Soluções:**
1. Execute cadeias mais longas: `tune=2000, draws=5000`
2. Verifique multimodalidade
3. Melhore inicialização com ADVI

### Amostragem Lenta

**Soluções:**
1. Use inicialização ADVI
2. Reduza complexidade do modelo
3. Aumente paralelização: `cores=8, chains=8`
4. Use inferência variacional se apropriado

## Melhores Práticas

### Construção de Modelo

1. **Sempre padronize preditores** para melhor amostragem
2. **Use priors fracamente informativos** (não planos)
3. **Use dimensões nomeadas** (`dims`) para clareza
4. **Parametrização não-centrada** para modelos hierárquicos
5. **Verifique preditiva anterior** antes de ajustar

### Amostragem

1. **Execute múltiplas cadeias** (pelo menos 4) para convergência
2. **Use `target_accept=0.9`** como linha de base (maior se necessário)
3. **Inclua `log_likelihood=True`** para comparação de modelos
4. **Defina seed aleatória** para reprodutibilidade

### Validação

1. **Verifique diagnósticos** antes de interpretação (R-hat, ESS, divergências)
2. **Verificação preditiva posterior** para validação de modelo
3. **Compare múltiplos modelos** quando apropriado
4. **Reporte incerteza** (intervalos HDI, não apenas estimativas pontuais)

### Fluxo de Trabalho

1. Comece simples, adicione complexidade gradualmente
2. Verificação preditiva anterior → Ajuste → Diagnósticos → Verificação preditiva posterior
3. Itere sobre especificação de modelo baseado em verificações
4. Documente suposições e escolhas de priors

## Recursos

Esta habilidade inclui:

### Referências (`references/`)

- **`distributions.md`**: Catálogo abrangente de distribuições PyMC organizado por categoria (contínua, discreta, multivariada, mistura, séries temporais). Use ao selecionar priors ou verossimilhanças.

- **`sampling_inference.md`**: Guia detalhado para algoritmos de amostragem (NUTS, Metropolis, SMC), inferência variacional (ADVI, SVGD) e tratamento de problemas de amostragem. Use ao encontrar problemas de convergência ou escolher métodos de inferência.

- **`workflows.md`**: Exemplos de fluxo de trabalho completo e padrões de código para tipos de modelo comuns, preparação de dados, seleção de priors e validação de modelo. Use como livro de receitas para análises Bayesianas padrão.

### Scripts (`scripts/`)

- **`model_diagnostics.py`**: Verificação de diagnóstico automatizada e geração de relatórios. Funções: `check_diagnostics()` para verificações rápidas, `create_diagnostic_report()` para análise abrangente com gráficos.

- **`model_comparison.py`**: Utilitários de comparação de modelos usando LOO/WAIC. Funções: `compare_models()`, `check_loo_reliability()`, `model_averaging()`.

### Templates (`assets/`)

- **`linear_regression_template.py`**: Template completo para regressão linear Bayesiana com fluxo de trabalho completo (preparação de dados, verificações de priors, ajuste, diagnósticos, previsões).

- **`hierarchical_model_template.py`**: Template completo para modelos hierárquicos/multinível com parametrização não-centrada e análise em nível de grupo.

## Referência Rápida

### Construção de Modelo
```python
with pm.Model(coords={'var': names}) as model:
    # Priors
    param = pm.Normal('param', mu=0, sigma=1, dims='var')
    # Verossimilhança
    y = pm.Normal('y', mu=..., sigma=..., observed=data)
```

### Amostragem
```python
idata = pm.sample(draws=2000, tune=1000, chains=4, target_accept=0.9)
```

### Diagnósticos
```python
from scripts.model_diagnostics import check_diagnostics
check_diagnostics(idata)
```

### Comparação de Modelos
```python
from scripts.model_comparison import compare_models
compare_models({'m1': idata1, 'm2': idata2}, ic='loo')
```

### Previsões
```python
with model:
    pm.set_data({'X': X_new})
    pred = pm.sample_posterior_predictive(idata.posterior)
```

## Notas Adicionais

- PyMC se integra com ArviZ para visualização e diagnósticos
- Use `pm.model_to_graphviz(model)` para visualizar estrutura do modelo
- Salve resultados com `idata.to_netcdf('results.nc')`
- Carregue com `az.from_netcdf('results.nc')`
- Para modelos muito grandes, considere ADVI minibatch ou subamostragem de dados
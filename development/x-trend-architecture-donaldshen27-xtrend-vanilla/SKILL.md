---
name: x-trend-architecture
description: Use when implementing X-Trend or attention-based trading models. Covers LSTM encoders, cross-attention, self-attention, sequence representations, entity embeddings, Variable Selection Networks, encoder-decoder patterns, Deep Momentum Networks, and interpretable predictions for trend-following strategies.
---

# X-Trend Architecture

## Purpose

Complete guide to implementing the X-Trend (Cross Attentive Time-Series Trend Network) architecture, combining LSTMs, attention mechanisms, and few-shot learning for trend-following strategies.

## When to Use

Activate this skill when:
- Implementing X-Trend or similar attention-based trading models
- Building encoder-decoder architectures for finance
- Using cross-attention mechanisms
- Implementing Deep Momentum Networks (DMNs)
- Creating interpretable trading predictions
- Combining forecasting with position-taking

## Architecture Overview

```
Input: Target sequence x[t] + Context set C
       ↓
[Encoder]
   - LSTM for sequences
   - Entity embeddings
   - Variable Selection Network (VSN)
   - Self-attention over context
   - Cross-attention: target ← context
       ↓
[Decoder]
   - LSTM with encoder output
   - Dual heads: Forecast + Position
   - PTP (Predictive distribution To Position)
       ↓
Output: Trading position z[t] ∈ [-1, 1]
        + Forecast distribution (μ, σ) or quantiles
```

## Core Components

### 1. Input Features

The model takes 8-dimensional feature vectors combining:
- **Normalized returns** at multiple timescales (5 features): 1, 21, 63, 126, 252 days
- **MACD indicators** at multiple (S,L) pairs (3 features): (8,24), (16,28), (32,96)

Normalization formula for returns:
```
r_hat[t-t', t] = r[t-t',t] / (σ[t] * sqrt(t'))
```

**IMPORTANT**: Use EWMA (exponentially weighted moving average) for volatility calculation:
```python
volatility = prices.pct_change().ewm(span=60).std()
```

See [IMPLEMENTATION.md](IMPLEMENTATION.md#input-features) for full code.

### 2. Variable Selection Network (VSN)

Learns to weight different input features dynamically:

- Transforms each feature with dedicated FFN: `v[j,t] = FFN_j(x[j,t])`
- Computes attention weights: `w[t] = softmax(FFN_weight(x[t]))`
- Produces weighted sum: `VSN(x[t]) = Σ w[j,t] * v[j,t]`

**Purpose**: Automatically determines which features (returns vs MACD, short-term vs long-term) are most relevant at each time step.

See [IMPLEMENTATION.md](IMPLEMENTATION.md#variable-selection-network-vsn) for PyTorch implementation.

### 3. Entity Embeddings

Learn asset-specific representations:

- Each asset gets learnable embedding vector
- Automatically clusters similar assets (equities, commodities, etc.)
- Added to sequence representations for few-shot learning

**Important**: Exclude entity embeddings for zero-shot learning (unseen assets).

See [IMPLEMENTATION.md](IMPLEMENTATION.md#entity-embeddings) for code.

### 4. Sequence Encoder

LSTM-based encoder with skip connections:

1. VSN for feature selection
2. LSTM for temporal modeling
3. LayerNorm + skip connections for stability
4. FFN with entity embedding
5. Final residual connection

**Architecture Pattern**: `x → VSN → LSTM → (+skip) → LayerNorm → FFN(+entity) → (+skip) → LayerNorm`

See [IMPLEMENTATION.md](IMPLEMENTATION.md#sequence-encoder) for full implementation.

### 5. Cross-Attention Mechanism

Target sequence attends to context sequences:

```
Attention(Q, K, V) = softmax(QK^T / √d) V

where:
- Q (queries): From target sequence
- K (keys): From context sequences
- V (values): From context sequences
```

**Multi-head attention** (4 heads recommended) allows model to focus on different aspects simultaneously.

See [IMPLEMENTATION.md](IMPLEMENTATION.md#cross-attention-mechanism) for code.

### 6. Self-Attention Over Context

Context sequences attend to each other before cross-attention:

- Identifies similarities between different context sequences
- Helps model understand relationships within context set
- Uses same attention mechanism as cross-attention (Q=K=V=context)

**Flow**: Context → Self-Attention → Cross-Attention with Target

See [IMPLEMENTATION.md](IMPLEMENTATION.md#self-attention-over-context) for implementation.

### 7. X-Trend Encoder

Combines all encoder components:

1. Encode each context sequence (LSTM + VSN + entity embedding)
2. Apply self-attention over context encodings
3. Encode target sequence
4. Apply cross-attention: target queries context
5. FFN with residual connection

**Output**: Enriched target representation informed by context patterns.

See [IMPLEMENTATION.md](IMPLEMENTATION.md#x-trend-encoder) for complete code.

### 8. Decoder

Produces trading signals and forecasts:

**Inputs**: Target features + Encoder output
**Outputs**: Position z[t] ∈ [-1,1] + Forecast (μ, σ) or quantiles

**Architecture**:
1. VSN on target features
2. Concatenate with encoder output
3. LSTM processing
4. Dual prediction heads:
   - **Forecast head**: Predicts return distribution
   - **Position head**: Either PTP (uses forecast) or direct Sharpe

**Three Variants**:
- **X-Trend**: Direct Sharpe optimization (no forecast)
- **X-Trend-G**: Joint Gaussian MLE + Sharpe
- **X-Trend-Q**: Joint Quantile Regression + Sharpe

See [IMPLEMENTATION.md](IMPLEMENTATION.md#decoder) for implementation details.

### 9. Complete Model

The full X-Trend model combines encoder and decoder:

```python
class XTrendModel(nn.Module):
    def __init__(self, input_dim=8, hidden_dim=64, num_assets=50,
                 forecast_type='gaussian', num_heads=4):
        self.encoder = XTrendEncoder(...)
        self.decoder = XTrendDecoder(...)

    def forward(self, target_features, target_asset_id,
               context_features, context_asset_ids, use_ptp=True):
        # Encode with attention over context
        encoder_output, attention_weights = self.encoder(...)

        # Decode to position + forecast
        position, forecast = self.decoder(...)

        return position, forecast, attention_weights
```

See [IMPLEMENTATION.md](IMPLEMENTATION.md#complete-x-trend-model) for full code.

## Training

### Loss Functions

**Sharpe Loss**:
```python
L_Sharpe = -sqrt(252) * mean(returns) / std(returns)
```

**Gaussian MLE Loss**:
```python
L_MLE = -log p(r | μ, σ)
```

**Joint Loss**:
```python
L_joint = α * L_forecast + L_Sharpe
```

Where α = 1.0 for Gaussian, α = 5.0 for Quantile.

### Training Protocol

1. **Episodic Learning**: Train in episodes, not mini-batches
2. **Sample target** (asset, time) from training set
3. **Sample context set** causally (before target time)
4. **Forward pass** through encoder + decoder
5. **Compute joint loss** balancing forecasting and trading
6. **Backward pass** with gradient clipping (max norm = 10.0)

### Hyperparameters

```python
{
    'input_dim': 8,
    'hidden_dim': 64,
    'num_assets': 50,
    'num_heads': 4,
    'context_size': 20,
    'seq_len': 126,        # 6 months
    'learning_rate': 1e-3,
    'alpha': 1.0,          # Joint loss weight
    'dropout': 0.3,
    'target_vol': 0.15
}
```

See [TRAINING.md](TRAINING.md) for complete training guide including:
- Full training loop implementation
- Validation procedures
- Optimizer configuration
- Common training issues and solutions

## Interpretation

### Attention Weights

Visualize which context sequences the model attends to:

```python
_, _, attention_weights = model(target, context)
# Shape: (batch, num_heads, seq_len, num_contexts)

# Average across heads and time
avg_attention = attention_weights.mean(dim=(0, 1, 2))

# Top 3 most important contexts
top_k = torch.topk(avg_attention, k=3)
```

**Use for**:
- Understanding model decisions
- Debugging unexpected predictions
- Validating that model uses context meaningfully

See [IMPLEMENTATION.md](IMPLEMENTATION.md#interpretation) for visualization code.

## Best Practices

### DO:

✅ **Use LayerNorm + skip connections** for stable training
✅ **Entity embeddings for few-shot** but exclude for zero-shot
✅ **Multi-head attention** (4 heads is good default)
✅ **Joint loss training** balances forecasting and trading
✅ **Episodic training** mimics test-time usage
✅ **Gradient clipping** (max norm = 10.0)
✅ **EWMA for volatility** (span=60) not simple rolling std
✅ **Monitor attention weights** to ensure meaningful patterns

### DON'T:

❌ **Don't skip warm-up** - first 63 predictions are unstable
❌ **Don't use entity embeddings in zero-shot** - model hasn't seen asset
❌ **Don't mix training data** - use episodes, not mini-batches
❌ **Don't ignore attention interpretation** - helps debug
❌ **Don't forget dropout** (0.3-0.5) for regularization
❌ **Don't use simple rolling std** - use EWMA for volatility

## Performance Expectations

Based on X-Trend paper results (2018-2023):

**Few-Shot Learning:**
- Baseline: Sharpe = 2.27
- X-Trend-Q: Sharpe = 2.70 (+18.9%)
- vs TSMOM: Sharpe = 0.23 (10× improvement)

**Zero-Shot Learning:**
- Baseline: Sharpe = -0.11 (loss-making)
- X-Trend-G: Sharpe = 0.47 (profitable)
- 5× improvement over baseline

**COVID-19 Recovery:**
- Baseline: 254 days to recover
- X-Trend: 162 days (2× faster)

## Implementation Checklist

When implementing X-Trend:

- [ ] Input features with EWMA volatility normalization
- [ ] Variable Selection Network for feature weighting
- [ ] Entity embeddings (few-shot) or exclude (zero-shot)
- [ ] LSTM encoders with LayerNorm and skip connections
- [ ] Self-attention over context set
- [ ] Multi-head cross-attention (4 heads)
- [ ] Decoder with dual prediction heads
- [ ] Joint loss function (α * L_forecast + L_Sharpe)
- [ ] Episodic training loop
- [ ] Gradient clipping (max norm = 10.0)
- [ ] Dropout regularization (0.3-0.5)
- [ ] CPD-based context sampling for best performance
- [ ] Attention weight visualization for interpretation

## Architecture Variants

### X-Trend (Base)
- **Objective**: Direct Sharpe optimization
- **Heads**: Position only (no forecast)
- **Best for**: Pure trading performance

### X-Trend-G (Gaussian)
- **Objective**: Joint MLE + Sharpe (α=1.0)
- **Forecast**: Gaussian (μ, σ)
- **Best for**: Balanced forecasting + trading

### X-Trend-Q (Quantile)
- **Objective**: Joint Quantile + Sharpe (α=5.0)
- **Forecast**: 13 quantiles
- **Best for**: Robust predictions, tail risk

## Related Skills

- `financial-time-series` - Input features, returns, momentum
- `few-shot-learning-finance` - Episodic training, context construction
- `change-point-detection` - CPD for context set improvement

## Reference Files

- [IMPLEMENTATION.md](IMPLEMENTATION.md) - Complete PyTorch implementations of all components
- [TRAINING.md](TRAINING.md) - Training loop, loss functions, hyperparameters, best practices

## References

- Attention Is All You Need (Vaswani et al. 2017)
- Deep Momentum Networks (Lim, Zohren, Roberts 2019)
- Attentive Neural Processes (Kim et al. 2019)
- X-Trend: Cross-Attentive Time-Series Trend Network (Wood, Kessler, Roberts, Zohren 2024)

---

**Last Updated**: Based on X-Trend paper (March 2024)
**Skill Type**: Architecture + Implementation
**Line Count**: ~370 (under 500-line rule ✅)

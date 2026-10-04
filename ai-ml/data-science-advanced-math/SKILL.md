---
name: data-science-advanced-math
description: Especialista em Matemática Avançada, Álgebra Linear, Topologia, Cálculo Diferencial e Otimização para Machine Learning e Ciência de Dados baseado nas obras Algebra, Topology, Differential Calculus, and Optimization Theory for CS and ML (Jean Gallier, Jocelyn Quaintance), Numerical Algorithms (Justin Solomon) e Essential Math for Data Science (Thomas Nield). Cobre Álgebra Linear e Fatorações Matriciais (SVD, Cholesky, QR, Moore-Penrose, Autovalores), Cálculo Tensorial e Backpropagation (Jacobianos, Hessianos, Taylor Multivariável), Otimização Convexa e Dualidade (Condições KKT, Multiplicadores de Lagrange), Otimizadores Numéricos de 1ª e 2ª Ordem (SGD, AdamW, Newton-Raphson, BFGS, L-BFGS, Levenberg-Marquardt), Sistemas Lineares em Larga Escala (Gradiente Conjugado, GMRES), Topologia de Variedades (Isomap, t-SNE, UMAP) e Inferência Bayesiana/Regularização (MLE, MAP, Lasso, Ridge, Elastic Net).
---

# Matemática Avançada, Álgebra e Otimização para Machine Learning

Esta skill estabelece os fundamentos matemáticos rigorosos e computacionais para modelagem estatística, arquiteturas de Deep Learning, otimização convexa/não-convexa e análise em alta dimensionalidade.

---

## 📐 1. Álgebra Linear Avançada e Fatorações Matriciais para ML

### 1.1 Decomposição em Valores Singulares (SVD)
Para qualquer matriz real $\mathbf{A} \in \mathbb{R}^{m \times n}$:
$$\mathbf{A} = \mathbf{U} \mathbf{\Sigma} \mathbf{V}^T = \sum_{i=1}^r \sigma_i \mathbf{u}_i \mathbf{v}_i^T$$
- $\mathbf{U} \in \mathbb{R}^{m \times m}$ e $\mathbf{V} \in \mathbb{R}^{n \times n}$ são matrizes ortogonais ($\mathbf{U}^T\mathbf{U} = \mathbf{I}, \mathbf{V}^T\mathbf{V} = \mathbf{I}$).
- $\mathbf{\Sigma} = \text{diag}(\sigma_1, \sigma_2, \dots, \sigma_r, 0, \dots, 0)$ com valores singulares ordenados $\sigma_1 \ge \sigma_2 \ge \dots \ge \sigma_r > 0$.
- **Teorema de Eckart-Young-Mirsky (Low-Rank Approximation)**:
  A melhor aproximação de posto $k < r$ em norma de Frobenius ou Espectral é:
  $$\mathbf{A}_k = \sum_{i=1}^k \sigma_i \mathbf{u}_i \mathbf{v}_i^T, \quad \|\mathbf{A} - \mathbf{A}_k\|_F = \sqrt{\sum_{i=k+1}^r \sigma_i^2}$$

### 1.2 Pseudo-Inversa de Moore-Penrose ($\mathbf{A}^+$)
$$\mathbf{A}^+ = \mathbf{V} \mathbf{\Sigma}^+ \mathbf{U}^T$$
Resolve problemas de mínimos quadrados lineares $\min_{\mathbf{x}} \|\mathbf{A}\mathbf{x} - \mathbf{b}\|_2^2$ com solução de norma mínima $\mathbf{x}^* = \mathbf{A}^+ \mathbf{b}$.

### 1.3 Fatorações de Cholesky e QR
- **Cholesky ($\mathbf{A} = \mathbf{L}\mathbf{L}^T$)**: Para matrizes simétricas e definidas positivas (SPD), computacionalmente duas vezes mais rápida que decomposição LU. Essencial para Processos Gaussianos e Amostragem MCMC.
- **QR ($\mathbf{A} = \mathbf{Q}\mathbf{R}$)**: Fatora em matriz ortogonal $\mathbf{Q}$ e triangular superior $\mathbf{R}$, fornecendo máxima estabilidade numérica para regressões.

---

## 📈 2. Cálculo Diferencial Multivariável e Cálculo Tensorial

### 2.1 Vetor Gradiente, Matriz Jacobiana e Hessiana
Dado um campo escalar $f: \mathbb{R}^n \to \mathbb{R}$ e uma função vetorial $\mathbf{F}: \mathbb{R}^n \to \mathbb{R}^m$:
- **Vetor Gradiente**: $\nabla f(\mathbf{x}) = \left[ \frac{\partial f}{\partial x_1}, \dots, \frac{\partial f}{\partial x_n} \right]^T \in \mathbb{R}^n$
- **Matriz Jacobiana**: $\mathbf{J}_{\mathbf{F}}(\mathbf{x}) = \left[ \frac{\partial F_i}{\partial x_j} \right]_{m \times n} \in \mathbb{R}^{m \times n}$
- **Matriz Hessiana (Curvatura de 2ª Ordem)**: $\mathbf{H}_f(\mathbf{x}) = \left[ \frac{\partial^2 f}{\partial x_i \partial x_j} \right]_{n \times n} \in \mathbb{R}^{n \times n}$

### 2.2 Série de Taylor Multivariável de 2ª Ordem
$$f(\mathbf{x} + \Delta\mathbf{x}) \approx f(\mathbf{x}) + \nabla f(\mathbf{x})^T \Delta\mathbf{x} + \frac{1}{2} \Delta\mathbf{x}^T \mathbf{H}_f(\mathbf{x}) \Delta\mathbf{x}$$

### 2.3 Regra da Cadeia Tensorial e Backpropagation
Para funções compostas em grafos computacionais:
$$\frac{\partial L}{\partial \mathbf{W}^{(l)}} = \left( \frac{\partial \mathbf{z}^{(l)}}{\partial \mathbf{W}^{(l)}} \right)^T \frac{\partial L}{\partial \mathbf{z}^{(l)}} = \boldsymbol{\delta}^{(l)} (\mathbf{a}^{(l-1)})^T \quad \text{onde } \boldsymbol{\delta}^{(l)} = (\mathbf{W}^{(l+1)})^T \boldsymbol{\delta}^{(l+1)} \odot \sigma'(\mathbf{z}^{(l)})$$

---

## 🎯 3. Otimização Convexa e Teoria da Dualidade (Gallier & Quaintance)

### 3.1 Problema Padrão de Otimização com Restrições
$$\min_{\mathbf{x} \in \mathbb{R}^n} f_0(\mathbf{x}) \quad \text{sujeito a } f_i(\mathbf{x}) \le 0 \; (i=1,\dots,m), \quad h_j(\mathbf{x}) = 0 \; (j=1,\dots,p)$$

### 3.2 Condições de Karush-Kuhn-Tucker (KKT)
Se o problema for convexo e satisfizer a condição de qualificação de restrições (Slater's condition), as seguintes condições são necessárias e suficientes para a otimalidade $(\mathbf{x}^*, \boldsymbol{\lambda}^*, \boldsymbol{\nu}^*)$:
1. **Estacionariedade**: $\nabla f_0(\mathbf{x}^*) + \sum_{i=1}^m \lambda_i^* \nabla f_i(\mathbf{x}^*) + \sum_{j=1}^p \nu_j^* \nabla h_j(\mathbf{x}^*) = \mathbf{0}$
2. **Viabilidade Primal**: $f_i(\mathbf{x}^*) \le 0 \; (\forall i)$ e $h_j(\mathbf{x}^*) = 0 \; (\forall j)$
3. **Viabilidade Dual**: $\lambda_i^* \ge 0 \; (\forall i=1,\dots,m)$
4. **Folga Complementar**: $\lambda_i^* f_i(\mathbf{x}^*) = 0 \; (\forall i=1,\dots,m)$

---

## ⚡ 4. Otimizadores Numéricos de Primeira e Segunda Ordem

### 4.1 Família Adam / AdamW (Primeira Ordem com Momentos Adaptativos)
$$\mathbf{m}_t = \beta_1 \mathbf{m}_{t-1} + (1 - \beta_1) \mathbf{g}_t, \quad \mathbf{v}_t = \beta_2 \mathbf{v}_{t-1} + (1 - \beta_2) \mathbf{g}_t^2$$
$$\hat{\mathbf{m}}_t = \frac{\mathbf{m}_t}{1 - \beta_1^t}, \quad \hat{\mathbf{v}}_t = \frac{\mathbf{v}_t}{1 - \beta_2^t}$$
- **AdamW (Decaimento de Peso Desacoplado)**:
  $$\boldsymbol{\theta}_{t+1} = \boldsymbol{\theta}_t - \eta \left( \frac{\hat{\mathbf{m}}_t}{\sqrt{\hat{\mathbf{v}}_t} + \epsilon} + \lambda \boldsymbol{\theta}_t \right)$$

### 4.2 Métodos de Segunda Ordem e Quase-Newton (BFGS e L-BFGS)
- **Método de Newton Puro**: $\Delta\mathbf{x} = - \mathbf{H}_f^{-1}(\mathbf{x}) \nabla f(\mathbf{x})$ (custo $\mathcal{O}(n^3)$ proibitivo para redes neurais).
- **L-BFGS (Limited-memory BFGS)**: Mantém apenas os últimos $m$ vetores de deslocamento $\mathbf{s}_k = \mathbf{x}_{k+1} - \mathbf{x}_k$ e variação de gradiente $\mathbf{y}_k = \mathbf{g}_{k+1} - \mathbf{g}_k$, computando a direção de descida em tempo $\mathcal{O}(mn)$ e espaço $\mathcal{O}(mn)$.

---

## 🌐 5. Métodos Iterativos para Sistemas Lineares em Larga Escala (Solomon)

### 5.1 Método do Gradiente Conjugado (CG)
Resolve $\mathbf{A}\mathbf{x} = \mathbf{b}$ para matrizes simétricas definidas positivas (SPD) em no máximo $n$ iterações, gerando direções $\mathbf{A}$-ortogonais ($\mathbf{p}_i^T \mathbf{A} \mathbf{p}_j = 0$ para $i \ne j$):
$$\alpha_k = \frac{\mathbf{r}_k^T \mathbf{r}_k}{\mathbf{p}_k^T \mathbf{A} \mathbf{p}_k}, \quad \mathbf{x}_{k+1} = \mathbf{x}_k + \alpha_k \mathbf{p}_k, \quad \mathbf{r}_{k+1} = \mathbf{r}_k - \alpha_k \mathbf{A} \mathbf{p}_k$$
$$\beta_k = \frac{\mathbf{r}_{k+1}^T \mathbf{r}_{k+1}}{\mathbf{r}_k^T \mathbf{r}_k}, \quad \mathbf{p}_{k+1} = \mathbf{r}_{k+1} + \beta_k \mathbf{p}_k$$

---

## 🗺️ 6. Topologia, Variedades e Redução Não-Linear de Dimensionalidade

### 6.1 Aprendizado em Variedades (Manifold Learning)
- **Isomap**: Preserva distâncias geodésicas calculadas em grafos de $k$-vizinhos mais próximos ($k$-NN) via Dijkstra + Classical Multidimensional Scaling (MDS).
- **t-SNE (t-Distributed Stochastic Neighbor Embedding)**: Modela probabilidades de vizinhança no espaço de alta dimensão com distribuição Gaussiana e no espaço de baixa dimensão com distribuição t-Student (1 grau de liberdade), minimizando a divergência de Kullback-Leibler:
  $$\text{KL}(P \parallel Q) = \sum_i \sum_j p_{j|i} \log \frac{p_{j|i}}{q_{j|i}}$$
- **UMAP (Uniform Manifold Approximation and Projection)**: Baseado em geometria Riemanniana e topologia algébrica (Fuzzy Simplicial Sets), garantindo preservação tanto de estrutura local quanto global.

---

## 🎲 7. Inferência Estatística e Regularização

### 7.1 Regularização L1, L2 e Elastic Net
$$\mathcal{L}_{\text{ElasticNet}}(\mathbf{w}) = \frac{1}{2n} \|\mathbf{y} - \mathbf{X}\mathbf{w}\|_2^2 + \lambda \left( \alpha \|\mathbf{w}\|_1 + \frac{1 - \alpha}{2} \|\mathbf{w}\|_2^2 \right)$$
- **L1 (Lasso, $\alpha=1$)**: Promove esparsidade induzindo pesos exatos a zero devido aos cantos do politopo da norma $L_1$.
- **L2 (Ridge, $\alpha=0$)**: Previne multicolinearidade e suaviza a norma dos coeficientes.

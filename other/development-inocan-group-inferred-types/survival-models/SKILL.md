---
name: survival-models
description: Bayesian survival analysis models including exponential, Weibull, log-normal, and piecewise exponential hazard models with censoring support.
---

# Survival Models

## Data Structure

```stan
data {
  int<lower=0> N;
  vector<lower=0>[N] time;      // Observed/censored time
  array[N] int<lower=0,upper=1> event;  // 1=event, 0=censored
  matrix[N, K] X;               // Covariates
}
```

## Exponential Model

### Stan
```stan
parameters {
  real alpha;           // Log baseline hazard
  vector[K] beta;
}
model {
  alpha ~ normal(0, 2);
  beta ~ normal(0, 1);

  for (n in 1:N) {
    real lambda = exp(alpha + X[n] * beta);
    if (event[n] == 1)
      target += exponential_lpdf(time[n] | lambda);
    else
      target += exponential_lccdf(time[n] | lambda);  // Survival
  }
}
```

### JAGS (with censoring)
```
model {
  for (i in 1:N) {
    is.censored[i] ~ dinterval(t[i], t.cen[i])
    t[i] ~ dexp(lambda[i])
    log(lambda[i]) <- alpha + inprod(X[i,], beta[])
  }
  alpha ~ dnorm(0, 0.25)
  for (k in 1:K) { beta[k] ~ dnorm(0, 1) }
}
```

## Weibull Model

### Stan (AFT Parameterization)
```stan
parameters {
  real alpha;                    // Intercept (log scale)
  vector[K] beta;
  real<lower=0> shape;           // Weibull shape
}
model {
  alpha ~ normal(0, 5);
  beta ~ normal(0, 2);
  shape ~ exponential(1);

  for (n in 1:N) {
    real mu = alpha + X[n] * beta;
    if (event[n] == 1)
      target += weibull_lpdf(time[n] | shape, exp(mu));
    else
      target += weibull_lccdf(time[n] | shape, exp(mu));
  }
}
```

### JAGS
```
model {
  for (i in 1:N) {
    is.censored[i] ~ dinterval(t[i], t.cen[i])
    t[i] ~ dweib(shape, lambda[i])
    log(lambda[i]) <- alpha + inprod(X[i,], beta[])
  }
  shape ~ dgamma(1, 0.001)
  alpha ~ dnorm(0, 0.01)
  for (k in 1:K) { beta[k] ~ dnorm(0, 0.01) }
}
```

## Log-Normal Model

### Stan
```stan
parameters {
  real alpha;
  vector[K] beta;
  real<lower=0> sigma;
}
model {
  for (n in 1:N) {
    real mu = alpha + X[n] * beta;
    if (event[n] == 1)
      target += lognormal_lpdf(time[n] | mu, sigma);
    else
      target += lognormal_lccdf(time[n] | mu, sigma);
  }
}
```

## Piecewise Exponential (Cox-like)

### Stan
```stan
data {
  int<lower=0> N;
  int<lower=0> J;               // Number of intervals
  vector[J] cuts;               // Cut points
  matrix[N, J] d;               // Time in each interval
  array[N] int<lower=0,upper=1> event;
  array[N] int<lower=1,upper=J> interval;  // Event interval
  matrix[N, K] X;
}
parameters {
  vector[J] log_baseline;       // Log baseline hazard per interval
  vector[K] beta;
}
model {
  log_baseline ~ normal(0, 2);
  beta ~ normal(0, 1);

  for (n in 1:N) {
    real log_hazard = log_baseline[interval[n]] + X[n] * beta;

    // Contribution from all intervals
    for (j in 1:J)
      target += -d[n,j] * exp(log_baseline[j] + X[n] * beta);

    // Event contribution
    if (event[n] == 1)
      target += log_hazard;
  }
}
```

## Frailty Model (Random Effects)

### Stan
```stan
data {
  int<lower=0> N;
  int<lower=0> G;               // Number of groups
  array[N] int<lower=1,upper=G> group;
  // ... rest of survival data
}
parameters {
  real alpha;
  vector[K] beta;
  real<lower=0> shape;
  vector[G] frailty_raw;        // Non-centered
  real<lower=0> sigma_frailty;
}
transformed parameters {
  vector[G] frailty = sigma_frailty * frailty_raw;
}
model {
  sigma_frailty ~ exponential(1);
  frailty_raw ~ std_normal();

  for (n in 1:N) {
    real mu = alpha + X[n] * beta + frailty[group[n]];
    // ... Weibull likelihood with censoring
  }
}
```

## Generated Quantities

```stan
generated quantities {
  // Hazard ratio for 1-unit increase in X[,1]
  real HR = exp(beta[1]);

  // Median survival at X=0
  real median_survival = exp(alpha) * pow(log(2), 1/shape);

  // Survival function at time t=1
  array[N] real S_1;
  for (n in 1:N)
    S_1[n] = exp(-pow(1 / exp(alpha + X[n] * beta), shape));
}
```

## Interpretation

- **Weibull shape**: <1 decreasing hazard, =1 constant (exponential), >1 increasing
- **HR**: Hazard ratio (multiplicative effect on hazard)
- **AFT**: Accelerated failure time (multiplicative effect on survival time)

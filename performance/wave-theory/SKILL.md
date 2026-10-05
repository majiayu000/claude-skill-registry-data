---
name: wave-theory
version: 1.0.0
description: Ocean wave theory including wave spectra, statistics, irregular seas, and wave transformation for offshore engineering
author: workspace-hub
category: subject-matter-expert
tags: [waves, wave-theory, spectra, jonswap, pierson-moskowitz, wave-statistics, irregular-seas]
platforms: [engineering]
---

# Wave Theory SME Skill

Comprehensive ocean wave theory expertise including wave mechanics, spectral analysis, wave statistics, and irregular sea modeling for offshore engineering applications.

## When to Use This Skill

Use wave theory knowledge when:
- **Wave spectra** - JONSWAP, Pierson-Moskowitz, scatter diagrams
- **Wave statistics** - Significant wave height, spectral parameters
- **Irregular seas** - Generate time series from spectra
- **Wave kinematics** - Particle velocities and accelerations
- **Wave transformation** - Shoaling, refraction, diffraction
- **Extreme values** - Design wave estimation

## Core Knowledge Areas

### 1. Regular Wave Theory

**Linear (Airy) Wave Theory:**
```python
import numpy as np

def airy_wave_properties(
    H: float,
    T: float,
    d: float,
    g: float = 9.81
) -> dict:
    """
    Calculate Airy wave properties.

    Valid for: H/L < 0.14, d/L > 0.5 (deep water) or d/L < 0.05 (shallow)

    Args:
        H: Wave height (m)
        T: Wave period (s)
        d: Water depth (m)
        g: Gravity (m/s²)

    Returns:
        Wave properties dictionary
    """
    # Wave frequency
    omega = 2 * np.pi / T

    # Dispersion relation: ω² = gk·tanh(kd)
    # Solve iteratively for wave number k
    from scipy.optimize import fsolve

    def dispersion(k):
        return omega**2 - g * k * np.tanh(k * d)

    k0 = omega**2 / g  # Deep water approximation
    k = fsolve(dispersion, k0)[0]

    # Wave length
    L = 2 * np.pi / k

    # Wave celerity (phase speed)
    C = omega / k

    # Group velocity
    n = 0.5 * (1 + 2*k*d / np.sinh(2*k*d))  # Shoaling coefficient
    Cg = n * C

    # Deep water classification
    if d / L > 0.5:
        regime = "Deep water"
    elif d / L < 0.05:
        regime = "Shallow water"
    else:
        regime = "Intermediate"

    return {
        'height_m': H,
        'period_s': T,
        'depth_m': d,
        'wavelength_m': L,
        'wave_number': k,
        'frequency_rad_s': omega,
        'frequency_hz': omega / (2*np.pi),
        'celerity_m_s': C,
        'group_velocity_m_s': Cg,
        'regime': regime,
        'd_over_L': d / L,
        'H_over_L': H / L,
        'steepness': H / L
    }

# Example
wave = airy_wave_properties(H=8, T=12, d=1500)

print(f"Wave Properties (H={wave['height_m']}m, T={wave['period_s']}s):")
print(f"  Wavelength: {wave['wavelength_m']:.1f} m")
print(f"  Regime: {wave['regime']} (d/L = {wave['d_over_L']:.3f})")
print(f"  Celerity: {wave['celerity_m_s']:.2f} m/s")
print(f"  Steepness: {wave['steepness']:.4f}")
```

**Wave Kinematics:**
```python
def wave_particle_kinematics(
    z: float,
    H: float,
    T: float,
    d: float,
    t: float = 0,
    x: float = 0,
    g: float = 9.81
) -> dict:
    """
    Calculate wave particle velocities and accelerations.

    Args:
        z: Vertical position (0 at SWL, negative below)
        H: Wave height (m)
        T: Wave period (s)
        d: Water depth (m)
        t: Time (s)
        x: Horizontal position (m)
        g: Gravity (m/s²)

    Returns:
        Particle kinematics
    """
    # Wave properties
    wave = airy_wave_properties(H, T, d, g)
    k = wave['wave_number']
    omega = wave['frequency_rad_s']

    # Amplitude
    a = H / 2

    # Hyperbolic functions
    cosh_kz_d = np.cosh(k * (z + d))
    sinh_kz_d = np.sinh(k * (z + d))
    cosh_kd = np.cosh(k * d)
    sinh_kd = np.sinh(k * d)

    # Wave phase
    phase = k * x - omega * t

    # Horizontal velocity
    u = (omega * a * cosh_kz_d / sinh_kd) * np.cos(phase)

    # Vertical velocity
    w = (omega * a * sinh_kz_d / sinh_kd) * np.sin(phase)

    # Horizontal acceleration
    ax = -(omega**2 * a * cosh_kz_d / sinh_kd) * np.sin(phase)

    # Vertical acceleration
    az = (omega**2 * a * sinh_kz_d / sinh_kd) * np.cos(phase)

    # Dynamic pressure
    p_dynamic = g * a * (cosh_kz_d / cosh_kd) * np.cos(phase)

    return {
        'horizontal_velocity': u,
        'vertical_velocity': w,
        'horizontal_acceleration': ax,
        'vertical_acceleration': az,
        'dynamic_pressure': p_dynamic,
        'total_velocity': np.sqrt(u**2 + w**2),
        'total_acceleration': np.sqrt(ax**2 + az**2)
    }

# Example: Surface velocity (z=0)
kinematics = wave_particle_kinematics(z=0, H=8, T=12, d=1500, t=0, x=0)

print(f"Surface Particle Kinematics:")
print(f"  Horizontal velocity: {kinematics['horizontal_velocity']:.2f} m/s")
print(f"  Vertical velocity: {kinematics['vertical_velocity']:.2f} m/s")
print(f"  Total velocity: {kinematics['total_velocity']:.2f} m/s")
```

### 2. Wave Spectra

**JONSWAP Spectrum:**
```python
def jonswap_spectrum(
    frequencies: np.ndarray,
    Hs: float,
    Tp: float,
    gamma: float = 3.3,
    alpha: float = None
) -> np.ndarray:
    """
    Calculate JONSWAP wave spectrum.

    S(f) = α g² (2π)^-4 f^-5 exp[-5/4(f/fp)^-4] γ^exp[-(f-fp)²/(2σ²fp²)]

    Args:
        frequencies: Frequency array (Hz)
        Hs: Significant wave height (m)
        Tp: Peak period (s)
        gamma: Peak enhancement factor (3.3 for North Sea)
        alpha: Phillips constant (calculated if None)

    Returns:
        Spectral density S(f) (m²/Hz)
    """
    g = 9.81
    fp = 1 / Tp  # Peak frequency (Hz)

    # Calculate alpha if not provided
    if alpha is None:
        # Relationship: Hs = 4*sqrt(m0)
        # For JONSWAP: alpha ≈ 5.061 * Hs² / Tp⁴ * (1 - 0.287*ln(γ))
        alpha = 5.061 * Hs**2 / Tp**4 * (1 - 0.287 * np.log(gamma))

    # Sigma parameter
    sigma = np.where(frequencies <= fp, 0.07, 0.09)

    # Pierson-Moskowitz spectrum
    S_PM = alpha * g**2 * (2*np.pi)**(-4) * frequencies**(-5) * \
           np.exp(-1.25 * (frequencies / fp)**(-4))

    # Peak enhancement
    r = np.exp(-(frequencies - fp)**2 / (2 * sigma**2 * fp**2))
    gamma_factor = gamma ** r

    # JONSWAP spectrum
    S = S_PM * gamma_factor

    return S

# Example: Generate JONSWAP spectrum
freq = np.linspace(0.01, 0.5, 500)
S = jonswap_spectrum(freq, Hs=8.5, Tp=12.0, gamma=3.3)

# Verify Hs
m0 = np.trapz(S, freq)
Hs_calc = 4 * np.sqrt(m0)

print(f"JONSWAP Spectrum:")
print(f"  Input Hs: 8.5 m")
print(f"  Calculated Hs: {Hs_calc:.2f} m")
print(f"  Peak frequency: {1/12:.4f} Hz")
```

**Pierson-Moskowitz Spectrum:**
```python
def pierson_moskowitz_spectrum(
    frequencies: np.ndarray,
    Hs: float,
    Tp: float = None,
    U19_5: float = None
) -> np.ndarray:
    """
    Calculate Pierson-Moskowitz spectrum (fully developed sea).

    Args:
        frequencies: Frequency array (Hz)
        Hs: Significant wave height (m)
        Tp: Peak period (s) - optional
        U19_5: Wind speed at 19.5m height (m/s) - optional

    Returns:
        Spectral density S(f) (m²/Hz)
    """
    g = 9.81

    if Tp is not None:
        # Use peak period
        fp = 1 / Tp
    elif U19_5 is not None:
        # Calculate from wind speed
        fp = 0.877 * g / (2 * np.pi * U19_5)
    else:
        raise ValueError("Must provide either Tp or U19_5")

    # Phillips constant
    alpha = 0.0081  # For fully developed seas

    # P-M spectrum
    S = alpha * g**2 * (2*np.pi)**(-4) * frequencies**(-5) * \
        np.exp(-1.25 * (frequencies / fp)**(-4))

    return S

# Example
S_PM = pierson_moskowitz_spectrum(freq, Hs=8.5, Tp=12.0)

m0_PM = np.trapz(S_PM, freq)
Hs_PM = 4 * np.sqrt(m0_PM)

print(f"P-M Spectrum Hs: {Hs_PM:.2f} m")
```

### 3. Wave Statistics

**Spectral Parameters:**
```python
def calculate_spectral_parameters(
    S: np.ndarray,
    frequencies: np.ndarray
) -> dict:
    """
    Calculate spectral wave parameters.

    Args:
        S: Wave spectrum (m²/Hz)
        frequencies: Frequency array (Hz)

    Returns:
        Spectral parameters
    """
    # Spectral moments
    m0 = np.trapz(S, frequencies)
    m1 = np.trapz(S * frequencies, frequencies)
    m2 = np.trapz(S * frequencies**2, frequencies)
    m4 = np.trapz(S * frequencies**4, frequencies)

    # Significant wave height
    Hs = 4 * np.sqrt(m0)

    # Mean period
    Tm01 = m0 / m1

    # Zero-crossing period
    Tz = np.sqrt(m0 / m2)

    # Peak period (from spectrum maximum)
    peak_idx = np.argmax(S)
    Tp = 1 / frequencies[peak_idx]

    # Spectral width
    epsilon = np.sqrt(1 - m2**2 / (m0 * m4))

    # Wave steepness
    k_mean = 2 * np.pi / (9.81 * Tz**2 / (2*np.pi))  # Deep water approx
    steepness = k_mean * Hs / 2

    return {
        'm0': m0,
        'm1': m1,
        'm2': m2,
        'm4': m4,
        'Hs': Hs,
        'Tp': Tp,
        'Tz': Tz,
        'Tm01': Tm01,
        'spectral_width': epsilon,
        'steepness': steepness
    }

# Example
params = calculate_spectral_parameters(S, freq)

print(f"Spectral Parameters:")
print(f"  Hs: {params['Hs']:.2f} m")
print(f"  Tp: {params['Tp']:.2f} s")
print(f"  Tz: {params['Tz']:.2f} s")
print(f"  Spectral width: {params['spectral_width']:.3f}")
```

**Wave Height Distribution:**
```python
def rayleigh_distribution(
    H: np.ndarray,
    Hs: float
) -> np.ndarray:
    """
    Rayleigh distribution for wave heights in irregular seas.

    P(H) = probability that wave height exceeds H

    Args:
        H: Wave height array (m)
        Hs: Significant wave height (m)

    Returns:
        Exceedance probability
    """
    # Rayleigh parameter
    H_rms = Hs / np.sqrt(2)

    # Exceedance probability
    P = np.exp(-(H / H_rms)**2)

    return P

def significant_wave_statistics(Hs: float) -> dict:
    """
    Calculate wave statistics from Hs using Rayleigh distribution.

    Args:
        Hs: Significant wave height (m)

    Returns:
        Wave statistics
    """
    H_rms = Hs / np.sqrt(2)

    # Various statistical wave heights
    H_mean = H_rms * np.sqrt(np.pi / 2)
    H_1_10 = H_rms * np.sqrt(2 * np.log(10))  # Average of highest 1/10
    H_1_100 = H_rms * np.sqrt(2 * np.log(100))  # Average of highest 1/100
    H_max_1000 = H_rms * np.sqrt(2 * np.log(1000))  # Most probable max in 1000 waves

    return {
        'Hs': Hs,
        'H_mean': H_mean,
        'H_rms': H_rms,
        'H_1_10': H_1_10,
        'H_1_100': H_1_100,
        'H_max_1000': H_max_1000
    }

# Example
stats = significant_wave_statistics(Hs=8.5)

print(f"Wave Statistics (Hs = {stats['Hs']} m):")
print(f"  Mean height: {stats['H_mean']:.2f} m")
print(f"  H_1/10: {stats['H_1_10']:.2f} m")
print(f"  H_1/100: {stats['H_1_100']:.2f} m")
print(f"  H_max (in 1000 waves): {stats['H_max_1000']:.2f} m")
```

### 4. Time Series Generation

**Generate Irregular Wave Time Series:**
```python
def generate_irregular_wave_time_series(
    S: np.ndarray,
    frequencies: np.ndarray,
    duration: float,
    dt: float,
    random_seed: int = None
) -> tuple[np.ndarray, np.ndarray]:
    """
    Generate irregular wave elevation time series from spectrum.

    Args:
        S: Wave spectrum (m²/Hz)
        frequencies: Frequency array (Hz)
        duration: Duration (s)
        dt: Time step (s)
        random_seed: Random seed for reproducibility

    Returns:
        (time, elevation) arrays
    """
    if random_seed is not None:
        np.random.seed(random_seed)

    # Time array
    time = np.arange(0, duration, dt)

    # Initialize elevation
    eta = np.zeros_like(time)

    # Frequency resolution
    df = frequencies[1] - frequencies[0]

    # Generate wave components
    for i, f in enumerate(frequencies):
        if S[i] > 0:
            # Amplitude from spectrum
            amplitude = np.sqrt(2 * S[i] * df)

            # Random phase
            phase = np.random.uniform(0, 2*np.pi)

            # Wave component
            omega = 2 * np.pi * f
            eta += amplitude * np.cos(omega * time + phase)

    return time, eta

# Example: Generate 1 hour of wave data
t, elevation = generate_irregular_wave_time_series(
    S, freq,
    duration=3600,
    dt=0.1,
    random_seed=42
)

# Verify statistics
Hs_timeseries = 4 * np.std(elevation)

print(f"Time Series Statistics:")
print(f"  Target Hs: {params['Hs']:.2f} m")
print(f"  Generated Hs: {Hs_timeseries:.2f} m")
print(f"  Duration: {len(t) * 0.1 / 3600:.2f} hours")
```

### 5. Wave Scatter Diagrams

**Create Wave Scatter Diagram:**
```python
def create_wave_scatter_diagram(
    Hs_bins: np.ndarray,
    Tp_bins: np.ndarray,
    location_data: dict
) -> np.ndarray:
    """
    Create wave scatter diagram (probability table).

    Args:
        Hs_bins: Hs bin edges (m)
        Tp_bins: Tp bin edges (s)
        location_data: Historical wave data or hindcast

    Returns:
        Probability matrix (sum = 1.0)
    """
    # This is typically based on hindcast data
    # Simplified example using lognormal distribution

    n_Hs = len(Hs_bins) - 1
    n_Tp = len(Tp_bins) - 1

    scatter = np.zeros((n_Hs, n_Tp))

    # Simplified: Tp roughly proportional to sqrt(Hs)
    for i in range(n_Hs):
        Hs_mid = (Hs_bins[i] + Hs_bins[i+1]) / 2

        # Expected Tp for this Hs (empirical: Tp ≈ 3.6*sqrt(Hs))
        Tp_expected = 3.6 * np.sqrt(Hs_mid)

        # Hs occurrence (Weibull distribution)
        from scipy.stats import weibull_min
        p_Hs = weibull_min.pdf(Hs_mid, c=2, scale=2.5)

        # Tp distribution given Hs (normal around expected)
        from scipy.stats import norm
        for j in range(n_Tp):
            Tp_mid = (Tp_bins[j] + Tp_bins[j+1]) / 2
            p_Tp_given_Hs = norm.pdf(Tp_mid, loc=Tp_expected, scale=1.5)

            scatter[i, j] = p_Hs * p_Tp_given_Hs

    # Normalize to probabilities
    scatter /= scatter.sum()

    return scatter

# Example
Hs_bins = np.array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
Tp_bins = np.array([0, 4, 6, 8, 10, 12, 14, 16])

scatter = create_wave_scatter_diagram(Hs_bins, Tp_bins, {})

# Annual hours
annual_hours = scatter * 8760

print(f"Wave Scatter Diagram:")
print(f"  Total probability: {scatter.sum():.4f}")
print(f"  Most probable sea state: Hs={Hs_bins[np.unravel_index(scatter.argmax(), scatter.shape)[0]]}-{Hs_bins[np.unravel_index(scatter.argmax(), scatter.shape)[0]+1]}m")
```

### 6. Extreme Value Analysis

**Design Wave from Return Period:**
```python
def calculate_extreme_wave_height(
    return_period_years: float,
    Hs_annual_max: np.ndarray = None,
    distribution: str = 'weibull'
) -> dict:
    """
    Calculate design wave height for given return period.

    Args:
        return_period_years: Return period (years)
        Hs_annual_max: Array of annual maximum Hs values
        distribution: 'weibull' or 'gumbel'

    Returns:
        Extreme wave height statistics
    """
    from scipy.stats import weibull_min, gumbel_r

    if Hs_annual_max is None:
        # Example data: 25 years of annual maxima
        np.random.seed(42)
        Hs_annual_max = weibull_min.rvs(c=2, scale=10, size=25)

    # Fit distribution
    if distribution == 'weibull':
        params = weibull_min.fit(Hs_annual_max)
        c, loc, scale = params
        dist = weibull_min(c, loc, scale)
    elif distribution == 'gumbel':
        loc, scale = gumbel_r.fit(Hs_annual_max)
        dist = gumbel_r(loc, scale)
    else:
        raise ValueError("Unknown distribution")

    # Exceedance probability for return period
    exceedance_prob = 1 / return_period_years

    # Extreme value
    Hs_extreme = dist.ppf(1 - exceedance_prob)

    # Confidence intervals (simplified)
    Hs_lower = dist.ppf(1 - exceedance_prob - 0.1)
    Hs_upper = dist.ppf(1 - exceedance_prob + 0.1)

    return {
        'return_period_years': return_period_years,
        'Hs_extreme': Hs_extreme,
        'Hs_lower_bound': Hs_lower,
        'Hs_upper_bound': Hs_upper,
        'distribution': distribution,
        'exceedance_probability': exceedance_prob
    }

# Example: 100-year return period
extreme_100yr = calculate_extreme_wave_height(
    return_period_years=100,
    distribution='weibull'
)

print(f"100-Year Wave:")
print(f"  Hs: {extreme_100yr['Hs_extreme']:.2f} m")
print(f"  Range: {extreme_100yr['Hs_lower_bound']:.2f} - {extreme_100yr['Hs_upper_bound']:.2f} m")
```

## Complete Examples

### Example 1: Complete Wave Analysis

```python
def complete_wave_analysis(
    Hs: float,
    Tp: float,
    depth: float,
    duration: float = 3600,
    output_dir: str = 'reports/wave_analysis'
) -> dict:
    """
    Complete wave analysis: spectrum, time series, statistics.

    Args:
        Hs: Significant wave height (m)
        Tp: Peak period (s)
        depth: Water depth (m)
        duration: Time series duration (s)
        output_dir: Output directory

    Returns:
        Complete analysis results
    """
    import plotly.graph_objects as go
    from plotly.subplots import make_subplots
    from pathlib import Path

    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    # 1. Generate spectrum
    freq = np.linspace(0.01, 0.5, 500)
    S = jonswap_spectrum(freq, Hs, Tp)

    # 2. Calculate spectral parameters
    params = calculate_spectral_parameters(S, freq)

    # 3. Generate time series
    t, eta = generate_irregular_wave_time_series(S, freq, duration, dt=0.1)

    # 4. Wave statistics
    wave_stats = significant_wave_statistics(Hs)

    # 5. Regular wave properties (using Tp)
    regular_wave = airy_wave_properties(Hs, Tp, depth)

    # 6. Create visualizations
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=(
            'JONSWAP Spectrum',
            'Wave Elevation Time Series',
            'Wave Height Distribution',
            'Wave Steepness'
        )
    )

    # Plot 1: Spectrum
    fig.add_trace(
        go.Scatter(x=freq, y=S, name='S(f)', line=dict(color='blue')),
        row=1, col=1
    )

    # Plot 2: Time series (first 10 minutes)
    t_plot = t[:6000]
    eta_plot = eta[:6000]
    fig.add_trace(
        go.Scatter(x=t_plot, y=eta_plot, name='η(t)', line=dict(width=1)),
        row=1, col=2
    )

    # Plot 3: Wave height distribution
    H_array = np.linspace(0, Hs*2, 100)
    P_exceedance = rayleigh_distribution(H_array, Hs)

    fig.add_trace(
        go.Scatter(
            x=H_array, y=P_exceedance,
            name='Rayleigh',
            line=dict(color='red')
        ),
        row=2, col=1
    )

    # Plot 4: Steepness vs frequency
    steepness_freq = (2*np.pi*freq)**2 / 9.81 * np.sqrt(S)

    fig.add_trace(
        go.Scatter(x=freq, y=steepness_freq, name='Steepness'),
        row=2, col=2
    )

    fig.update_layout(height=800, showlegend=True, title_text=f'Wave Analysis (Hs={Hs}m, Tp={Tp}s)')
    fig.write_html(output_path / 'wave_analysis.html')

    # Export summary
    summary = {
        'input': {
            'Hs': Hs,
            'Tp': Tp,
            'depth': depth
        },
        'spectral_params': params,
        'statistics': wave_stats,
        'regular_wave': regular_wave,
        'time_series': {
            'duration_s': duration,
            'timestep_s': 0.1,
            'points': len(t)
        }
    }

    import json
    with open(output_path / 'wave_summary.json', 'w') as f:
        json.dump(summary, f, indent=2, default=str)

    print(f"✓ Wave analysis complete")
    print(f"  Output: {output_dir}")

    return summary

# Example
analysis = complete_wave_analysis(
    Hs=8.5,
    Tp=12.0,
    depth=1500,
    duration=3600
)
```

## Resources

- **Shore Protection Manual**: US Army Corps of Engineers
- **Ocean Waves and Oscillating Systems**: J. Falnes
- **Water Wave Mechanics for Engineers and Scientists**: R.G. Dean & R.A. Dalrymple
- **DNV-RP-C205**: Environmental Conditions and Environmental Loads
- **ISO 19901-1**: Metocean design and operating considerations

---

**Use this skill for all wave analysis in DigitalModel!**

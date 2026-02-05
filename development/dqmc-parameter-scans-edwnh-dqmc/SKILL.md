---
name: dqmc-parameter-scans
description: Set up systematic DQMC parameter studies across temperature, interaction strength U, or chemical potential mu. Use when doing temperature sweeps, phase diagram calculations, or any grid of simulations.
---

# Parameter Scans

Generate a directory tree of simulation files (one directory per parameter point), then run with the queue system (see `dqmc-run`), then analyze (see `dqmc-analyze`).

## Temperature Scan

Vary L while adjusting dt to maintain Trotter error bound:

```python
from dqmc_util import gen_1band_hub
import numpy as np

U = 4.0
step = 5  # L must be divisible by n_matmul and period_eqlt (defaults: 5)
for T in [0.1, 0.2, 0.5, 1.0]:
    beta = 1.0 / T
    dt = min((0.05/U)**0.5, beta / 10)
    L = int(np.ceil(beta / dt / step) * step)
    dt = beta / L

    gen_1band_hub.create_batch(
        prefix=f"data/T{T:.2f}/bin",
        Nfiles=4, Nx=6, Ny=6, U=U, dt=dt, L=L
    )
```

## U-mu Scan

Grid over interaction strength and chemical potential:

```python
import itertools
import numpy as np
from dqmc_util import gen_1band_hub

dt, L = 0.1, 40  # sets beta = L*dt
for U, mu in itertools.product([2, 4, 6, 8], np.linspace(-4, 4, 9)):
    gen_1band_hub.create_batch(
        prefix=f"data/U{U}_mu{mu:.1f}/bin",
        Nfiles=4, Nx=6, Ny=6, U=U, mu=mu, dt=dt, L=L
    )
```

## Validation

- [ ] Directory structure created as expected
- [ ] Each directory has correct number of `.h5` files

## Tips

- Use descriptive directory names encoding key parameters
- Keep `Nfiles >= 4` for reliable error estimates
- For large scans, generate files first, then run via queue system

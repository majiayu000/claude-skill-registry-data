---
name: portal-synthetic-data
description: Generate reproducible synthetic financial silos (creditos, liquidez, derivados) with Polars + Faker, injected anomalies, catalog and user seeds. Use when writing ml/data/generators.py, the make data target, cryptic heterogeneous schemas, anomaly injection, or seed data for catalog and app_user.
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

# Portal Synthetic Data Skill

Generators: `! ls ml/data/generators.py 2>/dev/null || echo "not created yet"`

## Rules — NON-NEGOTIABLE

- SIEMPRE semilla fija (`SEED = 20260720`) en Polars, Faker y `numpy.random`: `make data` debe producir bytes idénticos entre corridas (base de las consultas de referencia de la capa semántica).
- Esquemas crípticos y heterogéneos A PROPÓSITO: cada silo nombra distinto el mismo concepto (`cli_ref` vs `id_cliente` vs `ctpty_cd`) — sin esto la capa semántica y el catálogo no tienen razón de ser.
- IDs de cliente COMPARTIDOS entre silos (mismo pool) para habilitar joins por contraparte.
- ~0.1 % de anomalías inyectadas deliberadamente (fechas imposibles, montos negativos, duplicados) y DOCUMENTADAS en `data/README.md` con conteos exactos.
- Volúmenes objetivo: `creditos` 1–5 M filas, `liquidez` ~1 M, `derivados` ~500 K → Parquet en `data/silos/*.parquet`. `data/` está en `.gitignore` (solo el README versionado).
- Honestidad de demo: los datos son sintéticos y se declaran como tales; cualquier previsión derivada se etiqueta "proyección simulada".
- Seed relacional: catálogo 200–400 entradas + ~30 notas tribales curadas; 7 usuarios (1 admin + 2 por perfil) con Argon2 — vía migraciones dbmate (skill `portal-db-migrations`).

## Esquemas por silo (crípticos, heterogéneos)

| Silo | Columnas (físicas) | Concepto compartido |
|------|--------------------|---------------------|
| `creditos` | `cli_ref`, `prod_cd`, `sdo_cap`, `dias_mora`, `tasa_pct`, `f_apert`, `f_venc` | cliente = `cli_ref` |
| `liquidez` | `fec_pos`, `bucket_venc`, `mto_disp`, `ratio_lcr`, `id_cliente` | cliente = `id_cliente` |
| `derivados` | `op_id`, `subyacente`, `nocional_usd`, `ctpty_cd`, `mtm_val`, `f_trade` | cliente = `ctpty_cd` |

## Generador (ml/data/generators.py)

```python
import numpy as np
import polars as pl
from faker import Faker

SEED = 20260720
N_CLIENTS = 50_000
ANOMALY_RATE = 0.001

fake = Faker("es_MX")
Faker.seed(SEED)
rng = np.random.default_rng(SEED)


def client_pool() -> np.ndarray:
    """Shared client IDs across silos (enables counterparty joins)."""
    return np.array([f"C{100000 + i}" for i in range(N_CLIENTS)])


def generate_creditos(n_rows: int = 2_000_000) -> pl.DataFrame:
    clients = client_pool()
    df = pl.DataFrame({
        "cli_ref": rng.choice(clients, n_rows),
        "prod_cd": rng.choice(["HIP", "AUT", "PYM", "TDC", "PER"], n_rows),
        "sdo_cap": rng.lognormal(11.5, 1.2, n_rows).round(2),
        "dias_mora": rng.choice([0, 0, 0, 0, 15, 30, 60, 90, 180], n_rows),
        "tasa_pct": rng.uniform(6.0, 42.0, n_rows).round(2),
        "f_apert": pl.date_range(date(2018, 1, 1), date(2026, 6, 30), eager=True)
                     .sample(n_rows, with_replacement=True, seed=SEED),
    })
    return inject_anomalies(df, silo="creditos")
```

## Inyección de anomalías (documentada)

```python
def inject_anomalies(df: pl.DataFrame, silo: str) -> pl.DataFrame:
    """Inject ~0.1% deliberate anomalies; counts are logged for data/README.md."""
    n = int(df.height * ANOMALY_RATE)
    idx = rng.choice(df.height, n, replace=False)
    third = n // 3
    df = df.with_row_index("_i")
    df = df.with_columns(                              # negative amounts
        pl.when(pl.col("_i").is_in(idx[:third]))
          .then(-pl.col("sdo_cap")).otherwise(pl.col("sdo_cap")).alias("sdo_cap"),
    ).with_columns(                                    # impossible dates
        pl.when(pl.col("_i").is_in(idx[third:2 * third]))
          .then(pl.date(2099, 2, 30, strict=False)).otherwise(pl.col("f_apert"))
          .alias("f_apert"),
    ).drop("_i")
    dupes = df.sample(n - 2 * third, seed=SEED)        # exact duplicates
    logger.info("anomalies_injected", silo=silo,
                negative=third, bad_dates=third, duplicates=n - 2 * third)
    return pl.concat([df, dupes])
```

## make data

```makefile
data:
	poetry run python -m ml.data.generators --out data/silos/
	poetry run python -m ml.data.seed_catalog        # 200-400 catalog entries from schemas
	@echo "Silos written to data/silos/ (fixed seed, see data/README.md)"
```

```python
# ml/data/generators.py __main__: writes parquet deterministically
generate_creditos().write_parquet(out / "creditos.parquet")
generate_liquidez().write_parquet(out / "liquidez.parquet")
generate_derivados().write_parquet(out / "derivados.parquet")
```

## Seed del catálogo desde los esquemas

```python
# ml/data/seed_catalog.py — one catalog_field per physical column + curated tribal notes
FIELD_DEFS = {
    ("creditos", "sdo_cap"): ("saldo de capital", "Outstanding principal balance", "sum"),
    ("liquidez", "ratio_lcr"): ("ratio LCR", "Liquidity coverage ratio (LCR-like)", "mean"),
    ("derivados", "mtm_val"): ("mark to market", "MtM valuation of the trade", "sum"),
    # ... 200-400 entries generated from silo schemas + manual curation
}
TRIBAL_NOTES = [
    ("liquidez", "fec_pos", "La fecha valor es T+1 respecto a la fecha de posicion",
     "aplica solo a posiciones de mercado local"),
    # ... ~30 curated notes with Tk-Boost applicability condition
]
```

## data/README.md obligatorio

Debe documentar: semilla, volúmenes generados, conteo exacto de anomalías por tipo y silo,
mapa de columnas crípticas → nombre de negocio, y la advertencia de datos sintéticos (honestidad de demo).

# Pepkio Standard Curve & Concentration Calculator

Run the Pepkio absorbance-curve-calculator CLI in a container to fit standard curves and obtain dilution-corrected concentrations with QC flags through the hosted API.

# What It Does

The image runs `pepkio-absorbance-curve-calculator`, a client for the Pepkio Standard Curve & Concentration Calculator REST API. Submit 96-well absorbance values, well layout (standard, sample, blank), standard concentrations, and dilution factors; receive model comparison with R², selected curve model, per-sample concentrations with formula paths, and QC flags for replicate CV, out-of-range ODs, and poor fit.

Typical workflows include BCA and Bradford protein assays, sandwich and competitive ELISA back-calculation, plate-reader reanalysis, and QC review before reporting. Calculator logic runs on Pepkio servers; provide a network connection and API key for `run` commands.

# Features

- Assay types: BCA, Bradford, sandwich ELISA, competitive ELISA
- Blank subtraction and assay-aware default models
- Model comparison: linear, quadratic, 4PL, inverted 4PL with R²
- Dilution correction with formula path in output
- QC flags: replicate CV > 20%, out-of-range ODs, R² thresholds
- Named manifest examples (e.g. `bca_linear`, `sandwich_elisa_4pl`)
- Manifest inspection without an API key

# Quick Start

```bash
docker pull pepkio/absorbance-curve-calculator:0.1.0
docker run --rm -e PEPKIO_API_KEY="your-key" pepkio/absorbance-curve-calculator:0.1.0 \
  pepkio-absorbance-curve-calculator run --example bca_linear
```

Manifest only (no API key):

```bash
docker run --rm pepkio/absorbance-curve-calculator:0.1.0 \
  pepkio-absorbance-curve-calculator manifest --examples
```

Set `PEPKIO_API_BASE_URL` to override the API host (default: `https://tools.pepkio.com`). Create an API key with **tools:run** scope at https://www.pepkio.com/account/api-keys.

# Quick Example

```bash
docker run --rm -e PEPKIO_API_KEY="$PEPKIO_API_KEY" pepkio/absorbance-curve-calculator:0.1.0 \
  pepkio-absorbance-curve-calculator run --example sandwich_elisa_4pl
```

# Typical Use Cases

- BCA protein assay standard curve from 96-well absorbance data
- ELISA sample concentration back-calculation with dilution factors
- Comparing linear vs 4PL fit for Bradford or ELISA data
- CI or workflow runners that need a fixed client environment
- Batch reanalysis of plate-reader exports in pipelines

# Scientific Background

Blank wells are averaged and subtracted before fitting. BCA and Bradford default to linear regression; ELISA defaults to 4PL (sandwich) or inverted 4PL (competitive). Corrected concentration = interpolated concentration × dilution factor. The engine flags R² below 0.98 (linear) or 0.995 (4PL), replicate CV above 20%, and ODs outside the standard range.

# Web Application

For researchers who prefer a graphical interface, an interactive web version is available.

Web Application: https://www.pepkio.com/tools/absorbance-curve-calculator

The web UI adds paste-from-Excel grid entry, one-click well exclusion with audit logging, CSV/PDF export with curve plots, and reload of recent runs.

# Documentation and Resources

GitHub Repository (source and Dockerfile): https://github.com/pepkio/pepkio-absorbance-curve-calculator

Web Application: https://www.pepkio.com/tools/absorbance-curve-calculator

# About Pepkio

Pepkio (https://www.pepkio.com/) develops software tools and bioinformatics solutions for life science researchers, including laboratory calculators and analysis services.

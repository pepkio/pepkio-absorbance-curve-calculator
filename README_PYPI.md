# Pepkio Standard Curve & Concentration Calculator

Call the Pepkio absorbance-curve-calculator REST API from Python to fit standard curves and return dilution-corrected sample concentrations with QC flags.

# What It Does

Plate-reader exports for BCA, Bradford, or ELISA assays need blank subtraction, curve model selection, interpolation, and dilution correction before concentrations can be reported. Rebuilding that workflow in a spreadsheet for each plate is slow and error-prone.

This package submits 96-well absorbance data, well layout, standard concentrations, and dilution factors to the same Pepkio Tools engine as the hosted web calculator. It returns fitted model parameters, side-by-side R² comparisons, per-sample concentrations with formula paths, and QC flags for high replicate CV or out-of-range ODs.

Programmatic runs require a network connection and a Pepkio API key. Calculations are not bundled for offline use.

# Features

- Assay types: BCA, Bradford, sandwich ELISA, competitive ELISA
- Blank subtraction and assay-aware default models (linear for protein assays, 4PL for ELISA)
- Model comparison: linear, quadratic, 4PL, inverted 4PL with R²
- Optional `model_override` and `excluded_wells`
- Dilution correction with formula path in output
- QC flags: replicate CV > 20%, out-of-range ODs, R² thresholds
- Manifest examples: `bca_linear`, `sandwich_elisa_4pl`, `competitive_elisa_4pl`, `blocking_few_standards`
- CLI: `pepkio-absorbance-curve-calculator manifest` and `run`
- Configuration via `PEPKIO_API_KEY` and `PEPKIO_API_BASE_URL`

# Installation

```bash
pip install pepkio-absorbance-curve-calculator
```

Set an API key with **tools:run** scope before calling `run()`:

```bash
export PEPKIO_API_KEY="your-key"
```

Create a key in your [Pepkio account API keys](https://www.pepkio.com/account/api-keys) settings.

# Quick Example

```python
from pepkio_absorbance_curve_calculator import PepkioClient

with PepkioClient() as client:
    inp = client.get_example_input("bca_linear")
    result = client.run(inp)
    for sample in result.result["samples"]:
        print(sample["sample_id"], sample["corrected_conc"], sample.get("formula_path"))
```

CLI:

```bash
pepkio-absorbance-curve-calculator run --example bca_linear
```

Manifest inspection does not require an API key.

# Typical Use Cases

- BCA protein assay standard curve from 96-well absorbance data
- ELISA sample concentration back-calculation with dilution factors
- Comparing linear vs 4PL fit for Bradford or ELISA data
- Automated reanalysis of plate-reader exports in notebooks or CI
- QC screening for R², replicate CV, and out-of-range samples before reporting

# Scientific Background

Blank wells are averaged and subtracted before fitting. BCA and Bradford default to linear regression; ELISA defaults to 4PL (sandwich) or inverted 4PL (competitive). Corrected concentration = interpolated concentration × dilution factor. The engine flags R² below 0.98 (linear) or 0.995 (4PL), replicate CV above 20%, and ODs outside the standard range.

# Web Application

For researchers who prefer a graphical interface, an interactive [Standard Curve Calculator](https://www.pepkio.com/tools/absorbance-curve-calculator) is available in the browser.

The web interface adds paste-from-Excel grid entry, one-click well exclusion with audit logging, CSV/PDF export with curve plots, and reload of recent runs.

# Documentation and Resources

Source code and issue tracking: [github.com/pepkio/pepkio-absorbance-curve-calculator](https://github.com/pepkio/pepkio-absorbance-curve-calculator)

Web application: [https://www.pepkio.com/tools/absorbance-curve-calculator](https://www.pepkio.com/tools/absorbance-curve-calculator)

# About Pepkio

Pepkio develops software tools and provides bioinformatics analysis services for life science research. See https://www.pepkio.com for additional tools and services.

# Keywords

standard curve, absorbance calculator, ELISA 4PL, BCA assay, Bradford assay, concentration back-calculation, plate reader analysis, 96-well absorbance, dilution factor, blank subtraction, optical density interpolation, model comparison R squared, replicate CV QC, pepkio-absorbance-curve-calculator, Python ELISA API, immunoassay quantification, protein assay calculator, REST API standard curve, how to fit BCA standard curve from Python, back-calculate ELISA concentration with dilution factor, compare linear and 4PL fit programmatically, automate plate reader absorbance analysis, flag out of range ELISA samples API, standard curve QC before reporting results, Python client absorbance to concentration

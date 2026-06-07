# Pepkio Standard Curve & Concentration Calculator

Turn pasted 96-well absorbance into dilution-corrected sample concentrations with assay-aware curve fitting and QC flags.

# Overview

Quantitative immunoassays and protein assays depend on a standard curve: known concentrations are measured for absorbance (optical density, OD), a regression model is fit, and unknown sample ODs are interpolated back to concentration. In practice, researchers paste plate-reader exports into spreadsheets, choose between linear, quadratic, or four-parameter logistic (4PL) models by hand, apply blank subtraction, and multiply by dilution factors—steps where layout errors, wrong model choice, or forgotten dilutions often go unnoticed until results are reported.

The Pepkio Standard Curve Calculator (tool ID: `absorbance-curve-calculator`) accepts a 96-well absorbance grid with well roles (standard, sample, blank), standard concentrations, and per-sample dilution factors. It blank-subtracts, selects an assay-appropriate curve model, compares linear, quadratic, and 4PL fits side by side with R² values, back-calculates concentrations with dilution math shown, and flags replicate coefficient of variation (CV) above 20%, out-of-range ODs, and poor curve fit before you report.

Researchers use standard-curve calculators for BCA and Bradford protein assays, sandwich and competitive ELISA, plate-reader reanalysis, and QC review before notebook or publication reporting. This repository provides a Python client and CLI for the same calculation engine used by the hosted web application at [https://www.pepkio.com/tools/absorbance-curve-calculator](https://www.pepkio.com/tools/absorbance-curve-calculator).

# Features

- **Assay presets:** BCA, Bradford, sandwich ELISA, and competitive ELISA with assay-aware default curve models
- **96-well absorbance input:** Paste or submit well absorbance values with layout roles (standard, sample, blank)
- **Blank subtraction:** Mean of blank wells subtracted before fitting
- **Model comparison:** Linear, quadratic, 4PL, and inverted 4PL fits compared side by side with R²
- **Model override:** Optional `model_override` (`linear`, `quadratic`, `four_pl`, `four_pl_inverted`)
- **Dilution correction:** Final concentration = interpolated concentration × dilution factor, with formula path shown
- **QC flags:** Replicate CV > 20%, out-of-range ODs, R² below 0.98 (linear) or 0.995 (4PL)
- **Well exclusion:** Optional `excluded_wells` list for outlier removal (logged in audit trail)
- **Structured output:** Sample concentrations, model comparison, selected/recommended model, QC summary, audit log
- **Manifest examples:** `bca_linear`, `sandwich_elisa_4pl`, `competitive_elisa_4pl`, `blocking_few_standards`
- **Python API and CLI:** `PepkioClient`, `get_manifest`, `get_example_input`, `run`
- **Shareable runs:** API returns `permalink` URLs for each completed run

The hosted web version adds an interactive plate grid, one-click well exclusion with audit logging, CSV and PDF export with curve plots and fit parameters, and browser storage of the last five runs.

# Common Use Cases

- **BCA protein assay:** Fit a linear standard curve from a 96-well plate and back-calculate sample protein concentrations in mg/mL
- **Bradford assay:** Compare linear vs quadratic fit when absorbance is not strictly linear across the standard range
- **Sandwich ELISA:** Fit a 4PL curve for sigmoidal dose–response and interpolate unknown sample concentrations in ng/mL
- **Competitive ELISA:** Use inverted 4PL when signal decreases with increasing analyte concentration
- **Dilution correction:** Apply a 10× or 20× dilution factor so reported concentrations reflect the original sample, not the diluted well
- **Plate-reader reanalysis:** Re-import absorbance data after export from SoftMax, Gen5, or Excel without rebuilding formulas
- **QC before reporting:** Check R², replicate CV, and out-of-range flags before entering results in a lab notebook or ELN
- **Supplementary figures:** Export curve plots and fit parameters for papers or electronic lab notebooks

# Why This Tool Exists

Spreadsheets require manual plate layout, trendline selection, and dilution arithmetic—errors in any step often pass unnoticed. GraphPad Prism fits curves well but requires reformatting plate data and is a paid desktop license. Online 4PL calculators may lack replicate QC, dilution tracking, and audit-ready export.

This tool accepts a pasted 96-well grid, applies blank subtraction and assay presets, compares models with visible R², flags replicate CV and range problems, and supports CSV/PDF export with parameters and excluded wells. The Python client lets you run the same engine from scripts, notebooks, or CI pipelines via the Pepkio Tools REST API.

# Installation

```bash
pip install pepkio-absorbance-curve-calculator
```

Or with [uv](https://docs.astral.sh/uv/):

```bash
uv add pepkio-absorbance-curve-calculator
```

Programmatic runs require a Pepkio API key with **tools:run** scope. Create one at [https://www.pepkio.com/account/api-keys](https://www.pepkio.com/account/api-keys).

```bash
export PEPKIO_API_KEY="your-key"
```

| Variable | Description |
|----------|-------------|
| `PEPKIO_API_KEY` | Production API key |
| `LOCAL_PEPKIO_API_KEY` | Local dev key when base URL points to `tools.localtest.me` |
| `PEPKIO_API_BASE_URL` | Override API host (default: `https://tools.pepkio.com`) |

Manifest inspection does not require an API key.

# Quick Start

### Python

```python
from pepkio_absorbance_curve_calculator import PepkioClient

with PepkioClient() as client:
    inp = client.get_example_input("bca_linear")
    result = client.run(inp)
    print(result.status, result.permalink)
    print("Model:", result.result["selected_model"])
    for sample in result.result["samples"]:
        print(
            sample["sample_id"],
            sample["corrected_conc"],
            result.result.get("concentration_unit", "mg/mL"),
        )
```

### CLI

```bash
# Manifest (no API key)
pepkio-absorbance-curve-calculator manifest
pepkio-absorbance-curve-calculator manifest --examples

# Run a named example (API key required)
pepkio-absorbance-curve-calculator run --example bca_linear

# Run custom JSON input
pepkio-absorbance-curve-calculator run --input-json '{"assay_type":"bca","concentration_unit":"mg/mL","wells":[],"layout":[],"standards":[]}'
```

Options: `--api-key`, `--base-url`, `--label`, `--idempotency-key`.

# Example Output

Running the `bca_linear` manifest example against the production API returns:

```json
{
  "status": "completed",
  "run_id": "718df5c7-2cf0-44bb-80a9-566b0ce29879",
  "permalink": "https://tools.pepkio.com/r/718df5c7-2cf0-44bb-80a9-566b0ce29879",
  "result": {
    "has_blocking_errors": false,
    "blank_subtracted": true,
    "blank_mean": 0.048,
    "selected_model": "linear",
    "recommended_model": "linear",
    "model_comparison": {
      "linear": { "model": "linear", "r_squared": 0.9986 },
      "quadratic": { "model": "quadratic", "r_squared": 0.9999 },
      "four_pl": { "model": "four_pl", "r_squared": 1.0 }
    },
    "samples": [
      {
        "sample_id": "S1",
        "wells": ["B1"],
        "mean_od": 0.147,
        "interpolated_conc": 0.1631,
        "corrected_conc": 0.1631,
        "dilution_factor": 1,
        "flags": [],
        "formula_path": "linear invert(OD=0.147) → 0.1631 mg/mL × 1 = 0.1631 mg/mL"
      },
      {
        "sample_id": "S2",
        "wells": ["B4"],
        "mean_od": 0.372,
        "interpolated_conc": 0.3912,
        "corrected_conc": 7.8237,
        "dilution_factor": 20,
        "flags": [],
        "formula_path": "linear invert(OD=0.372) → 0.3912 mg/mL × 20 = 7.8237 mg/mL"
      }
    ],
    "qc_summary": {
      "r_squared_pass": true,
      "r_squared_threshold": 0.98,
      "high_cv_count": 0,
      "out_of_range_count": 0
    }
  }
}
```

For ELISA examples, `sandwich_elisa_4pl` selects `four_pl` and `competitive_elisa_4pl` selects `four_pl_inverted`. The `blocking_few_standards` example returns `has_blocking_errors: true` when too few standard points are provided.

# Scientific Background

**Blank subtraction.** Absorbance readings include background signal from buffer and plate. The tool subtracts the mean absorbance of wells marked as blanks before fitting and interpolation.

**Standard curve models.** BCA and Bradford protein assays typically use a linear model over the working range. ELISA dose–response curves are often sigmoidal; sandwich ELISA uses four-parameter logistic (4PL) regression, and competitive ELISA uses an inverted 4PL when signal decreases with concentration.

**Dilution correction.** When a sample was diluted before plating, the concentration read from the curve applies to the diluted well. The corrected (reported) concentration is:

```
corrected concentration = interpolated concentration × dilution factor
```

**Quality control thresholds.** The engine flags replicate CV above 20%, sample ODs outside the standard range, and R² below 0.98 for linear models or 0.995 for 4PL models.

**Terminology.** Researchers search for standard curve calculator, absorbance to concentration, ELISA 4PL fit, BCA protein assay calculator, plate reader data analysis, optical density interpolation, and dilution factor correction—these workflows are what the absorbance-curve-calculator tool addresses.

# Frequently Asked Questions

**What is a standard curve?**
A standard curve relates known analyte concentrations (standards) to measured absorbance. Unknown sample absorbance values are interpolated on the fitted curve to estimate concentration.

**How do I prepare a standard curve for ELISA?**
Include serial dilutions of a known standard across at least five concentration levels plus blanks. For sandwich ELISA, signal increases with concentration and a 4PL model is typically appropriate. For competitive ELISA, signal decreases with concentration and an inverted 4PL may be used.

**What is the difference between BCA and Bradford assays?**
Both are colorimetric protein assays read by absorbance. BCA uses bicinchoninic acid chemistry; Bradford uses Coomassie dye binding. Both typically produce approximately linear standard curves over a defined working range; this tool defaults to linear fitting for both assay types.

**When should I use linear vs 4PL fitting?**
Linear fitting suits protein assays (BCA, Bradford) over a limited OD range. 4PL (four-parameter logistic) suits sigmoidal ELISA dose–response data with lower asymptote, upper asymptote, inflection point, and slope parameters.

**What is 4PL (four-parameter logistic)?**
A sigmoidal regression model with four parameters (minimum, maximum, inflection, slope) used to fit ELISA standard curves where response is not linear across the full concentration range.

**How do I apply a dilution factor?**
Enter the dilution factor for each sample ID (e.g., 20 if the sample was diluted 1:20 before plating). The tool multiplies the interpolated well concentration by this factor to report the original sample concentration.

**What is blank subtraction?**
Wells designated as blanks measure buffer-only absorbance. Their mean is subtracted from all standard and sample ODs before curve fitting to reduce background bias.

**What does R² mean for my standard curve?**
R² (coefficient of determination) measures how well the model fits the standard points. The tool flags linear fits below R² 0.98 and 4PL fits below R² 0.995.

**What is replicate CV and why is it flagged above 20%?**
Coefficient of variation (CV) measures spread among replicate wells for the same sample or standard. CV above 20% suggests pipetting or assay variability that may affect reported concentrations.

**What happens when a sample OD is outside the standard range?**
The tool flags out-of-range samples because extrapolation beyond the standard curve is less reliable. Dilute and re-run samples that exceed the upper standard, or concentrate samples below the lower standard.

**Can I exclude outlier wells?**
Yes. Pass well IDs in `excluded_wells`; each exclusion is recorded in the audit log. The web interface supports one-click exclusion with the same logging.

**How many standard points do I need?**
Too few standards produce blocking errors. The `blocking_few_standards` manifest example demonstrates failure when only two standard levels are provided.

**Can I override the automatic model selection?**
Yes. Set `model_override` to `linear`, `quadratic`, `four_pl`, or `four_pl_inverted` to force a specific model instead of the assay default.

**Does the Python client work offline?**
No. Calculations run on Pepkio servers via the REST API. A network connection and API key are required for `run()`. Manifest fetch works without a key.

**How do I export results for my lab notebook?**
The web application supports CSV copy, CSV download, and PDF reports with the curve, fit parameters, and QC log. The API returns structured JSON including `samples`, `model_comparison`, and `qc_summary`.

**What plate formats are supported?**
The tool accepts a list of well absorbance values with layout roles. The web UI is designed around a 96-well grid; the API accepts well IDs in standard microplate notation (e.g., A1, B4, H12).

**How do I compare linear and 4PL for the same data?**
The `model_comparison` output includes R² and parameters for linear, quadratic, 4PL, and inverted 4PL models fit to the same blank-subtracted standard points.

# Web Application

For researchers who prefer a graphical interface, an interactive [Standard Curve Calculator](https://www.pepkio.com/tools/absorbance-curve-calculator) is available in the browser.

The web version provides an interactive 96-well grid, paste-from-Excel workflow, side-by-side model comparison with R², one-click well exclusion with audit logging, CSV and PDF export with curve plots and fit parameters, and storage of your last five runs for quick reload. No install or account is required for the web workspace.

Use the web tool for initial exploration and PDF reports; use this Python package for scripted analysis, LIMS integration, or batch reanalysis pipelines.

# Related Resources

GitHub Repository: [https://github.com/pepkio/pepkio-absorbance-curve-calculator](https://github.com/pepkio/pepkio-absorbance-curve-calculator)

PyPI Package: [https://pypi.org/project/pepkio-absorbance-curve-calculator/](https://pypi.org/project/pepkio-absorbance-curve-calculator/)

Web Application: [https://www.pepkio.com/tools/absorbance-curve-calculator](https://www.pepkio.com/tools/absorbance-curve-calculator)

# About Pepkio

[Pepkio](https://www.pepkio.com/) develops software tools and bioinformatics solutions for life science researchers, including laboratory calculators and analysis services. Explore additional calculators and analysis offerings on the Pepkio website.

# License

# Keywords

standard curve calculator, absorbance curve calculator, concentration calculator, ELISA standard curve, BCA assay calculator, Bradford assay calculator, protein assay standard curve, 4PL curve fit, four parameter logistic ELISA, sandwich ELISA analysis, competitive ELISA analysis, plate reader data analysis, 96-well absorbance, optical density to concentration, OD interpolation, dilution factor correction, blank subtraction absorbance, replicate CV QC, R squared standard curve, linear regression assay, quadratic curve fit, immunoassay quantification, colorimetric assay analysis, microplate absorbance analysis, standard curve back-calculation, ELISA concentration calculator, protein quantification BCA, protein quantification Bradford, assay QC flags, out of range sample flag, pepkio-absorbance-curve-calculator, laboratory calculator Python, REST API standard curve, how to calculate concentration from absorbance, how to fit ELISA standard curve 4PL, how to apply dilution factor ELISA, BCA protein assay standard curve Excel alternative, compare linear vs 4PL Bradford assay, back-calculate sample concentration from plate reader, flag high CV replicates ELISA, standard curve R2 threshold 0.98, blank subtract 96-well plate absorbance, interpolate unknown sample OD standard curve, competitive ELISA inverted 4PL fit, export ELISA standard curve PDF report, reanalyze SoftMax plate export concentrations, Python script ELISA concentration from absorbance, automate standard curve fitting pipeline, dilution corrected sample concentration mg/mL, QC review before reporting assay results, supplementary figure standard curve parameters, audit log excluded wells ELISA, when to use linear vs sigmoidal standard curve, minimum standard points for curve fit, Pepkio Tools API absorbance calculator, GraphPad Prism alternative standard curve online

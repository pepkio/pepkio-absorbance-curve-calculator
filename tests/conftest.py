"""Pytest fixtures."""

from __future__ import annotations

from pathlib import Path

import pytest
from dotenv import load_dotenv

# Load monorepo .env for local integration runs (never log keys).
_monorepo_env = Path(__file__).resolve().parents[3] / ".env"
if _monorepo_env.is_file():
    load_dotenv(_monorepo_env, override=True)

_package_env = Path(__file__).resolve().parents[1] / ".env"
if _package_env.is_file():
    load_dotenv(_package_env, override=True)


@pytest.fixture
def mock_manifest() -> dict:
    return {
        "tool_id": "absorbance-curve-calculator",
        "title": "Standard Curve & Concentration Calculator",
        "execution_mode": "sync",
        "examples": [
            {
                "name": "bca_linear",
                "input": {
                    "assay_type": "bca",
                    "concentration_unit": "mg/mL",
                    "wells": [
                        {"well": "A1", "absorbance": 0.052},
                        {"well": "A4", "absorbance": 0.148},
                        {"well": "A6", "absorbance": 0.278},
                        {"well": "A8", "absorbance": 0.548},
                        {"well": "A10", "absorbance": 1.012},
                        {"well": "B1", "absorbance": 0.195},
                        {"well": "B4", "absorbance": 0.42},
                        {"well": "H1", "absorbance": 0.048},
                    ],
                    "layout": [
                        {"well": "A1", "role": "standard", "standard_level": 1},
                        {"well": "A4", "role": "standard", "standard_level": 2},
                        {"well": "A6", "role": "standard", "standard_level": 3},
                        {"well": "A8", "role": "standard", "standard_level": 4},
                        {"well": "A10", "role": "standard", "standard_level": 5},
                        {"well": "B1", "role": "sample", "sample_id": "S1"},
                        {"well": "B4", "role": "sample", "sample_id": "S2"},
                        {"well": "H1", "role": "blank"},
                    ],
                    "standards": [
                        {"level": 1, "concentration": 0},
                        {"level": 2, "concentration": 0.125},
                        {"level": 3, "concentration": 0.25},
                        {"level": 4, "concentration": 0.5},
                        {"level": 5, "concentration": 1},
                    ],
                    "dilution_factors": {"S1": 1, "S2": 20},
                    "excluded_wells": [],
                },
                "output": {"has_blocking_errors": False},
            },
            {
                "name": "blocking_few_standards",
                "input": {
                    "assay_type": "bca",
                    "concentration_unit": "mg/mL",
                    "wells": [
                        {"well": "A1", "absorbance": 0.05},
                        {"well": "A2", "absorbance": 1},
                    ],
                    "layout": [
                        {"well": "A1", "role": "standard", "standard_level": 1},
                        {"well": "A2", "role": "standard", "standard_level": 2},
                    ],
                    "standards": [
                        {"level": 1, "concentration": 0},
                        {"level": 2, "concentration": 1},
                    ],
                    "dilution_factors": {},
                    "excluded_wells": [],
                },
                "output": {"has_blocking_errors": True},
            },
            {
                "name": "sandwich_elisa_4pl",
                "input": {
                    "assay_type": "sandwich_elisa",
                    "concentration_unit": "ng/mL",
                    "wells": [{"well": "A1", "absorbance": 0.068}],
                    "layout": [{"well": "A1", "role": "standard", "standard_level": 1}],
                    "standards": [{"level": 1, "concentration": 0}],
                    "dilution_factors": {},
                    "excluded_wells": [],
                },
                "output": {"has_blocking_errors": False, "selected_model": "four_pl"},
            },
            {
                "name": "competitive_elisa_4pl",
                "input": {
                    "assay_type": "competitive_elisa",
                    "concentration_unit": "ng/mL",
                    "wells": [{"well": "A1", "absorbance": 2.35}],
                    "layout": [{"well": "A1", "role": "standard", "standard_level": 1}],
                    "standards": [{"level": 1, "concentration": 0}],
                    "dilution_factors": {},
                    "excluded_wells": [],
                },
                "output": {"has_blocking_errors": False, "selected_model": "four_pl_inverted"},
            },
        ],
    }


@pytest.fixture
def mock_run_response() -> dict:
    return {
        "run_id": "run_test123",
        "status": "completed",
        "result": {
            "has_blocking_errors": False,
            "selected_model": "linear",
            "samples": [
                {
                    "sample_id": "S1",
                    "concentration": 0.18,
                    "concentration_unit": "mg/mL",
                },
                {
                    "sample_id": "S2",
                    "concentration": 3.6,
                    "concentration_unit": "mg/mL",
                },
            ],
            "model_comparison": {"linear": {"r_squared": 0.99}},
            "warnings": [],
            "blank_mean": 0.048,
        },
        "error": None,
        "result_url": "https://tools.pepkio.com/api/tools/v1/runs/run_test123",
        "permalink": "https://tools.pepkio.com/r/run_test123",
    }

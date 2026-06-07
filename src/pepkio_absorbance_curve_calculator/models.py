"""Typed API request/response models (from manifest input/output schemas)."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from .exceptions import PepkioAPIError


class RunOptions(BaseModel):
    """Optional fields for POST .../run."""

    idempotency_key: str | None = None
    label: str | None = None


class AbsorbanceCurveToolInput(BaseModel):
    """Tool input (manifest: assay_type, concentration_unit, wells, layout, standards required)."""

    model_config = ConfigDict(extra="allow")

    assay_type: str = Field(..., description="bca, bradford, sandwich_elisa, or competitive_elisa")
    concentration_unit: str = Field(..., description="Concentration unit e.g. mg/mL or ng/mL")
    wells: list[dict[str, Any]] = Field(..., description="Well absorbance values")
    layout: list[dict[str, Any]] = Field(..., description="Well roles and group assignments")
    standards: list[dict[str, Any]] = Field(..., description="Standard level concentrations")
    dilution_factors: dict[str, float] | None = Field(
        default=None, description="Sample ID to dilution factor map"
    )
    excluded_wells: list[str] | None = Field(default=None, description="Wells excluded as outliers")
    model_override: str | None = Field(
        default=None, description="linear, quadratic, four_pl, or four_pl_inverted"
    )


class AbsorbanceCurveToolOutput(BaseModel):
    """Tool handler output shape (from manifest output schema)."""

    model_config = ConfigDict(extra="allow")

    has_blocking_errors: bool | None = None
    errors: list[Any] | None = None
    warnings: list[Any] | None = None
    samples: list[Any] | None = None
    model_comparison: dict[str, Any] | None = None
    selected_model: str | None = None
    recommended_model: str | None = None
    audit_log: list[Any] | None = None
    qc_summary: dict[str, Any] | None = None
    blank_mean: float | None = None


class RunResult(BaseModel):
    """Tool run response envelope."""

    model_config = ConfigDict(extra="allow")

    run_id: str
    status: str
    result: dict[str, Any] | None = None
    error: dict[str, Any] | None = None
    result_url: str | None = None
    permalink: str | None = None
    duration_ms: int | None = None

    def raise_for_error(self) -> None:
        """Raise PepkioAPIError if the run response includes an error field."""
        if self.error is None:
            return
        err = self.error
        raise PepkioAPIError(
            err.get("message", "Tool run failed"),
            code=err.get("code"),
            details=err.get("details") if isinstance(err.get("details"), dict) else {},
            response_body={"run_id": self.run_id, "status": self.status, "error": self.error},
        )


def parse_run_response(data: dict[str, Any]) -> RunResult:
    """Parse a run API JSON body into RunResult."""
    return RunResult.model_validate(data)

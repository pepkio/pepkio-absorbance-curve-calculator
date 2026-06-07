"""Integration tests against live Pepkio Tools API."""

from __future__ import annotations

import os

import pytest

from pepkio_absorbance_curve_calculator.client import PepkioClient
from pepkio_absorbance_curve_calculator.exceptions import PepkioAPIError

ENVIRONMENTS = [
    ("local", "https://tools.localtest.me"),
    ("production", "https://tools.pepkio.com"),
]

EXPECTED_EXAMPLES = (
    "bca_linear",
    "blocking_few_standards",
    "sandwich_elisa_4pl",
    "competitive_elisa_4pl",
)


def _api_key_for(base_url: str) -> str | None:
    if "localtest.me" in base_url:
        return os.getenv("LOCAL_PEPKIO_API_KEY")
    return os.getenv("PEPKIO_API_KEY")


def _resolve_environments() -> list[tuple[str, str]]:
    override = os.getenv("PEPKIO_API_BASE_URL")
    if override:
        name = "local" if "localtest.me" in override else "production"
        return [(name, override.rstrip("/"))]
    return ENVIRONMENTS


@pytest.fixture(params=_resolve_environments(), ids=lambda p: p[0])
def live_client(request):
    env_name, base_url = request.param
    api_key = _api_key_for(base_url)
    if not api_key:
        pytest.skip(f"No API key for {env_name} (set LOCAL_PEPKIO_API_KEY or PEPKIO_API_KEY)")
    with PepkioClient(api_key=api_key, base_url=base_url) as client:
        try:
            client.get_manifest(refresh=True)
        except PepkioAPIError as exc:
            if exc.status_code == 404 and exc.code == "TOOL_NOT_FOUND":
                pytest.skip(f"Tool not deployed on {env_name} ({base_url})")
            raise
        yield client


def test_get_manifest(live_client: PepkioClient):
    manifest = live_client.get_manifest(refresh=True)
    assert manifest["tool_id"] == "absorbance-curve-calculator"
    names = live_client.list_examples()
    for expected in EXPECTED_EXAMPLES:
        assert expected in names


def test_run_bca_linear(live_client: PepkioClient):
    inp = live_client.get_example_input("bca_linear")
    result = live_client.run(inp)
    assert result.status == "completed"
    assert result.run_id
    assert result.permalink
    assert result.result is not None
    assert result.result.get("has_blocking_errors") is False
    samples = result.result.get("samples")
    assert isinstance(samples, list)
    assert len(samples) >= 1
    assert result.result.get("selected_model") is not None


def test_run_sandwich_elisa_4pl(live_client: PepkioClient):
    inp = live_client.get_example_input("sandwich_elisa_4pl")
    result = live_client.run(inp)
    assert result.status == "completed"
    assert result.result is not None
    assert result.result.get("has_blocking_errors") is False
    assert result.result.get("selected_model") == "four_pl"
    model_comparison = result.result.get("model_comparison")
    assert isinstance(model_comparison, dict)
    four_pl = model_comparison.get("four_pl")
    assert isinstance(four_pl, dict)
    assert four_pl.get("r_squared", 0) > 0.99


def test_run_competitive_elisa_4pl(live_client: PepkioClient):
    inp = live_client.get_example_input("competitive_elisa_4pl")
    result = live_client.run(inp)
    assert result.status == "completed"
    assert result.result is not None
    assert result.result.get("has_blocking_errors") is False
    assert result.result.get("selected_model") == "four_pl_inverted"


def test_run_blocking_few_standards(live_client: PepkioClient):
    inp = live_client.get_example_input("blocking_few_standards")
    result = live_client.run(inp)
    assert result.status == "completed"
    assert result.result is not None
    assert result.result.get("has_blocking_errors") is True

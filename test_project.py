import math
from pathlib import Path

import pytest

from project import (
    load_csv,
    get_summary_stats,
    compute_correlation,
    is_number,
    export_report,
)


@pytest.fixture
def sample_csv(tmp_path: Path) -> Path:
    """Realistic and coherent dataset."""

    content = """date,temperature,humidity,rainfall,soil_moisture
2025-01-01,18.2,78,1.8,42.0
2025-01-02,19.5,75,0.6,41.2
2025-01-03,21.0,69,0.0,39.8
2025-01-04,22.5,63,0.0,38.5
2025-01-05,24.0,58,0.0,37.1
2025-01-06,25.0,53,0.0,36.0
2025-01-07,26.0,49,0.0,35.1
2025-01-08,27.2,45,0.2,34.8
2025-01-09,28.0,43,0.5,35.2
2025-01-10,27.5,47,1.0,36.5
"""
    p = tmp_path / "sample.csv"
    p.write_text(content, encoding="utf-8")
    return p


@pytest.fixture
def error_csv(tmp_path: Path) -> Path:
    """Dataset with errors."""
    content = """date,temperature,humidity,rainfall,soil_moisture
2025-01-01,18.2,62,0.0,33.4
2025-01-02,19.0,missing,0.2,34.1
2025-01-03,21.3,55,not available,35.0
2025-01-04,23.1,48,1.2,invalid
2025-01-05,24.5,45,,38.1
2025-01-06,,43,0.4,38.6
2025-01-07,26.0,40,0.0,39.2
2025-01-08,27.3,38,0.0,40.0
2025-01-09,28.1,35,1.5,41.4
2025-01-10,29.0,33,2.0,42.3
"""
    p = tmp_path / "sample_with_errors.csv"
    p.write_text(content, encoding="utf-8")
    return p


def test_load_csv_success(sample_csv: Path):

    data, headers = load_csv(str(sample_csv))
    assert data is not None and headers is not None
    assert len(data) == 10
    assert headers == ["date", "temperature", "humidity", "rainfall", "soil_moisture"]


def test_load_csv_missing_file():

    data, headers = load_csv("does_not_exist.csv")
    assert data is None and headers is None


def test_is_number():

    assert is_number("3.14") is True
    assert is_number("-2") is True
    assert is_number("  10  ") is True
    assert is_number("") is False
    assert is_number("abc") is False


def test_get_summary_stats_basic(sample_csv: Path):

    data, _ = load_csv(str(sample_csv))
    stats = get_summary_stats(data)

    assert "date" not in stats

    t = stats["temperature"]
    assert math.isclose(t["min"], 18.2, rel_tol=1e-9, abs_tol=1e-9)
    assert math.isclose(t["max"], 28.0, rel_tol=1e-9, abs_tol=1e-9)
    assert t["count"] == 10

    assert "soil_moisture" in stats
    sm = stats["soil_moisture"]
    assert sm["count"] == 10
    assert sm["min"] < sm["max"]


def test_compute_correlation_signs(sample_csv: Path):
    data, _ = load_csv(str(sample_csv))

    corr_temp_soil = compute_correlation(data, "temperature", "soil_moisture")
    corr_rh_soil = compute_correlation(data, "humidity", "soil_moisture")

    assert corr_temp_soil < -0.5
    assert corr_rh_soil > 0.5


def test_compute_correlation_constant_column(tmp_path: Path):

    content = """a,b
1,10
2,10
3,10
4,10
"""
    p = tmp_path / "const.csv"
    p.write_text(content, encoding="utf-8")
    data, _ = load_csv(str(p))
    corr = compute_correlation(data, "a", "b")
    assert corr == 0


def test_get_summary_stats_with_errors(error_csv: Path):
    data, _ = load_csv(str(error_csv))
    stats = get_summary_stats(data)

    total_rows = len(data)
    assert "rainfall" in stats
    assert 0 < stats["rainfall"]["count"] < total_rows

    assert "temperature" in stats
    assert stats["temperature"]["count"] < total_rows


def test_export_report_creates_file(sample_csv: Path, tmp_path: Path):
    data, _ = load_csv(str(sample_csv))

    export_report(data, output_dir=str(tmp_path))

    files = list(tmp_path.glob("report_*.txt"))
    assert len(files) == 1

    txt = files[0].read_text(encoding="utf-8")
    assert "DATASET ANALYZER REPORT" in txt
    assert "Column: temperature" in txt
    assert "Number of rows:" in txt

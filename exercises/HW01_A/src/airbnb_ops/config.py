
from dataclasses import dataclass
from pathlib import Path

BASE_DIR = Path.cwd()

@dataclass
class PipelineConfig:
    listings_path: Path = BASE_DIR / "data/raw/listings_sample.csv"
    segments_path: Path = BASE_DIR / "data/raw/neighbourhood_segments.csv"
    output_path: Path = BASE_DIR / "data/processed/airbnb_neighbourhood_summary.csv"
    report_path: Path = BASE_DIR / "reports/hw01_a_run_report.md"

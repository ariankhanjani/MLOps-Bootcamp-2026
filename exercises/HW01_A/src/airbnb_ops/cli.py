
from pathlib import Path
import typer

from airbnb_ops.config import PipelineConfig
from airbnb_ops.extract import read_csv_checked
from airbnb_ops.pii import handle_pii
from airbnb_ops.transform import build_neighbourhood_summary
from airbnb_ops.validate import validate_summary


app = typer.Typer(
    help="Airbnb neighbourhood summary pipeline."
)


@app.command("run")
def run() -> None:
    '''
    Execute the complete data pipeline.

    Steps:
    1. Read raw datasets.
    2. Remove or pseudonymize PII.
    3. Build neighbourhood-level aggregates.
    4. Validate output quality.
    5. Write output CSV and markdown report.
    '''

    config = PipelineConfig()

    # Load source datasets.
    listings = read_csv_checked(config.listings_path)
    segments = read_csv_checked(config.segments_path)

    # Remove direct PII and pseudonymize identifiers.
    listings = handle_pii(listings)

    # Create neighbourhood-level summary.
    summary = build_neighbourhood_summary(
        listings=listings,
        segments=segments,
    )

    # Ensure output satisfies all quality checks.
    validate_summary(summary)

    # Required homework output locations.
    output_csv = Path(
        "data/processed/airbnb_neighbourhood_summary.csv"
    )

    report_md = Path(
        "reports/hw01_a_run_report.md"
    )

    # Create parent directories if needed.
    output_csv.parent.mkdir(parents=True, exist_ok=True)
    report_md.parent.mkdir(parents=True, exist_ok=True)

    # Persist final dataset.
    summary.to_csv(output_csv, index=False)

    # Generate a simple run report.
    report_contents = f''' Airbnb Pipeline Run Report

## Run Summary

- Rows produced: {len(summary)}
- Columns produced: {len(summary.columns)}

## Output Files

- CSV: {output_csv}
- Report: {report_md}

## Validation

All validation checks passed successfully.
'''

    report_md.write_text(report_contents)

    typer.echo("Pipeline completed successfully.")
    typer.echo(f"Output written to: {output_csv}")
    typer.echo(f"Report written to: {report_md}")

if __name__ == "__main__":
    app()

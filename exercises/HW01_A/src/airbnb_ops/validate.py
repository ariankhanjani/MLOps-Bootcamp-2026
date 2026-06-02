
import pandas as pd

# Columns expected in the final neighbourhood summary.
REQUIRED_OUTPUT_COLUMNS = {
    "neighbourhood",
    "num_listings",
    "avg_price",
    "availability_365_avg",
}


# PII columns that must never appear in the final output.
FORBIDDEN_PII_COLUMNS = {
    "host_name",
    "host_id",
}


def validate_summary(summary: pd.DataFrame) -> None:
    '''
    Validate the final neighbourhood summary.

    Raises:
        ValueError: If any validation check fails.
    '''

    # The pipeline should never produce an empty output.
    if summary.empty:
        raise ValueError("Summary output is empty.")

    # Ensure all required columns are present.
    missing_columns = REQUIRED_OUTPUT_COLUMNS - set(summary.columns)
    if missing_columns:
        raise ValueError(
            f"Missing required output columns: {missing_columns}"
        )

    # Ensure no direct PII columns leaked into the output.
    present_pii = FORBIDDEN_PII_COLUMNS.intersection(summary.columns)
    if present_pii:
        raise ValueError(
            f"PII columns found in output: {present_pii}"
        )

    # Every row must belong to a neighbourhood.
    if summary["neighbourhood"].isna().any():
        raise ValueError("Null values found in neighbourhood column.")

    # Aggregated listing counts must be positive.
    if (summary["num_listings"] <= 0).any():
        raise ValueError(
            "num_listings must be greater than 0."
        )

    # Average prices cannot be negative.
    if (summary["avg_price"] < 0).any():
        raise ValueError(
            "avg_price must be non-negative."
        )

    # Average availability must be within valid Airbnb bounds.
    invalid_availability = (
        (summary["availability_365_avg"] < 0)
        | (summary["availability_365_avg"] > 365)
    )

    if invalid_availability.any():
        raise ValueError(
            "availability_365_avg must be between 0 and 365."
        )


import pandas as pd

REQUIRED_LISTING_COLUMNS = {
    "neighbourhood",
    "price",
    "minimum_nights",
    "availability_365",
    "number_of_reviews",
}

REQUIRED_SEGMENT_COLUMNS = {
    "neighbourhood",
    "tourism_segment",
    "priority_level",
}


def build_neighbourhood_summary(
    listings: pd.DataFrame,
    segments: pd.DataFrame,
) -> pd.DataFrame:

    missing_listing_cols = REQUIRED_LISTING_COLUMNS - set(listings.columns)
    if missing_listing_cols:
        raise ValueError(
            f"Listings missing required columns: {missing_listing_cols}"
        )

    missing_segment_cols = REQUIRED_SEGMENT_COLUMNS - set(segments.columns)
    if missing_segment_cols:
        raise ValueError(
            f"Segments missing required columns: {missing_segment_cols}"
        )

    summary = (
        listings.groupby("neighbourhood", as_index=False)
        .agg(
            num_listings=("listing_id", "count"),
            avg_price=("price", "mean"),
            median_price=("price", "median"),
            avg_minimum_nights=("minimum_nights", "mean"),
            availability_365_avg=("availability_365", "mean"),
            total_reviews=("number_of_reviews", "sum"),
        )
    )

    summary["reviews_per_listing"] = (
        summary["total_reviews"] / summary["num_listings"]
    )

    summary = summary.merge(
        segments,
        on="neighbourhood",
        how="left",
    )

    summary["tourism_segment"] = summary["tourism_segment"].fillna("unknown")
    summary["priority_level"] = summary["priority_level"].fillna("unknown")

    return summary


from hashlib import sha256
import pandas as pd


DIRECT_PII_COLUMNS = ["host_name"]

def pseudonymize_value(value, salt: str = "qbc12") -> str:
    '''
    Convert a sensitive identifier into a deterministic pseudonymous key.

    Args:
        value: Original identifier value.
        salt: Additional secret string used during hashing.

    Returns:
        SHA-256 hash represented as a hexadecimal string.
    '''

    raw_value = f"{salt}{value}"

    return sha256(raw_value.encode("utf-8")).hexdigest()


def handle_pii(df: pd.DataFrame) -> pd.DataFrame:
    '''
    Remove direct PII and pseudonymize host identifiers.

    Transformations:
    - Drop 'host_name'
    - Convert 'host_id' -> 'host_key'
    - Drop original 'host_id'
    '''

    # Work on a copy to avoid modifying the caller's DataFrame.
    df = df.copy()

    # Remove direct PII columns if they exist.
    existing_pii = [col for col in DIRECT_PII_COLUMNS if col in df.columns]
    df = df.drop(columns=existing_pii)

    # Create a pseudonymous host key from the original host_id.
    if "host_id" in df.columns:
        df["host_key"] = df["host_id"].apply(pseudonymize_value)

        # Remove the original identifier after pseudonymization.
        df = df.drop(columns=["host_id"])

    return df

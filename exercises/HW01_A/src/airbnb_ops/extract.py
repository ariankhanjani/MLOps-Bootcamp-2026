
from pathlib import Path
import pandas as pd

def read_csv_checked(path: Path) -> pd.DataFrame:
    '''
    Read a CSV file and return it as a DataFrame.

    Raises:
        FileNotFoundError: If the specified file does not exist.
    '''
    if not path.is_file():
        raise FileNotFoundError(f"File not found: {path}")

    return pd.read_csv(path)

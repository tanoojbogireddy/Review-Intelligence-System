"""
utils/io_helpers.py
-------------------
I/O utilities for RIAS:
  - load_csv : load a raw CSV into a pandas DataFrame
  - export_csv : convert a DataFrame to a UTF-8 CSV byte string
                 ready for Streamlit's st.download_button
"""

from __future__ import annotations

import io
import pandas as pd


def load_csv(file_obj) -> pd.DataFrame:
    """
    Load a CSV file into a DataFrame.

    Accepts either:
      - A file-like object (e.g. Streamlit UploadedFile)
      - A string / Path to a local file

    Returns
    -------
    pd.DataFrame
        Raw dataframe with all original columns preserved.

    Raises
    ------
    ValueError
        If the file cannot be parsed as a CSV.
    """
    try:
        df = pd.read_csv(file_obj, encoding="utf-8")
    except UnicodeDecodeError:
        # Try latin-1 as a fallback for files with Windows-style encoding
        df = pd.read_csv(file_obj, encoding="latin-1")
    except Exception as exc:
        raise ValueError(f"Failed to read CSV: {exc}") from exc

    return df


def export_csv(df: pd.DataFrame) -> bytes:
    """
    Serialise a DataFrame to a UTF-8 CSV byte string.

    Designed for use with Streamlit's st.download_button:
        st.download_button("Download", data=export_csv(df), ...)

    Returns
    -------
    bytes : UTF-8 encoded CSV content
    """
    buffer = io.StringIO()
    df.to_csv(buffer, index=False, encoding="utf-8")
    return buffer.getvalue().encode("utf-8")

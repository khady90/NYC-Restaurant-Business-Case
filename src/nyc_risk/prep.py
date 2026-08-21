import pandas as pd 
from nyc_risk.config import GRADABLE_INSP_TYPES, GRADABLE_ACTIONS, GRADABLE_MIN_DATE

def filter_gradable_inspections(
    df: pd.DataFrame,
    gradable_insp_types: list[str] | None = None,
    gradable_actions: list[str] | None = None,
    min_date: str = GRADABLE_MIN_DATE,
) -> pd.DataFrame:
    """Filter inspection records to those eligible for a risk grade.

    An inspection is gradable if its inspection type and action are both
    in the allowed sets, and it occurred on or after min_date.
    inspection_date is cast to datetime as part of filtering.

    Args:
        df: Raw or partially processed inspection records. Must contain
            'inspection_type', 'action', and 'inspection_date' columns.
        gradable_insp_types: Inspection type strings that qualify as
            gradable. Defaults to GRADABLE_INSP_TYPES from config.
        gradable_actions: Action strings that qualify as gradable.
            Defaults to GRADABLE_ACTIONS from config.
        min_date: Earliest inspection date (ISO string) to include.
            Defaults to GRADABLE_MIN_DATE from config.

    Returns:
        A new DataFrame containing only gradable inspection records,
        with inspection_date cast to datetime. The input df is not modified.
    """
    if gradable_insp_types is None:
        gradable_insp_types = GRADABLE_INSP_TYPES
    if gradable_actions is None:
        gradable_actions = GRADABLE_ACTIONS

    df = df.copy()
    df["inspection_date"] = pd.to_datetime(df["inspection_date"], errors="coerce")

    return df[
        df["inspection_type"].isin(gradable_insp_types)
        & df["action"].isin(gradable_actions)
        & (df["inspection_date"] >= pd.Timestamp(min_date))
    ]
URL: str = "https://data.cityofnewyork.us/resource/43nn-pn8j.csv?$limit=100000"

RELEVANT_COLS: list[str] = ['camis', 'dba', 'boro', 'inspection_date', 'action', 'violation_code',
       'violation_description', 'critical_flag', 'score', 'grade',
       'grade_date', 'inspection_type']

GRADABLE_INSP_TYPES: list[str] = [
    "Cycle Inspection / Initial Inspection",
    "Cycle Inspection / Re-inspection",
    "Pre-permit (Operational) / Initial Inspection",
    "Pre-permit (Operational) / Re-inspection"
]

GRADABLE_ACTIONS: list[str] = ["Violations were cited in the following area(s).",
                     "No violations were recorded at the time of this inspection.",
                     "Establishment Closed by DOHMH.Violations were cited in the following area(s) and those requiring immediate action were addressed."]

GRADABLE_MIN_DATE: str = "2010-07-27"

RISK_MAPPING: dict[str, str] = {
    "A": "Low",
    "B": "Moderate",
    "C": "High"
}

BOROUGH_URL: str = (
    "https://data.cityofnewyork.us/api/v3/views/"
    "gthc-hcne/query.geojson?accessType=DOWNLOAD"
)

# NYC Restaurant Inspection Risk Analysis

## Project overview

This project analyzes NYC restaurant inspection data to identify patterns associated with inspection risk and to classify inspections into three risk categories:

- **Low** — Grade A
- **Moderate** — Grade B
- **High** — Grade C

The analysis combines exploratory data analysis, data preparation, inspection-level aggregation, feature engineering, borough-level high-risk analysis, and a baseline classification model.

## Analytical approach

The analysis follows this workflow:

1. **Explore the source data**  
   Examine the complete restaurant inspection dataset to understand its structure, variables, missing values, and overall data quality.

2. **Define the analytical population**  
   Identify gradable inspections based on inspection type, action, and inspection date. A separate EDA is performed on this analytical population.

3. **Define the target**  
   Map inspection grades to risk categories:
   - A → Low
   - B → Moderate
   - C → High

   Records without grades A, B, or C are excluded from the modeling dataset.

4. **Aggregate to inspection level**  
   The source data contains multiple rows for an inspection because records are stored at the violation level. Records are therefore aggregated by restaurant (`camis`) and inspection date to create one row per inspection.

5. **Engineer features**
   - Violation-code features are created from violation-level records.
   - `violation_count` and `critical_count` summarize the inspection.
   - Borough is represented using one-hot encoding.
   - Inspection month is represented using one-hot encoding.

6. **Analyze high-risk inspections geographically**  
   High-risk inspection rates are compared across NYC boroughs and visualized on a geographic map.

7. **Build a baseline model**  
   A multinomial Logistic Regression classifier with balanced class weights is trained as a baseline and evaluated using accuracy, macro-F1, a classification report, and a confusion matrix. Model coefficients are inspected to understand features associated with the High-risk class.

## Key findings

### Borough-level analysis

Among the five NYC boroughs, the highest observed High-risk inspection rate is in **Queens**, while the lowest is in **Staten Island**.

| Borough | Inspections | High-risk inspections | High-risk rate |
|---|---:|---:|---:|
| Queens | 7,246 | 525 | 7.25% |
| Brooklyn | 7,805 | 451 | 5.78% |
| Manhattan | 11,666 | 640 | 5.49% |
| Bronx | 3,004 | 164 | 5.46% |
| Staten Island | 1,056 | 42 | 3.98% |

The borough comparison is descriptive: it shows differences in observed high-risk inspection rates and does not by itself establish causation.

### Baseline classification model

The final modeling dataset contains **30,812 inspections** and **82 model features**.

Target distribution:

- Low: **82.75%**
- Moderate: **11.32%**
- High: **5.92%**

The baseline Logistic Regression achieved:

- **Accuracy:** 0.67
- **Macro-F1:** 0.49

The model identifies a substantial share of High-risk inspections (recall **0.53**) but has lower precision for the High-risk and Moderate classes. This reflects the difficulty of classification under the strongly imbalanced target distribution.

The model interpretation also shows that several violation-code features and inspection-level violation counts have positive coefficients for the High-risk class.

## Data preparation notes

### Gradable inspections

The analysis focuses on four inspection types:

- Cycle Inspection / Initial Inspection
- Cycle Inspection / Re-inspection
- Pre-permit (Operational) / Initial Inspection
- Pre-permit (Operational) / Re-inspection

The analysis also restricts inspections to those on or after **2010-07-27** and uses selected inspection actions that allow a risk category to be defined.

### Missing violation features

Violation-code features are merged back to the inspection-level dataset. Inspections without recorded violation-code features are investigated separately. Where no violation codes are observed, the corresponding engineered violation features are represented as zero.

### Borough data quality

The borough field contains 35 records coded as `"0"` rather than one of the five NYC boroughs. These records are excluded from the borough-level geographic analysis but retained in the modeling dataset as their own categorical value.

### Feature exclusions

The target `risk_category` is excluded from the feature matrix. The original `grade` is also excluded because it directly defines the target and would cause target leakage.

Identifiers and raw fields not used directly as model features (`camis`, `inspection_date`, `boro`, and `inspection_month`) are also excluded after the relevant information has been represented through engineered features.

## Model evaluation

The data is split into:

- **80% training data**
- **20% test data**

The split uses `stratify=y` so that the class proportions remain approximately consistent between training and test sets.

The baseline model uses:

```python
LogisticRegression(
    class_weight="balanced",
    max_iter=1000,
    random_state=42
)
```

Macro-F1 is reported alongside accuracy because the target classes are strongly imbalanced and performance across all classes is important.

## Important interpretation note

The target is derived from the inspection grade, while several predictors are derived from information recorded during the same inspection, including violation counts and violation-code features.

Therefore, the baseline model should be interpreted as identifying **patterns associated with inspection risk within the available inspection records**, rather than as evidence of prospective prediction before an inspection takes place.

## Data source

The notebook loads the NYC restaurant inspection data from the NYC Open Data API:

`https://data.cityofnewyork.us/resource/43nn-pn8j.csv?$limit=100000`

Borough boundary data for the geographic visualization is retrieved from NYC Open Data in GeoJSON format.

## Installation

The project environment and required Python packages are specified in `requirements.txt`.

Install the dependencies with:

```bash
pip install -r requirements.txt
```

The notebook can then be opened and run in Jupyter Notebook or JupyterLab.

## Tools and libraries

The analysis is implemented in Python using:

- pandas
- NumPy
- seaborn
- Matplotlib
- GeoPandas
- scikit-learn
- Data Profiling
- requests

## Notebook

The main analysis is contained in:

`NYCRIRC_final.ipynb`

The notebook is organized as:

1. Project Setup
2. Data Loading and Initial Exploration
3. Data Preparation & Target Definition
4. Inspection-Level Aggregation
5. Feature Engineering
6. Borough-level High-Risk Analysis
7. Baseline Model and Evaluation

# Sleep Health and Lifestyle Analysis

## Project Overview

This project analyzes the relationship between sleep habits, lifestyle factors, and health indicators using the Sleep Health and Lifestyle Dataset. The objective is to identify patterns affecting sleep quality and overall well-being through data cleaning, statistical analysis, visualization, and correlation studies.

## Objectives

* Analyze factors influencing sleep quality.
* Study the impact of stress, physical activity, age, and daily habits on sleep.
* Explore relationships between health metrics such as blood pressure, heart rate, and sleep duration.
* Generate meaningful visualizations and business insights from the dataset.

## Dataset Information

The dataset contains information related to:

* Age
* Gender
* Occupation
* Sleep Duration
* Quality of Sleep
* Physical Activity Level
* Stress Level
* BMI Category
* Blood Pressure
* Heart Rate
* Daily Steps
* Sleep Disorders

## Technologies Used

* Python
* Pandas
* NumPy
* Matplotlib
* Seaborn

## Project Workflow

### 1. Data Cleaning

* Handled missing values.
* Standardized BMI categories.
* Split blood pressure into systolic and diastolic values.
* Checked duplicate records.
* Verified data types.

### 2. Exploratory Data Analysis

* Summary statistics generation.
* Distribution analysis.
* Category-wise comparisons.
* Occupation-based sleep quality analysis.

### 3. Correlation Analysis

* Pearson correlation matrix.
* Identification of factors strongly associated with sleep quality.

### 4. Data Visualization

Visualizations include:

* Sleep duration distribution
* Sleep quality distribution
* Sleep quality vs stress level
* Physical activity analysis
* Correlation heatmap
* Blood pressure trends
* Lifestyle factor comparisons

## Key Findings

* Higher stress levels are generally associated with lower sleep quality.
* Increased physical activity tends to improve sleep quality.
* Sleep duration shows a positive relationship with quality of sleep.
* Health indicators such as heart rate and blood pressure exhibit noticeable associations with lifestyle habits.

## Repository Structure

```text
├── analysis.py
├── Sleep_health_and_lifestyle_dataset.csv
├── cleaned_sleep_data.csv
├── summary_statistics.csv
├── correlation_matrix.csv
├── figures/
├── Project_Report.pdf
├── Presentation.pptx
└── README.md
```

## How to Run

1. Clone the repository:

```bash
git clone <repository-link>
```

2. Install dependencies:

```bash
pip install pandas numpy matplotlib seaborn
```

3. Run the analysis:

```bash
python analysis.py
```

## Results

The project generates:

* Cleaned dataset
* Summary statistics
* Correlation matrix
* Multiple visualizations
* Analytical insights regarding sleep health and lifestyle factors

## Author

**Akhil Bedi**
Data Science Student

## License

This project is created for educational and academic purposes.

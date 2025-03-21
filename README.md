# Vaccination Data Analysis Project

## Project Overview

This project focuses on analyzing and visualizing global vaccination data to provide insights into vaccination trends, disease incidence, and resource allocation. It leverages Python for data extraction and cleaning, SQL for database management, and Tableau for interactive dashboards.

---

## Table of Contents

- [Introduction](#introduction)
- [Technologies Used](#technologies-used)
- [Directory Structure](#directory-structure)
- [Data Sources](#data-sources)
- [Setup and Installation](#setup-and-installation)
- [Key Features](#key-features)
- [Deliverables](#deliverables)
- [Insights Generated](#insights-generated)

---

## Introduction

The Vaccination Data Analysis project aims to address key public health challenges by analyzing vaccination data and providing actionable insights. Key objectives include:

- Understanding vaccination coverage trends over time and across regions.
- Identifying regions with high disease incidence despite vaccination efforts.
- Evaluating vaccination drop-off rates between doses.

---

## Technologies Used

- **Python**: Data extraction, cleaning, and visualization.
- **SQL**: Structured and normalized database setup.
- **Tableau**: Interactive dashboards for data visualization.

---

## Directory Structure
```
Vaccination-Data-Analysis
│
├── analysis_scripts
│   ├── plot_helpers.py
│   ├── data_cleaning.py
│   ├── data_extraction.py
│
├── cleaned_xlsx
│   ├── cleaned_coverage_data.xlsx
│   ├── cleaned_incidence_rate.xlsx
│   ├── cleaned_reported_cases.xlsx
│   ├── cleaned_vaccine_introduction.xlsx
│   ├── cleaned_vaccine_schedule_data.xlsx
│
├── dashboards
│   ├── vaccination_dashboard.pbix
│
├── database
│   ├── create_tables.sql
│   ├── insert_data.sql
│   ├── queries.sql
│
├── README.md
└── .env
```

## Data Sources

The analysis uses cleaned versions of the following datasets:

1. `coverage_data.xlsx`: Vaccination coverage by region and year.
2. `incidence_rate.xlsx`: Disease incidence rates across regions.
3. `reported_cases.xlsx`: Reported cases of vaccine-preventable diseases.
4. `vaccine_introduction.xlsx`: Details on vaccine introductions.
5. `vaccine_schedule_data.xlsx`: National immunization schedules.

---

## Setup and Installation

1. Clone the repository:
2. Set up a Python virtual environment and install dependencies:
3. Configure database connection details in the `.env` file.
4. Run SQL scripts in the `database` folder to set up and populate the database.
5. Open Tableau and connect to the database or load the `vaccination_dashboard.twb` file.

---

## Key Features

- **Data Cleaning**: Handled missing values, inconsistent formats, and outliers.
- **Exploratory Data Analysis**:
  - Trends in vaccination coverage.
  - Correlations between vaccination coverage and disease incidence.
- **Interactive Dashboards**: Tableau dashboards showcasing key insights.

---

## Deliverables

1. **Python Scripts**: For data extraction and cleaning.
2. **SQL Database**: Structured and normalized for easy querying.
3. **Tableau Dashboards**: Interactive visualizations with actionable insights.

---

## Insights Generated

- **Vaccination Trends**: Identified trends in vaccination uptake over time.
- **Disease Incidence Analysis**: Highlighted regions with high disease incidence despite high vaccination rates.
- **Resource Allocation**: Provided insights for targeted interventions in underperforming regions.

---

## Note

Ensure that your database credentials are securely stored and not shared in public repositories.

## Plots






<img width="1652" alt="image" src="https://github.com/user-attachments/assets/64b88904-b7a8-422a-b9d1-40e9f69c6a51" />

![alt text](image.png)
![alt text](image-1.png)
![alt text](image-2.png)


Tableau Plots

<img width="1697" alt="image" src="https://github.com/user-attachments/assets/4e40e966-fec2-4ab8-9cb5-29e86c104469" />

<img width="1371" alt="image" src="https://github.com/user-attachments/assets/3d6ec971-edd2-49e7-bf4a-34347aca6075" />

<img width="1377" alt="image" src="https://github.com/user-attachments/assets/b0c1c29d-5516-47e7-8040-14ef152e87e7" />

<img width="1498" alt="image" src="https://github.com/user-attachments/assets/4ab770f6-f25d-4a20-a10a-6087d0a6b35f" />

<img width="1461" alt="image" src="https://github.com/user-attachments/assets/f8963fdf-dbc3-496c-ace7-0f98c1333f52" />

<img width="1488" alt="image" src="https://github.com/user-attachments/assets/18a69e72-d5d3-4727-91c2-4313374ca04d" />


<img width="1480" alt="image" src="https://github.com/user-attachments/assets/e6f8a649-6d52-43ee-9aae-acc2a2a071b4" />

<img width="1491" alt="image" src="https://github.com/user-attachments/assets/76bcecdb-04f9-46d8-9a90-1d7546decf3f" />



Streamlit app screens

<img width="1656" alt="image" src="https://github.com/user-attachments/assets/86193244-5665-4bad-8ed1-c071c76bd922" />

<img width="1681" alt="image" src="https://github.com/user-attachments/assets/9c9026e7-7cb8-40d5-b4dd-d9caf81eb7bb" />

<img width="1651" alt="image" src="https://github.com/user-attachments/assets/dc6b5f46-94a3-4db6-ae9f-0d3ef0f495d3" />

<img width="1642" alt="image" src="https://github.com/user-attachments/assets/57d08f37-8523-45b5-8e38-dee449dd0576" />

<img width="1665" alt="image" src="https://github.com/user-attachments/assets/0b2a7485-debc-4d34-8e4d-ad81b0477781" />

<img width="1631" alt="image" src="https://github.com/user-attachments/assets/674642e8-7e3e-4e2b-b2ba-2fd1b9ba4e72" />


<img width="1635" alt="image" src="https://github.com/user-attachments/assets/f5c627e6-75be-4270-a4be-eae0ed65597f" />

<img width="1623" alt="image" src="https://github.com/user-attachments/assets/1a566613-9d3e-4995-9153-caea8835b0f4" />













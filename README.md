# 🌦️ Weather Data Pipeline

A beginner-friendly Data Engineering project that collects weather data from an API, stores it in MySQL, cleans the data using Pandas, and exports it to Parquet files.

## 📌 Project Overview

This project demonstrates a simple ETL (Extract, Transform, Load) pipeline using Python.

The pipeline fetches current weather data for Dehradun, Uttarakhand, and processes it through different stages.

## 🛠️ Technologies Used

- Python
- Open-Meteo API
- MySQL
- Pandas
- Requests
- PyArrow
- Parquet
- Windows Task Scheduler

## 🔄 Pipeline Workflow

1. **Extract:** Fetch current weather data from the Open-Meteo API.
2. **Load Raw Data:** Store the fetched data in the MySQL `weather_raw` table.
3. **Transform:** Use Pandas to remove duplicate rows, handle missing values, and validate weather measurements.
4. **Load Cleaned Data:** Store the cleaned data in the MySQL `weather_cleaned` table.
5. **Export:** Save the cleaned data as Parquet files.
6. **Automation:** Schedule the pipeline to run daily using Windows Task Scheduler.

## 📁 Project Structure

```text
weather-data-pipeline/
│
├── api.py
├── clean_data.py
├── run_pipeline.py
├── .gitignore
└── README.md

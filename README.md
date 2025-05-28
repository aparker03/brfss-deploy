## BRFSS Depression Index Explorer

[![Streamlit App](https://img.shields.io/badge/launch-app-brightgreen)](https://state-of-mind.streamlit.app/)

This interactive web application allows users to explore depression-related health patterns in the United States using the 2022 Behavioral Risk Factor Surveillance System (BRFSS) dataset. The app features a custom Depression Index (DI) constructed from selected mental health and social variables, enabling users to filter by demographic groups, apply different imputation methods, and visualize outcomes in real time.

## Live App

Access the deployed application here: [state-of-mind.streamlit.app](https://state-of-mind.streamlit.app/)

> **Note:** The deployed version of this app uses a sampled subset of the full 2022 BRFSS dataset to optimize performance on Streamlit Cloud.  
> For full access to all features and data, please run the app locally using the installation instructions below.

## Features

This Streamlit app provides an interactive interface for exploring mental health patterns using data from the 2022 Behavioral Risk Factor Surveillance System (BRFSS). Key features include:

- **Custom Depression Index (DI):** A weighted score built on seven variables including PHQ-9 items and social support metrics.
- **Live Filtering:** Adjust filters for sex, general health, and education level to update visuals and statistics in real time.
- **Visualizations:**
  - Histogram and summary statistics of DI
  - Choropleth map showing average DI by U.S. state
  - Boxplots comparing DI across demographic groups
- **Imputation Selection:** Choose from multiple imputation strategies (median, mean, mode, zero, or none) to observe how data cleaning affects trends.
- **CSV Download:** Export a custom version of the dataset based on active filters.

The application is designed for accessibility, clarity, and ease of exploration across devices.

## Installation

To run the app locally, follow these steps:

1. **Clone the repository:**

    ```
    git clone https://github.com/aparker03/brfss-deploy.git
    cd brfss-deploy
    ```

2. **(Optional) Create and activate a virtual environment:**

    ```
    python -m venv venv
    source venv/bin/activate  # On Windows use venv\Scripts\activate
    ```

3. **Install the required dependencies:**

    ```
    pip install -r requirements.txt
    ```

4. **Run the app:**

    ```
    streamlit run brfss_app.py
    ```

The app will open in your browser at `http://localhost:8501`.

## Usage

Once the app is running, you can explore mental health trends using an interactive interface built on BRFSS 2022 data.

### Available Features:

- **Filter by demographic variables:**
  - Sex (Male, Female)
  - General Health (e.g., Excellent, Good, Poor)
  - Education Level (from Kindergarten to College Graduate)

- **Select an imputation method** to handle missing values:
  - Median
  - Mean
  - Mode
  - Zero
  - None (no imputation)

- **View the following visualizations:**
  - Histogram and summary statistics for the Depression Index (DI)
  - Choropleth map of average DI by U.S. state
  - Boxplots comparing DI across selected groups

- **Download filtered data** as a CSV for additional analysis.

The application is designed to support interactive exploration and reproducible analysis of behavioral health indicators.

## Project Structure

The repository is organized to support modular, maintainable development:

- `brfss_app.py` — Main Streamlit app script  
- `requirements.txt` — Python dependencies  
- `README.md` — Project overview and usage  
- `utils/` — Modular app components  
  - `__init__.py`  
  - `load.py` — Loads and prepares raw data  
  - `clean.py` — Data cleaning, imputation, and DI computation  
  - `ui.py` — Sidebar filters, layout configuration, footer  
  - `viz.py` — Visualizations (histogram, choropleth, boxplot, download)  

Each module is designed to be reusable and easy to maintain.  
The app automatically loads data remotely, so no large local files are needed for deployment.

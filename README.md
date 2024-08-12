# Currency Exchange Rate Tracker

This project is a web application that allows users to track and visualize relative changes in currency exchange rates for various countries over a selected date range. The application is built using Python, following an Object-Oriented Programming (OOP) approach, and runs within its own virtual environment.

## Table of Contents

- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [Structure](#structure)

## Features

- **Currency Rate Fetching**: Fetches exchange rates for USD, EUR, GBP, JPY, TRY, INR, and CNY for a user-specified date range from [finmarket.ru](https://www.finmarket.ru).
- **Country Currency Data**: Retrieves and updates the list of world currencies from [iban.ru](https://www.iban.ru/currency-codes).
- **Data Synchronization**: Synchronizes fetched data with a local SQLite database, ensuring only changed or new records are updated.
- **Relative Rate Calculation**: Calculates and stores relative changes in exchange rates for each country, based on a user-selected reference date.
- **Interactive Web Interface**: Users can visualize relative changes in currency rates for selected countries over a chosen date range.

## Prerequisites

- Python 3.7+
- Virtual Environment (`venv`)
- Internet connection for fetching data

## Installation

1. **Clone the Repository:**

    ```bash
    git clone https://github.com/qwer112358/python_intern.git
    cd currencyProject
    ```

2. **Set up the Virtual Environment:**

    ```bash
    python3 -m venv venv
    source venv/bin/activate   # On Windows use `venv\Scripts\activate`
    ```

3. **Install Dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

## Usage

1. **Run the Web Application:**

    ```bash
    python manage.py runserver
    ```

2. **Access the Application:**

   Open your web browser and navigate to `http://127.0.0.1:8000/`.

3. **Interact with the Interface:**
   - Select a date range to fetch currency exchange rates.
   - Choose countries and date ranges to visualize relative changes in currency rates.

## Structure

- **`main/models.py`**: Contains the database models for storing currency and country data.
- **`main/views.py`**: Handles web requests and responses, rendering HTML templates.
- **`main/utils/scraper.py`**: Contains classes and methods for fetching and processing data from external sources.
- **`main/utils/SyncDB.py`**: Contains logic for calculating relative currency changes.
- **`main/utils/CurrencyPlot.py`**: Handles the creation and encoding of plots for visualizing relative changes in currency rates using Matplotlib and Pandas.
- **`main/templates/`**: HTML templates for the web interface.
![download](https://github.com/user-attachments/assets/b42590ed-cb35-445b-981b-1d9686c86dca)

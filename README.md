# EV Market Dashboard

A small, beginner-friendly Streamlit project based on the EV industry scenarios.

## Features
- Filter by year, vehicle category, and manufacturer
- Summary metrics for sales, range, customer ratings, and manufacturer count
- Charts for category sales, manufacturer sales, battery technology, driving range, manufacturing country, and customer ratings
- Table of the filtered records

## Run locally
1. Install Python 3.10 or newer.
2. Open a terminal in this project folder.
3. Install the dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Start the dashboard:

   ```bash
   streamlit run app.py
   ```

## Data note
`data/ev_market_sample.csv` is illustrative sample data created for this demo. It is not verified real-world market data. Replace it with a reliable dataset before using the dashboard for research or business decisions.

## Project structure
```text
ev_market_dashboard/
├── app.py
├── requirements.txt
├── README.md
└── data/
    └── ev_market_sample.csv
```

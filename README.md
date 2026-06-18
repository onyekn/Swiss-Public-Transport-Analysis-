# Swiss Public Transport Analysis

Analysis of Swiss public transport delays using real operational data from SBB (Swiss Federal Railways), covering a full week (June 8–14, 2026). Built a Python data cleaning pipeline and an interactive Tableau dashboard to surface delay patterns by station, hour, and day of week.

## Data Source
- [opentransportdata.swiss](https://opentransportdata.swiss) — official Swiss public transport open data portal
- Raw "Ist-Daten" (actual vs. scheduled times), ~2.5M records per day across all transport modes (trains, buses, trams)
- Filtered down to a clean, analysis-ready subset for this project

## Process
1. Loaded and cleaned 7 days of raw CSV data using pandas
2. Translated German column names to English
3. Parsed mismatched datetime formats (scheduled vs. actual times)
4. Computed arrival and departure delay in minutes
5. Filtered outliers (data errors, midnight rollovers)
6. Aggregated by station, line, hour, and day of week
7. Built an interactive dashboard in Tableau

## Key Findings
- **Basel SBB has the highest average arrival delay (1.44 minutes)** among major stations, followed by Zürich HB (1.27 min) and Zürich Flughafen (1.24 min) — suggesting the busiest interchange hubs experience more congestion-driven delay than smaller stations.
- **Delays follow a clear weekly pattern**: Tuesday has the highest average delay (~1.04 min), while Sunday has the lowest (~0.73 min), consistent with heavier weekday commuter traffic.
- **S1 is by far the busiest line**, with 59,402 trips over the week — roughly 40% more than the second-busiest line (S14, 42,693 trips) — highlighting it as a critical artery in the Swiss S-Bahn network.

## Tools
Python (pandas), Tableau

## Files
- `clean_sbb_data.py` — data cleaning and aggregation script
- `sbb_summary_for_tableau.csv` — station-level aggregated data
- `sbb_line_summary_for_tableau.csv` — line-level aggregated data

## Dashboards
- [Station & Time Overview](https://public.tableau.com/views/Book1_17818217927350/StationTimeOverviewVis?:language=en-GB&publish=yes&:display_count=n&:origin=viz_share_link) — delay heatmap and station rankings
- [Routes & Trends](https://public.tableau.com/views/Book1_17818217927350/RoutesTrendsVis?:language=en-GB&publish=yes&:display_count=n&:origin=viz_share_link) — weekly delay trend and busiest routes

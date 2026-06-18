import pandas as pd
import glob

column_translation = {
    'BETRIEBSTAG': 'operating_day',
    'FAHRT_BEZEICHNER': 'trip_id',
    'BETREIBER_ID': 'operator_id',
    'BETREIBER_ABK': 'operator_abbr',
    'BETREIBER_NAME': 'operator_name',
    'PRODUKT_ID': 'product_type',
    'LINIEN_ID': 'line_id',
    'LINIEN_TEXT': 'line_name',
    'UMLAUF_ID': 'circulation_id',
    'VERKEHRSMITTEL_TEXT': 'vehicle_type',
    'ZUSATZFAHRT_TF': 'is_additional_trip',
    'FAELLT_AUS_TF': 'is_cancelled',
    'BPUIC': 'stop_id',
    'HALTESTELLEN_NAME': 'station_name',
    'ANKUNFTSZEIT': 'scheduled_arrival',
    'AN_PROGNOSE': 'actual_arrival',
    'AN_PROGNOSE_STATUS': 'arrival_status',
    'ABFAHRTSZEIT': 'scheduled_departure',
    'AB_PROGNOSE': 'actual_departure',
    'AB_PROGNOSE_STATUS': 'departure_status',
    'DURCHFAHRT_TF': 'is_passthrough',
    'SLOID': 'sloid'
}

files = glob.glob('2026-06-*_istdaten.csv')
print("Files found:", files)

all_dfs = []

for f in files:
    print(f"\nProcessing {f} ...")
    df = pd.read_csv(f, sep=';', low_memory=False)
    df = df.rename(columns=column_translation)

    # Keep trains only
    df = df[df['product_type'] == 'Zug']
    print(f"  -> {df.shape[0]} train rows")

    df = df[df['is_passthrough'] == False]
    df = df[df['is_cancelled'] == False]
    df = df.dropna(subset=['actual_arrival', 'actual_departure'], how='all')

    for col in ['scheduled_arrival', 'scheduled_departure']:
        df[col] = pd.to_datetime(df[col], format='%d.%m.%Y %H:%M', errors='coerce')
    for col in ['actual_arrival', 'actual_departure']:
        df[col] = pd.to_datetime(df[col], format='%d.%m.%Y %H:%M:%S', errors='coerce')

    df['arrival_delay_min'] = (df['actual_arrival'] - df['scheduled_arrival']).dt.total_seconds() / 60
    df['departure_delay_min'] = (df['actual_departure'] - df['scheduled_departure']).dt.total_seconds() / 60

    df = df[(df['arrival_delay_min'].between(-60, 120)) | df['arrival_delay_min'].isna()]
    df = df[(df['departure_delay_min'].between(-60, 120)) | df['departure_delay_min'].isna()]

    df['hour'] = df['scheduled_arrival'].dt.hour
    df['day_of_week'] = df['scheduled_arrival'].dt.day_name()
    df['date'] = df['scheduled_arrival'].dt.date

    print(f"  -> {df.shape[0]} rows after full cleaning")
    all_dfs.append(df)

combined = pd.concat(all_dfs, ignore_index=True)
print("\nCombined shape (trains only):", combined.shape)

# Station-level summary (for heatmap, rankings, peak hours)
summary = combined.groupby(['station_name', 'day_of_week', 'hour']).agg(
    avg_arrival_delay=('arrival_delay_min', 'mean'),
    avg_departure_delay=('departure_delay_min', 'mean'),
    num_trips=('trip_id', 'count')
).reset_index()
summary.to_csv('sbb_summary_for_tableau.csv', index=False)
print("Saved sbb_summary_for_tableau.csv:", summary.shape)

# Line-level summary (for "busiest routes")
line_summary = combined.groupby(['line_name', 'operator_name', 'day_of_week', 'hour']).agg(
    avg_arrival_delay=('arrival_delay_min', 'mean'),
    avg_departure_delay=('departure_delay_min', 'mean'),
    num_trips=('trip_id', 'count')
).reset_index()
line_summary.to_csv('sbb_line_summary_for_tableau.csv', index=False)
print("Saved sbb_line_summary_for_tableau.csv:", line_summary.shape)

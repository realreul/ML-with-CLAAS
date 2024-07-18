import pandas as pd
import os
import logging
from collections import defaultdict

# Logging konfigurieren
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def read_excel_files(file_paths):
    logging.info(f"Lese {len(file_paths)} Excel-Dateien ein...")
    dataframes = [pd.read_excel(file) for file in file_paths]
    combined_df = pd.concat(dataframes)
    logging.info("Excel-Dateien erfolgreich eingelesen und kombiniert.")
    return combined_df

def extract_and_create_columns(df, column_name):
    logging.info(f"Extrahiere und erstelle Spalten aus '{column_name}'...")
    if column_name in df.columns:
        split_columns = df[column_name].str.split()
        df['Merkmal'] = split_columns.str[0]
        df['Merkmalwert'] = split_columns.str[1]

        # Merkmalwert mit Merkmal und Bindestrich hinzufügen
        df['Merkmalwert'] = df['Merkmal'] + '-' + df['Merkmalwert']

        df['Maschinentyp'] = df['Seriennummer'].str[:3]
        logging.info("Spalten erfolgreich extrahiert und erstellt.")
    else:
        logging.error(f"Die Spalte {column_name} existiert nicht im DataFrame.")
    return df

def filter_and_clean_df(df, merkmale, columns_to_drop):
    logging.info("Filtere und bereinige DataFrame...")
    filtered_df = df[df['Merkmal'].isin(merkmale)].reset_index(drop=True)
    cleaned_df = filtered_df.drop(columns_to_drop, axis=1).reset_index(drop=True)
    logging.info("DataFrame erfolgreich gefiltert und bereinigt.")
    return cleaned_df

def calculate_monthly_aggregates(df):
    logging.info("ERstelle monatliche Zeitreihen...")
    monthly_aggregates = defaultdict(dict)
    total_monthly_by_merkmalname = {}

    grouped_by_merkmalname = df.groupby('Merkmal')
    for merkmalname, group in grouped_by_merkmalname:
        total_monthly = group.resample('M', on='Datum')['Bestätigte Menge'].sum()
        total_monthly_by_merkmalname[merkmalname] = total_monthly

    grouped = df.groupby(['Merkmal', 'Merkmalwert'])
    for (merkmalname, merkmalwert), group in grouped:
        monthly_data = group.resample('M', on='Datum')['Bestätigte Menge'].sum().reset_index()
        relative_share = monthly_data.set_index('Datum')['Bestätigte Menge'] / total_monthly_by_merkmalname[merkmalname].reindex(monthly_data['Datum'], fill_value=0)
        monthly_data['Relativer Anteil'] = relative_share.values
        monthly_data['Relativer Anteil'] = monthly_data['Relativer Anteil'].fillna(0)
        monthly_aggregates[merkmalname][merkmalwert] = monthly_data

    logging.info("Monatliche Zeitreihen erfolgreich erstellt.")
    return monthly_aggregates

def convert_aggregates_to_df(monthly_aggregates):
    logging.info("Konvertiere Zeitreihen in DataFrame...")
    rows = []
    for merkmal, merkmalwerte in monthly_aggregates.items():
        for merkmalwert, data_df in merkmalwerte.items():
            for _, row in data_df.iterrows():
                rows.append({
                    'Datum': row['Datum'],
                    'Merkmal': merkmal,
                    'Merkmalwert': merkmalwert,
                    'Bestätigte Menge': row['Bestätigte Menge'],
                    'Relativer Anteil': row['Relativer Anteil']
                })
    result_df = pd.DataFrame(rows)
    logging.info("Zeitreihen erfolgreich in DataFrame konvertiert.")
    return result_df

def read_and_process_external_files(directory):
    logging.info(f"Lese und verarbeite externe Dateien aus dem Verzeichnis '{directory}'...")
    file_list = [f for f in os.listdir(directory) if f.endswith('.xlsx')]
    dataframes = []

    for file in file_list:
        file_path = os.path.join(directory, file)
        df = pd.read_excel(file_path)
        df_reduced = df.iloc[:, -2:]
        df_reduced.columns = ['Datum', file.replace('.xlsx', '')]
        df_reduced = df_reduced[6:]
        df_reduced['Datum'] = pd.to_datetime(df_reduced['Datum'])
        df_reduced = df_reduced.sort_values(by='Datum').set_index('Datum')
        dataframes.append(df_reduced)

    combined_df = pd.concat(dataframes, axis=1)
    logging.info("Externe Dateien erfolgreich eingelesen und verarbeitet.")
    return combined_df

def merge_dataframes(result_df, combined_df):
    logging.info("Führe DataFrames zusammen...")
    result_df['Datum'] = pd.to_datetime(result_df['Datum'])
    combined_df.index = pd.to_datetime(combined_df.index)
    result_df['Datum'] = result_df['Datum'].dt.to_period('M').dt.to_timestamp()
    combined_df.index = combined_df.index.to_period('M').to_timestamp()
    merged_df = result_df.merge(combined_df, left_on='Datum', right_index=True, how='left')
    logging.info("DataFrames erfolgreich zusammengeführt.")
    return merged_df

def main():
    logging.info("Starte Hauptprozess...")
    excel_files = ['CLAAS_data/S611_Teil_1_P10_20240604.XLSX', 'CLAAS_data/S611_Teil_2_P10_20240604.XLSX']
    df = read_excel_files(excel_files)
    df = extract_and_create_columns(df, 'Merkmal/Wert/Bezeichng. f. Serienplanun')

    merkmale = ['P02', 'N02', 'N08', 'N05', 'B10', 'G02']
    columns_to_drop = ['Statistik-Herkunft', 'Version', 'Monat', 'Woche', 'Periode', 'Werk', 'Material', 
                       'Merkmal/Wert/Bezeichng. f. Serienplanun', 'GeschJahresvariante', 'Zeiger Verw.daten', 
                       'Basismengeneinheit', 'Bedarfsmenge']
    df = filter_and_clean_df(df, merkmale, columns_to_drop)
    df = df[['Datum', 'Geschäftsjahr', 'Seriennummer', 'Maschinentyp', 'CLAAS - Untertyp', 'Claas-Planungsland', 
             'Merkmal', 'Merkmalwert', 'Bestätigte Menge']]

    monthly_aggregates = calculate_monthly_aggregates(df)
    result_df = convert_aggregates_to_df(monthly_aggregates)

    combined_df = read_and_process_external_files('External_data')
    merged_df = merge_dataframes(result_df, combined_df)

    merged_df.to_csv('CLAAS_data/MLbase_DataFrame.csv', index=False)
    logging.info("Prozess abgeschlossen und DataFrame gespeichert.")

if __name__ == "__main__":
    main()
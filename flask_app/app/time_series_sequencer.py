import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler, LabelEncoder

class TimeSeriesSequencer:
    def __init__(self, file_path, date_column, target_column, sequence_length=12):
        """
        Initialisiert die Klasse TimeSeriesSequencer.

        :param file_path: Pfad zur CSV-Datei mit den Daten
        :param date_column: Spaltenname für das Datum
        :param target_column: Spaltenname für die Zielvariable
        :param sequence_length: Länge der Sequenzen
        """
        self.file_path = file_path
        self.date_column = date_column
        self.target_column = target_column
        self.sequence_length = sequence_length
        self.data = None
        self.label_encoders = {}
        self.scaler_X = MinMaxScaler()
        self.scaler_y = MinMaxScaler()
        self.load_data()
        self.fit_scalers()

    def load_data(self):
        """
        Lädt die Daten aus der CSV-Datei.
        """
        # Laden der CSV-Datei
        self.data = pd.read_csv(self.file_path)
        # Konvertieren der Datumsspalte in das Datetime-Format
        self.data[self.date_column] = pd.to_datetime(self.data[self.date_column])

    def fit_scalers(self):
        continuous_features = ['Monat_sin', 'Monat_cos', 'USTR10Y', 'WeizenSpot', 'CornSpot', 'GER10Y', 'WtiOilSpot', 'SoySpot', 'AgriSpot']
        if self.target_column in continuous_features:
            continuous_features.remove(self.target_column)
            self.scaler_X.fit(self.data[continuous_features])
        if self.target_column in self.data.columns:
            self.scaler_y.fit(self.data[[self.target_column]])
        else:
            raise KeyError(f"Target column '{self.target_column}' not found in the data.")

    def encode_categorical_features(self, categorical_features):
        """
        Kodiert kategoriale Merkmale mittels Label-Encoding.

        :param categorical_features: Liste der kategorialen Merkmale
        """
        for feature in categorical_features:
            # Initialisieren des LabelEncoders
            le = LabelEncoder()
            # Anpassen und Transformieren der Daten
            self.data[f'{feature}_encoded'] = le.fit_transform(self.data[feature])
            # Speichern des LabelEncoders
            self.label_encoders[feature] = le

    def normalize_features(self, continuous_features):
        """
        Normalisiert kontinuierliche Merkmale.

        :param continuous_features: Liste der kontinuierlichen Merkmale
        """
        # Normalisieren der kontinuierlichen Merkmale
        self.data[continuous_features] = self.scaler_X.transform(self.data[continuous_features])

    def normalize_target(self):
        """
        Normalisiert die Zielvariable.
        """
        self.data[self.target_column] = self.scaler_y.transform(self.data[[self.target_column]])

    def create_sequences(self, continuous_features, encoded_features):
        """
        Erstellt Sequenzen für das Training des Modells.

        :param continuous_features: Liste der kontinuierlichen Merkmale
        :param encoded_features: Liste der kodierten Merkmale
        :return: Sequenzen für die kontinuierlichen Merkmale, kodierten Merkmale, Zielvariablen, Startdaten und Merkmalwerte
        """
        X_cont_seq = []
        X_enc_seq = []
        y_seq = []
        start_dates = []
        merkmalwerte = []

        # Iteriere über alle Merkmalswerte
        for merkmalwert, group in self.data.groupby('Merkmalwert'):
            continuous_data = group[continuous_features].values
            encoded_data = group[encoded_features].values
            target_data = group[self.target_column].values
            dates = group[self.date_column].values
            
            # Erstelle Sequenzen für die aktuelle Gruppe
            for i in range(len(continuous_data) - self.sequence_length - 12 + 1):
                cont_seq = continuous_data[i:i+self.sequence_length]
                enc_seq = encoded_data[i:i+self.sequence_length]
                target_seq = target_data[i+self.sequence_length:i+self.sequence_length+12]
                X_cont_seq.append(cont_seq)
                X_enc_seq.append(enc_seq)
                y_seq.append(target_seq)
                start_dates.append(dates[i])
                merkmalwerte.append(merkmalwert)

        return np.array(X_cont_seq), np.array(X_enc_seq), np.array(y_seq), start_dates, merkmalwerte

    def get_data(self, categorical_features, continuous_features):
        """
        Lädt die Daten, kodiert kategoriale Merkmale, normalisiert kontinuierliche Merkmale und erstellt Sequenzen.

        :param categorical_features: Liste der kategorialen Merkmale
        :param continuous_features: Liste der kontinuierlichen Merkmale
        :return: Sequenzen für die kontinuierlichen Merkmale, kodierten Merkmale, Zielvariablen, Startdaten und Merkmalwerte
        """
        self.encode_categorical_features(categorical_features)
        self.normalize_features(continuous_features)
        self.normalize_target()
        encoded_features = [f'{feature}_encoded' for feature in categorical_features]
        return self.create_sequences(continuous_features, encoded_features)

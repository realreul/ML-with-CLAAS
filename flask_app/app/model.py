import pandas as pd
import tensorflow as tf
import numpy as np
from sklearn.preprocessing import MinMaxScaler, LabelEncoder
import joblib

def load_model(zielvariable):
    if zielvariable == 'Relativer Anteil':
        return tf.keras.models.load_model('models/deep_model18_tr.keras')
    elif zielvariable == 'Bestätige Menge':
        return tf.keras.models.load_model('models/deep_model18.keras')

def get_data(merkmal, merkmalswert, startdatum):
    dataset = pd.read_csv('data/MLbase_DataFrame.csv')
    dataset['Datum'] = pd.to_datetime(dataset['Datum'])
    startdatum = pd.to_datetime(startdatum)

    # Filtere die letzten 12 Monate vor dem Startdatum
    end_date = startdatum - pd.DateOffset(months=1)
    print(f"Enddatum: {end_date}")  # Debug-Ausgabe
    start_date = end_date - pd.DateOffset(months=11)
    print(f"Startdatum: {start_date}")  # Debug-Ausgabe
    if merkmalswert != "Alle Merkmalswerte":
        data = dataset[(dataset['Merkmal'] == merkmal) & (dataset['Merkmalwert'] == merkmalswert) & (dataset['Datum'] >= start_date) & (dataset['Datum'] <= end_date)]
    else:
        data = dataset[(dataset['Merkmal'] == merkmal) & (dataset['Datum'] >= start_date) & (dataset['Datum'] <= end_date)]
    
    return data

def load_preprocessors(zielvariable):
    if zielvariable == 'Relativer Anteil':
        scaler_y = joblib.load('models/scaler_y_tr.pkl')
    elif zielvariable == 'Bestätige Menge':
        scaler_y = joblib.load('models/scaler_y.pkl')

    scaler_X = joblib.load('models/scaler_X.pkl')
    label_encoders = joblib.load('models/label_encoders.pkl')
    return scaler_X, scaler_y, label_encoders

def predict(merkmal, merkmalswert, startdatum, zielvariable):
    # Anpassen des Zielvariablennamens
    if zielvariable == 'BestätigteMenge':
        zielvariable = 'Bestätige Menge'

    if zielvariable == 'OptionTakeRate':
        zielvariable = 'Relativer Anteil'

    model = load_model(zielvariable)
    data = get_data(merkmal, merkmalswert, startdatum)
    
    # Überprüfen, ob genügend Daten vorhanden sind
    if len(data) < 12:
        raise ValueError("Nicht genügend Daten für die Vorhersage vorhanden.")
    
    # Definiere die kontinuierlichen und kategorischen Merkmale
    continuous_features = ['Monat_sin', 'Monat_cos', 'USTR10Y', 'WeizenSpot', 'CornSpot', 'GER10Y', 'WtiOilSpot', 'SoySpot', 'AgriSpot']
    categorical_features = ['Merkmal', 'Merkmalwert']

    # Überprüfe, ob alle kontinuierlichen Merkmale in den Daten vorhanden sind
    if not all(feature in data.columns for feature in continuous_features + ['Jahr']):
        raise ValueError("Nicht alle kontinuierlichen Merkmale sind in den Daten vorhanden.")
    
    X_cont = data[continuous_features].values
    jahr = data['Jahr'].values.reshape(-1, 1)

    # Laden der gespeicherten Scaler und Encoder
    scaler_X, scaler_y, label_encoders = load_preprocessors(zielvariable)
    X_cont_scaled = scaler_X.transform(X_cont)
    
    # Kombiniere die skalierten kontinuierlichen Merkmale und die Jahr-Spalte
    X_cont_combined = np.hstack([jahr, X_cont_scaled])
    
    # Kodieren der kategorischen Merkmale
    X_cat_encoded = []
    for feature in categorical_features:
        encoder = label_encoders[feature]
        encoded_values = encoder.transform(data[feature].values)
        X_cat_encoded.append(encoded_values)
    X_cat_encoded = np.array(X_cat_encoded).T

    # Eingabeform für das Modell erstellen
    X_cont_combined = X_cont_combined.reshape(1, 12, len(continuous_features) + 1)
    X_cat_encoded = X_cat_encoded.reshape(1, 12, len(categorical_features))

    # Vorhersage erstellen
    predictions = model.predict([X_cont_combined] + [X_cat_encoded[:, :, i] for i in range(X_cat_encoded.shape[2])])
    predictions_rescaled = scaler_y.inverse_transform(predictions.reshape(-1, 12))

    print(f"Predictions rescaled before rounding: {predictions_rescaled}")  # Debug-Ausgabe

    if zielvariable == 'Bestätige Menge':
        predictions_rescaled = np.round(predictions_rescaled)
        print(f"Rounded predictions for Bestätige Menge: {predictions_rescaled}")  # Debug-Ausgabe
    elif zielvariable == 'Relativer Anteil':
        predictions_rescaled = np.round(predictions_rescaled, 4)
        print(f"Rounded predictions for Relativer Anteil: {predictions_rescaled}")  # Debug-Ausgabe
    
    return predictions_rescaled


def predict_all(merkmal, startdatum, zielvariable):
    # Anpassen des Zielvariablennamens
    if zielvariable == 'BestätigteMenge':
        zielvariable = 'Bestätige Menge'

    model = load_model(zielvariable)
    data = get_data(merkmal, "Alle Merkmalswerte", startdatum)
    
    # Definiere die kontinuierlichen und kategorischen Merkmale
    continuous_features = ['Monat_sin', 'Monat_cos', 'USTR10Y', 'WeizenSpot', 'CornSpot', 'GER10Y', 'WtiOilSpot', 'SoySpot', 'AgriSpot']
    categorical_features = ['Merkmal', 'Merkmalwert']

    scaler_X, scaler_y, label_encoders = load_preprocessors(zielvariable)

    results = []

    unique_merkmalswerte = data['Merkmalwert'].unique()
    print(f"Verarbeitete Merkmalswerte: {unique_merkmalswerte}")  # Ausgabe der einzigartigen Merkmalswerte

    for merkmalswert in unique_merkmalswerte:
        data_subset = data[data['Merkmalwert'] == merkmalswert]
        
        if len(data_subset) < 12:
            print(f"Nicht genügend Daten für den Merkmalswert {merkmalswert} vorhanden.")
            continue

        X_cont = data_subset[continuous_features].values
        jahr = data_subset['Jahr'].values.reshape(-1, 1)

        X_cont_scaled = scaler_X.transform(X_cont)
        X_cont_combined = np.hstack([jahr, X_cont_scaled])

        X_cat_encoded = np.array([label_encoders[feature].transform(data_subset[feature].values) for feature in categorical_features]).T

        X_cont_combined = X_cont_combined.reshape(1, 12, len(continuous_features) + 1)
        X_cat_encoded = X_cat_encoded.reshape(1, 12, len(categorical_features))

        predictions = model.predict([X_cont_combined] + [X_cat_encoded[:, :, i] for i in range(X_cat_encoded.shape[2])])
        #predictions_rescaled = np.round(scaler_y.inverse_transform(predictions.reshape(-1, 12)))
        predictions_rescaled = scaler_y.inverse_transform(predictions.reshape(-1, 12))

        if zielvariable == 'Bestätige Menge':
            predictions_rescaled = np.round(predictions_rescaled)
        elif zielvariable == 'Relativer Anteil':
            predictions_rescaled = np.round(predictions_rescaled, 4)

        results.extend([{'Merkmal': merkmal, 'Merkmalwert': merkmalswert, 'Monat': i+1, 'Vorhersage': pred} for i, pred in enumerate(predictions_rescaled[0])])
    
    return pd.DataFrame(results)



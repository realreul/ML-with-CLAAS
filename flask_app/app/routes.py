from flask import Blueprint, request, jsonify, send_file, render_template
from .model import load_model, get_data, predict, predict_all
import pandas as pd
import os
from io import BytesIO

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/predict', methods=['POST'])
def get_prediction():
    data = request.json
    merkmal = data.get('merkmal')
    merkmalswert = data.get('merkmalswert')
    startdatum = data.get('startdatum')
    zielvariable = data.get('zielvariable')


    if merkmalswert and merkmalswert != "Alle Merkmalswerte":
        predictions = predict(merkmal, merkmalswert, startdatum, zielvariable)
        print(f"Predictions for FE: {predictions}")  # Debug-Ausgabe
        return jsonify(predictions.tolist())
    else:
        predictions_df = predict_all(merkmal, startdatum, zielvariable)
        csv_buffer = BytesIO()
        predictions_df.to_csv(csv_buffer, index=False)
        csv_buffer.seek(0)
        return send_file(csv_buffer, as_attachment=True, mimetype='text/csv', download_name='predictions.csv')
    
    
@main.route('/get_merkmal', methods=['GET'])
def get_merkmal():
    dataset = pd.read_csv('data/MLbase_DataFrame.csv')
    merkmale = dataset['Merkmal'].unique().tolist()
    return jsonify(merkmale)

@main.route('/get_merkmalswert/<merkmal>', methods=['GET'])
def get_merkmalswert(merkmal):
    dataset = pd.read_csv('data/MLbase_DataFrame.csv')
    merkmalswerte = dataset[dataset['Merkmal'] == merkmal]['Merkmalwert'].unique().tolist()
    return jsonify(merkmalswerte)

@main.route('/get_dates/<merkmal>/<merkmalswert>', methods=['GET'])
def get_dates(merkmal, merkmalswert):
    dataset = pd.read_csv('data/MLbase_DataFrame.csv')
    if merkmalswert != "Alle Merkmalswerte":
        filtered_data = dataset[(dataset['Merkmal'] == merkmal) & (dataset['Merkmalwert'] == merkmalswert)]
    else:
        filtered_data = dataset[dataset['Merkmal'] == merkmal]
    
    dates = filtered_data['Datum'].drop_duplicates().sort_values()
    
    dates = dates.iloc[12:]
    return jsonify(dates.tolist())

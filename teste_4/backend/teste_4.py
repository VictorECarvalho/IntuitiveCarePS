from flask import Flask, render_template, request
from flask_cors import CORS
import pandas as pd
import json

CSV_PATH = '../../teste_3/temp/Relatorio_cadop.csv'

app = Flask(__name__)

app.config.from_object(__name__ )

CORS(app, resources={r"/*": {"origins": "http://localhost:8080", "allow_headers": "Access-Control-Allow-Origin"}})


@app.route('/get_data', methods=['GET'])
def get_data():
    try:
        df = pd.read_csv(CSV_PATH, sep=';')
        return json.dumps({
            'status': 'success',
            'data': json.loads(df.to_json(orient='records')),
            'columns': [col for col in df.columns],

        })
                
    except Exception as e:
        return str(e)

@app.route('/get_data', methods=['GET'])
def get_data():
    try:
        df = pd.read_csv(CSV_PATH, sep=';')
        return json.dumps({
            'status': 'success',
            'data': json.loads(df.to_json(orient='records')),
            'columns': [col for col in df.columns],

        })
                
    except Exception as e:
        return str(e)
    

if __name__ == '__main__':
    app.run(debug=True)
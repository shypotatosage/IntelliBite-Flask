from flask import Flask, Response
import pandas as pd
import json

app = Flask(__name__)

@app.route("/<name>")
def get_fruit_vegetables(name):
    df = pd.read_csv ('fruitvegetable.csv', delimiter=';')
    df_json = df.loc[df['name'] == name].to_json(orient="records")[1:-1]
    
    if not df.loc[df['name'] == name].empty:
        return json.dumps({'status': 200, 'message': "success", 'data': json.loads(df_json)})
    else:
        return Response(json.dumps({'status': 404, 'message': "Fruit/Vegetable Not Found", 'data': ""}), status=404, mimetype='application/json')

if __name__ == "__main__":
    app.run()
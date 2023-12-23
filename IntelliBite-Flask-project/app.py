from flask import Flask, Response
import pandas as pd
import json

app = Flask(__name__)

@app.route("/get-fruitvegetables/<name>")
def get_fruit_vegetables(name):
    df = pd.read_csv('fruitvegetable.csv', delimiter=';')
    df_json = df.loc[df['name'] == name].to_json(orient="records")[1:-1]
    
    if not df.loc[df['name'] == name].empty:
        return json.dumps({'status': 200, 'message': "success", 'data': json.loads(df_json)})
    else:
        return Response(json.dumps({'status': 404, 'message': "Fruit/Vegetable Not Found", 'data': ""}), status=404, mimetype='application/json')

@app.route("/get-ingredients")
def get_ingredients():
    df = pd.read_csv('data.csv', delimiter='#')
    ingredient_list = df['ingredients'].values.astype('str')
    ingredient_list = "$".join(ingredient_list)
    ingredient_list = ingredient_list.split('$')
    df_ingredient = pd.DataFrame(ingredient_list)
    df_json = df_ingredient[0].to_json(orient="records")
    
    return json.dumps({'status': 200, 'message': "success", 'data': json.loads(df_json)})

@app.route("/get-nutrition-profiles")
def get_nutrition_profiles():
    df = pd.read_csv('data.csv', delimiter='#')
    nutrition_profiles_list = df['nutrition_profiles'].values.astype('str')
    nutrition_profiles_list = "$".join(nutrition_profiles_list)
    nutrition_profiles_list = nutrition_profiles_list.split('$')
    df_nutrition_profiles = pd.DataFrame(nutrition_profiles_list)
    df_json = df_nutrition_profiles[0].to_json(orient="records")
    
    return json.dumps({'status': 200, 'message': "success", 'data': json.loads(df_json)})

if __name__ == "__main__":
    app.run()
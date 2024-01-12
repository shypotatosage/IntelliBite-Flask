# from crypt import methods
from flask import Flask, Response
import pandas as pd
import json

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

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
    ingredient_list = sorted(list(set(ingredient_list.split('$'))), key=str.lower)
    df_ingredient = pd.DataFrame(ingredient_list)
    df_json = df_ingredient[0].to_json(orient="records")
    
    return json.dumps({'status': 200, 'message': "success", 'data': json.loads(df_json)})


@app.route("/get-nutrition-profiles")
def get_nutrition_profiles():
    df = pd.read_csv('data.csv', delimiter='#')
    nutrition_profiles_list = df['nutrition_profiles'].values.astype('str')
    nutrition_profiles_list = "$".join(nutrition_profiles_list)
    nutrition_profiles_list = sorted(list(set(nutrition_profiles_list.split('$'))), key=str.lower)
    df_nutrition_profiles = pd.DataFrame(nutrition_profiles_list)
    df_json = df_nutrition_profiles[0].to_json(orient="records")
    
    return json.dumps({'status': 200, 'message': "success", 'data': json.loads(df_json)})


# Fungsi untuk mendapatkan vektor fitur dari bahan dan profil nutrisi
def get_feature_vector(recipe):
    ingredients_list = recipe['ingredients'].split(', ')
    nutrition_profiles_list = recipe['nutrition_profiles'].split(', ')
    feature_vector = ingredients_list + nutrition_profiles_list
    return ' '.join(feature_vector)

# Membuat matriks vektor fitur
dfRecipe = pd.read_csv('data.csv', delimiter='#')
    
vectorizer = CountVectorizer()
feature_matrix = vectorizer.fit_transform([get_feature_vector(recipe) for _, recipe in dfRecipe.iterrows()])

# Calculate cosine similarity
cosine_sim = cosine_similarity(feature_matrix)

@app.route("/get-recipes/<ingredients>/<nutrition_profiles>", methods=['GET'])
def recipes(ingredients, nutrition_profiles):
    # Process user input
    user_input = get_feature_vector({'ingredients': ingredients, 'nutrition_profiles': nutrition_profiles})
    user_input_vector = vectorizer.transform([user_input])

    # Calculate cosine similarity with user input
    similarity_scores = cosine_similarity(user_input_vector, feature_matrix).flatten()

    # Get indices of all recipes ordered by similarity
    ordered_indices = similarity_scores.argsort()[::-1]
    indices = []
    
    for i in ordered_indices:
        if similarity_scores[i] >= 0.5:
            indices.append(i)

    # Print cosine similarity scores
    print("Cosine Similarity Scores:")
    for idx, score in zip(ordered_indices, similarity_scores[ordered_indices]):
        print(f"Recipe: {dfRecipe.iloc[idx]['recipe_name']}, Similarity Score: {score}")

    # Get recommended recipes with servings and timetotal
    recommended_recipes = dfRecipe.iloc[indices][['recipe_name','servings', 'timetotal']].to_dict(orient='records')

    return json.dumps({'status': 200, 'message': "success", 'data': recommended_recipes})


@app.route("/get-detailrecipe/<name>", methods=['GET'])
def detailrecipe(name):
    if not dfRecipe.loc[dfRecipe["recipe_name"] == name].empty:

        # Get detailed information about the selected recipe
        selected_recipe = dfRecipe.loc[dfRecipe["recipe_name"] == name].to_json(orient="records")[1:-1]

        return json.dumps({'status': 200, 'message': "success", 'data': json.loads(selected_recipe)})
    else:
        return Response(json.dumps({'status': 404, 'message': "Recipe Not Found", 'data': ""}), status=404, mimetype='application/json')

if __name__ == "__main__":
    app.run()

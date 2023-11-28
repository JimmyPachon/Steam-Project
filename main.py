from fastapi import FastAPI
from fastapi.responses import JSONResponse
import pandas as pd
import ast
import uvicorn
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

app = FastAPI()



user_items=pd.read_csv('datos/user_items_reducido.csv',sep=';',encoding='utf-8')
steam_games=pd.read_csv('datos/steam_games.csv',sep=';',encoding='utf-8')
user_reviews=pd.read_csv('datos/user_reviews.csv',sep=';',encoding='utf-8')



# Función para convertir la cadena a un conjunto
def convert_to_set(column):
    try:
        # Utilizamos ast.literal_eval para evaluar la cadena como una expresión literal de Python

        return ast.literal_eval(column)
    except (SyntaxError, ValueError):
        # Si hay un error al evaluar la cadena, puedes manejarlo de alguna manera
        return set('No data')

# Aplicar la función a la columna 'genres' y 'specs'
user_items['genres'] = user_items['genres'].apply(convert_to_set)
steam_games['genres'] = steam_games['genres'].apply(convert_to_set)
steam_games['specs'] = steam_games['specs'].apply(convert_to_set)


@app.get("/")
def read_root():
    return {"Mensaje": "A continuación se encuentran las funciones solicitadas para el sistema de recomedacion de steam, poner al final de la URL /docs."}




@app.get('/PlayTimeGenre')


def PlayTimeGenre(genre):

       

        #Filtrar el DataFrame para el género específico
    
        df_genero = user_items[user_items['genres'].apply(lambda x: genre in x)]

        
    
    
        # Agrupar por año y sumar los minutos jugados
        df_agrupado = df_genero.groupby('release_date')['playtime_forever'].sum().reset_index()

        
    
        # Encontrar el año con la máxima cantidad de minutos jugados
        
        year_max_jugado = df_agrupado.loc[df_agrupado['playtime_forever'].idxmax(), 'release_date']


        
        
        return {"El año más jugado para este género es:":int(year_max_jugado)}


@app.get('/UserForGenre')

def UserForGenre(genre):

    df_genero = user_items[user_items['genres'].apply(lambda x: genre in x)]

    # Encontrar el usuario que ha jugado más horas
    usuario_max_horas = df_genero.loc[df_genero['playtime_forever'].idxmax(), 'user_id']

    # Filtrar el DataFrame para el usuario encontrado
    df_usuario = df_genero[df_genero['user_id'] == usuario_max_horas]

    # Crear una lista de horas jugadas por año
    tiempo_jugado_por_año = df_usuario.groupby('release_date')['playtime_forever'].sum().to_dict()

    return {"El usuario que mas ha jugado videojuegos de este genero es" : usuario_max_horas,"Su distribución de horas jugando el género es":tiempo_jugado_por_año}

@app.get('/UsersRecommend')

def UsersRecommend(year):

    # Filtrar user_reviews por el año dado y por la condición de recomendación y revisión
    filtered_reviews = user_reviews[user_reviews['posted'] == str(year) ]
   
    filtered_reviews=filtered_reviews[filtered_reviews['recommend'] == True]
    
    filtered_reviews=filtered_reviews[filtered_reviews['review'] == 1 | (filtered_reviews['review'] == 2)]

    # Merge para obtener los nombres de los items
    merged_data = pd.merge(filtered_reviews, user_items, on='item_id', how='left')


    # Contar la frecuencia de cada item y obtener el top 3
    top_games = merged_data['item_name'].value_counts()
   

    top_games=top_games[0:3]

    top_games=top_games.astype(str)

    return {"Los mejores juegos de este año son:": top_games}

@app.get('/UsersWorstDeveloper')

def UsersWorstDeveloper(year):

    # Filtrar user_reviews por el año dado y por la condición de no recomendación y revisión igual a 0
    filtered_reviews = user_reviews[user_reviews['posted'] == str(year)]

    filtered_reviews=filtered_reviews[filtered_reviews['recommend'] == False]
    filtered_reviews=filtered_reviews[filtered_reviews['review'] == 0]
    
    # Merge para obtener los desarrolladores correspondientes
    merged_data = pd.merge(filtered_reviews, steam_games, on='item_id', how='left')

    # Contar la frecuencia de cada desarrollador y obtener el top 3
    top_developers = merged_data['developer'].value_counts()

    top_developers=top_developers[0:3]

    top_developers=top_developers[0:3]

    top_developers=top_developers.astype(str)

    return {"Los peores desarrolladores de este año son" : top_developers}

@app.get('/sentiment_analysis')

def sentiment_analysis(developer_name):
    # Filtrar steam_games por el desarrollador dado
    filtered_steam_games = steam_games[steam_games['developer'] == developer_name]

    # Obtener los item_ids correspondientes al desarrollador
    item_ids = filtered_steam_games['item_id']

    # Filtrar user_reviews por los item_ids asociados al desarrollador
    filtered_reviews = user_reviews[user_reviews['item_id'].isin(item_ids)]

    # Contar la cantidad de ocurrencias de 'review' para ese desarrollador
    review_counts = filtered_reviews['review'].value_counts()

    # Crear un diccionario con las categorías y sus valores correspondientes
    result_dict = {'Desarrolladora': developer_name,
        'Negativo': int(review_counts.get(0, 0)),
        'Neutral': int(review_counts.get(1, 0)),
        'Positivo':int( review_counts.get(2, 0))
    }

    return {"Las reviews de este desarrollador son": result_dict}

@app.get('/recomendacion_juego')

def recomendacion_juego(juego):
    
    juego_seleccionado = steam_games[steam_games['app_name'] == juego]

    if juego_seleccionado.empty:
        return "El juego no se encuentra en el conjunto de datos."

    # Crear un conjunto de datos con los juegos que no son el juego seleccionado
    juegos_similares = steam_games[steam_games['app_name'] != juego].copy()  # Usar copy() para evitar SettingWithCopyWarning

    # Convertir los conjuntos a cadenas antes de la concatenación
    juego_combined_features = ' '.join(map(str, juego_seleccionado['specs'].values[0])) + ' ' + ' '.join(map(str, juego_seleccionado['genres'].values[0])) + ' ' + str(juego_seleccionado['developer'].values[0])
    juegos_similares['combined_features'] = juegos_similares.apply(lambda row: ' '.join(map(str, row['specs'])) + ' ' + ' '.join(map(str, row['genres'])) + ' ' + str(row['developer']), axis=1)

    # Utilizar TF-IDF Vectorizer para convertir el texto combinado en vectores
    tfidf_vectorizer = TfidfVectorizer()
    tfidf_matrix = tfidf_vectorizer.fit_transform(juegos_similares['combined_features'])

    # Calcular la similitud del coseno entre el juego seleccionado y los demás juegos
    cosine_similarities = linear_kernel(tfidf_matrix, tfidf_vectorizer.transform([juego_combined_features]))

    # Obtener los índices de los juegos más similares
    indices_similares = cosine_similarities.flatten().argsort()[:-6:-1]  # Tomar los 5 juegos más similares

    # Obtener información de los juegos más similares
    juegos_recomendados = steam_games.iloc[indices_similares]['app_name']
    juegos_recomendados.reset_index(inplace=True,drop=True)

    return {juegos_recomendados.astype(str)}


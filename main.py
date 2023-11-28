from fastapi import FastAPI
from fastapi.responses import JSONResponse
import pandas as pd
import ast
import uvicorn

app = FastAPI()



user_items=pd.read_csv('datos/user_items_reducido.csv',sep=';',encoding='utf-8')
steam_games=pd.read_csv('datos/steam_games.csv',sep=';',encoding='utf-8')
user_reviews=pd.read_csv('datos/user_reviews.csv',sep=';',encoding='utf-8')


user_reviews['review'] = pd.to_numeric(user_reviews['review'], errors='coerce')


# Función para convertir la cadena a un conjunto
def convert_to_set(column):
    try:
        # Utilizamos ast.literal_eval para evaluar la cadena como una expresión literal de Python

        return ast.literal_eval(column)
    except (SyntaxError, ValueError):
        # Si hay un error al evaluar la cadena, puedes manejarlo de alguna manera
        return set('No data')

# Aplicar la función a la columna 'genres'
user_items['genres'] = user_items['genres'].apply(convert_to_set)


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
    filtered_reviews = user_reviews[(user_reviews['posted'] == year) & (user_reviews['recommend'] == 'True') & ((user_reviews['review'] == 1) | (user_reviews['review'] == 2))]


    # Merge para obtener los nombres de los items
    merged_data = pd.merge(filtered_reviews, user_items, on='item_id', how='left')

    # Contar la frecuencia de cada item y obtener el top 3
    top_games = merged_data['item_name'].value_counts().nlargest(3)

    return {"Los 3 juegos más recomendados para este año son" : {"top 1": int(top_games[0]),"top 2": int(top_games[1]),"top3": int(top_games[2]) }}

@app.get('/UsersWorstDeveloper')

def UsersWorstDeveloper(year):

    # Filtrar user_reviews por el año dado y por la condición de no recomendación y revisión igual a 0
    filtered_reviews = user_reviews[(user_reviews['posted'] == year) & (user_reviews['recommend'] == 'False') & (user_reviews['review'] == 0)]

    # Merge para obtener los desarrolladores correspondientes
    merged_data = pd.merge(filtered_reviews, steam_games, on='item_id', how='left')

    # Contar la frecuencia de cada desarrollador y obtener el top 3
    top_developers = merged_data['developer'].value_counts().nlargest(3)

    return {"Los peores desarrolladores de este año son" : set(top_developers)}

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
        'Negativo': review_counts.get(0, 0),
        'Neutral': review_counts.get(1, 0),
        'Positivo': review_counts.get(2, 0)
    }

    return {"Las reviews de este desarrollador son": dict(result_dict)}


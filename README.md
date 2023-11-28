#**SISTEMA DE RECOMENDACIÓN PARA LA PLATAFORMA DE STEAM**

En el presente repositorio se entregan todos los Datasets y toda la documentación de una API que implementa un sistema de recomedación por similitud de items, también se entrega un link a los datos originales sin procesar y sin limpiar para posibles consultas o mejoras al proyecto. Encontrarás un análisis exploratorio de datos en el notebook "EDA.ipynb" donde se analizan principalmente los valores que faltan y los posibles outliers, también se encuentra el archivo principal de la API "main.py" donde se encuentran las funciones de consulta de datos. 

Si quiere interactuar con la API, te dejo el link a continuación:

**Link de la API:** https://steam-project-1b2p.onrender.com/docs

#**DOCUMENTACIÓN API**
En la API encontrarás 6 funciones con las que podrás interactuar, cada una realiza consultas muy específicas:

**PlayTimeGenre( genre ):** Recibe como parámetro un género de videojuegos y te regresa el año en el que más se jugó dicho género.

**UserForGenre( genre ):** Recibe como parámetro un género de videojuegos y regresa el ID del usuario con más minutos de juego para ese género, además da la distribución de tiempo de juego a lo largo de los años.

**UsersRecommend( year ):** Recibe un año y da el TOP 3 juegos con mejor recibimiento por la comunidad de Steam en ese año.

**UsersWorstDeveloper( year ):** Recibe un año y devuelve el TOP 3 desarrolladores peor calificados en ese año.

**sentiment_analysis( developer_name ):** Recibe el nombre de una empresa desarrolladora de videojuegos y calcula cuántas reseñas positivas, neutrales y negativas tiene.

Por último se encuentra la función principal y el propósito principal de este proyecto:

**recomendacion_juego( app_name ):** Ingresando el nombre de un juego, da como resultado los 5 juegos con mayor similitud encontrados en el dataset "steam_games.csv".

*ACLARACIÓN IMPORTANTE:* Esta API es un DEMO, por lo tanto no cuenta con los datos completos de los items adquiridos por los usuarios debido a falta de recursos técnicos. Teniendo eso en cuenta, es probable que las dos primeras funciones no den la información correcta; sin embargo la función principal de recomendación de juegos es totalmente confiable y cuenta con la información disponible.

**¿Qué parámetros tiene en cuenta la API?**

Para determinar la similitud de los videojuegos la API se basa en tres características principales: Los géneros a los que pertenece(Acción, Estrategia, Aventura, ... etc), las especificaciones(Online, PVP, ... etc) y la empresa desarrolladora. Con estos tres parámetros en cuenta se vectorizaron todas las palabras clave y se aplicó el método de similitud del coseno, luego se tomaron los 5 juegos que más se aproximaban al juego original.

**¿Qué se puede mejorar de la API?**

Hay muchas cosas por mejorar, para empezar los datasets se pueden normalizar para disminuir el tamaño de los archivos, además los mismos se podrían manipular en un formato .parquet para optimizar el rendimiento de la API y ocupar menos memoria.
Se podría hacer scrapping en la página de STEAM para buscar los datos que faltan y pueden ser relevantes, así como se hizo scrapping en la página de WIKIPEDIA para obtener la mitad de las fechas de lanzamiento que faltaban en el ETL.
Se puede llegar a mejorar la recomendación de juegos agregando un peso de importancia a las diferentes características, puede que importe más el género que el desarrollador por ejemplo. También se podría extrapolar a un sistema user-item donde se recomienden juegos que a otros usuarios les ha gustado.
La primera impresión es importante, mejorar la interfaz gráfica de la API sería de gran importancia ya que por el momento es incómoda y muy superficial.
Hay otros factores a tener en cuenta a la hora de recomendar un videojuego, por ejemplo el precio podría ser una forma de categorizarlos y sería una variable a tener en cuenta.

#**ARCHIVOS DEL REPOSITORIO**

**EDA:** Es el análisis exploratorio de los datos, podrás observar las conclusiones sobre los datos después del ETL: valores faltantes, valores irrelevantes, outliers, posibilidades de consulta. El archivo completo POST-EDA, es decir después de quitar outliers y valores que no importan está en el siguiente drive: https://drive.google.com/drive/folders/1AVQ-j-ZdrWbhDtspaI8VnQ53wLmxuBFp .
**ETL:** Es el archivo que se usó para tratar el conjunto de datos original que se encuentra en el siguiente link: https://drive.google.com/drive/folders/1HqBG2-sUkz_R3h1dZU5F2uAzpRn7BSpj .
**datos:**Esta carpeta contiene los datasets usados en la API como tal, la única diferencia de los datos completos es el dataset user_items_reducido, como su nombre lo indica ha sido minimizado para cumplir con los requerimientos técnicos. Sólo se tienen en cuenta los registros que tienen más de 10000 minutos de juego.
**main:**Es el archivo principal de la API donde se encuentras las funciones que se despliegan en render.
**requirements**: Son las librerias e instalaciones que solicita la API para su correcto funcionamiento.
**Diccionario**: Es una imagen que contiene la información de los datasets usados en el proyecto.



Para finalizar dejo el link al video explicativo del funcionamiento de la API:




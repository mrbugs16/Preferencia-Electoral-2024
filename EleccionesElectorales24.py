pip install --upgrade tweepy

"""Se importa la biblioteca tweepy, la cual nos facilita la interacción de los servicios de la API de X"""

import tweepy
import pandas as pd
import time

"Se guardan a variables los tokens y las llaves de autenticación que nos proporciona la API X"

api_key = ''
api_key_secret = ''
bearer_token = ''
access_token = ''
access_token_secret = ''

client_id = ''
client_secret = ''

"""La funión OAuthHandler nos permite establecer una conexión segura entre X y nuestro programa.
La función set_acces_token nos permite autenticar nuestro programa y permitir que interactúe en nombre de un usuario especifico en X
"""

autenticacion = tweepy.OAuth2BearerHandler(bearer_token)

"""La funcion API nos permite crear un objeto API, la cual nos permite usar metodos y funciones para realizar operaciones especificas en la API X."""

cliente = tweepy.Client(bearer_token,api_key,api_key_secret,access_token,access_token_secret)

"""Se crea una base datos vacía, que nos servirá para tener una copia de la base de datos anterior a la base de datos recien obtenida."""

copy_28 = pd.DataFrame()

#Se Busca la una frase, excluyendo  retweets, e incluyendo solo tweets en español
query = '("Hasta la victoria con Claudia") -is:retweet lang:es' #query

#nombre de columnas para nuestra base de datos
columnas = ["Tweet id","author_id", "Fecha de emision", "Fuente de emision", "Tweet","Geo"]

#limite de tweets a descargar por cada busqueda
numero_de_tweets = 100

############################################ tweets 28/04
#Debate presidencial: 28/04
#funcion para buscar tweets en los ultimos 7dias, con una fecha de inicio y final, con los campos de tweet establecios
try:
  tweets28 = cliente.search_recent_tweets(query,
                                        end_time = '2024-04-29T00:00:00Z',
                                        expansions = ['geo.place_id', 'author_id'],
                                        max_results = numero_de_tweets,
                                        place_fields = ['country','country_code'],
                                        start_time = '2024-04-28T00:00:00Z',
                                        tweet_fields = ['author_id','created_at','text','source','lang','geo'],
                                        user_fields = ['name','username','location','verified']
                                        )

except BaseException as e:
  print('Status Failed On',str(e))

#acceder a atributo "datos" de tweets28 para retirar información
info28 = tweets28.data

#Si info28 está vacio, entonces, imprime que no se encontró información
#Si no está vacio entonces:
if(info28 != None):

  #Se crea una varible con los atributos de la variable info28
  attributes_container28 = [[tweet.id, tweet.author_id, tweet.created_at, tweet.source, tweet.text, tweet.geo] for tweet in info28]

  #Se crea una base de datos "df28" que contenga los atributos extraidos, con los nombres de columnas que se encuentran en la variable "columnas"
  df28 = pd.DataFrame(attributes_container28,columns=columnas)

  #Si la copia está vacía
  if copy_28.empty:

    #Entonces hacer una copia de "df28"
    copy_28 = df28.copy()

  else:

    #Si no está vacía la copía entonces se concatena la copia con la base de datos recien extraída
    print("Se encontraron %d resultados." % len(df28))
    df28 = pd.concat([df28,copy_28],ignore_index=True)

    #Y se actualiza la copia con la base de datos recien concatenada
    copy_28 = df28.copy()
    print("Información recopilada total: %d tweets." % len(df28))

else:
  print("Sin informacion en tweets del 27/04")

"""Descargamos la copia de la base de datos."""

from google.colab import files
copy_28.to_csv('')
files.download('')
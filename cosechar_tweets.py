#pip install couchdb
#pip install tweepy

import couchdb #Libreria de CouchDB (requiere ser instalada primero)
from tweepy import Stream #tweepy es la libreria que trae tweets desde la API de Twitter (requiere ser instalada primero)
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import json #Libreria para manejar archivos JSON


ckey = "Us4CI45zdKBdA0KLUSnvZ2Hy5"
csecret = "4uFWyoDtM8idstVG1mqGQF8Q8TbSc6ywIJqYb2dv8Pk5WJsRXY"
atoken = "229573038-GTQC23YmJ7MPLpObjjLQ8Q42WAmm3rja0aU6Vl7j"
asecret = "HVrYYS2xzjXLn1aomGakWY2HGDNJEzOPwKv93aM67DK4l"

class listener(StreamListener):
    
    def on_data(self, data):
        dictTweet = json.loads(data)
        try:
            dictTweet["_id"] = str(dictTweet['id'])
           
            doc = db.save(dictTweet) #Aqui se guarda el tweet en la base de couchDB
            print ("Guardado " + "=> " + dictTweet["_id"])
        except:
            print ("Documento ya existe")
            pass
        return True
    
    def on_error(self, status):
        print (status)
        
auth = OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)
twitterStream = Stream(auth, listener())

#Setear la URL del servidor de couchDB
server = couchdb.Server('http://localhost:5984/')
try:
    #Si no existe la Base de datos la crea
    db = server.create('mundo')
except:
    #Caso contrario solo conectarse a la base existente
    db = server['mundo']
    
#Aqui se define el bounding box con los limites geograficos donde recolectar los tweets
twitterStream.filter(locations=[-108.87,25.35,-74.61,39.06])
twitterStream.filter(track = ["Pena de muerte", "death penalty"])


# coding: utf-8

# In[5]:


import json
import hashlib
from collections import OrderedDict
import requests


# In[27]:


### Función para crear el hash del json
def encrypt_string(hash_string):
    sha_signature =         hashlib.sha256(hash_string.encode()).hexdigest()
    return sha_signature

### Verificador de la existencia del hash dentro de la blockchain
# Hash programa: hash que se obtiene con el json
# Hash esperado: hash que se obtiene del composer server
def verificacion_hash(hash_programa, hash_esperado):
    ## Puede ser el mismo hash o estar contenido en el hash esperado
    verdad_falso=hash_programa in hash_esperado or hash_programa==hash_esperado
    return verdad_falso

def obtener_certId_json(data):
    # Creamos una lista de los items del diccionario creado a partir del json
    items=list(data.items())
    # Seleccionamos la segunda tupla que contiene el certificado ID
    numero=items[1][1]
    # Dicho numero es una variable string
    return numero

def url_id(url,certID):
    url_total=url+"?Id="+certID
    ## Header Accept: application/json
    results = requests.get(url_total, headers={'Accept': 'application/json'})
    abs_data = json.loads(results.text)[0] #first coincidence
    return abs_data

def id_blockchain(json_obj):
    # Segun lo que veo del json retornado, el hash esta en la 4 posicion 
    hash_code=json_obj['certHash']
    return hash_code


# In[ ]:


### Paso uno ###
### que se suba el json, aca yo solo usaré una prueba ###
with open('prueba.json', encoding='utf-8') as json_file:
    data = json.load(json_file, object_pairs_hook=OrderedDict)
hash_string=json.dumps(data, ensure_ascii=False,separators=(',', ':')).encode('utf8').decode()
### Hash del json subido por el usuario
sha_signature = encrypt_string(hash_string)
print(sha_signature)
### Buscamos el CertID en el json ingresado
certID=obtener_certId_json(data)
### Buscamos ahora el hash de la blockchain, faltaria definir bien la url
json_file_block=url_id('http://localhost:3000/api/queries/selectAbsCertByCertId',certID)
print(json_file_block)
### Se obtiene un json como respuesta
### Buscamos el hash en este json
hash_blockchain=id_blockchain(json_file_block)
### Verificamos que coincidan
if verificacion_hash(sha_signature,hash_blockchain):
    print("Es auténtico el certificado")
else:
    print("Está alterado el certificado")


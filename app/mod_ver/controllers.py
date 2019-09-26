# Import flask dependencies
from flask import Blueprint, request, jsonify, json
from flask_cors import CORS

import requests
import urllib

import json
import hashlib
from collections import OrderedDict


# Define the blueprint: 'auth', set its url prefix: app.url/auth
mod_ver = Blueprint('ver', __name__)
CORS(mod_ver)

# Set the route and accepted methods
@mod_ver.route('/verify/', methods=['POST'])
def verify():
    json_cert_txt = request.data.decode("utf-8")
    print(json_cert_txt)
    # json_cert = '{ "$class": "org.picert.cert", "certId": "134083306", "administrator": "resource:org.picert.Admin#admin@entidad.gov.co", "typeC": "Assertion", "name": "Certificado de Antecedentes", "message": "La PROCURADURIA GENERAL DE LA NACIÓN certifica que una vez consultado el Sistema de Información de Registro de Sanciones e Inhabilidades (SIRI), el(la) señor(a) CARLOS ALBERTO CASTRO IRAGORRI identificado(a) con Cédula de ciudadanía número 79947917: NO REGISTRA SANCIONES NI INHABILIDADES VIGENTES", "issuer": { "$class": "composer.blockcerts.Issuer", "id": "899999119", "typen": "Profile", "name": "Procuraduria General de la Nacion", "image": "procu.png", "signatureLines": { "$class": "composer.blockcerts.SignatureLines", "typen": "SignatureLine,Extension", "name": "Manuel A. Espinosa", "image": "firmaME.png", "jobtitle": "Jefe Division Centro de Atencion al Publico" } }, "context": "https://w3id.org/openbadges/v2,https://w3id.org/blockcerts/v2" }'
    json_cert = json.loads(json_cert_txt, object_pairs_hook=OrderedDict)
    hash_string=json.dumps(json_cert, ensure_ascii=False,separators=(',', ':')).encode('utf8').decode()
    ### Hash del json subido por el usuario
    sha_signature = encrypt_string(hash_string)
    print(sha_signature)
    ### Buscamos el CertID en el json ingresado
    certID=obtener_certId_json(json_cert)
    ### Buscamos ahora el hash de la blockchain, faltaria definir bien la url
    json_block=request_bc('http://localhost:3000/api/queries/selectAbsCertByCertId',certID)
    print(json_block)
    ### Se obtiene un json como respuesta
    ### Buscamos el hash en este json
    if len(json_block)>0:
        hash_blockchain=json_block[0]['certHash']
        ### Verificamos que coincidan
        auten = verificacion_hash(sha_signature,hash_blockchain)
    else:
        auten = False
    
    return jsonify(res=auten)




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
    # Seleccionamos la segunda tupla que contiene el certificado ID
    numero=data['certId']
    # Dicho numero es una variable string
    return numero

def request_bc(url,certID):
    url_total=url+"?Id="+certID
    ## Header Accept: application/json
    results = requests.get(url_total, headers={'Accept': 'application/json'})
    print(results.text)
    abs_data = json.loads(results.text) #first coincidence
    return abs_data

import json
import hashlib as h
import fabric
import base64


#### Conversion del json a un hash #####
#### Funcion hash: sha256

def hashn (archivo_json):
    enc=archivo_json.encode('utf-8')
    has=h.sha256(enc).hexdigest()
    return has

### Verificamos que el hash coincidan ####

def verificacion_hash(hash_programa, hash_esperado):
    ## Puede ser el mismo hash o estar contenido en el hash esperado
    verdad_falso=hash_programa in hash_esperado or hash_programa==hash_esperado
    return verdad_falso

#### Solicitud del hash que se encuentra en el nodo de fabric
def obtener_id_json(archivo_json):
    llaves=list(archivo_json.keys())
    
    return 



class VerificationCheck(object):
    """Individual task involved in verification"""

    def __init__(self, certificate, transaction_info=None, issuer_info=None):
        self.certificate = certificate
        self.transaction_info = transaction_info
        self.issuer_info = issuer_info

    def execute(self):
        return self.do_execute()

    def do_execute(self):
        """Steps should override this"""
        return False


with open('hola.json') as json_file:
    data = json.load(json_file)
    
a=json.dumps(data).encode('utf-8')
j=h.sha256(a)

hex_dig = j.hexdigest()
print(hex_dig)
print(base64.b64encode(h.sha256(a).digest()))

# Conexion profile con SDK (revisar) libreria SDK


# Tenemos que revisar que los json que se generan en cada una de las plataformas de blockchain
##with open("invima.json") as f:
##    em=f.read()
##
##
##
##
##
##encoded=em.encode('utf-8')
##j=h.sha256(encoded)
##
##hex_dig = j.hexdigest()
##print(hex_dig)
##
####
####a={"candidate":5,"data":1}
####a=json.dumps(a,sort_keys=True).encode("utf-8")


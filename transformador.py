
# coding: utf-8

# In[134]:


import PyPDF2 as p
import tika
from tika import parser
import re
import json
from PIL import Image 
import pytesseract 
import sys 
from pdf2image import convert_from_path 
import os 


# In[195]:


def leer_pdf():
    with open('CertificadoProcuraduria.pdf','rb') as f:
        pdf = p.PdfFileReader(f)
        pagina=pdf.getPage(0)
        datos=pdf.getDocumentInfo()
        FileName = "CertificadoProcuraduria.pdf"
        ## Realizamos el parse
        PDF_Parse = parser.from_file(FileName)
        contenido=pagina.extractText()
        diccionario=PDF_Parse['metadata']
        contenido=PDF_Parse['content']
        lista_datos=contenido.split('\n')
        #Retornamos tupla
    return diccionario, datos, lista_datos


def info_pdf(tupla):
    total=info(tupla[0],tupla[1],tupla[2])
    return total

def info(diccionario_parse,diccionario_get,diccionario_s):
    issuer_name=diccionario_parse['Author']
    name=diccionario_get['/Title']
    dato1=diccionario_s[55]
    dato2=diccionario_s[57]
    message=dato1+dato2
    issuer_signature_name=diccionario_s[84]
    issuer_signature_jobtitle=diccionario_s[86]
    lista_def=[issuer_name,name,message,issuer_signature_name,issuer_signature_jobtitle]
    return lista_def
    

def escribir_json(lista):
    data = {}
    data['$class'] = 'org.picert.cert'
    data['certID'] = '110101021513'
    data['administrator'] =''
    data['resource']='org.picert.Admin#admin@entidad.gov.co'
    data['typeC']='Assertion'
    data['name']=lista[1]
    data['message']=lista[2]
    data["issuer"]={}
    data["issuer"]["$class"]='org.picert.cert'
    data["issuer"]["id"]='101015456'
    data["issuer"]["typen"]='Profile'
    data["issuer"]["name"]=lista[0]
    data["issuer"]["image"]='101015456'
    data["issuer"]["signatureLines"]={}
    data["issuer"]["signatureLines"]["$class"]="composer.blockcerts.SignatureLines"
    data["issuer"]["signatureLines"]["typen"]="SignatureLine,Extension"
    data["issuer"]["signatureLines"]["name"]=lista[3]
    data["issuer"]["signatureLines"]["jobtitle"]=lista[4]
    data["context"]='https://w3id.org/openbadges/v2,https://w3id.org/blockcerts/v2'  
    file_name = "data.json"
    with open("prueba_escribir", 'w') as file:
        json.dump(data, file)
        
a=leer_pdf()
b=info_pdf(a)
escribir_json(b)
#b=info_pdf(a)


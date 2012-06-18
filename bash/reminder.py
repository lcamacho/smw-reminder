#!/env/bin/python

# load jsons
import urllib2
import json
json_tareas = urllib2.urlopen('https://www.mozilla-hispano.org/documentacion/Especial:Ask/-5B-5BCategor%C3%ADa:Tarea-5D-5D-5B-5Bestado::!Finalizado-5D-5D/-3FResponsable%3DRespon./-3FArea/-3FProyecto/-3FEstado/-3FFechafin%3DL%C3%ADmite/mainlabel%3D/order%3DASC,ASC/sort%3DFechafin,Estado/format%3Djson').read()
tareas = json.loads(json_tareas)
json_colab = urllib2.urlopen('https://www.mozilla-hispano.org/documentacion/Especial:Ask/-5B-5BCategoría:Colaborador-5D-5D/-3FCorreo/mainlabel%3D/format%3Djson').read()
colab = json.loads(json_colab)
n = len(colab["items"])

# jsons structures
# tareas['items'][0]['respon.']
# colab['items'][0]['label']
# colab['items'][0]['correo']

# transform list in dictionary

colab_new = {}

vars = [i for i in range(n)]
for var in vars:
    ncolab = colab['items'][int(var)]['label']
    try:
        mcolab = colab['items'][int(var)]['correo']
    except KeyError:
        mcolab = "no tiene"
    mcolab = [w.replace('ARROBA','@') for w in mcolab]
    mcolab = [w.replace('arroba','@') for w in mcolab]
    mcolab = [w.replace('AT','@') for w in mcolab]
    mcolab = [w.replace('PUNTO','.') for w in mcolab]
    mcolab = [w.replace('punto','.') for w in mcolab]
    mcolab = [w.replace('DOT','.') for w in mcolab]
    mcolab = [w.replace(' ','') for w in mcolab]
    colab_new.update({ncolab:mcolab})

# append mails with tareas respons (new file)
n = len(tareas['items'])

x = [i for i in range(n)]

tareas_new = {}
for i in x:
    try:
        resp = tareas['items'][int(i)]['respon.']
    except KeyError:
        resp = "sin asignar"
    try:
        resp1 = 'Usuario:'+resp[0]
    except KeyError:
        resp1= "no user"
    try:
        mailresp =colab_new[resp1][0]
    except KeyError:
        mailresp="no mail"
    tareas_new.update({'mail'+str(i):mailresp,'respon'+str(i):resp})

# send mails
import smtplib
import string
import unicodedata

FROM = "tareas@mozhipano.com"
HOST =  # 'mailserver:port'
username = # 'username'
password = # 'password'

SUBJECT = "You have a task pending"


for i in x:
    TO = tareas_new['mail'+str(i)]
    if (TO == 'no mail'):
        pass
    else:
        respon = tareas_new['respon'+str(i)][0]
        estado = tareas['items'][int(i)]['estado'][0]
        label = unicodedata.normalize('NFKD',tareas['items'][int(i)]['label']).encode('latin-1','ignore')
        text = "Hola, "+ respon + " tienes asignada la tarea "+ label+", la cual se encuentra como " + estado +", pero ya vencio la fecha limite asignada"
        BODY = string.join((
            "From: %s" % FROM,
            "To: %s" % TO,
            "Subject: %s" % SUBJECT ,
            "",
            text
            ),"\r\n") 
        server = smtplib.SMTP(HOST)
        server.starttls()
        server.login(username,password)
        server.sendmail(FROM, [TO], BODY)
        server.quit()

# Cálculo de IMC utilizando comando de voz e acessando banco de dados db2 da IBM com lista de profissionais do BR.

import pyttsx3 as ptx
import time
import speech_recognition as sr
import requests
import ibm_db
import ibm_db_dbi
import unidecode

dsn_hostname = "your_hostname"
dsn_uid = "your_userid"
dsn_pwd = "your_pwd"

dsn_driver = "{IBM DB2 ODBC DRIVER}"
dsn_database = "bludb"
dsn_port = "your_port"
dsn_protocol = "TCPIP"
dsn_security = "SSL"

dsn = (
    "DRIVER={0};"
    "DATABASE={1};"
    "HOSTNAME={2};"
    "PORT={3};"
    "PROTOCOL={4};"
    "UID={5};"
    "PWD={6};"
    "SECURITY={7};").format(dsn_driver, dsn_database, dsn_hostname, dsn_port, dsn_protocol, dsn_uid, dsn_pwd,dsn_security)

try:
    conn = ibm_db.connect(dsn, "", "")
    print ("Connected to database: ", dsn_database, "as user: ", dsn_uid, "on host: ", dsn_hostname)

except:
    print ("Unable to connect: ", ibm_db.conn_errormsg() )


engine = ptx.init()

engine.say('Olá, tudo bem? Me diga qual é o seu nome.')
engine.runAndWait()
print('Nome:')

rec = sr.Recognizer()
mic = sr.Microphone()
with sr.Microphone(0) as mic:
    rec.adjust_for_ambient_noise(mic)
    audio = rec.listen(mic)
    texto_nome = rec.recognize_google(audio, language="pt-BR")
    print(texto_nome)
    time.sleep(1.2)

engine = ptx.init()
engine.say(f'Oi {texto_nome}, como vai?, Me diga qual a sua altura')
engine.runAndWait()
print('Altura:')

rec = sr.Recognizer()
mic = sr.Microphone()
with sr.Microphone(0) as mic:
    rec.adjust_for_ambient_noise(mic)
    audio = rec.listen(mic)
    texto_alt = rec.recognize_google(audio, language="pt-BR")
    print(texto_alt)
    time.sleep(1.2)

engine = ptx.init()
engine.say(f'Muito bem, agora me diga qual o seu peso')
engine.runAndWait()
print('Peso:')

rec = sr.Recognizer()
mic = sr.Microphone()
with sr.Microphone(0) as mic:
    rec.adjust_for_ambient_noise(mic)
    audio = rec.listen(mic)
    texto_peso = rec.recognize_google(audio, language="pt-BR")
    print(texto_peso)
    time.sleep(1.2)

engine.say('Muito obrigado pelas informações, aguarde um momento enquanto eu calculo seu IMC.')
engine.runAndWait()
time.sleep(1.2)

texto_peso = float(texto_peso)
texto_alt = float(texto_alt)

imc = texto_peso/texto_alt**2
print(f'Seu IMC é: {round(imc, 2)}')

if imc < 18.5:
    engine.say('Seu IMC está abaixo dos valores de referência, sugiro você procurar um profissional de saúde')
    engine.say('Por favor me informe seu cep para lhe indicar um.')
    engine.runAndWait()
    print('CEP:')
    rec = sr.Recognizer()
    mic = sr.Microphone()
    with sr.Microphone(0) as mic:
        rec.adjust_for_ambient_noise(mic)
        audio = rec.listen(mic)
        texto_cep = rec.recognize_google(audio, language="pt-BR")
        print(texto_cep)
        time.sleep(1.2)

        link = f'https://viacep.com.br/ws/{texto_cep}/json/'
        requisicao = requests.get(link)
        dic_requisicao = requisicao.json()
        uf = dic_requisicao['uf']
        cidade = dic_requisicao['localidade']
        engine.say(f'Ok, vi que você mora em {cidade}.')

        print(cidade, uf)
        city = f'{cidade}'
        city_u = city.upper()

        city_u = unidecode.unidecode(city_u)
        pconn = ibm_db_dbi.Connection(conn)
        selectQuery = f"select * from NUTRI where MUNICIPIO = '{city_u}'"
        selectStmt = ibm_db.exec_immediate(conn, selectQuery)
        while ibm_db.fetch_row(selectStmt):

            print(f"{city_u}:", ibm_db.result(selectStmt, 3))
        engine.say('Estes são os profissionais de sua cidade.')
        engine.runAndWait()

elif imc > 18.5 and imc <= 24.9:
        engine.say('Seu IMC está dentro dos valores de referência, continue assim')
        engine.runAndWait()

elif imc > 25.0 and imc <= 29.9:
        engine.say('De acordo com o resultado de seu IMC, você está com sobrepeso, sugiro mudar sua alimentação'
                   ' fazer mais exercícios, e procurar um profissional de saúde')
        time.sleep(1.2)
        engine.say('Por favor me informe seu cep, para que eu possa lhe indicar um.')
        engine.runAndWait()
        print('CEP:')
        rec = sr.Recognizer()
        mic = sr.Microphone()
        with sr.Microphone(0) as mic:
            rec.adjust_for_ambient_noise(mic)
            audio = rec.listen(mic)
            texto_cep = rec.recognize_google(audio, language="pt-BR")
            print(texto_cep)
            time.sleep(1.2)

            link = f'https://viacep.com.br/ws/{texto_cep}/json/'
            requisicao = requests.get(link)
            dic_requisicao = requisicao.json()
            uf = dic_requisicao['uf']
            cidade = dic_requisicao['localidade']
            engine.say(f'Ok, vi que você mora em {cidade}.')

            print(cidade, uf)
            city = f'{cidade}'
            city_u = city.upper()

            city_u = unidecode.unidecode(city_u)
            pconn = ibm_db_dbi.Connection(conn)
            selectQuery = f"select * from NUTRI where MUNICIPIO = '{city_u}'"
            selectStmt = ibm_db.exec_immediate(conn, selectQuery)
            while ibm_db.fetch_row(selectStmt):
                print(f"{city_u}:", ibm_db.result(selectStmt, 3))
            engine.say('Estes são os profissionais de sua cidade.')
            engine.runAndWait()

elif imc > 30.0 and imc <= 39.9:
        engine.say('De acordo com o resuldado de seu IMC, você está com obesidade grau 2, '
                   'sugiro procurar um profissional de saúde.')
        time.sleep(1.2)
        engine.say('Por favor me informe seu cep, para que eu possa lhe indicar um.')
        engine.runAndWait()
        print('CEP:')
        rec = sr.Recognizer()
        mic = sr.Microphone()
        with sr.Microphone(0) as mic:
            rec.adjust_for_ambient_noise(mic)
            audio = rec.listen(mic)
            texto_cep = rec.recognize_google(audio, language="pt-BR")
            print(texto_cep)
            time.sleep(1.2)

            link = f'https://viacep.com.br/ws/{texto_cep}/json/'
            requisicao = requests.get(link)
            dic_requisicao = requisicao.json()
            uf = dic_requisicao['uf']
            cidade = dic_requisicao['localidade']
            engine.say(f'Ok, vi que você mora em {cidade}.')

            print(cidade, uf)
            city = f'{cidade}'
            city_u = city.upper()

            city_u = unidecode.unidecode(city_u)
            pconn = ibm_db_dbi.Connection(conn)
            selectQuery = f"select * from NUTRI where MUNICIPIO = '{city_u}'"
            selectStmt = ibm_db.exec_immediate(conn, selectQuery)
            while ibm_db.fetch_row(selectStmt):

                print(f"{city_u}:", ibm_db.result(selectStmt, 3))
            engine.say('Estes são os profissionais de sua cidade.')
            engine.runAndWait()

elif imc > 40.0:
        engine.say('De acordo com o resultado de seu IMC voce está com obesidade grau 3, que é grave, sugiro você '
                   'procurar urgente um profissional de saúde')
        time.sleep(1.2)
        engine.say('Por favor me informe seu cep, para que eu possa lhe indicar um.')
        engine.runAndWait()
        print('CEP:')
        rec = sr.Recognizer()
        mic = sr.Microphone()
        with sr.Microphone(0) as mic:
            rec.adjust_for_ambient_noise(mic)
            audio = rec.listen(mic)
            texto_cep = rec.recognize_google(audio, language="pt-BR")
            print(texto_cep)
            time.sleep(1.2)

            link = f'https://viacep.com.br/ws/{texto_cep}/json/'
            requisicao = requests.get(link)
            dic_requisicao = requisicao.json()
            uf = dic_requisicao['uf']
            cidade = dic_requisicao['localidade']

            engine.say(f'Ok, vi que você mora em {cidade}.')
            engine.runAndWait()
            print(cidade, uf)
            city = f'{cidade}'
            city_u = city.upper()

            city_u = unidecode.unidecode(city_u)
            pconn = ibm_db_dbi.Connection(conn)
            selectQuery = f"select * from NUTRI where MUNICIPIO = '{city_u}'"
            selectStmt = ibm_db.exec_immediate(conn, selectQuery)
            while ibm_db.fetch_row(selectStmt):

                print(f"{city_u}:", ibm_db.result(selectStmt, 3))
            engine.say('Estes são os profissionais de sua cidade.')
            engine.runAndWait()

ibm_db.close(conn)
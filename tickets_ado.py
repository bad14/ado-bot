'''
BOT para sacar ofertas de corridas de la página de ADO
Por: Rigoberto M. rigohvz14@gmail.com
'''
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
import time
from time import strftime
import datetime
import smtplib, email
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
# LUGAR_ORIGEN/_DESTINO tal cual se encuentran en el catalogo de ado
LUGAR_ORIGEN = 'Tlapacoyan, Tlapacoyan Ver.'
LUGAR_DESTINO = 'Xalapa CAXA, Xalapa-Enríquez Ver.'
#dia en el que se hará el viaje
DIA_CORRIDA = 22
seguir = True
while seguir:
    try:
        driver = webdriver.Firefox()
        driver.get('https://www.ado.com.mx/#/')

        wait = WebDriverWait(driver, 10)
        button = wait.until(EC.visibility_of_element_located((By.ID, "onesignal-popover-cancel-button")))
        button.click()
        
        origen = driver.find_element_by_xpath('//div[@id = "search-bar"]//div[@class = "origin"]//input[1]')
        driver.execute_script("arguments[0].click();", origen)
        origen.send_keys(LUGAR_ORIGEN)
        
        li_org = driver.find_element_by_css_selector('#search-bar .origin .ng-isolate-scope .dropdown-selector ul')
        li_org.click()

        destino = driver.find_element_by_id('selector-destino')
        destino.click()
        destino.send_keys(LUGAR_DESTINO)
        time.sleep(2)
        li_dest = driver.find_element_by_css_selector('#search-bar .destination .ng-isolate-scope .dropdown-selector ul')
        li_dest.click()
        #para pasar al siguiente mes/quitar si se requiere viajar el mes actual o aumentar para meses adelante
        btn_next = driver.find_element_by_css_selector('.font-icon-right-arrow')
        btn_next.click()
        
        #arreglo con todas las fechas del calendario
        fecha = driver.find_elements_by_css_selector('.ng-scope .int .ng-binding') #[24]
        iterador = 0
        for x in fecha:
            if x != '':
                if str(x.text) == str(DIA_CORRIDA):
                    break
            iterador+=1
        #boton en posicion del iterador
        fecha = driver.find_elements_by_css_selector('.ng-scope .int .ng-binding')[iterador]
        fecha.click()
        #click en buscar
        buscar = driver.find_element_by_class_name('font-icon-search ')
        buscar.click()
        #esperar hasta que el contenedor de resultados sea visible
        wait.until(EC.visibility_of_element_located((By.ID, "result-container")))
        #lista de precios por corrida
        precios = driver.find_elements_by_css_selector('#result-container #table-container .container-fluid .ng-scope .row-height')
        lista = ''
        for x in precios:
            info = x.text.split("\n")
            if int(info[7].replace('$', '')) < 150:
                lista = lista +"\n "+info[1]+" "+info[7]

        if lista != '':
            seguir=False
            print("Enviando mail ...")
            body = lista
            sender_email = "sender"
            # Lista de correos separador por comma a donde enviar mail
            receiver_email = ["my_mail@mail.com"]

            server = smtplib.SMTP('mail.host.com', 587)
            server.starttls()
            server.login("user", "pass")
              
            message = MIMEMultipart()
            message["From"] = sender_email
            message["To"] = ", ".join(receiver_email)
            message["Subject"] = "Ofertas encontradas :) por mi bot"

            # Add body to email
            message.attach(MIMEText(body, "plain"))
            text = message.as_string()

            server.sendmail(sender_email, receiver_email, text)
            server.quit()
    except:
        print("No se completo la tarea")
    finally:
        driver.close()

    currentDT = datetime.datetime.now()
    print("Esperando 20 minutos ... %s" % str(currentDT.strftime("%I:%M:%S %p")))
    time.sleep(1200)

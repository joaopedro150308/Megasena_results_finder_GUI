from driver_function import iniciar_driver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as condicao_esperada
from time import sleep
from urllib.parse import quote
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from selenium import webdriver

def preparar_driver():
    driver, wait = iniciar_driver()
    URL = driver.command_executor._url
    SESSION_ID = driver.session_id
    print(f'Url: {URL}; Session_id: {SESSION_ID}')

    return driver, wait, URL, SESSION_ID


def iniciar_automacao(window, telefone, driver_inicial, wait, url, session_id, login_is_done=bool):
    if login_is_done is False:
        logar_whatsapp(window, driver_inicial, wait)
    if login_is_done is True:
        enviar_relatorio(driver=driver_inicial, wait=wait, telefone=telefone)
        print('Relatório enviado com sucesso!')
        driver_inicial.quit()


def logar_whatsapp(window, driver, wait):
    driver.get('https://web.whatsapp.com')
    try:
        qrcode = wait.until(condicao_esperada.visibility_of_element_located((By.XPATH, "//canvas[@aria-label='Scan me!']")))
        window.write_event_value('qrcode_carregado', 'Qr code completamente carregado.')
        div = wait.until(condicao_esperada.presence_of_element_located((By.XPATH, "//div[@class='_aigv _aigw']")))
        window.write_event_value('login_completo', 'Login bem suscedido')
    except TimeoutException:
        window.write_event_value('login_error', 'Erro ao fazer login. Tempo esgotado.')


def varrer_site(driver, wait):
    # Navegar até o site e encontrar:
    driver.get("https://loterias.caixa.gov.br/Paginas/Mega-Sena.aspx")

    # Resultado
    resultado = wait.until(condicao_esperada.visibility_of_element_located((By.XPATH, "//div[@class='resultado-loteria']//h3[1]"))).text
    driver.save_screenshot('site.png')
    print(resultado)

    # Conscurso
    concurso = wait.until(condicao_esperada.visibility_of_element_located((By.XPATH, "//div[@class='title-bar clearfix']//h2//span"))).text.split(' ')[1]
    print(concurso)

    # Data
    data = wait.until(condicao_esperada.visibility_of_element_located((By.XPATH, "//div[@class='title-bar clearfix']//h2//span"))).text.split(' ')[2].replace('(', '').replace(')', '')
    print(data)

    # Numeros
    elementos = wait.until(condicao_esperada.presence_of_all_elements_located((By.XPATH, "//div[@class='resultado-loteria']//ul//li")))
    numeros = []
    for elemento in elementos:
        numero = elemento.text
        numeros.append(numero)
    print(numeros)

    return resultado, concurso, data, numeros


def formatar_dados(driver, wait):

    resultado, concurso, data, numeros = varrer_site(driver, wait)

    # Formatando os números de lista para uma só string
    numeros_formatado = ''
    for i, numero in enumerate(numeros):
        if i != (len(numeros) - 1):
            numeros_formatado += str(numero) + ', '
        else:
            numeros_formatado += str(numero)

    dados = {
        'Resultado': resultado,
        'Concurso': concurso,
        'Data': data,
        'Numeros': numeros_formatado
    }

    return dados


def formar_relatorio(driver, wait):
    dados = formatar_dados(driver, wait)

    relatorio = f'''Bom dia! Segue abaixo o relatório de hoje sobre a Mega Sena.\n
    \nResultado: {dados["Resultado"]}\n
    Concurso: {dados["Concurso"]}\n
    Data: {dados["Data"]}\n
    Numeros: {dados['Numeros']}'''
    
    return relatorio


def enviar_relatorio(driver, wait, telefone):
    relatorio = formar_relatorio(driver, wait)
    link_personalisado2 = f'''https://web.whatsapp.com/send/?phone={telefone}&text={quote(relatorio)}&type=phone_number&app_absent=0'''
    driver.get(link_personalisado2)
    
    # link_personalisado = f'https://wa.me//{TELEFONE}?text={quote(relatorio)}'
    # botao_iniciar_conversa = wait.until(condicao_esperada.element_to_be_clickable((By.XPATH, "//a[@id='action-button']")))
    # print(botao_iniciar_conversa)
    # link_final = botao_iniciar_conversa.get_attribute('href')
    # print(link_final)
    # driver.get(link_final)
    # botao_iniciar_conversa.click()

    driver.save_screenshot('site.png')

driver, wait, URL, SESSION_ID = preparar_driver()
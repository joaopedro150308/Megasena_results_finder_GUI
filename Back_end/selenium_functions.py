from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as condicao_esperada
from time import sleep
from urllib.parse import quote
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException


def iniciar_automacao(window, telefone, driver_inicial, wait):
    driver_inicial.maximize_window()
    enviar_relatorio(driver=driver_inicial, wait=wait, telefone=telefone)
    print('Relatório enviado com sucesso!')
    sleep(5)
    driver_inicial.quit()
    window.write_event_value(
        'fim_da_automacao', 'Relatório enviado com sucesso!')


def logar_whatsapp(window, driver, wait):
    driver.get('https://web.whatsapp.com')
    try:
        qrcode = wait.until(condicao_esperada.visibility_of_element_located(
            (By.XPATH, "//canvas[@aria-label='Scan me!']")))
        window.write_event_value(
            'qrcode_carregado', 'Qr code completamente carregado.')
        div_whatsapp = wait.until(condicao_esperada.presence_of_element_located(
            (By.XPATH, "//div[@class='_aigv _aigw']")))
        window.write_event_value('login_completo', 'Login bem suscedido')
    except TimeoutException:
        window.write_event_value(
            'login_error', 'Erro ao fazer login. Tempo esgotado.')


def varrer_site(driver, wait):
    # Navegar até o site e encontrar:
    driver.get("https://loterias.caixa.gov.br/Paginas/Mega-Sena.aspx")

    # Resultado
    resultado = wait.until(condicao_esperada.presence_of_element_located(
        (By.XPATH, "//div[@class='resultado-loteria']//h3[1]"))).text
    print(resultado)

    # Conscurso
    concurso = wait.until(condicao_esperada.presence_of_element_located(
        (By.XPATH, "//div[@class='title-bar clearfix']//h2//span"))).text.split(' ')[1]
    print(concurso)

    # Data
    data = wait.until(condicao_esperada.presence_of_element_located(
        (By.XPATH, "//div[@class='title-bar clearfix']//h2//span"))).text.split(' ')[2].replace('(', '').replace(')', '')
    print(data)

    # Numeros
    elementos = wait.until(condicao_esperada.presence_of_all_elements_located(
        (By.XPATH, "//div[@class='resultado-loteria']//ul//li")))
    numeros = []
    for elemento in elementos:
        numero = elemento.text
        numeros.append(numero)
    print(numeros)

    # Premio atual
    premio_acumulado = wait.until(condicao_esperada.presence_of_element_located((By.XPATH, "//div[@class='totals']/p[1]//span[2]"))).text
    print(f'Premio acumulado: {premio_acumulado}')

    return resultado, concurso, data, numeros, premio_acumulado


def formatar_dados(driver, wait):

    resultado, concurso, data, numeros, premio_acumulado = varrer_site(driver, wait)

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
        'Numeros': numeros_formatado,
        'Premio_acumulado': premio_acumulado
    }

    return dados


def formar_relatorio(driver, wait):
    dados = formatar_dados(driver, wait)

    relatorio = f'''Bom dia! Segue abaixo o relatório de hoje sobre a Mega Sena.\n
    \nResultado: {dados["Resultado"]}\n
Concurso: {dados["Concurso"]}\n
Data: {dados["Data"]}\n
Números: {dados['Numeros']}\n
Premio acumulado: {dados['Premio_acumulado']}'''

    return relatorio


def enviar_relatorio(driver, wait, telefone):
    relatorio = formar_relatorio(driver, wait)
    link_personalisado = f'''https://web.whatsapp.com/send/?phone={telefone}&text={quote(relatorio)}&type=phone_number&app_absent=0'''
    driver.get(link_personalisado)
    campo_conversa = wait.until(condicao_esperada.visibility_of_element_located(
        (By.XPATH, "//div[@class='_ak1l']")))
    campo_conversa.send_keys(Keys.ENTER)

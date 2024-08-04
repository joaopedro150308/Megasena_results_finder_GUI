from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as condicao_esperada
from time import sleep
from urllib.parse import quote
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException
from Back_end.uteis import verificar_data_de_emissao_do_ultimo_relatorio


def iniciar_automacao(window, telefone, driver, wait, is_the_first_run):
    driver.set_window_size(driver.get_window_size().get(
        'width'), driver.get_window_size().get('height'))
    enviar_relatorio(driver=driver, wait=wait, telefone=telefone,is_the_first_run=is_the_first_run)
    sleep(1)
    print('Relatório enviado com sucesso!')
    driver.minimize_window()
    window.write_event_value('fim_da_automacao', 'Relatório enviado com sucesso!')


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
    if resultado == '':
        resultado = 'Houveram ganhadores!'
        print(resultado)
    sleep(1)

    # Conscurso
    concurso_e_data = wait.until(condicao_esperada.presence_of_element_located(
        (By.XPATH, "//div[@class='title-bar clearfix']//h2//span"))).text
    print(concurso_e_data)
    sleep(1)
    # Numeros
    elementos = wait.until(condicao_esperada.presence_of_all_elements_located(
        (By.XPATH, "//div[@class='resultado-loteria']//ul//li")))
    numeros = []
    for elemento in elementos:
        numero = elemento.text
        numeros.append(numero)
    print(numeros)

    # Premio atual
    estimativa_proximo_concurso = wait.until(condicao_esperada.presence_of_element_located(
        (By.XPATH, "//div[@class='next-prize clearfix']//p[2]"))).text
    print(f'Premio estimado p/ proximo concurso: {estimativa_proximo_concurso}')

    return resultado, concurso_e_data, numeros, estimativa_proximo_concurso


def formatar_dados(driver, wait):

    resultado, concurso_e_data, numeros, estimativa_proximo_concurso = varrer_site(driver, wait)
    # Formatando concurso
    concurso = concurso_e_data.split(' ')[1]

    # Formatando data
    data = concurso_e_data.split(' ')[2].replace('(', '').replace(')', '')
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
        'estimativa_proximo_concurso': estimativa_proximo_concurso
    }

    return dados


def formar_relatorio(driver, wait):
    dados = formatar_dados(driver, wait)

    relatorio = f'''Bom dia! Segue abaixo o relatório de hoje sobre a Mega Sena.\n
    \nResultado: {dados["Resultado"]}\n
Concurso: {dados["Concurso"]}\n
Data: {dados["Data"]}\n
Números: {dados['Numeros']}\n
Premio estimado p/ próximo concurso: {dados['estimativa_proximo_concurso']}'''

    with open('relatorio.txt', 'w', encoding='utf-8') as arquivo:
        arquivo.write(relatorio)


def enviar_relatorio(driver, wait, telefone, is_the_first_run):
    if verificar_data_de_emissao_do_ultimo_relatorio() in (False, None):
        formar_relatorio(driver, wait)

    with open('relatorio.txt', 'r', encoding='utf-8') as arquivo:
        relatorio = ''
        for linha in arquivo:
            relatorio += linha
        print(f'O relatorio é: {relatorio}')
    link_personalisado = f'''https://web.whatsapp.com/send/?phone={telefone}&text={quote(relatorio)}&type=phone_number&app_absent=0'''
    driver.get(link_personalisado)
    campo_conversa = wait.until(condicao_esperada.visibility_of_element_located(
        (By.XPATH, "//div[@class='_ak1l']")))
    campo_conversa.send_keys(Keys.ENTER)


def encerrar_sessao_whatsapp(driver, wait):
    # Abrir a janela
    driver.set_window_size(800, 600)
    # Navegar até a página principal do wahtsapp
    driver.get('https://web.whatsapp.com')
    # Localizando o botão de configuração
    botao_configuracao = wait.until(condicao_esperada.element_to_be_clickable((By.XPATH, "//div[@aria-label='Configurações']")))
    print('Botão configurações localizado')
    botao_configuracao.click()
    # Localizando os botões presentes na aba de condigurações
    botoes_das_configuracoes = wait.until(condicao_esperada.visibility_of_any_elements_located((By.XPATH, "//div[@class='x78zum5 xdt5ytf x1iyjqo2 x2lah0s xdl72j9 x1odjw0f xh8yej3']/div//button")))
    print('Botões localizados')
    # Localizando campo pesquisar
    campo_pesquisar_configuracao = wait.until(condicao_esperada.element_to_be_clickable((By.XPATH, "//div[@title='Pesquisar configurações']")))
    print('Campo pesquisar configurações localizado')
    # Efetuando ações até clicar no botão sair
    chain = ActionChains(driver)
    chain.send_keys(Keys.DOWN)
    sleep(1)
    chain.send_keys(Keys.UP)
    sleep(1)
    chain.send_keys(Keys.ENTER)
    chain.perform()
    botao_desconectar = wait.until(condicao_esperada.element_to_be_clickable((By.XPATH, "//div[@class='x1n2onr6 x1iyjqo2 xs83m0k x1l7klhg x1mzt3pk xeaf4i8']//div[3]/div//button[2]")))
    chain.send_keys(Keys.TAB)
    sleep(1)
    chain.send_keys(Keys.TAB)
    sleep(1)
    chain.send_keys(Keys.ENTER)
    chain.perform()

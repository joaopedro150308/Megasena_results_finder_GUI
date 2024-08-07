import PySimpleGUI as sg
from Back_end.uteis import formatar_numero_de_telefone, atualizar_disabled_do_elemento, verificar_se_os_campos_estao_seguindo_as_formatacoes
from threading import Thread
from Back_end.driver_function import iniciar_driver
from Back_end.selenium_functions import iniciar_automacao, logar_whatsapp, encerrar_sessao_whatsapp


def iniciar_interface():
    # Tema
    sg.theme('DarkGray8')
    # Layout
    layout = [
        [sg.Text('Defina o número que receberá a mensagem')],
        [sg.Text('Código do país', size=(14, 1)), sg.Input(size=(3, 1), key='codigo_pais'), sg.Text(
            '<- Inválido', text_color='red', key='codigo_pais_aviso', visible=False)],
        [sg.Text('Código de area', size=(14, 1)), sg.Input(size=(3, 1), key='codigo_area'), sg.Text(
            '<- Inválido', text_color='red', key='codigo_area_aviso', visible=False)],
        [sg.Text('Número de telefone'), sg.Input(size=(10, 1), key='numero'), sg.Text(
            '<- Inválido', text_color='red', key='numero_aviso', visible=False)],
        [sg.Text('Por favor preencha todos os campos',
                 text_color='red', visible=False, key='texto_aviso')],
        [sg.Button('Logar', key='logar'), sg.Button('Começar', disabled=True, key='botao_comecar'),
         sg.Button('Definir número', key='botao_definir_numero'), sg.Button('Sair')]
    ]
    # Janela
    window = sg.Window('Resultados', layout=layout)
    is_the_first_run = True
    # Tratamento de eventos
    while True:
        event, values = window.read()

        if event == 'Sair' or event == sg.WIN_CLOSED:
            # pylint: disable=used-before-assignment
            try:
                if login_completo is True:
                    sg.popup_ok('Iniciando processo de logout do wahtsapp, a janela se encerrará em breve',
                                auto_close=True, auto_close_duration=5)
            except UnboundLocalError:
                print('Não houve login no wahtsapp')
            break

        elif event == 'botao_definir_numero':
            window['botao_definir_numero'].update(
                'Definir número', button_color=sg.theme_button_color())
            if verificar_se_os_campos_estao_seguindo_as_formatacoes(window, values) is True:
                # -- Confirmar se o número digitado é o desejado --
                if sg.popup_yes_no(f'Você realmente deseja enviar o resultado para este número?\n\n{formatar_numero_de_telefone(values)}') == 'Yes':
                    # Se for, dispara um evento que aciona a automacao e define o número alvo
                    TELEFONE = f'{values["codigo_pais"]}{values["codigo_area"]}{values["numero"]}'
                    window['botao_definir_numero'].update(
                        'Definido', button_color=f'green on  {sg.theme_button_color_background()}')

    # -- Eventos relacionados ao login da conta whatsapp --
        # --- Se clicar em "Logar" ---
        elif event == 'logar':
            sg.popup_no_titlebar('A tela de login está iniciando. Por favor aguarde a PRÓXIMA MENSAGEM.',
                                 auto_close=True, auto_close_duration=5, non_blocking=False)
            driver, wait = iniciar_driver()
            thread_logar = Thread(target=logar_whatsapp, args=(
                window, driver, wait), daemon=True)
            thread_logar.start()
            atualizar_disabled_do_elemento(window, 'logar', True)
            atualizar_disabled_do_elemento(window, 'botao_comecar', True)

        elif event == 'login_completo':
            login_completo = True
            thread_logar.join()
            driver.minimize_window()
            atualizar_disabled_do_elemento(window, 'logar', False)
            sg.popup_no_titlebar('Login bem suscedido. Botão "Começar" liberado!',
                                 non_blocking=True, auto_close=True, auto_close_duration=5)
            atualizar_disabled_do_elemento(window, 'botao_comecar', False)
            print('Login efetuado')

        elif event == 'qrcode_carregado':
            sg.popup_ok(
                'ATENÇÃO!!\n\nPor favor faça login com a conta do whatsapp que enviará o relatório.\n\nVocê tem ATÉ 5 minutos para fazer login.')

        elif event == 'login_error':
            thread_logar.join()
            atualizar_disabled_do_elemento(window, 'logar', False)
            sg.popup(
                'Ooops. Erro ao fazer login. Tempo excedido\n\nPor favor tente novamente.')

        # -- Eventos relacionados ao inicio do real processo de automação --
        elif event == 'botao_comecar':
            try:
                thread_automacao = Thread(target=iniciar_automacao, args=(
                    window, TELEFONE, driver, wait, is_the_first_run), daemon=True)
                sg.popup_no_titlebar('Iniciando automação!\n\nPor favor aguarde e aproveite ;)',
                                     auto_close=True, auto_close_duration=5)
                thread_automacao.start()
                atualizar_disabled_do_elemento(window, 'botao_comecar', True)
            except NameError:
                sg.popup_ok(
                    'Oops, parece que você ainda NÃO DEFINIU UM NÚMERO. faça-o para poder começar.')

        elif event == 'fim_da_automacao':
            is_the_first_run = False
            thread_automacao.join()
            atualizar_disabled_do_elemento(window, 'botao_comecar', False)
            sg.popup_ok('Relatório enviado com sucesso!',
                        auto_close=True, auto_close_duration=3, non_blocking=True)

    # Finalizer driver após o fechamento da janela
    try:
        return driver, wait
    except UnboundLocalError:
        print('O driver não foi iniciado')
        return None, None

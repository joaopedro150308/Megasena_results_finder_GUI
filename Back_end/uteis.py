import PySimpleGUI as sg
from datetime import date


def verificar_tamanho_minimo(valor=str, tamanho_minimo=int):
    if len(valor) >= tamanho_minimo:
        return True
    else:
        return False


def verificar_se_os_campos_foram_preenchidos(window, values):
    results = list()
    for v in values.values():
        if len(v) > 1:
            results.append(True)
        else:
            results.append(False)

    # Se algum dos campos não foi preenchido, informar o usuário
    if False in results:
        window['texto_aviso'].update(visible=True)
        print('Os campos não foram completamente preenchidos')
        return False
    else:
        window['texto_aviso'].update(visible=False)
        return True


def verificar_se_sao_numeros(window, values):
    resultado = list()
    # Verificando se os elementos são ou não caracteres númericos
    for key, valor in values.items():
        try:
            int(valor)
            resultado.append({'resultado': True, 'elemento': key})
        except ValueError:
            resultado.append({'resultado': False, 'elemento': key})

    resultados_booleanos = []
    for dicionario in resultado:
        resultados_booleanos.append(dicionario['resultado'])

        if dicionario['resultado'] is False:
            window[f'{dicionario["elemento"]}_aviso'].update(visible=True)
        else:
            window[f'{dicionario["elemento"]}_aviso'].update(visible=False)
    window.refresh()
    # Se algum dos valores for inválido, notificar o usuário
    if False in resultados_booleanos:
        sg.popup_ok(
            'Por favor use apenas números.\n\nEvite caracteres como "-, +" ou "(, )"')
        return False
    else:
        return True


def verificar_se_os_campos_estao_seguindo_as_formatacoes(window, values):
    # -- Verificando se os campos estão preenchidos --
    if verificar_se_os_campos_foram_preenchidos(window, values) is True:
        # -- Verificando se os valores indicados são números --
        if verificar_se_sao_numeros(window, values) is True:
            return True


def formatar_valores(*valores):
    caracteres_indesejadas = ('-', '+', '(', ')')
    valores_formatados = list()

    for valor in valores:
        for caracter in caracteres_indesejadas:
            if caracter in valor:
                valor = valor.replace(caracter, '').strip()
            else:
                valor = valor.strip()
        valores_formatados.append(valor)

    return valores_formatados


def formatar_numero_de_telefone(values):
    valores_formatados = formatar_valores(
        values['codigo_pais'], values['codigo_area'], values['numero'])
    codigo_pais = valores_formatados[0]
    codigo_area = valores_formatados[1]
    numero = valores_formatados[2]
    numero_formatado = f'{numero[:5] + "-" + numero[5:]}'
    formatacao_final = f'+{codigo_pais} ({codigo_area}) {numero_formatado}'

    return formatacao_final


def atualizar_disabled_do_elemento(window, element_key, disabled_to_be=bool):
    window[f'{element_key}'].update(disabled=disabled_to_be)
    window.refresh()


def conseguir_data_atual():
    data_de_hoje = date.today()
    data_formatada = data_de_hoje.strftime("%d/%m/%Y")
    print(data_formatada)

    return data_formatada
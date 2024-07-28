from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.common.exceptions import *
from selenium.webdriver.support.ui import WebDriverWait


def iniciar_driver():
    chrome_options = ChromeOptions()

    arguments = ['--lang=pt-BR', '--window-size=(1920, 1080)',
                 '--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36 Edg/115.0.1901.203']
    for argument in arguments:
        chrome_options.add_argument(argument)

    chrome_options.add_experimental_option('prefs', {
        'download.prompt_for_download': False,
        'profile.default_content_setting_values.notifications': 2,
        'profile.default_content_setting_values.automatic_downloads': 1,
        'external_protocol_dialog.show_always_open_checkbox': False,
        # Desativando a janela que pede permissão para abrir outra aplicação
        'protocol_handler.policy.auto_launch_protocols_from_origins': [{'protocol': 'whatsapp', 'allowed_origins': ['https://api.whatsapp.com']}]
    })

    driver = webdriver.Chrome(options=chrome_options)
    wait = WebDriverWait(
        driver,
        300,
        poll_frequency=1,
        ignored_exceptions=[
            NoSuchElementException,
            ElementNotVisibleException,
            ElementNotSelectableException,
            NoAlertPresentException
        ]
    )

    return driver, wait

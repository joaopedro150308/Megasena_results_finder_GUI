from Front_end.interface import iniciar_interface
from Back_end.selenium_functions import encerrar_sessao_whatsapp

driver, wait = iniciar_interface()
if driver is not None:
    encerrar_sessao_whatsapp(driver, wait)
    driver.quit()
print('Fim do programa')
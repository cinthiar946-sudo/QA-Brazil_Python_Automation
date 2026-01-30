from asyncio import timeout
from encodings.punycode import selective_find
from operator import truediv

from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


from data import PHONE_NUMBER
from helpers import retrieve_phone_code
import time


class UrbanRoutesPage:
    # Campos DE e PARA
    from_locator = (By.ID, "from")
    to_locator = (By.ID, "to")

    # Selecionar número de telefone
    phone_number_locator = (By.CSS_SELECTOR, '.np-text')
    number_enter = (By.ID, 'phone')
    number_confirm = (By.CSS_SELECTOR, '.button.full')
    number_code = (By.ID, 'code')
    code_confirm = (By.XPATH, '//button[contains(text(),"Confirmar")]')

    # Selecionar tarifa e chamar táxi
    taxi_option_locator = (By.XPATH, '//button[contains(text(),"Chamar")]')

    # Estes dois seletores precisam ser XPaths, CSS selectors ou IDs válidos
    comfort_icon_locator = (By.XPATH, '//img[@src="/static/media/kids.075fd8d4.svg"]')
    comfort_active = (By.XPATH, '//*[@id="root"]/div/div[3]/div[3]/div[2]/div[1]/div[5]')


    # METODO DE PAGAMENTO
    add_metodo_pagamento = (By.CSS_SELECTOR, '.pp-button.filled')
    add_card = (By.CSS_SELECTOR, '.pp-plus')
    number_card = (By.ID, 'number')
    code_card = (By.CSS_SELECTOR, 'input.card-input#code')
    add_finish_card = (By.XPATH, '//button[contains(text(),"Adicionar")]')
    close_button_card = (By.CSS_SELECTOR, '.payment-picker.open .close-button')
    comfirm_card = (By.CSS_SELECTOR, '.pp-value-text')

    # Adicionar Comentario
    campo_comment = (By.ID, 'comment')

    # Pedidos de mantas e lençois
    switch_blanket = (By.CSS_SELECTOR, '.switch')
    switch_blanket_active =(By.CSS_SELECTOR, '#root > div > div.workflow > div.workflow-subcontainer > div.tariff-picker.shown > div.form > div.reqs.open > div.reqs-body > div:nth-child(1) > div > div.r-sw > div > input')
    # Pedir sorvete
    add_icecream = (
        By.XPATH,
        '//*[@id="root"]/div/div[3]/div[3]/div[2]/div[2]/div[4]/div[2]/div[3]/div/div[2]/div[1]/div/div[2]/div/div[3]'
    )

    qnt_icecream = (By.CSS_SELECTOR, '#root > div > div.workflow > div.workflow-subcontainer > div.tariff-picker.shown > div.form > div.reqs.open > div.reqs-body > div.r.r-type-group > div > div.r-group-items > div:nth-child(1) > div > div.r-counter > div > div.counter-value')

    call_taxi_button = (By.CSS_SELECTOR, '#root > div > div.workflow > div.smart-button-wrapper > button > span.smart-button-secondary')
    pop_up = (By.CSS_SELECTOR, '#root > div > div.order')

    def __init__(self, driver):
        self.driver = driver


    # Inicio dos testes

    def enter_from_location(self, from_text):
        # inserir DE
        print("Iniciando teste enter_from_location")
        self.driver.find_element(*self.from_locator).send_keys(from_text)

    def enter_to_location(self, to_text):
        # Inserir Para
        self.driver.find_element(*self.to_locator).send_keys(to_text)
        # Inserir Localizações

    def enter_locations(self, from_text, to_text):
        self.enter_from_location(from_text)
        self.enter_to_location(to_text)
        # Obter Valor de localização

    def get_from_location_value(self):
        return WebDriverWait(self.driver, 3).until(EC.visibility_of_element_located(self.from_locator)).get_attribute(
            'value')
        # Obter o valor do local
    def get_to_location_value(self):
        return WebDriverWait(self.driver, 3).until(EC.visibility_of_element_located(self.to_locator)).get_attribute(
            'value')
        # Clicar na opção taxi
    def click_taxi_option(self):
        self.driver.find_element(*self.taxi_option_locator).click()
        # Clicar no icone do conforto
    def click_comfort_icon(self):
        self.driver.find_element(*self.comfort_icon_locator).click()

        # Conforto Ativo
    def click_comfort_active(self):
        try:
            active_button = self.driver.find_element(*self.comfort_active)
            return "active" in active_button.get_attribute('class')
        except:
            return False

        # Número de Telefone
    def click_number(self, phone_number):
        self.driver.find_element(*self.phone_number_locator).click()
        self.driver.find_element(*self.number_enter).send_keys(phone_number)
        self.driver.find_element(*self.number_confirm).click()

        code = retrieve_phone_code(self.driver)  # Digitar código
        code_input = WebDriverWait(self.driver, 3).until(
            EC.visibility_of_element_located(self.number_code)
        )
        code_input.clear()
        code_input.send_keys(code)
        self.driver.find_element(*self.code_confirm).click()  # Confirmar código

         # Confirmar número
    def confirmation_number(self):
        number = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.phone_number_locator))
        return number.text


        # Adicionar cartão de credito
    def click_add_cartao(self, cartao, code):
        self.driver.find_element(*self.add_metodo_pagamento).click()
        self.driver.find_element(*self.add_card).click()
        time.sleep(1)
        self.driver.find_element(*self.number_card).send_keys(cartao)
        time.sleep(1)
        self.driver.find_element(*self.code_card).send_keys(code)
        time.sleep(1)
        self.driver.find_element(*self.add_finish_card).click()
        self.driver.find_element(*self.close_button_card).click()

        # Confirmar cartão
    def confirm_cartao(self):
        return self.driver.find_element(*self.comfirm_card).text



     # Adicionar comentario
    def add_comment(self, comentario):
        self.driver.find_element(*self.campo_comment).send_keys(comentario)

        # Comentario para o motorista
    def comment_for_driver(self, comment_for_driver):
        return self.driver.find_element(*self.comment_for_driver).click()
        # Pedir cobertor e lençoes
    def switch_cobertor(self):
        switch_ativo = self.driver.find_element(*self.switch_blanket)
        switch_ativo.click()

        # Pedido de cobertor e lençoes ativo
    def switch_cobertor_active(self):
        switch = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(self.switch_blanket_active))
        return switch.is_selected()


        # Adicionar Gelo
    def add_ice(self):
        self.driver.find_element(*self.add_icecream).click()

        # Quantidade de Sorvete 2
    def qnt_sorvete(self):
        return self.driver.find_element(*self.qnt_icecream).text

        # Chamar Taxi
    def call_taxi(self):
        self.driver.find_element(*self.call_taxi_button).click()

        # Exibir popup
    def pop_up_show(self):
        pop_up = WebDriverWait(self.driver, 15).until(
            EC.presence_of_element_located(self.pop_up)
        )
        return pop_up.text










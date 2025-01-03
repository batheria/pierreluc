from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import time
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup


class MoveDriver():
    
    def __init__(self):
        self.file_name = 'messagge_popup.txt'
        pass
    def save_popup_content_message(self, file_name, data):
        """
        Guarda información en un archivo de texto.

        Args:
            nombre_archivo (str): El nombre del archivo donde se guardará la información.
            informacion (str): La información que se desea guardar.
        """
        try:
            with open(file_name, 'a', encoding='utf-8') as archivo:  # Modo 'a' para agregar al archivo
                archivo.write(data, '\n\n\n')
            print(f"Información guardada en {file_name}")
        except Exception as e:
            print(f"Error al guardar la información: {e}")


    def login_account(self, driver, user, passwd):
        login_container = WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.CLASS_NAME, 'login-droite-contenu'))
        )
        inputs_login = login_container.find_elements(By.TAG_NAME, 'input')
        button_connect = login_container.find_element(By.TAG_NAME, 'button')
        user_input, pass_input = inputs_login[0],inputs_login[1]

        for caracter in user:
            user_input.send_keys(caracter)
            time.sleep(0.05)
        for caracter in passwd:
            pass_input.send_keys(caracter)
            time.sleep(0.05)
        time.sleep(1)
        button_connect.click()

    def reservation_court(self, driver):
        wait = WebDriverWait(driver, 10)
        excluir_horarios = ["07:00 à 08:00 (01:00)", "08:00 à 09:00 (01:00)"]
        hours_filtered = []
        menu_container = wait.until(EC.visibility_of_element_located((By.ID, 'menugauche')))
        menu_buttons = menu_container.find_elements(By.TAG_NAME, 'li')
        for menu_button in menu_buttons:
            text_in = menu_button.text
            if 'Badminton / Pickleball' in text_in:
                menu_button.click()
        time.sleep(1)
        reservation_table = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'tableres')))
        a_reservations_table = reservation_table.find_elements(By.TAG_NAME, 'a')
        
        for a in a_reservations_table:
            text_in = a.text
            if 'AJOUTER UNE RÉSERVATION' in text_in:
                a.click()
        time.sleep(2)
        reservation_sport_select = wait.until(EC.visibility_of_element_located((By.ID, 'popuptest')))

        sports = reservation_sport_select.find_elements(By.CLASS_NAME, 'contenant')
        sports[-1].click()
        time.sleep(2)
        reservation_court_table = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'popup-content')))
        
        for _ in range(0,3):
            options_reservation = reservation_court_table.find_elements(By.CLASS_NAME, 'rangee')
            date_reservation = options_reservation[3].find_elements(By.CLASS_NAME, 'bouton-plat-icone')
            date_reservation[-1].click()
            time.sleep(1)
            
        reservation_court_table = driver.find_element(By.CLASS_NAME, 'popup-content')
        options_reservation = reservation_court_table.find_elements(By.CLASS_NAME, 'contenant')
        try:
            hour_reservation = options_reservation[1]

            hours = hour_reservation.find_elements(By.TAG_NAME, 'a')

            hour_texts = [hour.text for hour in hours]

            for hour in hour_texts:
                hour_filtered =  hour.split(' - ')
                if not hour_filtered[0] in excluir_horarios:
                    hours_filtered.append(hour)

            print("Available times:", hours_filtered)
            return hours_filtered
        except Exception as e:
            print("Error in hours container", e)
    

    def select_parteinaire(self, driver):
        wait = WebDriverWait(driver, 10)
        dropdown = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'popup-content')))
        reservation_options = dropdown.find_element(By.CLASS_NAME, 'avec-titre')
        select_partenaire = reservation_options.find_element(By.TAG_NAME, 'select')
        select_partenaire.click()
        select = Select(select_partenaire)

        # Seleccionar la opción deseada por texto visible
        select.select_by_visible_text("???, Stephane")
        button_complete = dropdown.find_elements(By.TAG_NAME, 'button')
        button_complete[2].click()
        time.sleep(1)
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        data = soup.find('div', {'class':'popup-content'}).text
        self.save_popup_content_message(self.file_name, data)

    def reservation_hours(self, driver, hour_text):
        wait = WebDriverWait(driver, 10)
        print(f'Booking: {hour_text}')
        time.sleep(1)
        driver.refresh()
        menu_container = wait.until(EC.visibility_of_element_located((By.ID, 'menugauche')))
        menu_buttons = menu_container.find_elements(By.TAG_NAME, 'li')
        for menu_button in menu_buttons:
            text_in = menu_button.text
            if 'Badminton / Pickleball' in text_in:
                menu_button.click()
        time.sleep(4)
        reservation_table = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'tableres')))
        a_reservations_table = reservation_table.find_elements(By.TAG_NAME, 'a')
        
        for a in a_reservations_table:
            text_in = a.text
            if 'AJOUTER UNE RÉSERVATION' in text_in:
                a.click()
        reservation_sport_select = wait.until(EC.visibility_of_element_located((By.ID, 'popuptest')))
        
        sports = reservation_sport_select.find_elements(By.CLASS_NAME, 'contenant')
        sports[-1].click()
        time.sleep(2)
        reservation_court_table = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'popup-content')))
        
        for _ in range(0,3):
            options_reservation = reservation_court_table.find_elements(By.CLASS_NAME, 'rangee')
            date_reservation = options_reservation[3].find_elements(By.CLASS_NAME, 'bouton-plat-icone')
            date_reservation[-1].click()
            time.sleep(1) 
        time.sleep(2)
        reservation_court_table = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'popup-content')))
        options_reservation = reservation_court_table.find_elements(By.CLASS_NAME, 'contenant')
        hour_reservation = options_reservation[1]
        hour = hour_reservation.find_element(By.XPATH, f".//a[text()='{hour_text}']")
        hour.click()
        self.select_parteinaire(driver)

    

    
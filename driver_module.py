from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import time
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class MoveDriver():
    def __init__(self):
        pass

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
        menu_container = WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.ID, 'menugauche'))
        )
        menu_buttons = menu_container.find_elements(By.TAG_NAME, 'li')
        for menu_button in menu_buttons:
            text_in = menu_button.text
            if 'Badminton / Pickleball' in text_in:
                menu_button.click()
        time.sleep(1)
        reservation_table = WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.CLASS_NAME, 'tableres'))
        )
        a_reservations_table = reservation_table.find_elements(By.TAG_NAME, 'a')
        
        for a in a_reservations_table:
            text_in = a.text
            if 'AJOUTER UNE RÉSERVATION' in text_in:
                a.click()
        time.sleep(1)
        reservation_sport_select = WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.ID, 'popuptest'))
        )
        
        sports = reservation_sport_select.find_elements(By.CLASS_NAME, 'contenant')
        sports[-1].click()
        time.sleep(1)
        reservation_court_table = WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.CLASS_NAME, 'popup-content'))
        )
        
        for _ in range(0,3):
            options_reservation = reservation_court_table.find_elements(By.CLASS_NAME, 'rangee')
            date_reservation = options_reservation[3].find_elements(By.CLASS_NAME, 'bouton-plat-icone')
            date_reservation[-1].click()
            time.sleep(1)
            
        reservation_court_table = driver.find_element(By.CLASS_NAME, 'popup-content')
        options_reservation = reservation_court_table.find_elements(By.CLASS_NAME, 'contenant')
        hour_reservation = options_reservation[1]
        hours = hour_reservation.find_elements(By.TAG_NAME, 'a')

        hour_texts = [hour.text for hour in hours]
        print("Horarios disponibles:", hour_texts)
        return hour_texts
    
    def select_parteinaire(self, driver):
        dropdown = WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.CLASS_NAME, 'popup-content'))
        )
        reservation_options = dropdown.find_element(By.CLASS_NAME, 'avec-titre')
        select_partenaire = reservation_options.find_element(By.TAG_NAME, 'select')
        select_partenaire.click()
        select = Select(select_partenaire)

        # Seleccionar la opción deseada por texto visible
        select.select_by_visible_text("???, Stephane")
        button_complete = dropdown.find_elements(By.TAG_NAME, 'button')
        button_complete[2].click()
        

    def reservation_hours(self, driver, hour_text):
        driver.refresh()
        menu_container = WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.ID, 'menugauche'))
        )
        menu_buttons = menu_container.find_elements(By.TAG_NAME, 'li')
        for menu_button in menu_buttons:
            text_in = menu_button.text
            if 'Badminton / Pickleball' in text_in:
                menu_button.click()
        time.sleep(4)
        reservation_table = WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.CLASS_NAME, 'tableres'))
        )
        a_reservations_table = reservation_table.find_elements(By.TAG_NAME, 'a')
        
        for a in a_reservations_table:
            text_in = a.text
            if 'AJOUTER UNE RÉSERVATION' in text_in:
                a.click()
        reservation_sport_select = WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.ID, 'popuptest'))
        )
        
        sports = reservation_sport_select.find_elements(By.CLASS_NAME, 'contenant')
        sports[-1].click()
        time.sleep(1)
        reservation_court_table = WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.CLASS_NAME, 'popup-content'))
        )
        
        for _ in range(0,3):
            options_reservation = reservation_court_table.find_elements(By.CLASS_NAME, 'rangee')
            date_reservation = options_reservation[3].find_elements(By.CLASS_NAME, 'bouton-plat-icone')
            date_reservation[-1].click()
            time.sleep(1) 
        
        reservation_court_table = driver.find_element(By.CLASS_NAME, 'popup-content')
        options_reservation = reservation_court_table.find_elements(By.CLASS_NAME, 'contenant')
        hour_reservation = options_reservation[1]
        hour = hour_reservation.find_element(By.XPATH, f".//a[text()='{hour_text}']")
        hour.click()
        time.sleep(2)
        self.select_parteinaire(driver)

    

    
import time
from driver_module import MoveDriver
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from datetime import datetime, timedelta
import re

url = 'https://caps-portail.uqtr.ca/capnet/login.coba'


user = 'Martialdoyon@hotmail.com'
passwd = 'BC12ya59'
instance = MoveDriver()

def parse_hour_range(hour_range):
    """Convierte un rango de horas en objetos datetime, extrayendo solo el rango de tiempo."""
    # Usar una expresión regular para extraer el rango de tiempo (HH:MM à HH:MM)
    match = re.search(r'(\d{2}:\d{2}) à (\d{2}:\d{2})', hour_range)
    if not match:
        raise ValueError(f"Formato de rango de hora no válido: {hour_range}")
    start_time, end_time = match.groups()
    return datetime.strptime(start_time, '%H:%M'), datetime.strptime(end_time, '%H:%M')

def is_one_hour_range(hour_range):
    """Verifica si el rango tiene una duración de 1 hora."""
    start, end = parse_hour_range(hour_range)
    return end - start == timedelta(hours=1)

def is_consecutive_hour(current_range, next_range):
    """Verifica si dos rangos de horas son consecutivos."""
    _, current_end = parse_hour_range(current_range)
    next_start, _ = parse_hour_range(next_range)
    return current_end == next_start

def wait_until_7_am():
    """Espera hasta las 7:00 a.m. del día actual."""
    now = datetime.now()
    target_time = now.replace(hour=7, minute=0, second=0, microsecond=0)

    # Si ya pasó la hora de las 7 a.m., espera hasta el día siguiente.
    if now >= target_time:
        target_time += timedelta(days=1)

    time_to_wait = (target_time - now).total_seconds()
    print(f"Waiting until 7:00 a.m. ({time_to_wait:.2f} seconds)")
    time.sleep(time_to_wait)

def main():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(options=chrome_options)
    driver.maximize_window()
    driver.get(url)
    instance.login_account(driver, user, passwd)
    hour_texts = instance.reservation_court(driver)
    
    if len(hour_texts) > 1:
        for i in range(len(hour_texts) - 1):
            current_hour = hour_texts[i]
            next_hour = hour_texts[i + 1]
            
            # Verificar si ambos horarios tienen una duración de 1 hora y son consecutivos
            if is_one_hour_range(current_hour) and is_one_hour_range(next_hour) and is_consecutive_hour(current_hour, next_hour):
                print(f'Consecutive 1 hour times found: {current_hour} and {next_hour}')
                found_hours = [current_hour, next_hour]
                break
        print(found_hours)
        if len(found_hours) > 1:
            for hour_text in found_hours:
                # Buscar el elemento <a> con el texto del horario
                instance.reservation_hours(driver, hour_text)
                
        else:
            print('There are no two consecutive 1-hour slots available.')

if __name__ == "__main__":
    wait_until_7_am()
    main()
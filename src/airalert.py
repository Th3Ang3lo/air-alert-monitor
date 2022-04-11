import chromedriver_binary

from selenium import webdriver

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as Ec
from selenium.webdriver.chrome.options import Options

from datetime import datetime
from datetime import timedelta

from database.database import Database

import os

from dotenv import load_dotenv

load_dotenv()


class AirAlertMonitor:
    _from = os.getenv('FROM')
    to = os.getenv('TO')
    adults = os.getenv('ADULTS')
    kids = os.getenv('KIDS')
    babies = os.getenv('BABIES')
    going_date = os.getenv('GOING_DATE')
    return_date = os.getenv('RETURN_DATE')
    _class = os.getenv('CLASS')

    def get_url(self):
        return 'https://123milhas.com/v2/busca?de=' + self._from + '&para=' + self.to + '&adultos=' + self.adults + '&criancas=' + self.kids + '&bebes=' + self.babies + '&ida=' + self.going_date + '&volta=' + self.return_date + \
              '&classe=' + self._class

    def start_monitoring(self):
        options = Options()

        options.add_argument('headless')

        driver = webdriver.Chrome(options=options)
        driver.get(self.get_url())

        going_date = datetime.strptime(self.going_date, '%d-%m-%Y')
        return_date = datetime.strptime(self.return_date, '%d-%m-%Y')

        try:
            database = Database()

            print('Verificando passagens de ida "'+going_date.strftime('%d/%m/%Y')+'" e volta "'+return_date.strftime('%d/%m/%Y')+'"')
            print('Aguardando carregamento das passagens...')
            WebDriverWait(driver, 50).until(Ec.presence_of_all_elements_located((By.CLASS_NAME, 'scale-in')))

            print('Salvando preços do dia...')
            prices = driver.find_elements(By.XPATH, '//p[@class[contains(.,"price-details__text")]]//span[2]')
            prices = map(lambda _price: int(_price.text.replace('.', '').strip()), prices)

            for price in prices:
                database.create_research(
                    _from=self._from,
                    to=self.to,
                    going_date=going_date.strftime('%Y-%m-%d'),
                    return_date=return_date.strftime('%Y-%m-%d'),
                    price=price
                )

        except Exception as e:
            print(e)
        finally:
            driver.quit()
            going_date = going_date + timedelta(days=1)

            end_date = datetime.strptime(os.getenv('RETURN_DATE'), '%d-%m-%Y')

            diff = end_date - going_date

            if diff.days > 15:
                self.going_date = going_date.strftime('%d-%m-%Y')
            else:
                # RESET
                self.going_date = os.getenv('GOING_DATE')

            self.start_monitoring()


air_alert_monitor = AirAlertMonitor()
air_alert_monitor.start_monitoring()

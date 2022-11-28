from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import lxml


class Parser():

    def __init__(self):

        options = webdriver.ChromeOptions()
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--headless")

        self.driver = webdriver.Chrome(options=options)
        self.driver.implicitly_wait(15)

    def func_chunks_generators(self, lst, n):
        for i in range(0, len(lst), n):
            yield lst[i: i + n]

    def parse(self, inn):

        url = "https://reestr.nostroy.ru/sro/all/member/list"
        self.driver.get(url)

        html = self.driver.page_source

        btn_xpath = "/html/body/div/div/div/main/div/div/div[3]/div[1]/div[2]/div/div/div[1]/div[3]/div/button"
        input_xpath = "/html/body/div/div/div/main/div/div/div[3]/div[1]/div[2]/div/div/div[1]/div[1]/input"

        input = self.driver.find_element(By.XPATH, input_xpath)
        btn = self.driver.find_element(By.XPATH, btn_xpath)

        try:
            self.driver.find_element(By.XPATH, "//*[@id=\"app\"]/div/div/main/div/div/div[3]/div[1]/div[2]/div/div/div[1]/div[2]/div/button").click()
        except:
            pass

        input.clear()
        input.send_keys(inn)

        btn.click()

        try:
            check = self.driver.find_element(By.CLASS_NAME, "message").text
            reestr = [' - ' for i in range(10)]
            reestr.insert(1, inn)
            return [reestr]
        except:
            None

        # ======================================================= #
        #                      поиск по инн    (2-6)              #
        # ======================================================= #

        p2 = 'Наименование члена СРО'
        p3 = ' ИНН '
        p4 = ' Текущий статус члена '
        p5 = ' Тип '  # ???
        p6 = ' Рег. номер СРО '

        point_2_6 = []

        cards = self.driver.find_element(By.CLASS_NAME, "card-list") \
                    .find_elements(By.CLASS_NAME, 'card')

        html = self.driver.page_source
        soup = BeautifulSoup(html, "lxml")

        title = soup\
            .find('table', class_='table__list')\
            .find_all_next('th')

        value = soup\
            .find('table', class_='table__list')\
            .find_all_next('td')

        t = [i.text for i in title]
        v = [i.text for i in value]

        while len(t) < len(v):
            t += [i.text for i in title]

        result = list(zip(t, v))

        for j in range(len(v) // 8):
            for i in [p2, p3, p4, p5, p6]:
                try:
                    point_2_6.append(next(info for (p_, info) in result if p_ == i))
                except:
                    point_2_6.append(" - ")

        point_2_6 = list(self.func_chunks_generators(point_2_6, 5))

        reestr = []

        for i in range(len(point_2_6)):
            try:
                self.driver.find_element(By.XPATH,
                                    f"//*[@id=\"app\"]/div/div/main/div/div/div[4]/div/div/div[1]/table/tr[2]/td[{i + 2}]").click()
            except:
                self.driver.find_element(By.XPATH,
                                    f"//*[@id=\"app\"]/div/div/main/div/div/div[4]/div/div/div[1]/div/div[{i + 1}]/button/span").click()
            result = self.zip7_12(point_2_6[i])
            for i in result:
                reestr.append(i)

        self.driver.close()
        self.driver.quit()
        return reestr

    def zip7_12(self, current_2_6):

        # ======================================================= #
        #                      поиск по сведениям  (7-8)          #
        # ======================================================= #

        p7 = " Регистрационный номер члена саморегулируемой организации и дата его регистрации в реестре членов саморегулируемой организации: "
        p8 = " Дата прекращения членства: "

        point_7_8 = []

        self.driver.find_element(By.CLASS_NAME, 'card-item__title')
        html = self.driver.page_source

        soup = BeautifulSoup(html, "lxml")

        title = soup.\
            find_all('div', class_='card-item')[0].\
            find_all('div', class_='card-item__title')

        value = soup.\
            find_all('div', class_='card-item')[0].\
            find_all('div', class_='card-item__value')

        t = [i.text for i in title]
        v = [i.text for i in value]

        result = list(zip(t, v))

        for i in [p7, p8]:
            try:
                point_7_8.append(next(info for (p_, info) in result if p_ == i).split(',')[-1])
            except:
                point_7_8.append(' - ')

        # ======================================================= #
        #                      поиск по правам     (9-12)         #
        # ======================================================= #

        p9 = ' Стоимость работ по одному договору подряда (уровень ответственности) '
        p10 = ' Размер обязательств по договорам подряда с использованием конкурентных ' \
              'способов заключения договоров (уровень ответственности) '

        point_9_12 = []

        self.driver.find_element(By.XPATH, "//*[@id=\"app\"]/div/div/main/div/div/div[2]/div[3]/div[4]/button").click()

        html = self.driver.page_source
        soup = BeautifulSoup(html, "lxml")

        reestr = []
        try:
            checkContent = soup.find('div', 'mt-3').contents
            for i in [0, 1, 2, 3]:
                point_9_12.append(' - ')

            reestr = [current_2_6 + point_7_8 + point_9_12]

        except:
            title = soup\
                .find_all('div', class_="v-expansion-panel-content__wrap")[1]\
                .find_all_next('table', class_='table__list')[0]\
                .find_all_next('th')

            value = soup\
                .find_all('div', class_="v-expansion-panel-content__wrap")[1]\
                .find_all_next('table', class_='table__list')[0]\
                .find_all_next('td')

            t = [i.text for i in title]
            v = [i.text for i in value]

            while len(t) < len(v):
                t.append(' Дата решения ')
                t.append(' Основание решения ')
                t.append(' Решение органов управления ')

            result = list(zip(t, v))

            point_9_10 = []

            for i in [p9, p10]:
                try:
                    point_9_10.append(next(info for (p_, info) in result if p_ == i))
                except:
                    point_9_10.append(" - ")

            if (len(v[7:]) != 0):
                np = list(self.func_chunks_generators(v[7:], 3))
                for i in np:
                    i.pop(1)
                    point_9_12.append(point_9_10 + i)
            else:
                point_9_12.append(point_9_10 + [' - '] + [' - '])

            for i in point_9_12:
                reestr.append(current_2_6 + point_7_8 + i)

        # ======================================================= #
        #                      поиск по архиву     (13-16)        #
        # ======================================================= #

        # не встретилось ни одной записи с вкладкой "архив"       #

        # ======================================================= #

        self.driver.execute_script("window.history.go(-1)")
        return reestr

def run(inns):

    ###########################
    parser = Parser()
    reestr = parser.parse(inns)
    ###########################

    return reestr
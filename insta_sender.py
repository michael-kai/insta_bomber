import requests
import logging
import selenium.common.exceptions
import time
import random
import re
import json
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from decouple import config


class SeleniumLogin:
    InstaUrl = 'https://www.instagram.com/'
    APIHost = 'https://i.instagram.com'
    InstaDM = 'https://www.instagram.com/direct/inbox/'
    MaxSubsCount = 500
    headers = {'accept': '*/*',
               'accept-encoding': 'gzip, deflate, br',
               'accept-language': 'en-US,en;q=0.9',
               'cookie': '',
               'origin': 'https://www.instagram.com',
               'referer': 'https://www.instagram.com/',
               'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="99", "Google Chrome";v="99"',
               'sec-ch-ua-mobile': '?0',
               'sec-ch-ua-platform': '"Linux"',
               'sec-fetch-dest': 'empty',
               'sec-fetch-mode': 'cors',
               'sec-fetch-site': 'same-site',
               'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36',
               'x-asbd-id': '198387',
               'x-ig-app-id': '936619743392459',
               'x-ig-www-claim': 'hmac.AR1Dqa90VC1NKP3c1-fLj81JO_0MY9M8_NVaHylIZjaXXKxM',
               }
    path_close_pop_up = 'aOOlW.HoLwm '
    path_send_message = 'sqdOP.L3NKy.y3zKF'
    path_if_user_exist = '/html/body/div[6]/div/div/div[2]/div[2]/div[1]/div/div[3]'
    path_close_msg = '/html/body/div[6]/div/div/div[1]/div/div[2]/div/button'
    path_choose_user = '/html/body/div[6]/div/div/div[2]/div[2]/div[1]/div/div[3]/button'
    path_press_next = 'sqdOP.yWX7d.y3zKF.cB_4K'
    path_msg_field = '/html/body/div[1]/section/div/div[2]/div/div/div[2]/div[2]/div/div[2]/div/div/div[2]/textarea'

    def __init__(self, account, login, password):
        self.account = account
        self.login = login
        self.password = password
        self.browser = webdriver.Chrome('driver/chromedriver')
        self.browser.delete_all_cookies()
        self.acc_id = None

    @staticmethod
    def prepare_msg():
        syn1 = ["Hello", "Hi", "Greetings"]
        syn2 = ["Our firm", "Our business", "Our agency"]
        syn3 = ["reduction", "discount", "cut price"]
        syn4 = ["product", "outcome", "result"]
        syn5 = ["Contact us", "Touch us", "Let us to know"]

        msg_text = f'''Message text with variables like {random.choice(syn1)}'''
        return msg_text

    @staticmethod
    def save_subs_to_file(subs_list=None):
        with open('statistics.json', 'r') as reader:
            subs = json.loads(reader.read())
            for sub in subs_list:
                subs['subs'].update({sub: 'unsent'})
        with open('statistics.json', 'w') as writer:
            json.dump(subs, writer, ensure_ascii=False)

    @staticmethod
    def is_duplicate_sub(sub):
        with open('statistics.json', 'r') as reader:
            subs = json.loads(reader.read())['subs']
            return False if subs[sub] == 'unsent' else True

    @staticmethod
    def get_subs_file():
        with open('statistics.json', 'r') as reader:
            subs = json.loads(reader.read())['subs']
            return list(subs.keys())

    @staticmethod
    def count_receiver(sub):
        with open('statistics.json', 'r+') as reader:
            subs = json.loads(reader.read())
            subs['subs'][sub] = 'sent'

        with open('statistics.json', 'w') as writer:
            json.dump(subs, writer, indent=4)

    @staticmethod
    def clear_statistic():
        with open('statistics.json', 'r+') as reader:
            subs = json.loads(reader.read())
            subs['subs'] = {}

        with open('statistics.json', 'w') as writer:
            json.dump(subs, writer, indent=4)

    def get_login(self):
        self.browser.get(self.InstaUrl)
        time.sleep(random.randrange(3, 5))
        username_input = self.browser.find_element(by=By.NAME, value='username')
        username_input.clear()
        username_input.send_keys(self.login)
        time.sleep(2)

        password_input = self.browser.find_element(by=By.NAME, value='password')
        password_input.clear()
        password_input.send_keys(self.password)
        password_input.send_keys(Keys.ENTER)
        time.sleep(5)

        try:
            self.browser.find_element(by=By.CLASS_NAME, value='MWDvN')
        except selenium.common.exceptions.NoSuchElementException:
            self.browser.close()
            self.browser.quit()
            raise ValueError(f'Wrong credentials, check login and password')
        time.sleep(5)
        logging.error(f'Login Succeeded for {self.login}')

    def get_id(self):
        self.browser.get(self.account)
        time.sleep(10)
        regex = re.compile(r'logging_page_id":"profilePage_([\d]+)')
        acc_id = re.findall(regex, self.browser.page_source)[0].strip()
        self.acc_id = acc_id
        logging.error(f'ID extracted for {self.account}')

    def prepare_headers(self):
        cookie = [None, None, None, None, None, None, None]

        for x in self.browser.get_cookies():
            if x['name'] == 'mid':
                part = f"mid={x.get('value', None)}; "
                cookie[0] = part
            if x['name'] == 'ig_did':
                part = f"ig_did={x.get('value', None)}; "
                cookie[1] = part
            if x['name'] == 'ig_nrcb':
                part = f"ig_nrcb={x.get('value', None)}; "
                cookie[2] = part
            if x['name'] == 'csrftoken':
                part = f"csrftoken={x.get('value', None)}; "
                cookie[3] = part
            if x['name'] == 'ds_user_id':
                part = f"ds_user_id={x.get('value', None)}; "
                cookie[4] = part
            if x['name'] == 'sessionid':
                part = f"sessionid={x.get('value', None)}; "
                cookie[5] = part
            if x['name'] == 'rur':
                part = f"rur={x.get('value', None)}"
                cookie[6] = part

        self.headers['cookie'] = ''.join(cookie)
        logging.error(f'Headers prepared')

    def get_subs(self):
        all_subs = []
        max_id = 0

        for step in range(self.MaxSubsCount):
            time.sleep(2)
            url = self.APIHost + f'/api/v1/friendships/{self.acc_id}/followers/?count=12&max_id={max_id}&search_surface=follow_list_page'
            resp = requests.get(url=url, headers=self.headers)

            if resp.status_code == 200:
                logging.error(f'Subscribers collecting {url}')

                try:
                    resp.json()['big_list']
                except KeyError:
                    raise f'Account private'
                if resp.json()['big_list']:
                    all_subs.append(resp.json()['users'])
                    max_id += 12
                else:
                    url = self.APIHost + f'/api/v1/friendships/{self.acc_id}/followers/?count=12&max_id={max_id}&search_surface=follow_list_page'
                    resp = requests.get(url=url, headers=self.headers)
                    all_subs.append(resp.json()['users'])
                    break
            else:
                try:
                    print('Error with', resp.json())
                except Exception:
                    print(resp.status_code)

        time.sleep(420)
        not_private_subs = []
        for users in all_subs:
            for user in users:
                if not user['is_private']:
                    not_private_subs.append(user['username'])

        logging.error(f'Subscribers with no private accounts {len(not_private_subs)}')
        logging.error(f'Subscribers collected - {len(not_private_subs)}')
        SeleniumLogin.save_subs_to_file(subs_list=not_private_subs)

        logging.error(f'Subscribers written to file statistics.json')

    def send_direct_msges(self):
        subs = SeleniumLogin.get_subs_file()

        self.browser.get(self.InstaDM)
        time.sleep(random.randrange(3, 6))

        self.browser.find_element(by=By.CLASS_NAME, value=self.path_close_pop_up).click()
        time.sleep(random.randrange(3, 6))

        for sub in subs:
            if SeleniumLogin.is_duplicate_sub(sub):
                logging.error(f'Message already sent to {sub}')
                continue
            time.sleep(random.randrange(4, 6))

            self.browser.find_element(by=By.CLASS_NAME, value=self.path_send_message).click()
            time.sleep(random.randrange(3, 6))

            enter_user_name = self.browser.find_element(by=By.NAME, value='queryBox')

            enter_user_name.clear()
            time.sleep(random.randrange(3, 6))

            enter_user_name.send_keys(sub)
            time.sleep(random.randrange(3, 6))

            try:
                self.browser.find_element(by=By.XPATH, value=self.path_if_user_exist)

            except selenium.common.exceptions.NoSuchElementException as error:
                logging.error(f'User {sub} does not exist, skipped')
                self.browser.find_element(by=By.XPATH, value=self.path_close_msg).click()
                self.browser.find_element(by=By.CLASS_NAME, value=self.path_send_message).click()
                time.sleep(random.randrange(3, 6))
                continue

            time.sleep(random.randrange(3, 6))
            self.browser.find_element(by=By.XPATH, value=self.path_choose_user).click()
            time.sleep(random.randrange(3, 6))

            try:
                self.browser.find_element(by=By.CLASS_NAME, value=self.path_press_next).click()
                time.sleep(random.randrange(3, 6))
            except selenium.common.exceptions.NoSuchElementException:
                raise f'Temporary ban from Instagram. Try after 5-6 hours'
            msg_field = self.browser.find_element(by=By.XPATH, value=self.path_msg_field)
            time.sleep(random.randrange(3, 6))

            msg_field.clear()
            msg_text = SeleniumLogin.prepare_msg()
            time.sleep(random.randrange(3, 6))

            msg_field.send_keys(f'{msg_text}')
            msg_field.send_keys(Keys.ENTER)
            logging.error(f'Message to {sub} has been sent')

            SeleniumLogin.count_receiver(sub)

            time.sleep(5)
            self.browser.get(self.InstaDM)

        SeleniumLogin.clear_statistic()
        logging.error(f'Messages delivered')
        time.sleep(3)
        self.browser.close()
        self.browser.quit()


if __name__ == '__main__':
    logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(message)s')
    account = 'Enter account here'
    # E.g. https://www.instagram.com/wsj/
    login = config('login')
    password = config('password')
    process = SeleniumLogin(account, login, password)
    try:
        process.get_login()
    except ValueError:
        raise
    process.get_id()
    process.prepare_headers()
    process.get_subs()
    process.send_direct_msges()



import pandas as pd
import requests

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import re


pd.options.mode.chained_assignment = None

chromedriver = r'C:\Users\keshiah\Desktop\chromedriver'
options = webdriver.ChromeOptions()
options.add_argument('headless')
driver = webdriver.Chrome(executable_path=chromedriver, chrome_options=options)


def Parser(link='https://wincuptt.com/schedule/'):

    chromedriver = r'C:\Users\keshiah\Desktop\chromedriver'
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    driver = webdriver.Chrome(executable_path=chromedriver, chrome_options=options)
    driver.get(link)

    df = pd.DataFrame(columns=['date','time', 'room', 'player_1', 'player_2', 'result',
                               'player_1_set', 'player_2_set', 'player_1_winner', 'player_2_winner',
                               'player_1_set_1_pts', 'player_2_set_1_pts', 'player_1_set_2_pts', 'player_2_set_2_pts',
                               'player_1_set_3_pts', 'player_2_set_3_pts', 'player_1_set_4_pts', 'player_2_set_4_pts',
                               'player_1_set_5_pts', 'player_2_set_5_pts']
                      )
    games = driver.find_elements_by_tag_name("li")

    for x in games:
        try:
            if x.find_element_by_class_name("st-result").get_attribute(
                    'textContent') != '\u00a0' and x.find_element_by_class_name("st-result").get_attribute(
                'textContent') != ':':
                dict = {
                    'time': x.find_element_by_class_name("st-time").get_attribute('textContent'),
                    'room': x.find_element_by_class_name("st-room").get_attribute('textContent'),
                    'result': x.find_element_by_class_name("st-result").get_attribute('textContent')}

                names = x.find_elements_by_class_name("st-player")
                counter = 1
                for name in names:
                    dict['player_' + str(counter)] = name.get_attribute('textContent')
                    counter += 1

                df = df.append(dict, ignore_index=True)
        except NoSuchElementException:
            pass
    return df
    driver.quit()



def find_result(df):
        result = re.match(r'.:.', df['result'][0])
        result.group(0)
        res = re.findall(r'\d+-\d+', df['result'][0])
        return df
def find_room(df):
        for row in range(len(df)):
            try:
                df['room'][row] = int(df['room'][row][-1])
            except IndexError:
                df.drop([row])

        for row in range(len(df)):
            total_result = re.match(r'.:.', df['result'].loc[row])[0]
            df['player_1_set'][row] = int(total_result[0])
            df['player_2_set'][row] = int(total_result[-1])
        return df
def clean_result(df):
    for row in range(len(df)):
        if df['player_1_set'].loc[row] > df['player_2_set'].loc[row]:
            df['player_1_winner'][row] = 1
            df['player_2_winner'][row] = 0
        else:
            df['player_1_winner'][row] = 0
            df['player_2_winner'][row] = 1
    for row in range(len(df)):
        set_results = re.findall(r'\d+-\d+', df['result'][row])
        for set in range(5):
            try:
                df['player_1_set_' + str(set + 1) + '_pts'][row] = re.findall(r'\d+', set_results[set])[0]
                df['player_2_set_' + str(set + 1) + '_pts'][row] = re.findall(r'\d+', set_results[set])[1]
            except IndexError:
                df['player_1_set_' + str(set + 1) + '_pts'][row] = 0
                df['player_2_set_' + str(set + 1) + '_pts'][row] = 0
    df=df.drop(['result'],axis=1)
    return df


if __name__ == "__main__":
    df=Parser()
    df=find_result(df)
    df=find_room(df)
    df=clean_result(df)
    df=drop_result(df)
    print(df)



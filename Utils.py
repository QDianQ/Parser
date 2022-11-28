import time
import os
import pandas as pd


def to_csv(reestr):
    baseDir = os.getcwd()
    index = '№ п/п'
    columns = [
        "Сокращенное наименование члена СРО",
        "ИНН",
        "Статус",
        "Тип",
        "Рег. Номер СРО",
        "Дата регистрации в реестре",
        "Дата прекращения членства в СРО",
        "Стоимость работ по одному договору подряда",
        "Размер обязательств по договорам подряда",
        "Дата",
        "статус",
    ]
    unpack = []

    for i in reestr:
        unpack += i
    reestr = unpack

    reestr_df = pd.DataFrame(columns=columns, data=reestr)
    reestr_df.index.name = index
    reestr_df.index += 1
    path = baseDir + '/output/reestr.csv'
    reestr_df.to_csv(path)
    # print("[ - ]\tData saved to reestr.csv")

def get_inns(path):

    with open(path, 'r+') as file:
        inns = [line.rstrip('\n') for line in file]


    return inns
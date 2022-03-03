from bs4 import BeautifulSoup
import requests
import emoji

URL = "http://novoderevenkovsky--orl.sudrf.ru"
HEADERS = {
 "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 YaBrowser/21.8.1.468 Yowser/2.5 Safari/537.36"
}
numServer = 1
'''1 - п. Хомутово
   2- п. Красная Заря'''
# Проверка сайта
def isConnected():
    try:
        resource = requests.get(URL, headers=HEADERS)
        return resource.status_code
    except:
        return

#Из списка с разделителем делаю словарь
def sepListFromDict(lst, sep):
    dct = {}
    cnt = 0
    tmp = []
    for i in lst + [sep]:
        if i == sep and tmp:
            dct[cnt] = tmp
            cnt += 1
            tmp = []
        if i != sep:
            tmp += [i]
    return dct

#Делю список на подсписок
def splitDict(lst, c_num):
        return [lst[i:i + c_num] for i in range(0, len(lst), c_num)]

def getData(dt):
    listCorrectData = []
    if isConnected() == 200:
        urlPage = URL + "/modules.php?name=sud_delo&srv_num="+str(numServer)+"&H_date="+dt+""
        try:
            rq = requests.get(urlPage, headers=HEADERS)
            soup = BeautifulSoup(rq.text, 'html.parser')
            tables = soup.find('table', id = "tablcont")
            tableHeaders = []
            #Если таблица существует
            if tables != None:
                for stats in tables.find('tr'):
                    if stats.text != "\n":
                        if stats.text == "Судебныеакты":
                            tableHeaders.append("Судебные акты")
                            continue
                        #Добавляю заголовки таблиц
                        tableHeaders.append(stats.text)
                subTitleHeader = []
                sTHinText = []
                #Ищу подзаголовки
                for tr in tables.findAll('tr', {"bgcolor": "#DEDEDE"}):
                    subTitleHeader.append(tr.text)
                #Ищу ячейки для конкретного подзаголовка
                for td in tables.find('tr', {"bgcolor":"#DEDEDE"}).find_all_next('td'):
                    if td.text in subTitleHeader:
                        sTHinText.append("---"+str(0)+"---")
                        continue
                    #Меняю символ пробела на пробел
                    text = td.text.replace("\xa0", " ")
                    #Если в строке тольо пробелы
                    if td.text.isspace():
                        text = "Не указано!"
                    sTHinText.append(text)
                #print(sTHinText)
                """
                Спарсил все данные в словарь, при этом расрапсил списки на подсписки
                """
                dictData = {}
                for i in sepListFromDict(sTHinText, "---0---"):
                   dictData[i] = splitDict(sepListFromDict(sTHinText, "---0---")[i], 8)
                #print(dictData)
                for i in range(len(dictData)):
                    for j in range(len(dictData[i])):
                        allTextData = emoji.emojize(":detective: ") + subTitleHeader[i].upper() + "\n"
                        for num in range(len(tableHeaders)):
                            allTextData += emoji.emojize(":right_arrow: ") + tableHeaders[num] + ": " + dictData[i][j][num] + "\n"
                        listCorrectData.append(allTextData)
                return listCorrectData
            else:
                listCorrectData.append(emoji.emojize(":warning: ")+"Нет заседаний")
                #Неверная дата или нет засиданий
                return listCorrectData
        except:
            pass
        else:
            #Нет подключения к сайту
            listCorrectData.append(emoji.emojize(":warning: ")+"Нет подключения к сайту")
            return listCorrectData
#for item in getData("24.01.2022"):
#   print (item)

import time
import requests
from bs4 import BeautifulSoup
import csv


def get_html(url):
    r = requests.get(url)
    return r.text


def uptime(url):
    get_page_data(get_html(url))
    time.sleep(60)
    check_new(get_html(url))
    uptime(url)

def check_new(html):
    flag = 1
    soup = BeautifulSoup(html, 'lxml')
    table = soup.select("table#threadslist tr")
    with open('hpc_name.csv', 'r') as file:
        for tr in table:
            td = tr.select('td div > a')
            upd = tr.select('td div.smallfont')
            if td:
                title = td[0].get_text()
                urlpost = td[0].get('href')
            else:
                continue
            if upd:
                author = upd[0].get_text().strip()
                dataup = upd[1].get_text(' ', strip=True).split('от')
                dataupd = dataup[0].strip()
                lastauth = dataup[1].strip()


            for line in file.readline():
                if line[0] == title and line[3] == dataupd and line[4] == lastauth:
                    flag = 0
                    break
            if flag == 1:
                data = {'title': title,
                        'urlpost': urlpost,
                        'author': author,
                        'dataupd': dataupd,
                        'lastauth': lastauth}

                write_csv(data)
            elif flag == 0:
                break





def write_csv(data):
    with open('hpc_name.csv', 'a') as f:
        writer = csv.writer(f)
        writer.writerow((data['title'],
                         data['urlpost'],
                         data['author'],
                         data['dataupd'],
                         data['lastauth']))


def get_page_data(html):    

    first = {'title':  'Title',    #Название темы
           'urlpost':  'Url',      #Ссылка на тему
           'author':   'Author',   #Дата последнего обновления топика
           'dataupd':  'Update',   #Автор последнего обновления топика
           'lastauth': 'Lastauth'} #Автор топика
    write_csv(first)

    soup = BeautifulSoup(html, 'lxml')
    table = soup.select("table#threadslist tr")

    for tr in table:
        td = tr.select('td div > a')
        upd = tr.select('td div.smallfont')
        if td:
            title = td[0].get_text()
            urlpost = td[0].get('href')
        else:
            continue
        if upd:
            author = upd[0].get_text().strip()
            dataup = upd[1].get_text(' ', strip=True).split('от')
            dataupd = dataup[0].strip()
            lastauth = dataup[1].strip()



        data = {'title':    title,
                'urlpost':  urlpost,
                'author':   author,
                'dataupd':  dataupd,
                'lastauth': lastauth}

        write_csv(data)
        print(data)

def main():

    url = 'http://hpc.name/search.php?do=getdaily'
    uptime(url)



if __name__ == '__main__':
    main()
import time
import requests
import hashlib
from bs4 import BeautifulSoup
import csv



#
TICK_EVERY = 60  # sec
FILE_NAME = 'hpc_name.csv'
URL = 'http://hpc.name'
DAILY_URI = '/search.php?do=getdaily'
#LOGIN = ''
#PASSWORD = ''

#

def get_html(url):
    r = requests.get(url)
    return r.text


"""def authorization():
    session = requests.Session()
    #passwor = hashlib.md5(PASSWORD.encode('utf-8')).hexdigest()
    login_data = {
        "vb_login_username": LOGIN,
        "vb_login_password": PASSWORD,
        "s": "",
        "securitytoken": "guest",
        "do": "login",
        "vb_login_md5password": '51688dad6223f9a1dc0872e69e47aa15',
        "vb_login_md5password_utf": '51688dad6223f9a1dc0872e69e47aa15'
    }
    login = session.post("https://hpc.name/login.php?do=login", data=login_data)
    first_page_ = session.get(URL, cookies=login.cookies)
    print('не авторизовался' if 'Вы ввели неправильное имя или пароль' in first_page_.text else u'авторизовался')"""



def read_csv():
    topics = {}
    try:
        with open(FILE_NAME, 'r',newline='') as file:
            reader = csv.reader(file)
            for row in reader:
                # ','.join(row)
                topics[row[0]] = hashlib.md5(",".join(row).encode('utf-8')).hexdigest()


    except OSError:
        write_csv(
            {
                'title': 'Title',
                'urlpost': 'Url',
                'author': 'Author',
                'dataupd': 'Update',
                'lastauth': 'Lastauth'
            }
        )
    return topics


def write_csv(data):
    with open(FILE_NAME, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow((data['title'],
                         data['urlpost'],
                         data['author'],
                         data['dataupd'],
                         data['lastauth']))


def get_page_data(html, topics):
    soup = BeautifulSoup(html, 'html.parser')
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

        if title in topics:
            newHash = hashlib.md5(",".join([title, urlpost, author, dataupd, lastauth]).encode('utf-8')).hexdigest()
            if topics[title] == newHash:
                continue
            else:
                write_csv({'title': title,
                           'urlpost': urlpost,
                           'author': author,
                           'dataupd': dataupd,
                           'lastauth': lastauth}
                          )
        else:
            write_csv({'title': title,
                       'urlpost': urlpost,
                       'author': author,
                       'dataupd': dataupd,
                       'lastauth': lastauth}
                      )


def main():
    while True:
        topics = read_csv()
        get_page_data(get_html(URL + DAILY_URI), topics)
        time.sleep(TICK_EVERY)


if __name__ == '__main__':
    main()
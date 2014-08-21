from bs4 import BeautifulSoup
import requests


def getNames(fileName):
    f = open(fileName)
    countries = f.readlines()
    f.close()
    for c in countries:
        countries[countries.index(c)] = c.rstrip('\n')
    return countries


def generateUrls(countries):

    urls = []
    for c in countries:
        urls.append("https://www.constituteproject.org/constitution/" +
                    c.rstrip('\n'))

    return urls


def getPage(url):
    r = requests.get(url)
    if r.status_code != requests.codes.ok:
        raise Exception("Error: couldn't get page, Status code = " +
                        str(r.status_code))

    data = r.content
    soup = BeautifulSoup(data)
    return soup


def getText(soup):
    txt = soup.get_text().encode("utf-8")
    txt = '\n'.join(txt.split('\n')[52:])
    txt = txt.split('\n')
    txt = '\n'.join(txt[:(len(txt)-38)])
    return txt


def saveConstitution(name, text):
    f = open("../constitutions/"+name+".txt", "w")
    f.write(text)
    f.close()


def downloadOne(name, url):
    page = getPage(url)
    text = getText(page)
    saveConstitution(name, text)


def downloadAll():
    names = getNames("../data/state_urls.txt")
    urls = generateUrls(names)
    failed_urls = []

    for l in urls:
        ind = urls.index(l)
        try:
            page = getPage(l)
        except Exception:
            failed_urls.append(names[ind])
            continue

        text = getText(page)
        saveConstitution(names[ind], text)

    if len(failed_urls) > 0:
        print("Some constitutions couldn't be retrieved: ")
        for u in failed_urls:
            print(u)


def downloadScores(url=fh_url, filename="../data/fh.xls"):
    r = requests.get(url)
    if r.status_code != requests.codes.ok:
        raise Exception("Couldn't retrieve scores, error code:" +
                        str(r.status_code))

    with open(filename, 'w') as file:
        file.write(r.content)

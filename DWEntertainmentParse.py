#!/usr/bin/python

from bs4 import BeautifulSoup

class DWEntertainmentParse : 
    def __init__(self, filename) : 
        self.setHTMLFilename(filename)
        self.dinings = list()
    
    def setHTMLFilename(self, filename) : 
        self.filename = filename

    def parse(self) :
        html = '' 
        with open(self.filename, encoding = 'utf8') as htmlfile : 
            html = htmlfile.read()
        self.soup = BeautifulSoup(html, 'html.parser')
        # html parse
        for cardsoup in self.soup.find_all(attrs={'class': 'card show entertainment'}) :
            name = ''
            link = ''
            local = list()

            if cardsoup.find_all('h2') : 
                name = cardsoup.find_all('h2')[0].get_text()
            if cardsoup.find(attrs={'class': 'cardLinkOverlay lowOverlay'}) : 
                link = cardsoup.find(attrs={'class': 'cardLinkOverlay lowOverlay'}).get('href')

            if cardsoup.find(attrs={'aria-label': 'local'}) : 
                local = cardsoup.find(attrs={'aria-label': 'local'}).get_text().split(', ')
            if len(local) >= 2 : 
                park = local[0]
                area = local[1]
            else : 
                park = local[0]
                area = ''

            print('[DEBUG] name: [' + name + ']')
            print('[DEBUG] link: [' + link + ']')
            print('[DEBUG] park: [' + park + ']')
            print('[DEBUG] area: [' + area + ']')


if __name__ == '__main__' : 
    # downloaded page from https://disneyworld.disney.go.com/pt-br/entertainment/
    entertainment = DWEntertainmentParse('C:\\Users\\fabio\\Documents\\Projects\\Concierge\\pages\\entertainment.html')
    entertainment.parse()


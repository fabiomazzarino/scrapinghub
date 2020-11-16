#!/usr/bin/python

from bs4 import BeautifulSoup

class DWDiningParse : 
    def __init__(self, filename) : 
        self.setHTMLFilename(filename)
        self.dinings = list()

    @staticmethod
    def _fixprice(price) :
        ans = '' 
        for ch in price : 
            if ch == '$' : 
                ans += ch
            else : 
                break
        return ans
         
    
    def setHTMLFilename(self, filename) : 
        self.filename = filename

    def parse(self) :
        html = '' 
        with open(self.filename, encoding = 'utf8') as htmlfile : 
            html = htmlfile.read()
        self.soup = BeautifulSoup(html, 'html.parser')
        # html parse
        for cardsoup in self.soup.find_all(attrs={'class': 'card show dining'}) :
            name = ''
            link = ''
            diningtype = ''
            local = list()
            foodinfo = list()

            if cardsoup.find_all('h2') : 
                name = cardsoup.find_all('h2')[0].get_text()
            if cardsoup.find(attrs={'class': 'cardLinkOverlay lowOverlay'}) : 
                link = cardsoup.find(attrs={'class': 'cardLinkOverlay lowOverlay'}).get('href')
            if cardsoup.find(attrs={'aria-label': 'tipo de refeição'}) : 
                diningtype = cardsoup.find(attrs={'aria-label': 'tipo de refeição'}).get_text()

            if cardsoup.find(attrs={'aria-label': 'local'}) : 
                local = cardsoup.find(attrs={'aria-label': 'local'}).get_text().split(', ')
            if len(local) >= 2 : 
                park = local[0]
                area = local[1]
            else : 
                park = local[0]
                area = ''

            if cardsoup.find(attrs={'aria-label': 'facetas'}) : 
                foodinfo = cardsoup.find(attrs={'aria-label': 'facetas'}).get_text().split(', ')

            prices = list()
            types = list()
            for info in foodinfo : 
                if info[0] == '$' : 
                    prices.append(DWDiningParse._fixprice(info))
                else : 
                    types.append(info)
            foodprice = ', '.join(prices)
            foodtype = ', '.join(types)


if __name__ == '__main__' : 
    # downloaded page from https://disneyworld.disney.go.com/pt-br/dining/
    attractions = DWDiningParse('C:\\Users\\fabio\\Documents\\Projects\\Concierge\\pages\\dining.html')
    attractions.parse()


#!/usr/bin/python

from bs4 import BeautifulSoup
from DBAccess import DBAccess
from ParkGroup import ParkGroup
from Park import Park
from ParkArea import ParkArea
from ParkAttraction import ParkAttraction

class WDWAttractionsParse (DBAccess): 
    def __init__(self, filename) : 
        self.setHTMLFilename(filename)
        self.attractions = list()
    
    def setHTMLFilename(self, filename) : 
        self.filename = filename

    def parse(self) :
        html = '' 
        with open(self.filename, encoding = 'utf8') as htmlfile : 
            html = htmlfile.read()
        self.soup = BeautifulSoup(html, 'html.parser')
        # html parse
        for cardsoup in self.soup.find_all(attrs={'class': 'card show attractions'}) :
            name = ''
            link = ''
            short = ''
            local = list()

            if cardsoup.find_all('h2') : 
                name = cardsoup.find_all('h2')[0].get_text()
            if cardsoup.find(attrs={'class': 'cardLinkOverlay lowOverlay'}) : 
                link = cardsoup.find(attrs={'class': 'cardLinkOverlay lowOverlay'}).get('href')
                if link.split('/')[-1] != '' : 
                    short = link.split('/')[-1]
                else : 
                    short = link.split('/')[-2]
            if cardsoup.find(attrs={'aria-label': 'local'}) : 
                local = cardsoup.find(attrs={'aria-label': 'local'}).get_text().split(', ')
            if len(local) >= 2 : 
                parkname = local[0]
                areaname = local[1]
            else : 
                parkname = local[0]
                areaname = ''

            groups = ParkGroup.getParkGroupsByField('short', 'walt_disney_world_resort')
            if len(groups) == 0 : 
                continue
            else : 
                group = groups[0]

            safeparkname = parkname.replace("'", "''")
            parks = Park.getParksByField('name', safeparkname)
            if len(parks) == 0 : 
                print('*** NO PARK FOUND: ' + parkname)
                newpark = {
                    'parkgroupid':  group.getAttr('id'), 
                    'name':         safeparkname
                }
                park = Park.insert(newpark)
            else : 
                park = parks[0]

            if areaname != '' : 
                safeareaname = areaname.replace("'", "''")
                areas = ParkArea.getParkAreasByField('name', safeareaname)
                if len(areas) == 0 : 
                    print('*** NO PARK AREA FOUND: ' + areaname)
                    newarea = {
                        'parkid':   park.getAttr('id'), 
                        'name':     safeareaname
                    }
                    area = ParkArea.insert(newarea)
                else : 
                    area = areas[0]
            else : 
                area = None

            safename = name.replace("'", "''")
            attractions = ParkAttraction.getAttractionsByField('name', safename)
            if len(attractions) == 0 : 
                print('*** NO ATTRACTION FOUND: ' + name)
                newattraction = {
                    'parkid':   park.getAttr('id'), 
                    'name':     safename, 
                    'short':    short, 
                    'link':     link, 
                    'status':   'NEW'
                }
                if area is not None :
                    newattraction['parkareaid'] = area.getAttr('id') 
                ParkAttraction.insert(newattraction)

            else : 
                newattraction = False
                dupeattraction = False
                delattraction = False
                realattraction = False
                for attraction in attractions : 
                    if attraction.getAttr('status') == 'NEW' : 
                        newattraction = True
                    elif attraction.getAttr('status') == 'DUPE' : 
                        dupeattraction = True
                    elif attraction.getAttr('status') == 'DEL' : 
                        delattraction = True
                    elif attraction.getAttr('status') == 'EDIT' or attraction.getAttr('status') == 'PUBL' : 
                        realattraction = True

                if newattraction : 
                    if dupeattraction : 
                        print("*** DON'T KNOW HOW TO UPDATE DUPE ATTRACTION: " + name)
                    else : 
                        newattraction = {
                            'parkid':   park.getAttr('id'), 
                            'name':     safename,
                            'short':    short,  
                            'link':     link, 
                            'status':   'DUPE'
                        }
                        if area is not None :
                            newattraction['parkareaid'] = area.getAttr('id') 
                        ParkAttraction.insert(newattraction)
                else : 
                    newattraction = {
                        'parkid':   park.getAttr('id'), 
                        'name':     safename, 
                        'short':    short, 
                        'link':     link, 
                        'status':   'NEW'
                    }
                    if area is not None :
                        newattraction['parkareaid'] = area.getAttr('id') 
                    ParkAttraction.insert(newattraction)
                
                    


            


if __name__ == '__main__' : 
    # downloaded page from https://disneyworld.disney.go.com/pt-br/attractions/
    WDWAttractionsParse.connect('192.168.0.19', 'concierge', 'concierge', 'concierge')
    attractions = WDWAttractionsParse('C:\\Users\\fabio\\Documents\\Projects\\Concierge\\pages\\attractions.html')
    attractions.parse()


#!/usr/bin/park

from DBAccess import DBAccess
from Park import Park

from ParkAttraction import ParkAttraction

class ParkArea (DBAccess): 
    TABLENAME = 'parkarea'
    def __init__(self, wherecursor) : 
        super().__init__('parkarea', wherecursor)

    @staticmethod
    def getParkAreas(wherecursor = '') :
        if type(wherecursor) == str :
            qry = "SELECT * FROM parkarea"
            if wherecursor != '' : 
                qry += " WHERE " + wherecursor

            cursor = ParkArea.connector.cursor()
            cursor.execute(qry)
            areas = ParkArea.getParkAreas(cursor)
            cursor.close()

            return areas

        else : 
            areas = list()
            while True :
                area = ParkArea(wherecursor)
                if area.isEmpty() :
                    break
                areas.append(area)
            return areas

    @staticmethod
    def getParkAreasByField(fieldname, fieldvalue) : 
        where = fieldname + " = '" + str(fieldvalue) + "'"
        return ParkArea.getParkAreas(where)
        
    def getPark(self) :
        return Park.getParksByField('id', self.getAttr('parkid'))[0]

    def getAttractions(self) : 
        where = "parkid = " + self.getPark().getAttr('parkid') + " AND parkareaid = " + self.getAttr('id')
        return ParkAttraction.getAttractions(where)

    @staticmethod
    def insert(attrs) : 
        id = super(ParkArea, ParkArea).insert(ParkArea.TABLENAME, attrs)
        where = "id = " + str(id)
        area = ParkArea(where)
        return area




if __name__ == '__main__' : 
    ParkArea.connect('192.168.0.19', 'concierge', 'concierge', 'concierge')
    areas = ParkArea.getParkAreas()
    for area in areas : 
        print('[TEST] name: [' + area.getAttr('name') + ']')

    area = ParkArea.getParkAreasByField('name', 'Tomorrowland')[0]
    print('[TEST] short: [' + area[0].getAttr('short') + ']')
    
    park = area.getPark()
    print('[TEST] name: [' + park.getAttr('name') + ']')

    attractions = area.getAttractions()
    for attraction in attractions : 
        print('[TEST] name: [' + attraction.getAttr('name') + ']')

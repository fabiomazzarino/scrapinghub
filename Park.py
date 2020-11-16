#!/usr/bin/park

import DBAccess

import ParkGroup
import ParkAttraction

class Park (DBAccess.DBAccess): 
    TABLENAME = 'park'

    def __init__(self, wherecursor) : 
        super().__init__('parkgroup', wherecursor)

    @staticmethod
    def getParks(wherecursor = '') :
        if type(wherecursor) == str :
            qry = "SELECT * FROM park"
            if wherecursor != '' : 
                qry += " WHERE " + wherecursor

            cursor = Park.connector.cursor()
            cursor.execute(qry)
            parks = Park.getParks(cursor)
            cursor.close()

            return parks

        else : 
            parks = list()
            while True :
                park = Park(wherecursor)
                if park.isEmpty() :
                    break
                parks.append(park)
            return parks

    @staticmethod
    def getParksByField(fieldname, fieldvalue) :
        where = fieldname + " = '" + str(fieldvalue) + "'"
        return Park.getParks(where)
        
    def getParkGroup(self) :
        return ParkGroup.ParkGroup.getParkGroupsByField('id', self.getAttr('parkgroupid'))[0]

    def getAttractions(self) : 
        return ParkAttraction.ParkAttraction.getAttractionsByField('parkid', self.getAttr('parkid'))

    @staticmethod
    def insert(attrs) : 
        id = super(Park, Park).insert(Park.TABLENAME, attrs)
        where = "id = " + str(id)
        park = Park(where)
        return park


if __name__ == '__main__' : 
    Park.connect('192.168.0.19', 'concierge', 'concierge', 'concierge')
    parks = Park.getParks()
    for park in parks : 
        print('[TEST] name: [' + park.getAttr('name') + ']')

    park = Park.getParksByField('name', 'Magic Kingdom')[0]
    print('[TEST] short: [' + parks[0].getAttr('short') + ']')
    
    parkgroup = park.getParkGroup()
    print('[TEST] name: [' + parkgroup.getAttr('name') + ']')

    attractions = park.getAttractions()
    for attraction in attractions : 
        print('[TEST] name: [' + attraction.getAttr('name') + ']')

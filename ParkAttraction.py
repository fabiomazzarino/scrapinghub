#!/usr/bin/python

import DBAccess
import Park

class ParkAttraction (DBAccess.DBAccess) : 
    TABLENAME = 'parkattraction'

    def __init__(self, wherecursor) : 
        super().__init__('parkattraction', wherecursor)

    @staticmethod
    def getAttractions(wherecursor = '') : 
        if type(wherecursor) == str :
            qry = "SELECT * FROM parkattraction"
            if wherecursor != '' : 
                qry += " WHERE " + wherecursor

            cursor = ParkAttraction.connector.cursor()
            cursor.execute(qry)
            attractions = ParkAttraction.getAttractions(cursor)
            cursor.close()

            return attractions

        else : 
            attractions = list()
            while True :
                attraction = ParkAttraction(wherecursor)
                if attraction.isEmpty() :
                    break
                attractions.append(attraction)
            return attractions

    @staticmethod
    def getAttractionsByField(fieldname, fieldvalue) : 
        where = fieldname + " = '" + str(fieldvalue) + "'"
        return ParkAttraction.getAttractions(where)
        
    def getPark(self) :
        return Park.Park.getParksByField('id', self.getAttr('parkid'))[0]

    @staticmethod
    def insert(attrs) : 
        id = super(ParkAttraction, ParkAttraction).insert(ParkAttraction.TABLENAME, attrs)
        where = "id = " + str(id)
        attraction = ParkAttraction(where)
        return attraction

    def update(self) :
        where = "id = '" + str(self.getAttr('id'))
        super(ParkAttraction, ParkAttraction).update(ParkAttraction.TABLENAME, self.getAttrs(), where)
        attraction = ParkAttraction(where)





if __name__ == '__main__' : 
    ParkAttraction.connect('192.168.0.19', 'concierge', 'concierge', 'concierge')

    attractions = ParkAttraction.getAttractions()
    for attraction in attractions : 
        print('[TEST] name: [' + attraction.getAttr('name') + ']')

    
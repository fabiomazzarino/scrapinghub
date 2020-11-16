#!/usr/bin/python

from DBAccess import DBAccess
from Park import Park

class ParkGroup(DBAccess) :
    TABLENAME = 'parkgroup'
 
    def __init__(self, wherecursor) :
        super().__init__(ParkGroup.TABLENAME, wherecursor)

    @staticmethod
    def getParkGroups(wherecursor = '') :
        if type(wherecursor) == str :
            qry = "SELECT * FROM " + ParkGroup.TABLENAME
            if wherecursor != '' :
                qry += " WHERE " + wherecursor

            cursor = ParkGroup.connector.cursor()
            cursor.execute(qry)
            parkgroups = ParkGroup.getParkGroups(cursor)
            cursor.close()
            return parkgroups

        else : 
            parkgroups = list()
            while True :
                parkgroup = ParkGroup(wherecursor)
                if parkgroup.isEmpty() :
                    break
                parkgroups.append(parkgroup)
            return parkgroups

    @staticmethod
    def getParkGroupsByField(fieldname, fieldvalue) : 
        where = fieldname + " = '" + str(fieldvalue) + "'"
        return ParkGroup.getParkGroups(where)

    def getParks(self) :
        return Park.getParksByField('parkgroupid', self.getAttr('id'))

    @staticmethod
    def insert(attrs) : 
        id = super().insert(ParkGroup.TABLENAME, attrs)
        where = "id = " + id
        group = ParkGroup(where)
        return group


if __name__ == '__main__' : 
    ParkGroup.connect('192.168.0.19', 'concierge', 'concierge', 'concierge')

    parkgroups = ParkGroup.getParkGroups()
    for parkgroup in parkgroups : 
        print('[TEST] name: [' + parkgroup.getAttr('name') + ']')

    parkgroup = ParkGroup.getParkGroupsByField('name', 'Walt Disney World Resort')[0]
    print('[TEST] short: [' + parkgroup.getAttr('short') + ']')
    parks = parkgroup.getParks()
    for park in parks : 
        print('[TEST] name: [' + park.getAttr('name') + ']')



#!/usr/bin/python

import mysql.connector

class DBAccess : 
    TABLENAME = ''

    def _setAttrs(self, wherecursor) :
        self._clearAttrs()

        if type(wherecursor) == str :
            qry = "SELECT * FROM " + self.getTable() + " WHERE " + wherecursor
            cursor = self.connector.cursor()
            cursor.execute(qry)
            self._setAttrs(cursor)
            cursor.close()

        if type(wherecursor) == mysql.connector.cursor.MySQLCursor :
            row = wherecursor.fetchone()
            if not row is None :
                idx = 0
                for column in wherecursor.column_names :
                    self.attrs[column] = row[idx]
                    idx += 1

    def _clearAttrs(self) : 
        self.attrs = dict()

    def __init__(self, table = None, wherecursor = None) :
        self.setTable(table)
        self._setAttrs(wherecursor)

    def setTable(self, table) : 
        self.table = table

    def getTable(self) : 
        return self.table

    def getAttrs(self) : 
        return self.attrs

    def getAttr(self, name) : 
        if self.isEmpty() : 
            return ''
        return self.getAttrs()[name]

    def setAttr(self, name, value) : 
        if not self.isEmpty() : 
            self.getAttrs[name] = value

    def isEmpty(self) : 
        if len(self.attrs) == 0 : 
            return True
        return False

    @staticmethod
    def connect(host, user, passwd, dbname) : 
        if host is None : 
            host = ''
        if user is None : 
            user = ''
        if passwd is None : 
            dbname = ''

        DBAccess.connector = mysql.connector.connect(host="192.168.0.19", user="concierge", passwd="concierge", database="concierge")
        DBAccess.connected = True

    @staticmethod
    def disconnect() : 
        DBAccess.connector.disconnect()
        DBAccess.connected = False

    @staticmethod
    def isconnected() : 
        return DBAccess.connected

    @staticmethod
    def insert(table, attrs) :
        fields = ', '.join(attrs.keys())
        values = "', '".join(list(map(lambda x:str(x), list(attrs.values()))))
        sql = "INSERT INTO " + table + "(" + fields + ") VALUES ('" + values + "')"

        cursor = DBAccess.connector.cursor()
        cursor.execute(sql)
        DBAccess.connector.commit()
        if cursor.lastrowid : 
            id = cursor.lastrowid
        else : 
            id = None
        cursor.close()
        return id

    @staticmethod
    def update(table, attrs, where) :
        setlist = []
        for key, value in attrs.items() : 
            setlist.append(key + " = '" + value + "'")

        setclause = ', '.join(setlist)
        sql = "UPDATE " + table + " SET " + setclause + " WHERE " + where
        print("[DEBUG] sql: [" + sql + "]")

        cursor = DBAccess.connector.cursor()
        cursor.execute(sql)
        DBAccess.connector.commit()
        if cursor.lastrowid : 
            id = cursor.lastrowid
        else : 
            id = None
        cursor.close()
        return id         


if __name__ == '__main__' : 
    DBAccess.connect('192.168.0.19', 'concierge', 'concierge', 'concierge')
    print('[TEST] connected: [' + str(DBAccess.isconnected()) + ']')
    DBAccess.disconnect()
    print('[TEST] connected: [' + str(DBAccess.isconnected()) + ']')

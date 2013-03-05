#!/usr/bin/python
import MySQLdb

class db_restaurant:

   db_tableName = 'restaurant'

   def __init__(self):
        self.db = MySQLdb.connect(host="localhost", user="root", passwd="0178894", db="foodchain", charset="utf8")
        curs = self.db.cursor()
        curs.execute("SET NAMES utf8")
        curs.execute("SET CHARACTER_SET_CLIENT=utf8")
        curs.execute("SET CHARACTER_SET_RESULTS=utf8")
        self.db.commit()

   def connect(self):
      self.db = MySQLdb.connect(host="localhost", user="root", passwd="0178894", db="foodchain", charset="utf8")

   def close(self):
      self.db.close()

   def crawled(self, url):
      cursor = self.db.cursor()
      cursor.execute('SELECT crawled FROM ' + self.db_tableName + ' WHERE url=%s', [url])
      numResult = int(cursor.rowcount)
      boolResult = False
      if (numResult <=0):
         boolResult = False
      else:
         rowdata = cursor.fetchone()
         
         if rowdata[0] == 0:
            boolResult = False
         else:
            boolResult = True
      return boolResult

   def exist(self, name):
      cursor = self.db.cursor()

      cursor.execute('SELECT * FROM ' + self.db_tableName + ' WHERE name=%s', name)
      numOfResult = int(cursor.rowcount)
      boolResult = False
      if (numOfResult <= 0):
         boolResult = False
      else:
         boolResult = True
      return boolResult

   def insert(self, name,  tel,  address):
      if (not self.exist(name)):
         cursor = self.db.cursor()
         cursor.execute('INSERT INTO ' + self.db_tableName + '(name,tel,address) VALUES(%s,%s,%s)', [name, tel, address])
         self.db.commit()

   def update(self, url, crawled):
      cursor = self.db.cursor()
      cursor.execute('UPDATE ' + self.db_tableName + ' SET crawled=%s WHERE url=%s', [crawled, url])
      self.db.commit()
      
   def list(self):
      cursor = self.db.cursor()
      cursor.execute("SELECT * FROM " + self.db_tableName)
      numrows = int(cursor.rowcount)

      for x in range(0,numrows):
         row = cursor.fetchone()
         print row[0], "-->", row[1], "-->", row[2]

   def getUID(self,  resname):
      cursor = self.db.cursor()
      cursor.execute("SELECT * FROM " + self.db_tableName + " WHERE name =%s",  [resname])
      numrows = int(cursor.rowcount)
      
      row = cursor.fetchone()
      return row[0]
    
   def getResByUID(self,  resuid):
       cursor = self.db.cursor()
       cursor.execute("SELECT name,tel,address FROM " + self.db_tableName + " WHERE resuid = %s",  [resuid])
       
       row = cursor.fetchone()
       return row
   #def findByFoodUID(self, fooduid):
       
#a = db_food()
#print a.search('www')
#a.update('www',False)
#a.update('xxx',True)
#print a.crawled('www')
#print a.crawled('xxx')
#print a.exist('www')

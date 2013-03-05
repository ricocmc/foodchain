#!/usr/bin/python
import MySQLdb

class db_restaurantLinks:

   db_tableName = 'restaurantLinks'

   def __init__(self):
      self.db = MySQLdb.connect(host="localhost", user="root", passwd="0178894", db="foodchain")

   def connect(self):
      self.db = MySQLdb.connect(host="localhost", user="root", passwd="0178894", db="foodchain")

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

   def exist(self, url):
      cursor = self.db.cursor()

      cursor.execute('SELECT * FROM ' + self.db_tableName + ' WHERE url=%s', url)
      numOfResult = int(cursor.rowcount)
      boolResult = False
      if (numOfResult <= 0):
         boolResult = False
      else:
         boolResult = True
      return boolResult

   def insert(self, url):
      if (not self.exist(url)):
         cursor = self.db.cursor()
         cursor.execute('INSERT INTO ' + self.db_tableName + '(url) VALUES(%s)', url)
         self.db.commit()

   def update(self, url, crawled):
      cursor = self.db.cursor()
      cursor.execute('UPDATE ' + self.db_tableName + ' SET crawled=%s WHERE url=%s', [crawled, url])
      self.db.commit()
    
   def getNextUncrawled(self):
        cursor = self.db.cursor()
        cursor.execute("SELECT * FROM " + self.db_tableName + " WHERE crawled=0 LIMIT 0,1")
        row = cursor.fetchone()
        return row[1]
        
   def getAllUncrawled(self):
        cursor = self.db.cursor()
        cursor.execute("SELECT * FROM " + self.db_tableName + " WHERE crawled=0")
        rows = cursor.fetchall()
        return rows
        
   def list(self):
      cursor = self.db.cursor()
      cursor.execute("SELECT * FROM " + self.db_tableName)
      numrows = int(cursor.rowcount)

      for x in range(0,numrows):
         row = cursor.fetchone()
         print row[0], "-->", row[1], "-->", row[2]


#a = db_restaurantLinks()
#a.update('www',False)
#a.update('xxx',True)
#print a.crawled('www')
#print a.crawled('xxx')
#print a.exist('www')

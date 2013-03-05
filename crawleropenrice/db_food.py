#!/usr/bin/python
import MySQLdb

class db_food:

   db_tableName = 'food'
   db_relationTableName = 'foodres'
   
   def __init__(self):
      self.db = MySQLdb.connect(host="localhost", user="root", passwd="0178894", db="foodchain")
      curs = self.db.cursor()
      curs.execute("SET NAMES utf8")
      curs.execute("SET CHARACTER_SET_CLIENT=utf8")
      curs.execute("SET CHARACTER_SET_RESULTS=utf8")
      self.db.commit()

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

   def exist(self, food):
      cursor = self.db.cursor()

      cursor.execute('SELECT * FROM ' + self.db_tableName + ' WHERE name=%s', food)
      numOfResult = int(cursor.rowcount)
      boolResult = False
      if (numOfResult <= 0):
         boolResult = False
      else:
         boolResult = True
      return boolResult

   def insert(self, food):
      if (not self.exist(food)):
         cursor = self.db.cursor()
         cursor.execute('INSERT INTO ' + self.db_tableName + '(name) VALUES(%s)', food)
         self.db.commit()
    
   def insertFoodRes(self, fooduid,  resuid):
        cursor = self.db.cursor()
        cursor.execute('INSERT INTO ' + self.db_relationTableName + '(fooduid, resuid) VALUES(%s, %s)', [fooduid,  resuid])
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

   def search(self,  text):
      cursor = self.db.cursor()
      cursor.execute("SELECT fooduid, name FROM " + self.db_tableName + " WHERE name like %s",  ["%"+text+"%"])
      numrows = int(cursor.rowcount)
      
      #result = ""
      #for x in range(0,numrows):
         #row = cursor.fetchone()
         #result +=  str(row[1]) + " | "
      #return result
      return cursor.fetchall()
      
   def getUID(self,  name):
      cursor = self.db.cursor()
      cursor.execute("SELECT * FROM " + self.db_tableName + " WHERE name =%s",  [name])
      numrows = int(cursor.rowcount)
      
      row = cursor.fetchone()
      return row[0]

   def getResUIDFromFoodUID(self,  fooduid):
       cursor = self.db.cursor()
       cursor.execute("SELECT resuid FROM " + self.db_relationTableName + " WHERE fooduid =%s",  [fooduid])
       numrows = int(cursor.rowcount)
      
       row = cursor.fetchone()
       return row[0]
#a = db_food()
#print a.search('www')
#a.update('www',False)
#a.update('xxx',True)
#print a.crawled('www')
#print a.crawled('xxx')
#print a.exist('www')

# -*- coding: utf-8 -*-

#from flask import Flask
import flask, flask.views

import sys
sys.path.insert(0, './crawleropenrice')

from db_food import db_food
from db_restaurant import db_restaurant

app = flask.Flask(__name__)

#dont't do this!
app.secret_key = "bacon"

#@app.route("/")

class Main(flask.views.MethodView):
   def get(self):
      return flask.render_template('index/index.html')
   
   def post(self):
	print flask.request.data
        input = flask.request.form['searchInput']
        a = db_food()
        b = db_restaurant()
        
        resultList = a.search(input.encode('utf-8'))
        
        finalresult = ""
        for result in resultList:
            fooduid = result[0]
            name = result[1]
            resuid = a.getResUIDFromFoodUID(fooduid)
            res = b.getResByUID(resuid)
            resname = res[0].encode('utf-8')
            restel = res[1].encode('utf-8')
            resaddress = res[2].encode('utf-8')
            finalresult += name + "(*****)," + resname + "," + restel + "," + resaddress + " | "
            #finalresult += name + " | "
            
        a.close()
        b.close()
        
        if (finalresult!=""):
            flask.flash(finalresult.decode('utf-8'))
        else:
            flask.flash("Food data not found.")
        return self.get()

class Posts(flask.views.MethodView):
   def get(self):
      return flask.render_template('posts/index.html')

   def post(self):
       
      return flask.request.form['searchInput']

app.add_url_rule('/', 
				 view_func=Main.as_view('index'), 
				 methods=['GET', 'POST'])

app.add_url_rule('/posts',
				 view_func=Posts.as_view('main'),
				 methods=['GET', 'POST'])

#app.debug = True

if __name__ == "__main__":
   app.run(host='0.0.0.0')

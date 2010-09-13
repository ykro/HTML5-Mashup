#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import os
from google.appengine.ext.webapp import template
from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db
from django.utils import simplejson

#clases para ElModelo
class Entry (db.Model):
  date = db.DateTimeProperty(auto_now_add=True)
  llmap = db.GeoPtProperty()
  img = db.TextProperty()

  def to_dict(self):
       return dict([(p, unicode(getattr(self, p))) for p in self.properties()])
#se acaban las clases para ElModelo

class CreateEntry (webapp.RequestHandler):
	def post(self):
		values = self.request.body.split("&", 3)
		en = Entry()
		en.img = (values[2])[4:]
		lat = (values[0])[4:]
		lon = (values[1])[4:]
		en.llmap = db.GeoPt(lat,lon)
		en.put()

class ListEntries (webapp.RequestHandler):
	def post(self):
		entries = Entry.all().order('-date')	
		entries = entries.fetch(50)	
		self.response.out.write(simplejson.dumps([e.to_dict() for e in entries]))
		
class MainHandler(webapp.RequestHandler):
	def get(self):
		entries = Entry.all().order('-date')
		entries = entries.fetch(50)		
		template_values = {  
			'entries': entries
	    }
		path = os.path.join(os.path.dirname(__file__), 'index.html')
		self.response.out.write(template.render(path, template_values)) 
	
application = webapp.WSGIApplication(
	                                 [('/', MainHandler),
                                     ('/create', CreateEntry),
                                     ('/entries', ListEntries)],	
	                                 debug=True)
def main():
	run_wsgi_app(application)


if __name__ == '__main__':
    main()

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
import webapp2
import cgi
import jinja2
import os
from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir))

#create the database of blog posts
class BlogPost(db.Model):
    title = db.StringProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)

#create base handler others will inherit from
class Handler(webapp2.RequestHandler):

    #creates generic error message all handlers can use
    def renderError(self, error_code):
        self.error(error_code)
        self.response.write("Oops! Something went wrong.")

#creates main page
class Index(Handler):

    def get(self):
        pass
        #check syntax on this
        last_five = db.GqlQuery("SELECT * FROM BlogPost ORDER created DESC LIMIT 5)

        t = jinja_env.get_template("index.html")
        content = t.render(
                        movies = unwatched_movies,
                        error = self.request.get("error"))
        self.response.write(content)

class NewPostHandler(Handler):
    def get (self):
        pass

    def post (self):
        pass

class ViewPostHandler(Handler):
    def get(self, id):
        pass

app = webapp2.WSGIApplication([
    ('/', Index)
    ('/newpost', NewPostHandler)
    ('/blog/<id:\d+>', ViewPostHandler)
], debug=True)

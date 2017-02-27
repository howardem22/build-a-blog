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
import webapp2, cgi, jinja2, os
from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir))

#create the database of blog posts
class BlogPost(db.Model):
    title = db.StringProperty(required = True)
    body = db.StringProperty(required = True)
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
        query = BlogPost.all().order("-created")
        last_five = query.fetch(limit = 5)

        t = jinja_env.get_template("index.html")
        content = t.render(recent = last_five)
        self.response.write(content)

class NewPostHandler(Handler):
    def get (self):
        t = jinja_env.get_template("newpost.html")
        content = t.render(error = "")
        self.response.write(content)

    def post (self):
        user_title = self.request.get("blogname")
        user_body = self.request.get("blogtext")

        #needs both title and body, else regenerate form with error message
        if user_title == "" or user_body == "":
            t = jinja_env.get_template("newpost.html")
            content = t.render(error = "You need to add some content")
            self.response.write(content)
        else:
            entry = BlogPost(title = user_title, body = user_body)
            entry.put()
            id = entry.key().id()
            self.redirect('/blog/%s' %id)

class ViewPostHandler(webapp2.RequestHandler):
    def get(self, id):
        post= BlogPost.get_by_id(int(id))
        t = jinja_env.get_template("blogpost.html")
        content = t.render(post=post)
        self.response.write(content)

app = webapp2.WSGIApplication([
    ('/', Index),
    ('/newpost', NewPostHandler),
    webapp2.Route('/blog/<id:\d+>', ViewPostHandler)
], debug=True)

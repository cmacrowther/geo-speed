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
import jinja2
from google.appengine.ext import ndb
import json
import datetime

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(["templates"]),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class Result(ndb.Model):
    location = ndb.GeoPtProperty(required=True)
    mbps_upload = ndb.FloatProperty(required=True)
    mbps_download = ndb.FloatProperty(required=True)
    friendly_location = ndb.StringProperty()
    isp = ndb.StringProperty()
"""
    Handels adding the location and speed to the datastore. Should
    be sent in this format

    {'location' : {'longitude' : 0, 'latitude' :  0}, 'time' : 12:00, 'upload': 34.4, 'download' : 76, 'isp' : "Rogers"}
"""
class SubmitHandler(webapp2.RequestHandler):
    def post(self):
        longitude = float(self.request.get('longitude'))
        latitude = float(self.request.get('latitude'))
        upload = float(self.request.get('upload'))
        download = float(self. request.get('download'))
        isp = self.request.get('isp')
        friendly_location = self.request.get('friendly_location')

        entity = Result(location =ndb.GeoPt(latitude, longitude), mbps_upload=upload, mbps_download=download, isp=isp, friendly_location=friendly_location)
        entity.put()

        results = Result.query().fetch()
        resultList = []
        for obj in results:
            resultList.append({'longitude': obj.location.lon,
                               'latitude': obj.location.lat,
                               'upload': obj.mbps_upload,
                               'download': obj.mbps_download,
                                'friendly_location': obj.friendly_location,
                               'isp': obj.isp})
        theJson = json.dumps(resultList)
        self.response.write(theJson)

"""
    return results back to the client in JSON format.
"""
class ReturnHandler(webapp2.RequestHandler):
    def get(self):
        results = Result.query().fetch()
        resultList = []
        for obj in results:
            resultList.append({'longitude': obj.location.lon,
                               'latitude': obj.location.lat,
                               'upload': obj.mbps_upload,
                               'download': obj.mbps_download,
                                'friendly_location': obj.friendly_location,
                               'isp': obj.isp})
        theJson = json.dumps(resultList)
        self.response.write(theJson)
class MainHandler(webapp2.RequestHandler):
    def get(self):
        template = JINJA_ENVIRONMENT.get_template("index.html")
        self.response.write((template.render({})))

app = webapp2.WSGIApplication([
    ('/', MainHandler), ('/submit', SubmitHandler), ('/request', ReturnHandler)
], debug=True)

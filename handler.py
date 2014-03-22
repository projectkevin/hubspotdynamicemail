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
import urllib2
import json
from app.handler import BaseHandler
from google.appengine.api import memcache


class Start(BaseHandler):
    def get(self):
        template_values = {
                           'placeholder':'yay!'
                           }
        self.render('start.html', **template_values)

class pick(BaseHandler):
    def post(self):
        apikey = self.request.get('apikey')
        portalid = self.request.get('portalid')
        #store apikey in memcache callable by the portal ID
        memcache.add(key=portalid, value=apikey, time=3600)
        url = 'http://api.hubapi.com/content/api/v2/templates'
        parameters = 'limit=100'
        r = urllib2.urlopen('{}?hapikey={}&{}'.format(url, apikey, parameters))
        raw_json = r.read()
        readable_json = json.loads(raw_json)
        #count = readable_json['total_count']
        
        id = []
        name = []
        img = []
        
        for i in range(len(readable_json['objects'])):
            id.append(readable_json['objects'][i]['id'])
            name.append(readable_json['objects'][i]['label'])
            img.append(readable_json['objects'][i]['thumbnail_path'])

       
        template_values = {
                           'templates': zip(id,name,img),
                           'portalid':portalid
                         
                           }
        self.render('choose.html', **template_values)
        
class send(BaseHandler):
    def post(self):
        ids = self.request.get_all('id')
        portalid = self.request.get('portalid')
        
        template_values = {
                           'ids' : ids,
                           'portalid': portalid
                           }
        self.render('send.html', **template_values)
        #for id in ids:
            #self.response.write(ids)     
            
class confirm(BaseHandler):
    def post(self):
        ids = self.request.get_all('id') 
        portalid = self.request.get('portalid')
        oldapikey =  memcache.get(portalid)
        newapikey = self.request.get('apikey')
        httpcode = []
        for id in ids:
            url = 'http://api.hubapi.com/content/api/v2/templates'
            template_id = id
            r = urllib2.urlopen('{}/{}?hapikey={}'.format(url, template_id, oldapikey))
            raw_json = r.read()
            readable_json = json.loads(raw_json)

            #make category_id available as a variable to change if we want
            try:
                readable_json['category_id']
            except:
                pass
            else:
                new_category_id = readable_json['category_id']
            #make folder available as a variable to change if we want
            try:
                readable_json['folder']
            except:
                pass
            else:
                new_folder = readable_json['folder']
            #make id available as a variable to change if we want
            try:
                readable_json['id']
            except:
                pass
            else:
                new_id = readable_json['id']
            #make label available as a variable to change if we want
            try:
                readable_json['label']
            except:
                pass
            else:
                new_label = readable_json['label']
            #make path available as a variable to change if we want
            try:
                readable_json['path']
            except:
                pass
            else:
                new_path = readable_json['path']
            #make source available as a variable to change if we want
            try:
                readable_json['source']
            except:
                pass
            else:
                new_source = readable_json['source']
            #make thubmnail_path available as a variable to change if we want
            try:
                readable_json['thumbnail_path']
            except:
                pass
            else:
                new_thumbnail_path = readable_json['thumbnail_path']
            
            #alt_path = 'custom/page/' + readable_json['folder'] +'/' + readable_json['label'] + '.html'
            alt_path = 'custom/page/imported_groups/' + readable_json['label'] + '.html'
            print alt_path
            payload = {'category_id': new_category_id, 'folder': new_folder, 'id': new_id, 'label': new_label, 'path': alt_path, 'thumbnail_path': new_thumbnail_path, 'source': new_source}
            payload = json.dumps(payload)
            #payload = urllib.urlencode(payload)
            #self.response.write('{}?hapikey={}'.format(url,newapikey))
            r = urllib2.urlopen('{}?hapikey={}'.format(url,newapikey),payload)
            rcode = r.code
            httpcode.append(rcode)
            
        
        template_values = {
                           'placeholder' : 'yay!',
                           'responses' : httpcode 
                           
                           }    
        self.render("/confirm.html",**template_values)



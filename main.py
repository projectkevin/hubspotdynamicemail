#This is designed to work with the post webhook functionality using the hubspot platform
#Question sends them to salesengineers@hubspot.com

import webapp2
import json
import requests


class MainHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write('Hello world!')

    def post(self):
        #grab a template to replace.  I have hardcoded in a template id for an email template called "ToBeReplaced"
		#http://api.hubapi.com/content/api/v2/templates?access_token=d6ddc47d-b1e2-11e3-9a71-c9c13c316bd2&limit=100
		#template id = 602923916

        #This is a json block from the wbehook that could be parsed or used in different ways.  I am just going to return the webhook data back as part
        #of the email template
        values = self.request

		#This needs to be in every mail otherwise the template update will fail
        canspam = """
    				{{site_settings.company_city}}
					{{site_settings.company_state}}
					{{site_settings.company_street_address_1}}
					{{site_settings.company_name}}
					{{unsubscribe_link}}
					"""

		#This is where we will create the html we want to use for the email.  We could pull this dyanmically from another site like twitter
		#or call another CRM or whatever our little heart desires.  In this case I am emailing out the contents of the request

        newhtml = "<h1>Enter whatever html/css you want to appear for the end client</h1>" + "<div>" + str(values) + "</div>"

        payload = {}
        payload['source'] = newhtml + canspam

        tosend = json.dumps(payload)

        url = 'http://api.hubapi.com/content/api/v2/templates/602923916?access_token=d6ddc47d-b1e2-11e3-9a71-c9c13c316bd2'

		#result = urlfetch.put(url=url,payload=tosend)  urlfetch put function doesn't work.  Will investigate later
        result = requests.put(url=url, data=tosend) #requests always works, not part of the default google app engine package


app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)

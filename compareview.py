import webapp2
import sys
import os
import jinja2
from google.appengine.api import users
from google.appengine.ext import ndb
from myuser import MyUser
from gpudata import GpuData
from datetime import datetime

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__) + "/templates"),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True
)


class CompareView(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        user = users.get_current_user()
        value = self.request.get('compare', allow_multiple=True)

        if not value:
            self.redirect('/compare')
            return
        
        if user is None:
            template_values = {
                'gpulist': data,
                'login_url': users.create_login_url(self.request.uri)
            }
            template = JINJA_ENVIRONMENT.get_template("index.html")
            self.response.write(template.render(template_values))
            return          

        value1 = value[0]
        value2 = value[1]
        gpu_query = GpuData.query(GpuData.devicename.IN([value1,value2]))
        data = gpu_query.fetch() 
        myuser_key = ndb.Key('MyUser', user.user_id())
        myuser = myuser_key.get()
        if myuser is None:
            myuser = MyUser(id=user.user_id())
            myuser.put()

        template_values = {
            'logout_url': users.create_logout_url(self.request.uri),
            'gpudata': myuser.data,
            'gpulist': data,
            'value1': value1,
            'value2': value2,
        }
        template = JINJA_ENVIRONMENT.get_template("compareView.html")
        self.response.write(template.render(template_values))
        
        

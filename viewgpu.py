import webapp2
import sys
import os
import jinja2
from google.appengine.api import users
from google.appengine.ext import ndb
from myuser import MyUser
from gpudata import GpuData
from compare import Compare

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__) + "/templates"),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True
)


class ViewGpu(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        
        user = users.get_current_user()
        gpus_query = GpuData.query()
        gpus = gpus_query.fetch()
        if user is None:
            template_values = {
                'gpu_list': gpus,
                'login_url': users.create_login_url(self.request.uri)
            }
            template = JINJA_ENVIRONMENT.get_template("index.html")
            self.response.write(template.render(template_values))
            return          
 
        myuser_key = ndb.Key('MyUser', user.user_id())
        myuser = myuser_key.get()
        if myuser is None:
            myuser = MyUser(id=user.user_id())
            myuser.put()

        template_values = {
            'logout_url': users.create_logout_url(self.request.uri),
            'gpudata': myuser.data,
            'gpu_list': gpus,
            'name': self.request.get('name')
        }
        template = JINJA_ENVIRONMENT.get_template("viewgpu.html")
        self.response.write(template.render(template_values))

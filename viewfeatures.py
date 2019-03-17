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


class ViewFeatures(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        action = self.request.get('button')
        user = users.get_current_user()
        query = GpuData.query()
        
        if self.request.get('geometryShader'):
            query = query.filter(GpuData.geometryShader == True)

        if self.request.get('tesselationShader'):
            query = query.filter(GpuData.tesselationShader == True)       

        if self.request.get('shaderInt16'):
            query = query.filter(GpuData.shaderInt16 == True)

        if self.request.get('sparseBinding'):
            query = query.filter(GpuData.sparseBinding == True)

        if self.request.get('textureCompressionETC2'):
            query = query.filter(GpuData.textureCompressionETC2 == True)        

        if self.request.get('vertexPipelineStoresAndAtomics'):
            query = query.filter(GpuData.vertexPipelineStoresAndAtomics == True)

        data = query.fetch()
        
        if user is None:
            template_values = {
                'login_url': users.create_login_url(self.request.uri),
                'data': data,
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
            'data': data,
        }
        template = JINJA_ENVIRONMENT.get_template("features.html")
        self.response.write(template.render(template_values))

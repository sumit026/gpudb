import webapp2
import jinja2
import os
from google.appengine.api import users
from google.appengine.ext import ndb
from myuser import MyUser
from gpudata import GpuData
from viewgpu import ViewGpu
from datetime import datetime
from compare import Compare

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__) + "/templates"),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True
)


class Edit(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        
        user = users.get_current_user()
        gpu_query = GpuData.query()
        data = gpu_query.fetch()
        
        myuser_key = ndb.Key('MyUser', user.user_id())
        myuser = myuser_key.get()
        
        template_values = {
            'logout_url': users.create_logout_url(self.request.uri),
            'view': myuser.data,
            'data':data,
            'name':self.request.get('name'),
            'check':'Checked',
        }
        template = JINJA_ENVIRONMENT.get_template("edit.html")
        self.response.write(template.render(template_values))

    def post(self):
        self.response.headers['Content-Type'] = 'text/html'
        action = self.request.get('button')

        if action == 'Update GPU':
            devicename = self.request.get('devicename')
            manufacturer = self.request.get('manufacturer')
            dateissued = self.request.get('dateissued')
            if self.request.get('geometryShader'):
                    geometryShader = True
            else:
                geometryShader = False

            if self.request.get('tesselationShader'):
                tesselationShader = True
            else:
                tesselationShader = False

            if self.request.get('shaderInt16'):
                shaderInt16 = True
            else:
                shaderInt16 = False

            if self.request.get('sparseBinding'):
                sparseBinding = True
            else:
                sparseBinding = False

            if self.request.get('textureCompressionETC2'):
                textureCompressionETC2 = True
            else:
                textureCompressionETC2 = False

            if self.request.get('vertexPipelineStoresAndAtomics'):
                vertexPipelineStoresAndAtomics = True
            else:
                vertexPipelineStoresAndAtomics = False

            user = users.get_current_user()

            myuser_key = ndb.Key('MyUser', user.user_id())
            myuser = myuser_key.get()

            new_data = GpuData(id=devicename, devicename=devicename, manufacturer=manufacturer, dateissued=datetime.strptime(dateissued, '%Y-%m-%d'), geometryShader=geometryShader, tesselationShader=tesselationShader,
                                    shaderInt16=shaderInt16, sparseBinding=sparseBinding, textureCompressionETC2=textureCompressionETC2, vertexPipelineStoresAndAtomics=vertexPipelineStoresAndAtomics)
            new_data.put()

            self.redirect('/')

        elif action == 'Cancel':
            self.redirect('/')

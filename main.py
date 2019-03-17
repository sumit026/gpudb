import webapp2
import sys
import os
import jinja2
from google.appengine.api import users
from google.appengine.ext import ndb
from myuser import MyUser
from gpudata import GpuData
from viewgpu import ViewGpu
import logging
from edit import Edit
from view import View
from compare import Compare
from viewfeatures import ViewFeatures
from compareview import CompareView
from datetime import datetime

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__) + "/templates"),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True
)


class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        
        user = users.get_current_user()
        gpus_query = GpuData.query()
        gpus = gpus_query.fetch()
        if user is None:
            template_values = {
                'gpu_list': gpus,
                'login_url': users.create_login_url(self.request.uri),
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
            'data': myuser.data,
            'gpu_list': gpus,
        }
        template = JINJA_ENVIRONMENT.get_template("main.html")
        self.response.write(template.render(template_values))

    def post(self):
        self.response.headers['Content-Type'] = 'text/html'
        action = self.request.get('button')
        if action == 'Add GPU':

            gpu_exist = ndb.Key('GpuData', self.request.get('devicename'))
            my_gpu = gpu_exist.get()

            if my_gpu != None:
                template_values = {
                    'message': 'Already exist in the database. Please click to add new GPU information.',
                }
                template = JINJA_ENVIRONMENT.get_template("main.html")
                self.response.write(template.render(template_values))

            else:
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


app = webapp2.WSGIApplication([
('/', MainPage),
('/viewgpu', ViewGpu),
('/edit', Edit),
('/view', View),
('/compare', Compare),
('/viewfeatures', ViewFeatures),
('/compareview', CompareView),
], debug=True)

#if __name__ == '__main__':
#    app.run(debug=True)

from google.appengine.ext import ndb
from gpudata import GpuData


class MyUser(ndb.Model):
        username = ndb.StringProperty()
        data = ndb.StructuredProperty(GpuData, repeated=True)

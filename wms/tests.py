from django.test import TestCase
from django.test.client import RequestFactory
from wms import layers, maps, views
from django.contrib.gis.db import models

test_cartography =  [
        {
            'name': 'Category A',
            'color': '58 112 38',
            'symbol': 'hash'
        }]

class TestPolygon(models.Model):
    geom = models.PolygonField()
    objects = models.GeoManager()

class VectorLayer(layers.WmsVectorLayer):
    model = TestPolygon
    cartography = test_cartography

class MyMap(maps.WmsMap):
    layer_classes = [VectorLayer]

class MyWms(views.WmsView):
    map_class = MyMap

class TestPolygonView(TestCase):

    def setUp(self):
        self.view = MyWms.as_view()
        self.factory = RequestFactory()
        TestPolygon.objects.create(geom='POLYGON ((30 10, 40 40, 20 40, 10 20, 30 10))')

    def test_wms_service(self):
        request = self.factory.get('/wms/?REQUEST=GetMap&LAYERS=testpolygon&FORMAT=image%2Fpng&HEIGHT=400&WIDTH=400&SRS=EPSG%3A3086&BBOX=0,0,50,50&VERSION=1.1.1&styles=default')
        response = self.view(request)
        self.assertEqual(response.status_code, 200)

    def test_tms_service(self):
        request = self.factory.get('/tile/testpolygon/9/141/216.png')
        response = self.view(request)
        self.assertEqual(response.status_code, 200)

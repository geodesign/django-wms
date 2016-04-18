from django.contrib.gis.db import models


class TestPolygon(models.Model):
    geom = models.PolygonField()

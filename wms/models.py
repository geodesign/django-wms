from django.contrib.gis.db import models

# from activities.models import Activity
# from species.models import Species

# ###############################################################################
# class SpeciesStyle(models.Model):
#     """Style object for a species wms layer"""
#     species = models.OneToOneField(Species)
#     background_hex = models.CharField(default='#777777', max_length = 7)
#     outline_hex = models.CharField(default='#000000', max_length = 7)
#     outline_width = models.IntegerField(default=2, help_text="Width refers to the thickness of line work drawn, in pixels")
#     opacity = models.IntegerField(default=50, help_text="Layer opacity percentage in range [0, 100]")
#     hatch_angle = models.FloatField(blank=True, null=True, help_text="Angle, given in degrees, to draw the line work. Leave empty for no hash.")
#     def __unicode__(self):
#         return '{0} (Background {1})'.format(self.species.name, self.background_hex)


# ###############################################################################
# class ActivityStyle(models.Model):
#     """
#     Style object for an activity wms layer.

#     Note that new symbol choices have to be added to the wms/maps/symbolset.py
#     file, to be added to the wms basemap and be available to the activity layer.
#     """
#     SYMBOL_CHOICES = (
#         ('circle', 'circle'),
#         ('square', 'square'),
#         ('triangle', 'triangle'), 
#         ('cross', 'cross'),
#         ('diagonal', 'diagonal'))

#     activity = models.OneToOneField(Activity)
#     symbol = models.CharField(max_length = 10, choices=SYMBOL_CHOICES, default='cross')
#     color_hex = models.CharField(default='#000000', max_length = 7)
#     opacity = models.IntegerField(default=80, help_text="Layer opacity percentage in range [0, 100]")
#     size = models.IntegerField(default=10, help_text="Symbol size in pixels")
#     def __unicode__(self):
#         return '{0} (Symbol {1})'.format(self.activity.name, self.symbol)



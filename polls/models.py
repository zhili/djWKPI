from django.db import models
import datetime
# Create your models here.

# class Poll(models.Model):
#     question = models.CharField(max_length=200)
#     pub_date = models.DateTimeField('date published')
#     def __unicode__(self):
#         return self.question
#     def was_published_today(self):
#         return self.pub_date.date() == datetime.date.today()
#     was_published_today.short_description = 'Published today?'
# class Choice(models.Model):
#     poll = models.ForeignKey(Poll)
#     choice = models.CharField(max_length=200)
#     votes = models.IntegerField()
#     def __unicode__(self):
#         return self.choice
 
class Cell(models.Model):
    rnc_id = models.CharField(max_length=10)
    cell_name = models.CharField(max_length=30, unique=True)
    def __unicode__(self):
        return u"%s" % (self.cell_name)

class KPI(models.Model):
    
    date = models.DateField()
    ucell = models.ForeignKey(Cell)
    K01 = models.FloatField()
    K02 = models.FloatField()
    K03 = models.FloatField()
    K04 = models.FloatField()
    K05 = models.FloatField()
    K08_a = models.IntegerField()
    K08_b = models.IntegerField()
    K09_a = models.IntegerField()
    K09_b = models.IntegerField()
    K10_a = models.IntegerField()
    K10_b = models.IntegerField()
    K11_a = models.IntegerField()
    K11_b = models.IntegerField() 
    K12_a = models.IntegerField() 
    K12_b = models.IntegerField()
    K13_1a = models.IntegerField()
    K13_1b = models.IntegerField()
    K13_2a = models.IntegerField()
    K13_2b = models.IntegerField()
    K14_1a = models.IntegerField()
    K14_1b = models.IntegerField() 
    K15 = models.FloatField()
    K16_a = models.IntegerField() 
    K16_b = models.IntegerField() 
    K19_a = models.IntegerField() 
    K19_b = models.IntegerField()
    K20_a = models.IntegerField()
    K20_b = models.IntegerField()
    K21_a = models.IntegerField()
    K21_b = models.IntegerField()
    K22_ucell = models.FloatField()
    K24 = models.FloatField() 
    K25_a = models.IntegerField()
    K25_b = models.IntegerField() 
    K26_a = models.IntegerField()
    K26_b = models.IntegerField()
    K27 = models.FloatField() 
    K29 = models.FloatField()
    K30_a = models.IntegerField()
    K30_b = models.IntegerField()
    K31_a = models.IntegerField()
    K31_b = models.IntegerField()
    K33_ucell = models.FloatField()
    K34_ucell = models.FloatField() 
    K06 = models.FloatField()
    K28 = models.FloatField()
    K07 = models.FloatField()
    K23 = models.FloatField()
    K17_a = models.IntegerField() 
    K17_b = models.IntegerField()
    K18_a = models.IntegerField()
    K18_b = models.IntegerField()
    K32_a = models.IntegerField()
    K32_b = models.IntegerField()

    def __unicode__(self):
        return  u"%s" % self.date.strftime('%m/%d/%Y %H:%M:%S')

    class Meta:
        ordering = ('date',)
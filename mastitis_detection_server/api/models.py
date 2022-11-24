from django.db import models
from datetime import date
# Create your models here.

# animal
class Animal(models.Model):
    animal_number = models.CharField(max_length=200)
    animal_name = models.CharField(max_length=200, null=True, blank=True)
    date_of_birth = models.DateField()
    created = models.DateTimeField(auto_now_add=True)
    def __str__(self):
       birthdate = self.date_of_birth
       today = date.today()
       age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))
       animal_name = self.animal_name if self.animal_name else "No name"
       return "%s - %s: Age: %s year(s)" % (self.animal_number, animal_name, age)

# animal
class TempretureTest(models.Model):
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE)
    right_front_udder_quarter = models.FloatField()
    left_front_udder_quarter = models.FloatField()
    right_rear_udder_quarter = models.FloatField()
    left_rear_udder_quarter = models.FloatField()
    has_mastitis = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    def __str__(self):
       status = "NO MASTITIS" if self.has_mastitis else "HAS MASTITIS"
       return "%s - (%s)" % (self.animal, status)

# 
class MilkTest(models.Model):
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE)
    conductivity_lf = models.FloatField()
    conductivity_lr = models.FloatField()
    conductivity_rf = models.FloatField()
    conductivity_rr = models.FloatField()
    has_mastitis = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    def __str__(self):
       status = "NO MASTITIS" if self.has_mastitis else "HAS MASTITIS"
       return "%s - (%s)" % (self.animal, status)
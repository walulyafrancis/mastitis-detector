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
    created = models.DateTimeField(auto_now_add=True)
    def __str__(self):
       return "%s - (%s) - RFUQ: %s -LFUQ: %s - RRUQ: %s - LRUQ: %s" % (self.animal, str(self.created), str(self.right_front_udder_quarter), str(self.left_front_udder_quarter), str(self.right_rear_udder_quarter), str(self.left_rear_udder_quarter))


class TempretureResult(models.Model):
    test = models.ForeignKey(TempretureTest, on_delete=models.CASCADE)
    right_front_udder_quarter = models.IntegerField()
    left_front_udder_quarter = models.IntegerField()
    right_rear_udder_quarter = models.IntegerField()
    left_rear_udder_quarter = models.IntegerField()
    created = models.DateTimeField(auto_now_add=True)
    def __str__(self):
       return "%s - RFUQ: (%s) -LFUQ: (%s) - RRUQ: (%s) - LRUQ:(%s)" % (str(self.test), self.MastistResults(self.right_front_udder_quarter), self.MastistResults(self.left_front_udder_quarter), self.MastistResults(self.right_rear_udder_quarter), self.MastistResults(self.left_rear_udder_quarter))

    def MastistResults(self, prediction):
        if(prediction==2):
            return"clinical Mastitis Detected"
        elif (prediction==1):
            return "subclinical mastitis Detected"
        else:
           return "Healthy animal and no mastitis Detected"

##################3right_front_udder_quarter
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
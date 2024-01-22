from django.db import models

class Mode(models.Model):
    name = models.CharField(max_length=50)
    
    def __str__(self):
        return self.name
    
class State(models.Model):
    name = models.CharField(max_length=50)
    
    def __str__(self):
        return self.name
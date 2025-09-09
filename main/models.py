from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=200)  
    price = models.IntegerField()            
    description = models.TextField()        
    thumbnail = models.URLField()           
    category = models.CharField(max_length=100)  
    is_featured = models.BooleanField(default=False)  

    def _str_(self):
        return self.name
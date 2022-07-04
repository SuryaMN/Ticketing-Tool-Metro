from distutils.command.upload import upload
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
from django.db import models

class Ticket(models.Model):
    user = models.ForeignKey(User,null=True,related_name='tickets',on_delete=models.SET_NULL)
    issue_type = models.CharField(max_length=50)
    issue_sub_type = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='images/',blank=True)
    priority = models.CharField(max_length=6)
    created_datetime = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10,default="Pending")
    deleted = models.BooleanField(default=False)

    class Meta:
        db_table = "Tickets"

    def __str__(self):
        return (self.issue_type + " - " +self.user.username)

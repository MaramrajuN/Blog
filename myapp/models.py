from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class TimeStamp(models.Model):
	created_time=models.DateTimeField(auto_now_add=True)
	updated_time=models.DateTimeField(auto_now=True)
	user=models.ForeignKey(User,on_delete=models.CASCADE)

	class Meta:
		abstract= True


class Post(TimeStamp):
	title=models.CharField(max_length=100,verbose_name='Blog')
	description=models.TextField()
	image=models.ImageField(upload_to='')
	likes=models.IntegerField(default=0)

	def __str__(self):
		return self.title

class Comment(TimeStamp):
	post=models.ForeignKey(Post,on_delete=models.CASCADE)
	comment=models.TextField()

import datetime
from django.utils import timezone
from django.db import models

# Create your models here.
class Question(models.Model):
    # Attributes
    question_text = models.CharField(max_length=200)
    publication_date = models.DateTimeField("date published")

    def was_published_recently(self) -> bool:
        return self.publication_date >= timezone.now() - datetime.timedelta(days=3)

    # String representation
    def __str__(self) -> str:
        return self.question_text

class Choice(models.Model):
    # Attributes
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    # String representation
    def __str__(self) -> str:
        return self.choice_text
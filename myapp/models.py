
from django.db import models


class Question(models.Model):
    question = models.CharField(max_length=200)
    category = models.CharField(max_length=100)
    answer = models.TextField()
    practiced = models.BooleanField(default=False)

    def __str__(self):
        return self.question


class PracticeResult(models.Model):
    total_questions = models.IntegerField()
    correct_answers = models.IntegerField()
    score = models.IntegerField()
    percentage = models.FloatField()
    practiced_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Score: {self.score}/{self.total_questions}"


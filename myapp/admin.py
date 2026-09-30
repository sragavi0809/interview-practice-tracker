from django.contrib import admin
from .models import Question


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ("id", "question", "category", "practiced")
    list_filter = ("category", "practiced")
    search_fields = ("question", "category", "answer")

# Register your models here.

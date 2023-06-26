from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Todo(models.Model):
    Title = models.CharField(max_length=100, blank=True)
    Description = models.TextField(blank=True)
    Date = models.DateTimeField(auto_now_add=True)
    Completed = models.BooleanField(default=False)
    User = models.ForeignKey(User, on_delete=models.CASCADE)
    is_favorite = models.BooleanField(default=False)

    def __str__(self):
        return self.Title

    def save(self, *args, **kwargs):
        if not self.pk:  # Vérifie si l'instance est nouvelle (création)
            self.Title = self.Title.strip()  # Supprime les espaces vides au début et à la fin du titre
        super().save(*args, **kwargs)

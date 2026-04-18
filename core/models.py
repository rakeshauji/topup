from django.db import models

class Slide(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    button_text = models.CharField(max_length=50)
    button_link = models.CharField(max_length=200)
    background = models.ImageField(upload_to='slides/')

    def __str__(self):
        return self.title


class Game(models.Model):
    name = models.CharField(max_length=100)
    title = models.CharField(max_length=200, null=True, blank=True)
    link = models.URLField(null=True, blank=True)
    image = models.ImageField(upload_to='games/', null=True, blank=True)

    def __str__(self):
        return self.name


class Package(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    price = models.IntegerField()
    image = models.ImageField(upload_to='packages/', null=True, blank=True)

    def __str__(self):
        return f"{self.game.name} - {self.name}"


class SiteSettings(models.Model):
    logo = models.ImageField(upload_to='logo/')
    site_name = models.CharField(max_length=100, default="TopUp Center")

    def __str__(self):
        return self.site_name
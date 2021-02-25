from django.contrib.postgres.fields import JSONField
from django.db import models

AUDIO_TYPE = (("Song", "Song"),
              ("Podcast", "Podcast"),
              ("Audiobook", "Audiobook"))


# Create your Song as an Audio type.
class Audio(models.Model):
    name = models.CharField(max_length=100)
    audio_type = models.CharField(max_length=10, choices=AUDIO_TYPE, default='Song')
    duration = models.IntegerField()
    audio_file = JSONField(default=dict)
    upload_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name


# Extend Audio for Podcast as type of Audio
class Podcast(models.Model):
    audio = models.OneToOneField(Audio, on_delete=models.CASCADE, related_name='podcast')
    host = models.CharField(max_length=100)
    participants = JSONField(default=list)

    def __str__(self):
        return self.audio.name

    def __repr__(self):
        return self.audio.name


# Extend Audio for Audiobook as type of Audio
class Audiobook(models.Model):
    audio = models.OneToOneField(Audio, on_delete=models.CASCADE, related_name='audiobook')
    author_of_title = models.CharField(max_length=100)
    narrator = models.CharField(max_length=100)

    def __str__(self):
        return self.audio.name

    def __repr__(self):
        return self.audio.name


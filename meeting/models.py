from django.conf import settings
from django.db import models
from django.utils import timezone



class User(models.Model):
    name = models.CharField(max_length = 200 ,null=True, blank=True)
    age = models.IntegerField(null=True, blank=True)

    def get_json(self):
        result = {}
        result["id"] = self.id
        result["name"] = self.name
        result["age"] = self.age if self.age else None
        return result

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name


class Meeting(models.Model):
    name = models.TextField()
    meeting_date = models.DateTimeField(blank=True, null=True)

    def get_json(self):
        result = {}
        result["name"] = self.name
        result["meeting_date"] = get_epoch(self.meeting_date)
        return result

    def __unicode__(self):
        return (str(self.name))

    def __str__(self):
        return self.name


class Audio(models.Model):
    user = models.ForeignKey('User',on_delete=models.CASCADE,null=True, blank=True)
    meeting = models.ForeignKey('Meeting',on_delete=models.CASCADE,null=True, blank=True)
    audio_start = models.DateTimeField(blank=True, null=True)
    audio_end = models.DateTimeField(blank=True, null=True)

    def get_json(self):
        result = {}
        result["user"] = self.user.name
        result["audio_start"] = get_epoch(self.audio_start)
        result["audio_end"] = get_epoch(self.audio_end)
        return result


    def __unicode__(self):
        return (str(self.user.name))

    def __str__(self):
        return self.user.name



def get_epoch(dateof):
    if dateof:
        try:
            m_date = int(dateof.strftime('%s'))
            m_date = m_date
            return m_date
        except:
            return None
    else:
        return None
from django.conf import settings
from django.db import models
from django.utils import timezone



class Meeting(models.Model):
    name = models.TextField()
    meeting_date = models.DateTimeField(blank=True, null=True)

    def get_json(self):
        result = {}
        result["name"] = self.user
        result["meeting_date"] = get_epoch(self.meeting_date)
        return result

    def __unicode__(self):
        return (str(self.name))

    def __str__(self):
        return self.name


class Audio(models.Model):
    user = models.TextField()
    meeeting = models.ForeignKey('Meeting',on_delete=models.CASCADE,null=True, blank=True)
    audio_start = models.DateTimeField(blank=True, null=True)
    audio_end = models.DateTimeField(blank=True, null=True)

    def get_json(self):
        result = {}
        result["user"] = self.user
        result["audio_start"] = get_epoch(self.audio_start)
        result["audio_end"] = get_epoch(self.audio_end)
        return result


    def __unicode__(self):
        return (str(self.user))

    def __str__(self):
        return self.user





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
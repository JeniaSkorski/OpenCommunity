from communities.models import Community
from django.conf import settings
from django.db import models
from django.utils.formats import date_format, time_format
from issues.models import Issue
from django.utils.translation import ugettext_lazy as _


class AgendaItem(models.Model):
    meeting = models.ForeignKey('Meeting', verbose_name=_("Meeting"))
    issue = models.ForeignKey(Issue, verbose_name=_("Issue"))
    order = models.PositiveIntegerField(default=100, verbose_name=_("Order"))

    def __unicode__(self):
        return self.issue.title

    class Meta:
        unique_together = (("meeting", "issue"),)
        verbose_name = _("Agenda Item")
        verbose_name_plural = _("Agenda Items")


class Meeting(models.Model):
    community = models.ForeignKey(Community, related_name="meetings", verbose_name=_("Community"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created at"))
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="meetings_created", verbose_name=_("Created by"))

    held_at = models.DateTimeField(_("Held at"))

    scheduled_at = models.DateTimeField(_("Scheduled at"),
                                        null=True, blank=True)
    location = models.CharField(_("Location"), max_length=300, null=True, blank=True)
    comments = models.TextField(_("Comments"), null=True, blank=True)

    summary = models.TextField(_("Summary"), null=True, blank=True)

    agenda_items = models.ManyToManyField(Issue, through=AgendaItem, blank=True, verbose_name=_("Agenda items"))

    participants = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                          related_name="participated_in_meeting", verbose_name=_("Participants"))

    class Meta:
        verbose_name = _("Meeting")
        verbose_name_plural = _("Meetings")
        ordering = ("-held_at", )

    def __unicode__(self):
        return date_format(self.scheduled_at) + ", " + time_format(self.scheduled_at)

    @models.permalink
    def get_absolute_url(self):
        return ("meeting", (str(self.community.pk), str(self.pk),))


class MeetingExternalParticipant(models.Model):
    meeting = models.ForeignKey(Meeting, verbose_name=_("Meeting"))
    name = models.CharField(max_length=200, verbose_name=_("Name"))

    class Meta:
        verbose_name = _("Meeting External Participant")
        verbose_name_plural = _("Meeting External Participants")

    def __unicode__(self):
        return self.name

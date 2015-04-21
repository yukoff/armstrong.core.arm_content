from django.db import models
from django.contrib.sites.models import Site
from datetime import datetime
from model_utils.managers import InheritanceManager

PUB_STATUS_CHOICES = (
    ('D', 'Draft'),
    ('E', 'Edit'),
    ('P', 'Published'),
    ('T', 'Trash'),
)

PUB_STATUSES = dict((pair[1], pair[0]) for pair in PUB_STATUS_CHOICES)


class SimplePublicationMixin(models.Model):
    pub_date = models.DateTimeField(db_index=True)
    pub_status = models.CharField(('Publication status'), max_length=1,
        choices=PUB_STATUS_CHOICES, help_text=(
            'Only published items will appear on the site'))

    @property
    def is_published(self):
        return self.pub_date <= datetime.now() \
            and self.pub_status == "P"

    class Meta:
        abstract = True


class PublicationMixin(SimplePublicationMixin, models.Model):
    sites = models.ManyToManyField(Site)

    class Meta:
        abstract = True


class PublishedManager(InheritanceManager):
    """ Returns published objects where the pub_date has already passed """
    def get_query_set(self):
        return super(PublishedManager, self).get_query_set()\
                .filter(pub_date__lte=datetime.now())\
                .filter(pub_status="P")

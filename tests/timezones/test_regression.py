from django.utils.timezone import timedelta
from django.db import models
from django.db.models import F
from django.test import TestCase
from django.test import override_settings
from django.utils import timezone


@override_settings(TIME_ZONE='America/New_York', USE_TZ=True)
class ProveRegression(TestCase):
    def setUp(self):
        self.timestamp = ArbitraryTimestamp()

    def test_F_expression_fails(self):
        now = timezone.now()
        self.timestamp.updated = now - timedelta(hours=2)
        self.timestamp.save()
        self.timestamp.refresh_from_db()
        self.assertEqual(now - timedelta(hours=2), self.timestamp.updated)
        users_timestamps = ArbitraryTimestamp.objects.all()
        users_timestamps.update(updated=F('updated') + timedelta(hours=2))
        self.timestamp.refresh_from_db()
        self.assertAlmostEqual(self.timestamp.updated, now, delta=timedelta(seconds=1))


class ArbitraryTimestamp(models.Model):
    updated = models.DateTimeField(null=True, blank=True)

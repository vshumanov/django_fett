from datetime import datetime

from django.db import models


class DownloadedFile(models.Model):
    filename = models.CharField(max_length=150)
    # TODO: think about timezone.
    date = models.DateTimeField(default=datetime.now)

    class Meta:
        ordering = ["-date"]
        db_table = "downloaded_files"

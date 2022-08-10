from django.db import models
import uuid
from django.utils.translation import gettext_lazy as _
from users.models import Profile


class Project(models.Model):
    owner = models.ForeignKey(Profile, null=True, blank=True, on_delete=models.CASCADE)
    title = models.CharField(verbose_name=_("title"), max_length=200)
    description = models.TextField(verbose_name=_("description"), null=True, blank=True)
    featured_image = models.ImageField(
        null=True,
        blank=True,
        upload_to="projects/",
        default="projects/default.jpg",
    )
    demo_link = models.CharField(
        verbose_name=_("demo link"), max_length=2000, null=True, blank=True
    )
    source_link = models.CharField(
        verbose_name=_("source link"), max_length=2000, null=True, blank=True
    )
    tags = models.ManyToManyField("Tag", blank=True)
    vote_total = models.IntegerField(
        verbose_name=_("vote total"), default=0, null=True, blank=True
    )
    vote_ratio = models.IntegerField(
        verbose_name=_("vote ratio"), default=0, null=True, blank=True
    )
    created = models.DateTimeField(verbose_name=_("created at"), auto_now_add=True)
    id = models.UUIDField(
        verbose_name=_("id"),
        default=uuid.uuid4,
        unique=True,
        primary_key=True,
        editable=False,
    )

    class Meta:
        verbose_name = "project"
        verbose_name_plural = "projects"
        ordering = ["-vote_ratio", "-vote_total", "-title"]

    def __str__(self):
        return self.title

    @property
    def imageURL(self):
        try:
            url = self.featured_image.url
        except:
            url = ""
        return url

    @property
    def reviewers(self):
        queryset = self.review_set.all().values_list("owner__id", flat=True)
        return queryset

    @property
    def get_vote_count(self):
        reviews = self.review_set.all()
        up_votes = reviews.filter(value="up").count()
        total_votes = reviews.count()

        ratio = (up_votes / total_votes) * 100
        self.vote_total = total_votes
        self.vote_ratio = ratio
        self.save()


class Review(models.Model):
    VOTE_TYPE = (
        ("up", "Up Vote"),
        ("down", "Down Vote"),
    )
    owner = models.ForeignKey(Profile, null=True, blank=True, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    body = models.TextField(verbose_name=_("body"), null=True, blank=True)
    value = models.CharField(verbose_name=_("value"), max_length=200, choices=VOTE_TYPE)
    created = models.DateTimeField(verbose_name=_("created at"), auto_now_add=True)
    id = models.UUIDField(
        verbose_name=_("id"),
        default=uuid.uuid4,
        unique=True,
        primary_key=True,
        editable=False,
    )

    class Meta:
        unique_together = [["owner", "project"]]

    def __str__(self):
        return self.value


class Tag(models.Model):
    name = models.CharField(verbose_name=_("name"), max_length=200)
    created = models.DateTimeField(verbose_name=_("created at"), auto_now_add=True)
    id = models.UUIDField(
        verbose_name=_("id"),
        default=uuid.uuid4,
        unique=True,
        primary_key=True,
        editable=False,
    )

    def __str__(self):
        return self.name

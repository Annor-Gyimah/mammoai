from django.db import models
from userauths.models import User, Profile
from shortuuid.django_fields import ShortUUIDField
import shortuuid
from django.utils.text import slugify
from django.utils.html import mark_safe



class Team(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    fullname = models.CharField(max_length=100, null=True, blank=True)
    #image = models.ImageField(upload_to="our_team")  # Use ImageField for image files
    #description = models.CharField(max_length=100)
    facebook = models.URLField(null=True, blank=True)
    linkedin = models.URLField(null=True, blank=True)
    slug = models.SlugField(unique=True, blank=True)  # Allow blank for slug field

    def __str__(self):
        return str(self.user)  # Ensure this returns a string, not a User object

    def save(self, *args, **kwargs):
        if not self.slug:  # Check if slug is empty or None
            uuid_key = shortuuid.uuid()
            uniqueid = uuid_key[:4]
            self.slug = slugify(self.description[:30]) + '-' + uniqueid.lower()  # Use description for slug
        super(Team, self).save(*args, **kwargs)

    # def thumbnail(self):
    #     if self.image:  # Check if image exists
    #         return mark_safe(f"<img src='{self.image.url}' width='50' height='50' style='object-fit: cover; border-radius: 6px;' />")
    #     return ''  # Return empty string if no image

    class Meta:
        verbose_name = "Team Member"
        verbose_name_plural = "Team Members"
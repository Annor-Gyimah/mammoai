from django.db import models
from userauths.models import User




NOTIFICATION_TYPE = (
    ("User Registered", "User Registered"),
    
)

# Create your models here.
class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    # booking = models.ForeignKey(Booking, on_delete=models.SET_NULL, blank=True, null=True)
    type = models.CharField(max_length=180, choices=NOTIFICATION_TYPE)
    seen = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.user.username}" 
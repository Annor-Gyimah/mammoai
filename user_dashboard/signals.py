import os
import shutil
from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver
from .models import Patient



@receiver(pre_save, sender=Patient)
def delete_old_files(sender, instance, **kwargs):
    if not instance.pk:
        return False
    try:
        old_instance = Patient.objects.get(pk=instance.pk)
    except Patient.DoesNotExist:
        return False
    
    for field in ['mammogram_image', 'risk_assessment_form']:
        old_file = getattr(old_instance, field)
        new_file = getattr(instance, field)
        if old_file and old_file != new_file:
            if os.path.isfile(old_file.path):
                os.remove(old_file.path)


@receiver(post_delete, sender=Patient)
def delete_patient_directory(sender, instance, **kwargs):

    user_dir = f'user_{instance.user.id}/patient_{instance.firstname}'
    user_directory_path = os.path.join('media', user_dir)
    if os.path.isdir(user_directory_path):
        shutil.rmtree(user_directory_path)

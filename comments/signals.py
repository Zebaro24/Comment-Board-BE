import logging
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Comment

logger = logging.getLogger(__name__)

@receiver(post_save, sender=Comment)
def comment_created_event(sender, instance, created, **kwargs):
    if created:
        logger.info(f"[Event] New comment created: {instance.id} by {instance.username}")
# myapp/models.py
import threading
import time
from django.db import models, transaction
from django.db.models.signals import post_save
from django.dispatch import receiver

# Define a sample model
class MyModel(models.Model):
    name = models.CharField(max_length=100)

# Define a signal handler with a delay
# @receiver(post_save, sender=MyModel)
# def my_signal_handler1(sender, instance, **kwargs):
#     print("Signal handler started.")
#     time.sleep(5)  # Simulate a delay to show synchronous behavior
#     print("Signal handler finished.")

# @receiver(post_save, sender=MyModel)
# def my_signal_handler2(sender, instance, **kwargs):
#     print("Signal handler thread ID:", threading.get_ident())

# @receiver(post_save, sender=MyModel)
# def my_signal_handler3(sender, instance, created, **kwargs):
#     print("Signal handler started.")
#     # Simulate an error to test transaction rollback
#     raise Exception("Simulating an error to test transaction rollback")
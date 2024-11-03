# Django Signals Example

This project demonstrates key behaviors of Django's `post_save` signals by answering three questions:

1. Are Django signals executed synchronously or asynchronously?
2. Do Django signals run in the same thread as the caller?
3. Do Django signals run in the same database transaction as the caller?

Each question is addressed by a specific signal handler. By uncommenting each handler one at a time and running the provided code in the Django shell, you can observe and confirm Django's default signal behavior.

## Model Definition

A simple model, `MyModel`, is defined in `myapp/models.py` with a single field, `name`. 

### Signal Handlers

There are three signal handlers in the code, each serving a specific purpose:

1. **Synchronous Execution** (`my_signal_handler1`): Demonstrates that signals are executed synchronously.
2. **Thread Context** (`my_signal_handler2`): Demonstrates that signals run in the same thread as the caller.
3. **Transaction Management** (`my_signal_handler3`): Demonstrates that signals run in the same database transaction as the caller.

Uncomment only one handler at a time to test its functionality in isolation.

## Testing Instructions

### 1. Synchronous Execution

To confirm that Django signals are executed synchronously, uncomment `my_signal_handler1` in `myapp/models.py`:

```python
@receiver(post_save, sender=MyModel)
def my_signal_handler1(sender, instance, **kwargs):
    print("Signal handler started.")
    time.sleep(5)  # Simulate a delay to show synchronous behavior
    print("Signal handler finished.")
```
Then, in the Django shell, run:
```python
from myapp.models import MyModel

print("Creating instance...")
instance = MyModel(name="Test")
instance.save()  # This will trigger my_signal_handler1
print("Instance created.")
```
Expected Output:
```python
Creating instance...
Signal handler started.
(5-second delay)
Signal handler finished.
Instance created.
```
This delay confirms that the signal is handled synchronously, as `Instance created`. only prints after the signal handler completes.
### 2. Thread Context

To confirm that Django signals run in the same thread as the caller, uncomment `my_signal_handler2`:
```python
@receiver(post_save, sender=MyModel)
def my_signal_handler2(sender, instance, **kwargs):
    print("Signal handler thread ID:", threading.get_ident())
```
In the Django shell, run:
```python
from myapp.models import MyModel
import threading

print("Caller thread ID:", threading.get_ident())
instance = MyModel(name="Test")
instance.save()  # This will trigger my_signal_handler2
```
Expected Output:
```python
Caller thread ID: <thread_id>
Signal handler thread ID: <same_thread_id>
```
The thread IDs should match, confirming that the signal runs in the same thread as the calling code.
### 3. Transaction Management

To confirm that signals run in the same database transaction as the caller, uncomment `my_signal_handler3`:
```python
@receiver(post_save, sender=MyModel)
def my_signal_handler3(sender, instance, created, **kwargs):
    print("Signal handler started.")
    # Simulate an error to test transaction rollback
    raise Exception("Simulating an error to test transaction rollback")
```
In the Django shell, run:
```python
from myapp.models import MyModel
from django.db import transaction

try:
    with transaction.atomic():
        print("Creating instance...")
        instance = MyModel(name="Test")
        instance.save()  # This will trigger my_signal_handler3
except Exception as e:
    print(f"Transaction rolled back due to error: {e}")

# Check if the instance was saved
if MyModel.objects.filter(name="Test").exists():
    print("Instance was saved despite the error.")
else:
    print("Instance was not saved due to rollback.")
```
Expected Output:
```python
Creating instance...
Signal handler started.
Transaction rolled back due to error: Simulating an error to test transaction rollback
Instance was not saved due to rollback.
```
Since the instance does not persist in the database, this shows that the signal handler runs within the same transaction as the caller.
### Summary

1. **Synchronous Execution**: Signals are executed synchronously by default.
2. **Thread Context**: Signals run in the same thread as the caller.
3. **Transaction Management** : Signals share the same transaction context as the caller.



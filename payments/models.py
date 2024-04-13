from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.utils.translation import gettext as _

class User(AbstractUser):
    USER_TYPES = (
        ('merchant', 'Merchant'),
        ('customer', 'Customer'),
    )
    type = models.CharField(max_length=10, choices=USER_TYPES)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = 'users'
    groups = models.ManyToManyField(
        Group,
        verbose_name=_('groups'),
        blank=True,
        related_name='payment_users_groups'
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=_('user permissions'),
        blank=True,
        related_name='payment_users_permissions'
    )

class Transaction(models.Model):
    from_user = models.ForeignKey(User, related_name='sent_transactions', on_delete=models.CASCADE)
    to_user = models.ForeignKey(User, related_name='received_transactions', on_delete=models.CASCADE)
    order = models.ForeignKey('Order', related_name='transactions', null=True, blank=True, on_delete=models.SET_NULL)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    STATUS_CHOICES = (
        ('Completed', 'Completed'),
        ('Initiated', 'Initiated'),
        ('Failed', 'Failed'),
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    timestamp = models.DateTimeField(auto_now_add=True)
    payment_method = models.CharField(max_length=50)

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    STATUS_CHOICES = (
        ('Created', 'Created'),
        ('Fulfilled', 'Fulfilled'),
        ('Cancelled', 'Cancelled'),
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    timestamp = models.DateTimeField(auto_now_add=True)
    description = models.TextField()

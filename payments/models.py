from django.db import models

class Member(models.Model):
    USER_TYPES = (
        ('merchant', 'Merchant'),
        ('customer', 'Customer'),
    )
    type = models.CharField(max_length=10, choices=USER_TYPES)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = 'members'

class Transaction(models.Model):
    from_member = models.ForeignKey(Member, related_name='sent_transactions', on_delete=models.CASCADE)
    to_member = models.ForeignKey(Member, related_name='received_transactions', on_delete=models.CASCADE)
    order = models.ForeignKey('Order', related_name='transactions', null=True, blank=True, on_delete=models.SET_NULL)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    STATUS_CHOICES = (
        ('Completed', 'Completed'),
        ('Initiated', 'Initiated'),
        ('Failed', 'Failed'),
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    timestamp = models.DateTimeField(auto_now_add=True)
    payment_method = models.CharField(max_length=50, null=True)
    class Meta:
        db_table = 'transactions'

class Order(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    STATUS_CHOICES = (
        ('Created', 'Created'),
        ('Fulfilled', 'Fulfilled'),
        ('Cancelled', 'Cancelled'),
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    timestamp = models.DateTimeField(auto_now_add=True)
    description = models.TextField()
    class Meta:
        db_table = 'orders'

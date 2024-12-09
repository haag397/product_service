from django.db import models
from uuid import uuid4
from user.models import User


class Product(models.Model):
    id = models.UUIDField(default=uuid4, unique=True, primary_key=True, editable=False)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    # image = models.ImageField(upload_to='products/', blank=True, null=True)
    image = models.ImageField(upload_to='products/') 
    def __str__(self):
        return self.name

class Invoice(models.Model):
    id = models.UUIDField(default=uuid4, unique=True, primary_key=True, editable=False)
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='invoices')
    products = models.ManyToManyField('Product', through='InvoiceProduct')
    created_at = models.DateTimeField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f"Invoice {self.id} for {self.user.email}"

# Through model for Invoice and Product relationship
# class InvoiceProduct(models.Model):

#     invoice = models.ForeignKey('Invoice', on_delete=models.CASCADE)
#     product = models.ForeignKey('Product', on_delete=models.CASCADE)
#     quantity = models.PositiveIntegerField(default=1)
    
    
class Transaction(models.Model):
    id = models.UUIDField(default=uuid4, unique=True, primary_key=True, editable=False)
    user = models.ForeignKey(User, related_name='transactions', on_delete=models.CASCADE)
    invoice = models.ForeignKey(Invoice, related_name='transactions', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, choices=[
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ])

    def __str__(self):
        return f"Transaction {self.id} for Invoice #{self.invoice.id}"
    
    # def __str__(self):
        # return f"Transaction {self.transaction_id} - {self.status}"
from rest_framework import serializers
from .models import Product, Invoice, Transaction, User

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'image']

class InvoiceSerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True)

    class Meta:
        model = Invoice
        fields = ['id', 'user', 'created_at', 'total_amount', 'products']

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['id', 'user', 'invoice', 'amount', 'transaction_date', 'status']

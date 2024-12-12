from rest_framework import serializers
from .models import Product, Invoice, Transaction, User

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'image']

class InvoiceSerializer(serializers.ModelSerializer):
    products = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Product.objects.all()
    )
    class Meta:
        model = Invoice
        fields = ['id','created_at', 'total_amount', 'products']


class TransactionSerializer(serializers.ModelSerializer):

    invoice = serializers.PrimaryKeyRelatedField(queryset=Invoice.objects.all())

    class Meta:
        model = Transaction
        fields = ['id', 'invoice', 'amount', 'transaction_date', 'status']
    
    def create(self, validated_data):
        # Automatically set the user based on the request
        user = self.context['request'].user
        return Transaction.objects.create(user=user, **validated_data)
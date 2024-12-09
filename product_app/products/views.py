from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import Product, Invoice, Transaction
from .serializers import ProductSerializer, InvoiceSerializer, TransactionSerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    authentication_classes = [JWTAuthentication] 

class InvoiceViewSet(viewsets.ModelViewSet):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer
    authentication_classes = [JWTAuthentication] 

    def get_queryset(self):
        # * only shows invoices and products belonging to the user
        return Invoice.objects.filter(user=self.request.user)

class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    authentication_classes = [JWTAuthentication] 
    
    def perform_create(self, serializer):
        invoice_id = self.request.data.get('invoice')
        invoice = Invoice.objects.get(id=invoice_id)
        serializer.save(user=self.request.user, invoice=invoice)
        
    def get_queryset(self):
        # * only shows transactions of user
        return Transaction.objects.filter(user=self.request.user)

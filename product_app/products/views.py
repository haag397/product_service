from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import Product, Invoice, Transaction
from .serializers import ProductSerializer, InvoiceSerializer, TransactionSerializer

class ProductViewSet(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication] 
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class InvoiceViewSet(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication] 
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer

    def get_queryset(self):
        # * only shows invoices and products belonging to the user
        # return Invoice.objects.filter(user=self.request.user)
        return self.queryset.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        
class TransactionViewSet(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication] 
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    
    # def perform_create(self, serializer):
    #     invoice_id = self.request.data.get('invoice')
    #     invoice = Invoice.objects.get(id=invoice_id)
    #     serializer.save(user=self.request.user, invoice=invoice)
        
    # def get_queryset(self):
    #     # * only shows transactions of user
    #     return Transaction.objects.filter(user=self.request.user)
    def get_queryset(self):
        return self.queryset.filter(invoice__user=self.request.user)
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import Product, Invoice, Transaction
from .serializers import ProductSerializer, InvoiceSerializer, TransactionSerializer
from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsAdminOrReadOnly(BasePermission):
    """
    Custom permission to allow only admin users to create, update, or delete.
    Regular users can only view.
    """
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return request.user and request.user.is_superuser
    
class ProductViewSet(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication] 
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class InvoiceViewSet(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication] 
    permission_classes = [IsAuthenticated]
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer

    def get_queryset(self):
        # * only shows invoices and products belonging to the user
        return self.queryset.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        
class TransactionViewSet(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication] 
    permission_classes = [IsAuthenticated]
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    
    def get_queryset(self):
        return self.queryset.filter(invoice__user=self.request.user)
    
    def get_serializer_context(self):
        # Pass the request context to the serializer
        return {'request': self.request}
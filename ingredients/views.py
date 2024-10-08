from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import IngredientItem
from .serializers import IngredientItemSerializer
from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView
from django.utils import timezone
from drf_yasg import openapi

# 1. Add a new ingredient item
class AddIngredientItemView(generics.CreateAPIView):
    serializer_class = IngredientItemSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Add a new ingredient item with name, date_of_manufacture, date_of_expiration, and category fields."
    )
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user) 
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 2. Edit an existing ingredient item
class EditIngredientItemView(generics.UpdateAPIView):
    serializer_class = IngredientItemSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Edit an existing ingredient item using its ID."
    )
    def put(self, request, pk):
        try:
            item = IngredientItem.objects.get(pk=pk, user=request.user)  # Filter by user
        except IngredientItem.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ViewAllIngredientItemsView(generics.ListAPIView):
    serializer_class = IngredientItemSerializer
    permission_classes = [IsAuthenticated]

    # Define the 'category' parameter for Swagger documentation
    category_param = openapi.Parameter(
        name='category', 
        in_=openapi.IN_QUERY, 
        description="Filter ingredient items by category (use 'expired' to view all expired items)",
        type=openapi.TYPE_STRING
    )

    @swagger_auto_schema(
        manual_parameters=[category_param],
        operation_description="Retrieve a list of all ingredient items for the authenticated user. Use 'expired' as category to see all expired items."
    )
    def get_queryset(self):
        category = self.request.query_params.get('category')
        
        if category == 'expired':
            return IngredientItem.objects.filter(
                user=self.request.user,
                date_of_expiration__lt=timezone.now()
            )
        elif category:
            return IngredientItem.objects.filter(
                user=self.request.user,
                category=category
            )
        # Default to returning all items for the authenticated user
        return IngredientItem.objects.filter(user=self.request.user)
    
# 4. Delete a single ingredient item
class DeleteIngredientItemView(generics.DestroyAPIView):
    serializer_class = IngredientItemSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Delete an ingredient item by ID."
    )
    def delete(self, request, pk):
        try:
            item = IngredientItem.objects.get(pk=pk, user=request.user)  # Filter by user
        except IngredientItem.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# 5. Delete all ingredient items for the authenticated user
class DeleteAllIngredientItemsView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Delete all ingredient items for the authenticated user."
    )
    def delete(self, request):
        IngredientItem.objects.filter(user=request.user).delete()  # Filter by user
        return Response(status=status.HTTP_204_NO_CONTENT)

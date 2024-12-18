from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import GroceryItem
from .serializers import GroceryItemSerializer
from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView
from django.db.models import F



# 1. Add a new grocery item
class AddGroceryItemView(generics.CreateAPIView):
    serializer_class = GroceryItemSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Add a new grocery item with name and quantity fields."
    )
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user) 
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 2. Edit an existing grocery item
class EditGroceryItemView(generics.UpdateAPIView):
    serializer_class = GroceryItemSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Edit an existing grocery item using its ID."
    )
    def put(self, request, pk):
        try:
            item = GroceryItem.objects.get(pk=pk, user=request.user)  # Filter by user
        except GroceryItem.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 3. View all grocery items for the authenticated user
class ViewAllGroceryItemsView(generics.ListAPIView):
    serializer_class = GroceryItemSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Retrieve a list of all grocery items for the authenticated user."
    )
    def get_queryset(self):
        return GroceryItem.objects.filter(user=self.request.user) 


# 4. Delete a single grocery item
class DeleteGroceryItemView(generics.DestroyAPIView):
    serializer_class = GroceryItemSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Delete a grocery item by ID."
    )
    def delete(self, request, pk):
        try:
            item = GroceryItem.objects.get(pk=pk, user=request.user)  # Filter by user
        except GroceryItem.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# 5. Delete all grocery items for the authenticated user
class DeleteAllGroceryItemsView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Delete all grocery items for the authenticated user."
    )
    def delete(self, request):
        GroceryItem.objects.filter(user=request.user).delete()  # Filter by user
        return Response(status=status.HTTP_204_NO_CONTENT)

class AddMultipleGroceryItemsView(APIView):
    serializer_class = GroceryItemSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Add multiple grocery items at once. If items with the same name are provided, they will be consolidated by summing their quantities.",
        request_body=GroceryItemSerializer(many=True)
    )
    def post(self, request):
        serializer = self.serializer_class(data=request.data, many=True)
        if serializer.is_valid():
            for item_data in serializer.validated_data:
                item_name = item_data["name"]
                item_quantity = int(item_data.get("quantity", 1))

                grocery_item = GroceryItem.objects.filter(user=request.user, name=item_name).first()

                if grocery_item:
                    grocery_item.quantity = F('quantity') + item_quantity
                    grocery_item.save()
                else:
                    GroceryItem.objects.create(user=request.user, **item_data)

            return Response(serializer.validated_data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
# food_app/views.py

from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Cuisine, Food
from .serializers import CuisineSerializer, FoodSerializer, CreateFoodSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.views import APIView


# 1. Fetch list of cuisines
class FetchCuisinesView(generics.ListAPIView):
    serializer_class = CuisineSerializer

    @swagger_auto_schema(
        operation_description="Retrieve a list of all cuisines."
    )
    def get_queryset(self):
        return Cuisine.objects.all()


# 2. Fetch list of food
class FetchFoodView(generics.ListAPIView):
    serializer_class = FoodSerializer

    @swagger_auto_schema(
        operation_description="Retrieve a list of all food items."
    )
    def get_queryset(self):
        return Food.objects.all()

class AddPreferredCuisinesView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Add preferred cuisines for the logged-in user.",
        request_body=openapi.Schema(
            type=openapi.TYPE_ARRAY,
            items=openapi.Items(type=openapi.TYPE_INTEGER),
            description="List of cuisine IDs to add to the user's preferences."
        )
    )
    def post(self, request):
        user = request.user

        # Handle request.data as a list or dictionary
        if isinstance(request.data, list):
            cuisine_ids = request.data
        elif isinstance(request.data, dict):
            cuisine_ids = request.data.get('cuisines', [])
        else:
            return Response(
                {"error": "Invalid data format. Expected a list or a dictionary."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            cuisines = Cuisine.objects.filter(id__in=cuisine_ids)
            user.preferred_cuisines.add(*cuisines)
            return Response({"message": "Preferred cuisines updated successfully."}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)



class AddPreferredFoodView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Add preferred food items for the logged-in user.",
        request_body=openapi.Schema(
            type=openapi.TYPE_ARRAY,
            items=openapi.Items(type=openapi.TYPE_INTEGER),
            description="List of food IDs to add to the user's preferences."
        )
    )
    def post(self, request):
        user = request.user

        # Handle request.data as a list or dictionary
        if isinstance(request.data, list):
            food_ids = request.data
        elif isinstance(request.data, dict):
            food_ids = request.data.get('food', [])
        else:
            return Response(
                {"error": "Invalid data format. Expected a list or a dictionary."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            food_items = Food.objects.filter(id__in=food_ids)
            user.preferred_food.add(*food_items)
            return Response({"message": "Preferred food updated successfully."}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class RetrievePreferredCuisinesView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CuisineSerializer

    @swagger_auto_schema(
        operation_description="Retrieve the preferred cuisines for the authenticated user."
    )
    def get_queryset(self):
        user = self.request.user
        return user.preferred_cuisines.all()

class RetrievePreferredFoodView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = FoodSerializer

    @swagger_auto_schema(
        operation_description="Retrieve the preferred food items for the authenticated user."
    )
    def get_queryset(self):
        user = self.request.user
        return user.preferred_food.all()

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from .models import MealPlan
from .serializers import MealPlanSerializer, MealPlanCreateSerializer
from django.db.models import Case, When, Value, IntegerField

class MealPlanView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == "POST":
            return MealPlanCreateSerializer
        return MealPlanSerializer

    @swagger_auto_schema(
        operation_description="Add a recipe to the meal plan. Provide date, meal_type, and recipe ID.",
        request_body=MealPlanCreateSerializer
    )
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            date = serializer.validated_data['date']
            meal_type = serializer.validated_data['meal_type']
            existing_meal_plan = MealPlan.objects.filter(date=date, meal_type=meal_type).first()
            if existing_meal_plan:
                existing_meal_plan.delete() 

            serializer.save()  
            return Response({"message": "Meal plan added successfully."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

    def get(self, request):
        date = request.query_params.get('date')
        if not date:
            return Response({"error": "Date is required."}, status=status.HTTP_400_BAD_REQUEST)
        
        # Fetch meal plans for the given date and order by meal_type
        meal_plans = MealPlan.objects.filter(date=date).order_by(
            Case(
                When(meal_type='breakfast', then=Value(1)),
                When(meal_type='lunch', then=Value(2)),
                When(meal_type='dinner', then=Value(3)),
                default=Value(4), # in case there's an unexpected value for meal_type
                output_field=IntegerField()
            )
        )
        
        # Serialize the data
        serializer = self.get_serializer(meal_plans, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description="Delete a meal plan by ID. Provide the 'id' query parameter."
    )
    def delete(self, request):
        meal_plan_id = request.query_params.get('id')
        try:
            meal_plan = MealPlan.objects.get(id=meal_plan_id)
            meal_plan.delete()
            return Response({"message": "Meal plan deleted successfully."})
        except MealPlan.DoesNotExist:
            return Response({"error": "Meal plan not found."}, status=status.HTTP_404_NOT_FOUND)


class BulkMealPlanView(generics.GenericAPIView):
    serializer_class = MealPlanCreateSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Add multiple recipes to the meal plan. Send a list of meal plans with date, meal_type, and recipe ID.",
        request_body=MealPlanCreateSerializer(many=True)
    )
    def post(self, request):
        data = request.data
        if not isinstance(data, list):
            return Response({"error": "Data must be a list of meal plans."}, status=status.HTTP_400_BAD_REQUEST)
        
        for meal_plan_data in data:
            serializer = self.get_serializer(data=meal_plan_data)
            if serializer.is_valid():
                date = serializer.validated_data['date']
                meal_type = serializer.validated_data['meal_type']
                existing_meal_plan = MealPlan.objects.filter(date=date, meal_type=meal_type).first()
                if existing_meal_plan:
                    existing_meal_plan.delete()  
                
                serializer.save()  
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({"message": "Meal plans added successfully."}, status=status.HTTP_201_CREATED)

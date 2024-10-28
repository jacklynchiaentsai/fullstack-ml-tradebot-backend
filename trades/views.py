from rest_framework import status, views
from rest_framework.response import Response
from .models import Simulation
from .serializers import SimulationSerializer

class RunTradeBotView(views.APIView):
    def post(self, request):
        serializer = SimulationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Simulation data stored successfully!'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

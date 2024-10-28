from rest_framework import status, views, generics
from rest_framework.response import Response
from .models import Simulation
from .serializers import SimulationSerializer
import subprocess
import os
from datetime import datetime
from django.core.exceptions import ObjectDoesNotExist
import re

class RunTradeBotView(views.APIView):
    def post(self, request):
        serializer = SimulationSerializer(data=request.data)

        if serializer.is_valid():
            symbol = serializer.validated_data['symbol']
            start_date = serializer.validated_data['start_date']
            end_date = serializer.validated_data['end_date']

            # Convert dates to strings for the command
            start_date_str = start_date.strftime('%Y-%m-%d')
            end_date_str = end_date.strftime('%Y-%m-%d')

            # date and time for when the tradingbot.py script is run
            date_str = datetime.now().strftime('%Y-%m-%d')
            time_str = datetime.now().strftime('%H-%M')
            html_time = f"{date_str}_{time_str}"

            # Define the command to run tradingbot.py with arguments
            command = [
                'python3', 
                'trades/trading-bot/tradingbot.py', 
                symbol, 
                start_date_str, 
                end_date_str
            ]

            try:
                # Run the trading bot script using subprocess
                result = subprocess.run(command, capture_output=True, text=True)

                # Check if the script ran successfully
                if result.returncode == 0:
                    print("Trading Bot Output:", result.stdout)

                    # Save simulation data to the database
                    simulation = serializer.save(
                        html_time=html_time
                    )

                    return Response(
                        {'message': 'Simulation data stored successfully!'},
                        status=status.HTTP_201_CREATED
                    )
                else:
                    # Log any error output from the script
                    print("Trading Bot Error:", result.stderr)
                    return Response(
                        {'message': 'Error running trading bot', 'details': result.stderr},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR
                    )

            except Exception as e:
                # Handle exceptions during subprocess execution
                print(f"Exception occurred: {e}")
                return Response(
                    {'message': 'Failed to run trading bot', 'error': str(e)},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

        # Log validation errors if data is invalid
        print("Validation errors:", serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SimulationListView(generics.ListAPIView):
    queryset = Simulation.objects.all()
    serializer_class = SimulationSerializer

class GetSimulationDataView(views.APIView):
    def post(self, request):
        symbol = request.data.get('symbol')
        start_date = request.data.get('start_date')
        end_date = request.data.get('end_date')

        try:
            # Find the simulation with matching symbol, start_date, and end_date
            simulation = Simulation.objects.get(
                symbol=symbol,
                start_date=start_date,
                end_date=end_date
            )

            html_time = simulation.html_time
            logs_directory = '../backend/logs'
            tearsheet_file = None
            trades_file = None

            # Regular expressions for matching files
            tearsheet_pattern = re.compile(rf"MLTrader_{html_time}.*tearsheet\.html")
            trades_pattern = re.compile(rf"MLTrader_{html_time}.*trades\.html")

            # Search for matching files in the logs directory
            for file_name in os.listdir(logs_directory):
                if tearsheet_pattern.match(file_name):
                    tearsheet_file = file_name
                elif trades_pattern.match(file_name):
                    trades_file = file_name

            # Print the found file names
            print(f"Tearsheet File: {tearsheet_file}")
            print(f"Trades File: {trades_file}")

            # Create URLs for the files if they exist
            tearsheet_url = f'/static/{tearsheet_file}' if tearsheet_file else None
            trades_url = f'/static/{trades_file}' if trades_file else None

            return Response({
                'tearsheet_url': tearsheet_url,
                'trades_url': trades_url
            }, status=status.HTTP_200_OK)

        except ObjectDoesNotExist:
            # Return an error if no matching simulation is found
            return Response({'error': 'Simulation not found'}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            # Handle any other exceptions
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
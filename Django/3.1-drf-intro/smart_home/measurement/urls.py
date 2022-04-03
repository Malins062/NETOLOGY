from django.urls import path

from measurement.views import Sensors, SingleSensor, Measurements

urlpatterns = [
    path('sensors/', Sensors.as_view()),
    path('sensors/<int:pk>/', SingleSensor.as_view()),
    path('measurements/', Measurements.as_view()),
]

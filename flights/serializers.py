from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model

from .models import Booking, Flight


class FlightSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flight
        fields = ["destination", "time", "price", "id"]


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ["flight", "date", "id"]


class BookingDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ["flight", "date", "passengers", "id"]


class UpdateBookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ["date", "passengers"]


# here i wnat to check my solution 
class CreateBookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = "__all__"




User = get_user_model()

class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    # For Token
    access =  serializers.CharField(allow_blank=True,read_only=True)

    def validate(seld,data):
        username = data.get("username")
        password = data.get("password")


        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise serializers.ValidationError("Looks Like User Dose Not Exist!")
        if not user.check_password(password):
            raise serializers.ValidationErorr("Looks like password incorrect !" )

        # Token code here
        payload = RefreshToken.for_user(user)
        token = str(payload.access_token)
        data["access"] = token
        return data 



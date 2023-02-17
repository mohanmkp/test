from rest_framework import serializers



class ws_auth_serializer(serializers.Serializer):
    username = serializers.CharField(max_length=20)
    password = serializers.CharField(max_length=20)
    packet_id = serializers.CharField(max_length=200)
    class Meta:
        fields = ["username", "password", "packet_id"]




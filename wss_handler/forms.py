from django import forms
from .models import ws_sessions



class wss_session_form(forms.ModelForm):
    class Meta:
        model = ws_sessions
        fields = ["packet_id", "username", "password"]



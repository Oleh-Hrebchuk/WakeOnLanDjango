from django.conf.urls import url
from views import WakeOnLanView

urlpatterns = [
    url(r'^wol/$', WakeOnLanView.as_view(), name="wol"),
]
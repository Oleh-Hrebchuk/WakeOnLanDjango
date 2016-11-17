from django.conf.urls import include, url
from django.contrib import admin
from  wakeonlanapp.views import WakeOnLanView
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', WakeOnLanView.as_view()),
    url(r'^wols/', include('wakeonlanapp.urls')),
]

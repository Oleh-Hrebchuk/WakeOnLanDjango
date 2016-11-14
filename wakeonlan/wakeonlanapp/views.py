from django.views.generic import FormView
from forms import WakeOnLan


# Create your views here.
class WakeOnLanView(FormView):
    form_class = WakeOnLan
    template_name = 'wakeonlan.html'
    success_url = '/'

    def form_valid(self, form):
        print form.cleaned_data
        return super(WakeOnLanView, self).form_valid(form)

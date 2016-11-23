from django.views.generic import FormView
from forms import WakeOnLan
from scripts import SSHManager


# Create your views here.
class WakeOnLanView(FormView, SSHManager):
    form_class = WakeOnLan
    template_name = 'wakeonlan.html'
    success_url = '/'
    s = SSHManager()

    def form_valid(self, form):
        data = form.cleaned_data
        get_cp = data.get('computer_name')
        self.s.ssh_rem_comand(get_cp)
        return super(WakeOnLanView, self).form_valid(form)


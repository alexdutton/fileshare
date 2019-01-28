from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.generic import CreateView

from . import models


@method_decorator(login_required, name='dispatch')
class UserFileCreateView(CreateView):
    model = models.UserFile
    fields = ('file', 'public')

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.filename = form['file'].data.name
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('userfile-list')

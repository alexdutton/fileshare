import urllib.parse

from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.generic import ListView, CreateView, View

from . import models


@method_decorator(login_required, name='dispatch')
class UserFileListView(ListView):
    model = models.UserFile

    def get_queryset(self):
        return self.model.objects.filter(Q(user=self.request.user) | Q(public=True))


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


@method_decorator(login_required, name='dispatch')
class UserFileDownloadView(View):
    def get(self, request, pk):
        userfile = get_object_or_404(models.UserFile,
                                     Q(user=request.user) | Q(public=True),
                                     pk=pk)
        response = HttpResponse(userfile.file.file,
                                content_type='application/octet-stream')
        response['Content-Disposition'] = 'attachment; filename={}'.format(
            urllib.parse.quote(userfile.filename, encoding='utf-8'))
        return response


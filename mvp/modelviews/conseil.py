from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.views.generic import CreateView, UpdateView, DetailView, DeleteView
from mvp.models import Conseil, Contract, Company, Service
from mvp.forms import ConseilForm, ServiceForm
from mvp.modelviews import PERMISSION_DENIED
from mvp.controllers import redirectWorkspaceFail, FillConseilLicenseForm, routeDeletePermissions


def CreateConseilPermissions(self, company_pk, contract_pk):
    if hasattr(self.request.user, 'manager'):
        manager = self.request.user.manager
        if manager.company.id == company_pk and (manager.role == 1 or manager.role == 2):
            return True
    elif hasattr(self.request.user, 'commercial'):
        contract = get_object_or_404(Contract, pk=contract_pk)
        commercial = self.request.user.commercial
        if not contract.validated and commercial.company.id == company_pk and commercial.id == contract.commercial.id:
            return True
    else:
        return False


def UpdateDeleteConseilPermissions(self, company_pk, contract_pk, license_pk):
    contract = get_object_or_404(Contract, pk=contract_pk)
    if hasattr(self.request.user, 'manager'):
        manager = self.request.user.manager
        if manager.company.id == company_pk and contract.company.id == manager.company.id \
                and (manager.role == 1 or manager.role == 2):
            return True
    elif hasattr(self.request.user, 'commercial'):
        conseil = get_object_or_404(Conseil, pk=license_pk)
        if conseil.contract.validated:
            return False
        commercial = self.request.user.commercial
        if not contract.validated and commercial.company.id == company_pk \
                and commercial.id == conseil.contract.commercial.id:
            return True
    return False


class ConseilCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Conseil
    form_class = ConseilForm
    template_name = 'mvp/views/conseil_form.html'
    object = None
    pk_url_kwarg = 'contract_pk'
    extra_context = {"create_conseil": True, "button": "Ajouter un conseil",
                     "page_title": "Easley - Create Conseil", "page_heading": "Gestion des conseils",
                     "section": "conseil", "content_heading": "Créer un conseil"}
    permission_denied_message = PERMISSION_DENIED
    success_message = f'Conseil Créé !'

    def test_func(self):
        cpny_pk = self.kwargs.get('cpny_pk')
        if hasattr(self.request.user, 'manager'):
            manager = self.request.user.manager
            if manager.company.id == cpny_pk and (manager.role == 1 or manager.role == 2):
                return True
        elif hasattr(self.request.user, 'commercial'):
            contract = get_object_or_404(Contract, pk=self.kwargs.get(self.pk_url_kwarg))
            commercial = self.request.user.commercial
            if commercial.company.id == cpny_pk and commercial.id == contract.commercial.id:
                return True
        return False

    def form_valid(self, form):
        # print(form.instance)
        return super().form_valid(form)

    def get_success_url(self):
        messages.success(self.request, self.success_message)
        return self.object.get_absolute_url(self.object.contract.company.id, self.object.contract.id)

    def get_form_kwargs(self, *args, **kwargs):
        return FillConseilLicenseForm(self, ConseilCreateView, *args, **kwargs)

    def handle_no_permission(self):
        return redirectWorkspaceFail(self.request, self.permission_denied_message)


class ConseilUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Conseil
    form_class = ConseilForm
    template_name = 'mvp/views/conseil_form.html'
    object = None
    pk_url_kwarg = 'conseil_pk'
    extra_context = {"update_conseil": True, "button": "Modifier le conseil",
                     "page_title": "Easley - Update Conseil", "page_heading": "Gestion des conseils.",
                     "section": "conseil", "content_heading": "Modifier le conseil."}
    permission_denied_message = PERMISSION_DENIED
    success_message = f'Conseil Modifié'

    def test_func(self):
        cpny_pk = self.kwargs.get('cpny_pk')
        if hasattr(self.request.user, 'manager'):
            manager = self.request.user.manager
            if manager.company.id == cpny_pk and manager.role != 3:
                return True
        elif hasattr(self.request.user, 'commercial'):
            contrat = get_object_or_404(Contract, pk=self.kwargs.get('contract_pk'))
            commercial = self.request.user.commercial
            if commercial.company.id == cpny_pk and commercial.id == contrat.commercial.id:
                return True
        return False

    def form_valid(self, form):
        if hasattr(form, 'servicelist'):
            conseil = form.instance
            for service in conseil.service_set.all():
                service.delete()
            for data in form.servicelist:
                print(data)
                service = Service(
                    conseil=conseil,
                    description=data[0],
                    estimated_date=data[1],
                    senior_day=data[2],
                    junior_day=data[3],
                )
                print(service)
                service.save()
            conseil.__delattr__('servicelist')
            conseil.save()
        return super().form_valid(form)

    def get_success_url(self):
        messages.success(self.request, self.success_message)
        return self.object.get_absolute_url(self.object.company.id, self.object.contract.id)

    def get_form_kwargs(self, *args, **kwargs):
        return FillConseilLicenseForm(self, ConseilUpdateView, *args, **kwargs)

    def handle_no_permission(self):
        return redirectWorkspaceFail(self.request, self.permission_denied_message)


class ConseilDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Conseil
    template_name = 'mvp/views/conseil_details.html'
    object = None
    pk_url_kwarg = 'conseil_pk'
    extra_context = {"delete_conseil": True,
                     "page_title": "Easley - Delete Conseil", "page_heading": "Gestion des conseils",
                     "section": "conseil", "content_heading": "Supprimer un conseil"}
    permission_denied_message = PERMISSION_DENIED
    success_message = f'Conseil Supprimé !'

    def test_func(self):
        return routeDeletePermissions(self, self.pk_url_kwarg, self.model)

    def get_success_url(self):
        if hasattr(self.request.user, 'commercial'):
            messages.warning(self.request, self.success_message)
            return reverse('mvp-conseil-list', args=[self.object.company.id, self.request.user.commercial.id])
        elif hasattr(self.request.user, 'manager'):
            messages.warning(self.request, self.success_message)
            return reverse('mvp-conseil-list', args=[self.object.company.id, self.request.user.manager.id])
        else:
            return redirectWorkspaceFail('mvp-workspace', self.success_message)

    def handle_no_permission(self):
        return redirectWorkspaceFail(self.request, self.permission_denied_message)


# @ TODO: Faire permissions, faire la gestion du changement d'excel
@login_required
def ConseilDetails(request, cpny_pk=None, contract_pk=None, conseil_pk=None):
    context = {
        'content_heading': 'Rentrer les informations nécessaires à la création du conseil.',
        'object': get_object_or_404(Conseil, pk=conseil_pk)
    }
    contract = get_object_or_404(Contract, pk=contract_pk)

    if contract.validated:
        context['content_heading'] = 'Détails du conseil'
        context['services'] = context['object'].service_set.all() or None
        return render(request, 'mvp/views/conseil_details.html', context)
    form = ServiceForm(request.POST or None, user=request.user, company=contract.company, conseil=context['object'])
    if request.method == "POST" and ('delete_conseil' in request.POST):
        context['object'].delete()
        return redirect('mvp-contract-details', cpny_pk=contract.company.id, contract_pk=contract.id)
    if request.method == "POST" and form.is_valid():
        # @ TODO faire excel management
        form.save()
        return render(request, 'mvp/views/conseil_details.html', context)
    context['services'] = context['object'].service_set.all() or None
    context['form'] = form
    return render(request, 'mvp/views/conseil_details.html', context)


# class ConseilDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
#     model = Conseil
#     template_name = 'mvp/views/conseil_details.html'
#     pk_url_kwarg = 'conseil_pk'
#     extra_context = {"details": True,
#                      "page_title": "Easley - Conseil Details", "page_heading": "Gestion des conseils",
#                      "section": "conseil", "content_heading": "Informations conseil"}
#     permission_denied_message = PERMISSION_DENIED
#
#     def get_queryset(self):
#         return Conseil.objects.filter(id=self.kwargs.get(self.pk_url_kwarg))
#
#     def test_func(self):
#         cpny_pk = self.kwargs.get('cpny_pk')
#         if hasattr(self.request.user, 'manager'):
#             if self.request.user.manager.company.id == cpny_pk:
#                 return True
#         elif hasattr(self.request.user, 'commercial'):
#             contrat = get_object_or_404(Contract, pk=self.kwargs.get('contract_pk'))
#             commercial = self.request.user.commercial
#             if commercial.company.id == cpny_pk and commercial.id == contrat.commercial.id:
#                 return True
#         return False
#
#     def handle_no_permission(self):
#         return redirectWorkspaceFail(self.request, self.permission_denied_message)


# class ConseilListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
#     model = Conseil
#     template_name = 'mvp/views/conseil_list.html'
#     ordering = ['id']
#     pk_url_kwarg = 'com_pk'
#     extra_context = {"list_conseil": True, "section": "conseil", }
#     permission_denied_message = PERMISSION_DENIED
#
#     def get_queryset(self):
#         if hasattr(self.request.user, 'commercial'):
#             return self.request.user.commercial.conseil_set.all()
#         elif hasattr(self.request.user, 'manager'):
#             return self.request.user.manager.company.conseil_set.all()
#         else:
#             return HttpResponseNotFound
#
#     def test_func(self):
#         return routeListPermissions(self, self.pk_url_kwarg)
#
#     def handle_no_permission(self):
#         return redirectWorkspaceFail(self.request, self.permission_denied_message)


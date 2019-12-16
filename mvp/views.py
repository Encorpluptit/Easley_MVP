from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.forms import modelformset_factory
from dateutil.relativedelta import relativedelta
from dateutil.utils import today
from django.db.models import Sum
from .models import Company, Commercial, Manager, Client, Conseil, License, Contract, Invoice, InviteChoice, Invite
from .controllers import customRegisterUser, CreateAllInvoice
from .forms import (
    UserRegisterForm,
    CompanyForm,
    ContractForm,
    ClientForm,
    ServiceForm,
    InviteForm,
)


# Create your views here.
# from django.core.mail import send_mail
# from django.conf import settings
# def email(request):
#     subject = 'Thank you for registering to our site'
#     message = ' it  means a world to us '
#     email_from = settings.EMAIL_HOST_USER
#     recipient_list = ['damien.bernard@epitech.eu', ]
#     send_mail(subject, message, email_from, recipient_list)
#     return redirect('mvp-home')
#

def home(request):
    return render(request, 'mvp/misc/home.html')


def about(request):
    return render(request, 'mvp/misc/about.html')


def contact(request):
    return render(request, 'mvp/misc/contact.html')


def register(request):
    form = UserRegisterForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        if customRegisterUser(request, form):
            return redirect('mvp-company-register')
        else:
            return redirect(request, 'mvp-home')
    return render(request, 'mvp/misc/register.html', {'form': form})


@login_required
def Employees(request):
    company = request.user.manager.company
    managers = company.manager_set.all()
    invites = company.invite_set.all()
    context = {
        'section': "employees",
        'commercials': company.commercial_set.all() or None,
        'factus': managers.filter(role=3) or None,
        'accounts': managers.filter(role=2) or None,
        'managers': managers.filter(role=1) or None,
    }

    inviteformset = modelformset_factory(Invite, extra=4, exclude=('company', 'role'),)
    formset = inviteformset(request.POST or None, queryset=Invite.objects.none())
    for index, form in enumerate(formset):
        for nb, string in InviteChoice:
            if nb == (index + 1):
                form.instance.role = nb
                form.instance.company = company
                form.fields['email'].widget.attrs.update({'class': 'form-control'})
                break
    if request.method == "POST":
        print("POST\n", request.POST)
        print(formset.is_valid())
        instances = formset.save(commit=False)
        print(instances)
        for form in instances:
            # print('form in instance', form, type(form))
            if (Invite.objects.filter(email=form.email) or None) or (User.objects.filter(email=form.email) or None):
                messages.warning(request, f"Une invitation a déjà été envoyée pour cette adresse email ou\
                un utilsateur avec cette adresse existe déjà.")
                break
            # print('save')
            form.save()
            # formset.full_clean()
            # formset._should_delete_form(form)
            # formset.delete_existing(form)
    context['invite_commercial'] = invites.filter(role=4) or None
    context['invite_factus'] = invites.filter(role=3) or None
    context['invite_accounts'] = invites.filter(role=2) or None
    context['invite_managers'] = invites.filter(role=1) or None
    context['formset'] = formset
    return render(request, 'mvp/misc/employees.html', context)


@login_required
def companyCreation(request):
    form = CompanyForm(request.POST or None, ceo=request.user)
    if request.method == "POST" and form.is_valid():
        try:
            company = form.save()
            ceo = Manager.objects.create(user=request.user, company=company, role=1)
            ceo.save()
            messages.success(request, f'Company {company.name} Created, Welcome {ceo} !')
            # @ TODO: faire les invitations des commerciaux
        except:
            messages.warning(request, f'An Error occurred ! Please try again later')
        return redirect('mvp-workspace')
    return render(request, 'mvp/misc/company_creation.html', {'form': form})


# @ TODO: Faire permissions
@login_required
def CreateContractClient(request, **kwargs):
    context = {
        'page': 'contract_client',
        'post': False,
        'section': 'contract',
        'create_contract': True
    }
    company, manager = None, False

    if hasattr(request.user, 'commercial'):
        context['client_list'] = request.user.commercial.client_set.all()
        company = request.user.commercial.company
    if hasattr(request.user, 'manager'):
        context['client_list'] = request.user.manager.company.client_set.all()
        company = request.user.manager.company
        manager = True
    form = ClientForm(request.POST or None, user=request.user, company=company, manager=manager)
    if request.method == "POST":
        context['post'] = True
        if form.is_valid():
            client = form.save()
            messages.success(request, f'Client créé.')
            return redirect('mvp-contract-form', company.id, client.id)
    context['form'] = form
    return render(request, 'mvp/views/contract_client.html', context)


# @ TODO: Faire permissions
@login_required
def CreateContractForm(request, cpny_pk=None, client_pk=None):
    context = {}
    client = get_object_or_404(Client, pk=client_pk)
    company = get_object_or_404(Company, pk=cpny_pk)
    form = ContractForm(request.POST or None, user=request.user, client=client, company=company)
    if request.method == "POST":
        if form.is_valid():
            contract = form.save()
            messages.success(request, f'Contrat créé.')
            return redirect('mvp-contract-details', company.id, contract.id, )
    context['form'] = form
    return render(request, 'mvp/views/contract_form.html', context)


# @ TODO: Faire permissions


@login_required
def ContractDetails(request, cpny_pk=None, contract_pk=None, conseil_pk=None):
    context = {
        "page_title": "Easley - Contrat Details", "page_heading": "Gestion des Contrats",
        "section": "contract", "content_heading": "Détail Contrat",
    }
    contract = get_object_or_404(Contract, pk=contract_pk)
    conseils = contract.conseil_set.all().order_by('start_date', '-price') or None
    licenses = contract.license_set.all().order_by('start_date', '-price') or None

    context['object'] = contract
    context['licenses'] = licenses
    context['conseils'] = conseils
    context['invoices'] = contract.invoice_set.all()
    context['progression'] = 0
    date_now = today().date()
    if contract.start_date <= date_now:
        try:
            context['progression'] = int((date_now - contract.start_date) / (contract.end_date - contract.start_date) * 100)
        except ZeroDivisionError:
            pass
    if request.method == "POST" and ('delete_contract' in request.POST):
        contract.delete()
        return redirect('mvp-contract-list', cpny_pk=contract.company.id)
    if contract.validated:
        return render(request, 'mvp/views/contract_details.html', context)
    if request.method == "POST" and not contract.validated:
        if conseils.count() <= 0 and licenses.count() <= 0:
            messages.info(request, f"Le contrat est vide. Veuillez rentrer une license ou un conseil.")
        else:
            CreateAllInvoice(contract, licenses, conseils)
            contract.validated = True
            contract.save()
            messages.success(request, f'Contrat Validé.')
            return redirect(contract.get_absolute_url(contract.company.id))
    return render(request, 'mvp/views/contract_details.html', context)


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
        return render(request, 'mvp/views/conseil_details.html', context)
    company = get_object_or_404(Company, pk=cpny_pk)
    form = ServiceForm(request.POST or None, user=request.user, company=company, conseil=context['object'])
    if request.method == "POST" and form.is_valid():
        form.save()
        return render(request, 'mvp/views/conseil_details.html', context)
    context['form'] = form
    return render(request, 'mvp/views/conseil_details.html', context)


@login_required
def ContractListView(request, cpny_pk=None):
    context = {'validated_contracts': None, 'section': 'contract', 'list_contract': True}
    if hasattr(request.user, 'commercial'):
        contracts = request.user.commercial.contract_set.all()
        context['validated_contracts'] = contracts.filter(validated=True).order_by('start_date', '-price')
        context['not_validated_contracts'] = contracts.filter(validated=False).order_by('start_date', '-price')
    elif hasattr(request.user, 'manager'):
        contracts = request.user.manager.company.contract_set.all()
        context['validated_contracts'] = contracts.filter(validated=True).order_by('start_date', '-price')
        context['not_validated_contracts'] = contracts.filter(validated=False).order_by('start_date', '-price')
    return render(request, 'mvp/views/contract_list.html', context)


def join_company(request, invite_email):
    invite = get_object_or_404(Invite, email=invite_email)
    form = UserRegisterForm(request.POST or None, email=invite_email)
    if request.method == "POST" and form.is_valid():
        if customRegisterUser(request, form):
            manager = Manager.objects.create(user=request.user, company=invite.company, role=invite.role)
            invite.delete()
            return redirect('mvp-workspace')
        else:
            return redirect(request, 'mvp-home')
    return render(request, 'mvp/misc/register.html', {'form': form})


@login_required
def CommercialWorkspace(request):
    context = {
        'section': 'workspace',
        'month_prime': 0,
        'year_prime': 0,
    }
    commercial = request.user.commercial
    contracts = commercial.contract_set.all()
    date = today()
    month_prime = contracts.filter(start_date__month=date.month, validated=True).aggregate(Sum('price'))['price__sum']
    year_prime = contracts.filter(start_date__year=date.year, validated=True).aggregate(Sum('price'))['price__sum']
    if month_prime:
        context['month_prime'] = month_prime / 10
    if year_prime:
        context['year_prime'] = year_prime / 10
    context['unfinished_contracts'] = contracts.filter(validated=False).count()
    context['finished_contracts'] = contracts.filter(validated=True).count()
    context['new_clients'] = commercial.client_set.filter(created_at__gte=today().date() - relativedelta(months=1)).count()
    return render(request, 'mvp/workspace/bizdev.html', context)


@login_required
def ManagerWorkspace(request):
    context = {
        'section': 'workspace',
    }
    return render(request, 'mvp/workspace/manager.html', context)


@login_required
def FactuWorkspace(request):
    context = {
        'section': 'workspace',
    }

    date = today()
    factu = request.user.manager
    company = factu.company
    invoices = company.invoice_set.all()
    context['invoice_to_facture'] = invoices.filter(
        contract__factu_manager=factu, facturated=False,
        date__month__lte=date.month, date__year__lte=date.year).order_by('contract__id', 'date').distinct('contract')
    # invoices = company.invoice_set.order_by('contract__id', 'date').distinct('contract')
    # context['invoice_to_facture'] = invoices.filter(
    #     contract__factu_manager=factu, facturated=False,
    #     date__month__lte=date.month, date__year__lte=date.year)
    context['invoice_late'] = invoices.filter(
        contract__factu_manager=factu, facturated=True, payed=False,
        date__month__lte=date.month, date__year__lte=date.year)
    for inv in context['invoice_to_facture']:
        qs = inv.contract.invoice_set.filter(
            facturated=False, date__month__lt=date.month, date__year__lte=date.year) or None
        print(inv)
        print(qs)
        if qs:
            inv.late = qs.count()
    return render(request, 'mvp/workspace/factu.html', context)


@login_required
def AccountWorkspace(request):
    context = {
        'section': 'workspace',
        'nb_services_to_validate': 0,
    }
    manager = request.user.manager
    date = today()
    services = manager.company.contract_set.filter(
        validated=True,
        client__account_manager=manager,
        conseil__service__estimated_date__month__lte=date.month,
        conseil__service__estimated_date__year__lte=date.year,
    ) or None
    if services:
        context['nb_services_to_validate'] = services.count()
    context['services'] = services
    return render(request, 'mvp/workspace/account.html', context)


@login_required
def workspace(request):
    user = request.user
    if hasattr(user, 'commercial'):
        return CommercialWorkspace(request)
    elif hasattr(user, 'manager'):
        if user.manager.role == 1:
            return ManagerWorkspace(request)
        elif user.manager.role == 2:
            return AccountWorkspace(request)
        elif user.manager.role == 3:
            return FactuWorkspace(request)
    return redirect('mvp-company-register')


# @login_required
# def serviceCreation(request):
#     form = ConseilForm(request.POST or None, user=request.user)
#     # print(request.POST)
#     if request.method == "POST" and form.is_valid():
#         if hasattr(request.user, 'commercial'):
#             # clean_form = form.save(commit=False)
#             # clean_form.company = request.user.commercial.company
#             # clean_form.commercial = request.user.commercial
#             form.save()
#             messages.success(request, f'service created!')
#             return redirect('mvp-workspace')
#         elif hasattr(request.user, 'manager'):
#             # clean_form = form.save(commit=False)
#             # clean_form.company = request.user.manager.company
#             form.save()
#             messages.success(request, f'service created!')
#             return redirect('mvp-workspace')
#     return render(request, 'mvp/service/service_form.html', {'form': form})
#
#
# @login_required
# def licenseCreation(request):
#     form = LicenseForm(request.POST or None, user=request.user)
#     if request.method == "POST" and form.is_valid():
#         if hasattr(request.user, 'commercial'):
#             clean_form = form.save(commit=False)
#             clean_form.company = request.user.commercial.company
#             clean_form.commercial = request.user.commercial
#             form.save()
#             messages.success(request, f'license created!')
#             return redirect('mvp-workspace')
#     return render(request, 'mvp/license/license_form.html', {'form': form})


# class ContractDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
#     model = Contract
#     template_name = 'mvp/views/contract_details.html'
#     pk_url_kwarg = 'contract_pk'
#     extra_context = {"details": True,
#                      "page_title": "Easley - Contrat Details", "page_heading": "Gestion des Contrats",
#                      "section": "contrat", "content_heading": "Détail Contrat"}
#     permission_denied_message = PERMISSION_DENIED
#
#     def get_queryset(self):
#         return Contract.objects.filter(id=self.kwargs.get(self.pk_url_kwarg))
#
#     def test_func(self):
#         return routeDetailsPermissions(self, self.pk_url_kwarg, self.model)
#
#     def handle_no_permission(self):
#         return redirectWorkspaceFail(self.request, self.permission_denied_message)
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['licenses'] = self.object.license_set.all()
#         context['conseils'] = self.object.conseil_set.all()
#         return context


# @login_required
# def LicenseUpdate(request,  cpny_pk=None, contract_pk=None, license_pk=None):
#     context = {
#         'content_heading': 'Modifier la license.',
#     }
#     license = get_object_or_404(License, pk=license_pk)
#     contract = license.contract
#     form = LicenseForm(instance=license, company=contract.company, contract=contract)
#     # form.fields['duration'].initial = license.duration
#     print(request.POST, form.is_valid())
#     if request.method == "POST" and form.is_valid():
#         new_license = form.save()
#         contract.price += (new_license.price - license.price)
#         print("VALID")
#         contract.save()
#         return redirect('mvp-license-details', contract.company.id, contract.id, license.id)
#     context['form'] = form
#     return render(request, 'mvp/views/license_form.html', context)

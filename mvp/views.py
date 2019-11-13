from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserRegisterForm, CompanyRegisterForm, ClientRegisterForm, UserUpdateForm
from .models import Commercial, Company
from .controllers import customRegisterUser, customCompanyRegister


# Create your views here.


def home(request):
    return render(request, 'mvp/base/home.html')


def about(request):
    return render(request, 'mvp/base/about.html')


def contact(request):
    return render(request, 'mvp/base/contact.html')


def register(request):
    form = UserRegisterForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        if customRegisterUser(request, form):
            return redirect('mvp-login')
            # return redirect('mvp-join-company')
        else:
            return redirect(request, 'mvp-home')
    # return render(request, 'mvp/register.html', locals())
    return render(request, 'mvp/login_register/register.html', {'form': form})


@login_required
def updateUser(request):
    form = UserUpdateForm(instance=request.user)
    if request.method == "POST":
        print("post")
    return render(request, 'mvp/login_register/register.html',  {'form': form})


@login_required
def companyCreation(request):
    form = CompanyRegisterForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        customCompanyRegister(request, form)
        return redirect('mvp-home')
    return render(request, 'mvp/forms/company_form.html', {'form': form})


@login_required
def clientCreation(request):
    # print(request)
    form = ClientRegisterForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        clean_form = form.save(commit=False)
        commercial_var = Commercial.objects.get(user=request.user)
        if commercial_var:
            clean_form.company = commercial_var.company
        form.save()
        return redirect('mvp-home')
    return render(request, 'mvp/forms/client_form.html', {'form': form})


@login_required
def join_company(request):
    if request.method == "POST":
        company = Company.objects.filter(pk=int(request.POST['company_id'])).first()
        if company:
            Commercial.objects.create(user=request.user, company=company)
            redirect('mvp-commercial-workspace')
        else:
            messages.warning(request, f'Wrong company ID')
    return render(request, 'mvp/base/join_company.html')


@login_required
def commercialWorkspace(request):
    return render(request, 'mvp/commercial/commercial_workspace.html')


@login_required
def ceoWorkspace(request):
    return render(request, 'mvp/ceo/ceo_workspace.html')


@login_required
def workspace(request):
    if hasattr(request.user, 'commercial'):
        return redirect('mvp-commercial-workspace')
    elif hasattr(request.user, 'ceo'):
        return redirect('mvp-ceo-workspace')
    else:
        return redirect('mvp-join-company')

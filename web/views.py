from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic import ListView
from django.contrib.auth.models import User
from django.contrib.auth import login
from .forms import UserForm, WalletForm, TransferForm
from .models import Wallet, Transfer


class UserCreateView(CreateView):
    model = User
    form_class = UserForm
    success_url = "/"
    template_name = "web/create_user.html"

    def form_valid(self, form):
        """If the form is valid, save the associated model."""
        self.object = form.save()
        # Login User instance.
        login(self.request, self.object)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["has_wallets"] = Wallet.objects.filter(user=self.request.user).exists()
        return context
    

    def get_success_url(self):
        return self.success_url


class WalletCreateView(LoginRequiredMixin, CreateView):
    model = Wallet
    success_url = "/"
    fields = "__all__"
    template_name = "web/create_wallet.html"

    def get_context_data(self, **kwargs):
        """Insert the form into the context dict."""
        if "form" not in kwargs:
            form = self.get_form()
            form.initial["user"] = User.objects.filter(username=self.request.user).first()
            kwargs["form"] = form
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        # Verify that user doesnt create more than 10 wallets
        if len(Wallet.objects.filter(user=self.request.user)) > 9:
            return self.success_url
        else:
            # TODO return cannot create more wallets (limit 10) err
            return super().form_valid(form)

    def get_success_url(self):
        return self.success_url


class TransferCreateView(LoginRequiredMixin, CreateView):
    model = Transfer
    form_class = TransferForm
    success_url = "/"
    template_name = "web/wallet-transfer.html"

    def get_context_data(self, **kwargs):
        kwargs["wallet"] = Wallet.objects.get(pk=self.kwargs['pk'])
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        return super().form_valid(form)

    def get_success_url(self):
        return self.success_url


class WalletListView(ListView):
    model = Wallet
    template_name = "web/list_wallet.html"

    def get_context_data(self, **kwargs):
        kwargs["wallets"] = Wallet.objects.filter(user=self.request.user)
        return super().get_context_data(**kwargs)


def post_users(request):
    """
        POST Endpoint to create users. If request is not POST it will redirect to the index view. 
    """
    if request.method == 'POST':
        User.objects.create(
            username=request.POST['username'],
            password=request.POST['password'],
            email=request.POST['email'])
    else:
        return HttpResponseRedirect(reverse('index'))


def post_wallets(request):
    """
        POST Endpoint to create wallets. If request is not POST it will redirect to the index view. 
    """
    if request.method == 'POST':
        pass
    else:
        return HttpResponseRedirect(reverse('index'))


def get_wallet_address(request):
    pass


def post_transactions(request):
    pass


def get_transactions(request):
    pass


def get_statictics(request):
    pass
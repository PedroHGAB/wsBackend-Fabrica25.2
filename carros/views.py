import requests
from decimal import Decimal, InvalidOperation

from django.contrib import messages
from django.db import IntegrityError
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView

from .models import Garagem, CarroSalvo


API_FIPE_URL = "https://parallelum.com.br/fipe/api/v1/carros"


class HomeView(TemplateView):
	template_name = "carros/home.html"


class GaragemCriarView(CreateView):
	model = Garagem
	fields = ["nome"]
	template_name = "carros/garagem_form.html"
	success_url = reverse_lazy("carros:garagem_lista")


class GaragemListaView(ListView):
	model = Garagem
	template_name = "carros/garagem_lista.html"
	context_object_name = "garagens"


class GaragemDetalheView(DetailView):
	model = Garagem
	template_name = "carros/garagem_detalhe.html"
	context_object_name = "garagem"

class GaragemEditarView(UpdateView):
    model = Garagem
    fields = ["nome"]
    template_name = "carros/garagem_form.html"

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Nome da garagem atualizado!")
        return response

    def get_success_url(self):
        return reverse_lazy("carros:garagem_detalhe", kwargs={"pk": self.object.pk})


class GaragemExcluirView(DeleteView):
	model = Garagem
	template_name = "carros/garagem_confirm_delete.html"
	success_url = reverse_lazy("carros:garagem_lista")


class MeusCarrosView(ListView):
	model = CarroSalvo
	template_name = "carros/meus_carros.html"
	context_object_name = "carros"


class CarroExcluirView(DeleteView):
	model = CarroSalvo
	template_name = "carros/carro_confirm_delete.html"

	def get_success_url(self):
		return reverse_lazy("carros:garagem_detalhe", kwargs={"pk": self.object.garagem_id})


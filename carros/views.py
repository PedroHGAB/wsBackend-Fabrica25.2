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


def marcas(request):
	try:
		r = requests.get(f"{API_FIPE_URL}/marcas")
		marcas = r.json()
	except Exception:
		messages.error(request, "Falha ao obter marcas da FIPE.")
		marcas = []
	return render(request, "carros/marcas.html", {"marcas": marcas})


def modelos(request, marca_id):
	try:
		r = requests.get(f"{API_FIPE_URL}/marcas/{marca_id}/modelos")
		modelos = r.json().get("modelos", [])
	except Exception:
		messages.error(request, "Falha ao obter modelos da FIPE.")
		modelos = []
	return render(request, "carros/modelos.html", {"modelos": modelos, "marca_id": marca_id})


def anos(request, marca_id, modelo_id):
	try:
		r = requests.get(f"{API_FIPE_URL}/marcas/{marca_id}/modelos/{modelo_id}/anos")
		anos = r.json()
	except Exception:
		messages.error(request, "Falha ao obter anos da FIPE.")
		anos = []
	return render(request, "carros/anos.html", {"anos": anos, "marca_id": marca_id, "modelo_id": modelo_id})


def detalhe(request, marca_id, modelo_id, ano_codigo):
	try:
		r = requests.get(f"{API_FIPE_URL}/marcas/{marca_id}/modelos/{modelo_id}/anos/{ano_codigo}")
		carro = r.json()
	except Exception:
		messages.error(request, "Falha ao obter detalhes do carro.")
		carro = {}

	garagens = Garagem.objects.all().order_by("nome")

	if request.method == "POST":
		garagem = get_object_or_404(Garagem, pk=request.POST.get("garagem_id"))

		ano = carro.get("AnoModelo", 0)
		ano = int(ano)

		preco = brl_to_decimal(carro.get("Valor", "0"))

		CarroSalvo.objects.create(
			garagem=garagem,
			marca=carro.get("Marca", ""),
			modelo=carro.get("Modelo", ""),
			ano=ano,
			preco=preco,
		)
		messages.success(request, "Carro salvo na garagem!")

		return redirect("carros:garagem_detalhe", pk=garagem.id)

	return render(request, "carros/detalhe.html", {"carro": carro, "garagens": garagens})


# Função que converte string do campo preço para Decimal feita com ia, pois a API retorna o preço nesse formato.
def brl_to_decimal(texto: str) -> Decimal:
	limpo = (texto.replace("R$", "")
					.replace("\xa0", "")
					.replace(" ", "")
					.replace(".", "")
					.replace(",", "."))
	try:
		return Decimal(limpo)
	except InvalidOperation:
		return Decimal("0.00")
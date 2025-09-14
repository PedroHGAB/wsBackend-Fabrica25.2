from django.urls import path
from . import views

app_name = "carros"

urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),

    # consulta fipe
    path("marcas/", views.marcas, name="marcas"),
    path("marcas/<marca_id>/modelos/", views.modelos, name="modelos"),
    path("marcas/<marca_id>/modelos/<modelo_id>/anos/", views.anos, name="anos"),
    path("marcas/<marca_id>/modelos/<modelo_id>/anos/<ano_codigo>/", views.detalhe, name="detalhe"),

    # garagens
    path("garagens/", views.GaragemListaView.as_view(), name="garagem_lista"),
    path("garagens/nova/", views.GaragemCriarView.as_view(), name="garagem_nova"),
    path("garagens/<int:pk>/", views.GaragemDetalheView.as_view(), name="garagem_detalhe"),
    path("garagens/<int:pk>/editar/", views.GaragemEditarView.as_view(), name="garagem_editar"),
    path("garagens/<int:pk>/excluir/", views.GaragemExcluirView.as_view(), name="garagem_excluir"),

    # carros
    path("meus-carros/", views.MeusCarrosView.as_view(), name="meus_carros"),
    path("carros/<int:pk>/excluir/", views.CarroExcluirView.as_view(), name="carro_excluir"),
]

from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.views import View
from .models import Pergunta, Alternativa

class IndexView(View):
    def get(self, request, *arg, **kwargs):
        lista = Pergunta.objects.order_by('-data_pub')
        contexto = {'pergunta_list': lista}
        return render(request, 'enquetes/index.html', contexto)

class DetalhesView(View):
    def get(self, request, *arg, **kwargs):
       pergunta_id=kwargs['pk']
       enquete = get_object_or_404(Pergunta, pk=pergunta_id)
       return render(
           request, 'enquetes/detalhes.html',{'pergunta':enquete})
    def post(self, request, *args, **kwargs):
        pergunta_id=kwargs['pk']
        pergunta = get_object_or_404(Pergunta, pk=pergunta_id)
        try:
            id_votado = request.POST['escolha']
            alt_selecionada = pergunta.alternativa_set.get(pk=id_votado)
        except(KeyError, Alternativa.DoesNotExist):
            contexto = {'pergunta':pergunta, 'erro': 'Escolha uma alternativa válida!',}
            return render(request, 'enquetes/detalhes.html', contexto)
        else:
            alt_selecionada.quant_votos += 1
            alt_selecionada.save()
            return HttpResponseRedirect(reverse('enquetes:resultado', args=(pergunta_id,)))


class ResultadoView(View):
    def get(self, request, *args, **kwargs):
        pergunta_id=kwargs['pk']
        enquete = get_object_or_404(Pergunta, pk=pergunta_id)
        return render(
            request, 'enquetes/resultado.html',{'pergunta':enquete})

"""
INDEX V1.0
def index(request):
    def index(request):
    return HttpResponse("Bem vindo a aplicação de <b>Enquetes<b> Aeeeeeeeeeeeeee")

INDEX V2.0
def index(request):
    lista = Pergunta.objects.all()
    resposta = '<br>'.join([p.texto for p in lista])
    return HttpResponse(resposta)

INDEX V3.0
def index(request):
    lista = Pergunta.objects.order_by('-data_pub')
    contexto = {'lista_enquetes': lista}
    return render(request, 'enquetes/index.html', contexto)

INDEX V4.0
class IndexView(generic.ListView):
    template_name = 'enquetes/index.html'
    def get_queryset(self):
        return Pergunta.objects.order_by('-data_pub')

RESULTADO V1.0
def resultado(request, pergunta_id):
    enquete = get_object_or_404(Pergunta, pk=pergunta_id)
    return render(request, 'enquetes/resultado.html',{'pergunta':enquete})

DETALHES V1.0
def detalhes(request, pergunta_id):
    resultado = 'DETALHES da Enquete #%s'
    return HttpResponse(resultado % pergunta_id)

DETALHES V3.0
class DetalhesView(generic.DetailView):
    model = Pergunta


VOTAÇÃO V1.0
def votacao(request, pergunta_id):
    resultado = 'VOTAÇÃO da Enquete #%s'
    return HttpResponse(resultado % pergunta_id)
"""
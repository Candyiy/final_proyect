from django.shortcuts import render, redirect
from .forms import OfertaForm
from .models import OfertaLaboral
from django.contrib.auth.decorators import login_required

@login_required
def crear_oferta(request):

    if request.method == 'POST':
        form = OfertaForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('lista_ofertas')

    else:
        form = OfertaForm()

    return render(request, 'ofertas/formulario.html', {'form': form})

@login_required
def lista_ofertas(request):

    ofertas = OfertaLaboral.objects.all()

    return render(request, 'pages/job.html', {'ofertas': ofertas})
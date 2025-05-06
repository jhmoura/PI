from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import *
import json
from datetime import datetime
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('calendar')  # redirecione para o dashboard ou página principal
        else:
            return render(request, 'calendario/login.html', {'error': 'Usuário ou senha inválidos'})
    return render(request, 'calendario/login.html')

@login_required
def calendar_view(request):
    return render(request, 'calendario/calendar.html')

@login_required
def get_events(request):
    events = Event.objects.all()
    event_list = []
    for event in events:
        event_list.append({
            'id': event.id,
            'title': event.title,
            'start': event.start.isoformat(),
            'end': event.end.isoformat(),
            'client': event.client.name,
            'value': str(event.value),
            'backgroundColor': '#007bff',  # Cor para dias com eventos
            'borderColor': '#007bff',
        })
    return JsonResponse(event_list, safe=False)

@login_required
def get_clients(request):
    clients = Client.objects.all()
    client_list = [{'id': client.id, 'name': client.name} for client in clients]
    return JsonResponse(client_list, safe=False)

@login_required
@csrf_exempt
def add_event(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        title = data.get('title')
        client_id = data.get('client_id')
        start = datetime.fromisoformat(data.get('start').replace('Z', '+00:00'))
        end = datetime.fromisoformat(data.get('end').replace('Z', '+00:00'))
        value = data.get('value')

        client = Client.objects.get(id=client_id)
        event = Event.objects.create(
            title=title,
            client=client,
            start=start,
            end=end,
            value=value
        )
        return JsonResponse({'status': 'success', 'id': event.id})
    return JsonResponse({'status': 'error'}, status=400)

from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Client
import json

# Página principal de clientes

@login_required
def clients_page(request):
    return render(request, 'calendario/clients.html')

# API: Listar todos os clientes
@login_required
def get_clients(request):
    clients = Client.objects.all()
    data = [{'id': client.id, 'name': client.name, 'telefone': client.telefone, 
             'endereco': client.endereco, 'observacoes': client.observacoes} 
            for client in clients]
    return JsonResponse(data, safe=False)

# API: Buscar clientes por nome
@login_required
def search_clients(request):
    query = request.GET.get('query', '')
    clients = Client.objects.filter(name__icontains=query)
    data = [{'id': client.id, 'name': client.name, 'telefone': client.telefone, 
             'endereco': client.endereco, 'observacoes': client.observacoes} 
            for client in clients]
    return JsonResponse(data, safe=False)

# API: Criar ou editar cliente
@login_required
@csrf_exempt
def add_client(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        client_id = data.get('id')
        if client_id:
            # Editar cliente existente
            client = Client.objects.get(id=client_id)
            client.name = data.get('name')
            client.telefone = data.get('telefone')
            client.endereco = data.get('endereco')
            client.observacoes = data.get('observacoes')
            client.save()
        else:
            # Criar novo cliente
            client = Client.objects.create(
                name=data.get('name'),
                telefone=data.get('telefone'),
                endereco=data.get('endereco'),
                observacoes=data.get('observacoes')
            )
        return JsonResponse({'status': 'success', 'id': client.id})
    return JsonResponse({'status': 'error'}, status=400)

# API: Excluir cliente
@login_required
@csrf_exempt
def delete_client(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        client_id = data.get('id')
        try:
            client = Client.objects.get(id=client_id)
            client.delete()
            return JsonResponse({'status': 'success'})
        except Client.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Cliente não encontrado'}, status=404)
    return JsonResponse({'status': 'error'}, status=400)

@login_required
def fornecedores_page(request):
    return render(request, 'calendario/fornecedores.html')

@login_required
def get_fornecedores(request):
    fornecedores = Fornecedor.objects.select_related('tipo').all()
    data = [{
        'id': f.id,
        'nome': f.nome,
        'tipo': f.tipo.nome,
        'tipo_id': f.tipo.id,
        'telefone': f.telefone,
        'preco': float(f.preco),
        'descricao': f.descricao,
    } for f in fornecedores]
    return JsonResponse(data, safe=False)

@login_required
def get_tipos_servico(request):
    tipos = TipoServico.objects.all().order_by('nome')
    data = [{'id': t.id, 'nome': t.nome} for t in tipos]
    return JsonResponse(data, safe=False)

@csrf_exempt
def add_fornecedor(request):
    data = json.loads(request.body)
    nome = data.get('nome')
    telefone = data.get('telefone')
    preco = data.get('preco')
    descricao = data.get('descricao')
    tipo_novo = data.get('tipo_novo')
    tipo_existente = data.get('tipo_existente')

    # Definir tipo
    if tipo_novo:
        tipo, _ = TipoServico.objects.get_or_create(nome=tipo_novo.strip())
    else:
        tipo = get_object_or_404(TipoServico, id=tipo_existente)

    # Criar ou atualizar
    if data.get('id'):
        fornecedor = get_object_or_404(Fornecedor, id=data['id'])
    else:
        fornecedor = Fornecedor()

    fornecedor.nome = nome
    fornecedor.tipo = tipo
    fornecedor.telefone = telefone
    fornecedor.preco = preco
    fornecedor.descricao = descricao
    fornecedor.save()

    return JsonResponse({'status': 'success'})

@csrf_exempt
def delete_fornecedor(request):
    data = json.loads(request.body)
    fornecedor_id = data.get('id')
    try:
        fornecedor = Fornecedor.objects.get(id=fornecedor_id)
        fornecedor.delete()
        return JsonResponse({'status': 'success'})
    except Fornecedor.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Fornecedor não encontrado'})

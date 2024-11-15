from django.shortcuts import render, redirect
from .models import Produto
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import login, authenticate
from django.contrib import messages

def home(request):
    return render(request, 'delivery/index.html')


# Função para exibir os produtos no menu
def menu(request):
    produtos = Produto.objects.all()  # Obtém todos os produtos do banco de dados
    return render(request, 'delivery/menu.html', {'produtos': produtos})


# Função para adicionar produtos ao carrinho utilizando sessões
def adicionar_ao_carrinho(request, produto_id):
    produto = Produto.objects.get(id=produto_id)

    # Se o carrinho não existir na sessão, cria um novo carrinho
    if 'carrinho' not in request.session:
        request.session['carrinho'] = {}

    # Obtém o carrinho da sessão
    carrinho = request.session['carrinho']

    # Se o produto ainda não estiver no carrinho, adiciona com quantidade 1
    if produto.id not in carrinho:
        carrinho[produto.id] = {'produto': produto.nome, 'quantidade': 1, 'preco': str(produto.preco)}
    else:
        # Caso o produto já esteja no carrinho, aumenta a quantidade
        carrinho[produto.id]['quantidade'] += 1

    # Atualiza o carrinho na sessão
    request.session['carrinho'] = carrinho

    # Redireciona para a página de menu
    return redirect('menu')


# Função para visualizar o carrinho

from django.shortcuts import render, redirect
from .models import Produto


def ver_carrinho(request):
    carrinho = request.session.get('carrinho', {})
    total = 0  # Inicializa o total

    # Verifica se foi feita uma requisição POST para excluir um item
    if request.method == 'POST':
        produto_id = request.POST.get('produto_id')  # Pega o id do produto enviado pelo formulário
        if produto_id and produto_id in carrinho:
            del carrinho[produto_id]  # Remove o produto do carrinho

        # Atualiza a sessão com o carrinho alterado
        request.session['carrinho'] = carrinho

        return redirect('ver_carrinho')  # Redireciona de volta para a página do carrinho

    # Cálculo do valor total do carrinho
    for produto_id, item in carrinho.items():
        total += float(item['preco']) * item['quantidade']

    return render(request, 'delivery/carrinho.html', {'carrinho': carrinho, 'total': total})


from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required


# Exemplo de view para finalizar o pedido
@login_required
def finalizar_pedido(request):
    # Acessando o carrinho da sessão
    carrinho = request.session.get('carrinho', {})

    # Aqui você pode adicionar a lógica de finalização de pedido
    if request.method == 'POST':
        # Se o usuário estiver logado, finaliza o pedido
        request.session['carrinho'] = {}  # Limpa o carrinho na sessão
        return render(request, 'delivery/confirmacao.html', {'mensagem': 'Pedido finalizado com sucesso!'})

    # Caso o usuário não esteja logado, redireciona para a página de login
    if not request.user.is_authenticated:
        return redirect('login_cliente')

    return render(request, 'delivery/finalizar_pedido.html')  # Página de finalização do pedido
# Função para login
def login_cliente(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            # Autentica o usuário
            user = form.get_user()
            login(request, user)
            # Redireciona para o carrinho após login
            return redirect('ver_carrinho')
        else:
            # Mensagem de erro caso o login falhe
            messages.error(request, "Usuário ou senha inválidos")
    else:
        form = AuthenticationForm()

    return render(request, 'delivery/login.html', {'form': form, 'register_form': UserCreationForm()})

# Função para cadastro de um novo cliente
def registrar_cliente(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            # Cria o novo usuário
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f"Conta criada para {username}!")
            return redirect('login_cliente')  # Redireciona para a página de login após criar a conta
        else:
            # Se houver erro, mostra uma mensagem de erro
            messages.error(request, "Erro ao criar a conta. Verifique os dados inseridos.")
    else:
        form = UserCreationForm()

    return render(request, 'delivery/login.html', {'form': AuthenticationForm(), 'register_form': form})
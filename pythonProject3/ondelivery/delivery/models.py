from django.db import models

class Produto(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField()
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    imagem = models.ImageField(upload_to='produtos/', null=True, blank=True)

    def __str__(self):
        return self.nome

# Simulação de um carrinho em memória (dicionário)
# Em uma aplicação real, você usaria o banco de dados ou sessões do usuário

def adicionar_ao_carrinho(request, produto_id):
    produto = Produto.objects.get(id=produto_id)
    if produto.id not in carrinho:
        carrinho[produto.id] = {'produto': produto, 'quantidade': 1}
    else:
        carrinho[produto.id]['quantidade'] += 1
    return redirect('menu')  # Redireciona para a página de menu
# delivery/models.py

from django.db import models

class Pedido(models.Model):
    STATUS_CHOICES = [
        ('P', 'Pendente'),
        ('A', 'Em andamento'),
        ('F', 'Finalizado'),
    ]

    cliente_nome = models.CharField(max_length=255)
    cliente_email = models.EmailField()
    cliente_telefone = models.CharField(max_length=15)
    endereco = models.CharField(max_length=255)
    forma_pagamento = models.TextField(help_text="Informa como vai pagar", blank=True, null=True)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='P')
    data_criacao = models.DateTimeField(auto_now_add=True)

    produtos = models.ManyToManyField(Produto, related_name='pedidos')

    def __str__(self):
        return f"Pedido {self.id} - {self.cliente_nome} - {self.status}"

    class Meta:
        ordering = ['-data_criacao']

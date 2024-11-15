# delivery/admin.py

from django.contrib import admin
from .models import Produto, Pedido

# Configuração para o modelo Produto
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'descricao', 'preco', 'imagem')
    search_fields = ('nome', 'descricao')
    list_filter = ('preco',)

# Configuração para o modelo Pedido
class PedidoAdmin(admin.ModelAdmin):
    list_display = ('id', 'cliente_nome', 'cliente_email', 'status', 'data_criacao', 'total')
    search_fields = ('cliente_nome', 'cliente_email', 'status')
    list_filter = ('status', 'data_criacao')
    readonly_fields = ('total', 'data_criacao')

    # Método para mostrar o total do pedido
    def total(self, obj):
        return sum([produto.preco for produto in obj.produtos.all()])
    total.short_description = 'Total'

# Registrar os modelos no admin
admin.site.register(Produto, ProdutoAdmin)
admin.site.register(Pedido, PedidoAdmin)


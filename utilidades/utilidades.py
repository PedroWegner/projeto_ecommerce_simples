def forma_preco(float):
    """
    funcao definida para formatar os precos do site, para aparecer a sigla do 
    real
    """
    return f'R$ {float:.2f}'.replace('.', ',')


def quantidade_total(carrinho):
    return sum([valor['quantidade'] for valor in carrinho.values()])


def compra_total(carrinho):
    return sum([item.get('preco_produto') for item in carrinho.values()])

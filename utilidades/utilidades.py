def forma_preco(float):
    """
    funcao definida para formatar os precos do site, para aparecer a sigla do 
    real
    """
    return f'R$ {float:.2f}'.replace('.', ',')

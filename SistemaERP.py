import pymysql.cursors
import matplotlib.pyplot as plt

conexao = pymysql.connect(
    host='localhost',
    user='root',
    password='',
    db='erp',
    charset='utf8mb4',
    cursorclass=pymysql.cursors.DictCursor)

autentico = False

def logarCadastrar():
    usuarioExistente = 0
    autenticado = False
    usuarioMaster = False

    if decisao == 1:
        nome = input('Digite seu nome: ')
        senha = input('Digite sua senha: ')
        for linha in resultado:
            if nome == linha['nome'] and senha == linha['senha']:
                if linha['nivel'] == 1:
                    usuarioMaster = False
                elif linha['nivel'] == 2:
                    usuarioMaster = True
                autenticado = True
                break
            else:
                autenticado = False
        if not autenticado:
            print('Email ou senha errada!')

    elif decisao == 2:
        print('Faça seu cadastro')
        nome = input('Digite seu nome: ')
        senha = input('Digite sua senha: ')
        for linha in resultado:
            if nome == linha['nome'] and senha == linha['senha']:
                usuarioExistente = 1
        if usuarioExistente == 1:
            print('Usuário já existe! Tente um nome ou senha diferente')
        elif usuarioExistente == 0:
            try:
                with conexao.cursor() as cursor:
                    cursor.execute('INSERT INTO cadastros(nome, senha, nivel) VALUES(%s, %s, 1)', (nome, senha))
                    conexao.commit()
                    print('Usuário cadastrado com sucesso!')
            except:
                print('Erro ao inserir os dados!')
    return autenticado, usuarioMaster

def cadastrarProdutos():
    nome = input('Digite o nome do produto: ')
    ingredientes = input('Digite os ingredientes do produto: ')
    grupo = input('Digite o grupo pertencente à esse produto: ')
    preco = float(input('Digite o preço do produto: R$'))

    try:
        with conexao.cursor() as cursor:
            cursor.execute('INSERT INTO produtos(nome, ingredientes, grupo, preco)  VALUES(%s, %s, %s, %s)', (nome, ingredientes, grupo, preco))
            conexao.commit()
            print('Produto cadastrado com sucesso!!')
    except:
        print('Erro ao inserir produtos no banco de dados!')

def listarProdutos():
    produtos = []
    try:
        with conexao.cursor() as cursor:
            cursor.execute('SELECT * FROM produtos')
            produtosCadastrados = cursor.fetchall()
    except:
        print('Erro ao conectar ao banco de dados!')
    for i in produtosCadastrados:
        produtos.append(i)
    if len(produtos) != 0:
        for i in range(0, len(produtos)):
            print(produtos[i])
    else:
        print('Nenhum produto cadastrado')

def excluirProduto():
    listarProdutos()
    idDeletar = int(input('Digite o id do produto que você deseja excluir: '))
    try:
        with conexao.cursor() as cursor:
            cursor.execute('DELETE FROM produtos WHERE id={}'.format(idDeletar))
            print('Produto deletado com sucesso!')
    except:
        print('Erro ao excluir o produto!')

def editarProduto():
    listarProdutos()
    idEditar = int(input('Digite o id do produto de você deseja editar: '))
    novoNome = input('Digite o novo nome do produto: ')
    novoIngredientes = input('Digite os novos ingredientes do produto: ')
    novoGrupo = input('Digite o novo grupo pertencente à esse produto: ')
    novoPreco = float(input('Digite o novo preço do produto: R$'))
    try:
        with conexao.cursor() as cursor:
            cursor.execute('UPDATE produtos SET nome="{}", ingredientes="{}", grupo="{}", preco={} WHERE id={}'.format(novoNome, novoIngredientes, novoGrupo, novoPreco, idEditar))
            print('Produto editado com sucesso!')
    except:
        print('Erro ao editar produto!')

def listarPedidos():
    pedidos = []
    decision = 0
    while decision != 2:
        pedidos.clear()

        try:
            with conexao.cursor() as cursor:
                cursor.execute('SELECT * FROM pedidos')
                listaPedidos = cursor.fetchall()
        except:
            print('Erro ao conectar ao banco de dados! ')

        for i in listaPedidos:
            pedidos.append(i)

        if len(pedidos) != 0:
            for i in range(0, len(pedidos)):
                print(pedidos[i])
        else:
            print('Não há nenhum pedido!')

        decision = int(input('[1] - Dar produto como entregue | [2] - Voltar\n'))

        if decision == 1:
            idDeletar = int(input('Digite o id do pedido entregue: '))
            try:
                with conexao.cursor() as cursor:
                    cursor.execute('DELETE FROM pedidos WHERE id={}'.format(idDeletar))
                    print('Produto dado como entregue!')
            except:
                print('Erro ao dar o pedido como entregue!')

def gerarEstatistica():
    nomeProdutos = []
    nomeProdutos.clear()

    try:
        with conexao.cursor() as cursor:
            cursor.execute('select * from produtos')
            produtos = cursor.fetchall()
    except:
        print('erro ao fazer consulta no banco de dados')

    try:
        with conexao.cursor() as cursor:
            cursor.execute('select * from estatisticaVendido')
            vendido = cursor.fetchall()
    except:
        print('erro ao fazer a consulta no banco de dados')


    estado = int(input('[0] - Sair | [1] - Pesquisar por nome | [2] - Pesquisar por grupo\n'))
    if estado == 1:
        decisao3 = int(input('[1] - Pesquisar por dinheiro | [2] - Pesquisar por quantidade unitária\n'))
        if decisao3 == 1:
            for i in produtos:
                nomeProdutos.append(i['nome'])

            valores = []
            valores.clear()

            for h in range(0, len(nomeProdutos)):
                somaValor = -1
                for i in vendido:
                    if i['nome'] == nomeProdutos[h]:
                        somaValor += i['preco']
                if somaValor == -1:
                    valores.append(0)
                elif somaValor > 0:
                    valores.append(somaValor+1)

            plt.plot(nomeProdutos, valores) # passa os eixos x e y no gráfico
            plt.xlabel('produtos')  # escreve no gráfico indicando o que é o eixo x
            plt.ylabel('quantidade vendida em reais') # escreve no gráfico indicando o que é o eixo y
            plt.show() # mostra o gráfico na tela

        if decisao3 == 2:
            grupoUnico = []
            grupoUnico.clear()

            try:
                with conexao.cursor() as cursor:
                    cursor.execute('select * from produtos')
                    grupo = cursor.fetchall()
            except:
                print('erro na consulta')

            try:
                with conexao.cursor() as cursor:
                    cursor.execute('select * from estatisticavendido')
                    vendidoGrupo = cursor.fetchall()
            except:
                print('erro na consulta')

            for i in grupo:
                grupoUnico.append(i['nome'])

            grupoUnico = sorted(set(grupoUnico))

            qntFinal = []
            qntFinal.clear()

            for h in range(0, len(grupoUnico)):
                qntUnitaria = 0
                for i in vendidoGrupo:
                    if grupoUnico[h] == i['nome']:
                        qntUnitaria += 1
                qntFinal.append(qntUnitaria)

            plt.plot(grupoUnico, qntFinal)
            plt.ylabel('quantidade unitaria vendida')
            plt.xlabel('produtos')
            plt.show()

    elif estado == 2:
        decisao3 = int(input('[1] - Pesquisar por dinheiro | [2] - Pesquisar por quantidade unitária\n'))
        if decisao3 == 1:
            for i in produtos:
                nomeProdutos.append(i['grupo'])

            valores = []
            valores.clear()

            for h in range(0, len(nomeProdutos)):
                somaValor = -1
                for i in vendido:
                    if i['grupo'] == nomeProdutos[h]:
                        somaValor += i['preco']
                if somaValor == -1:
                    valores.append(0)
                elif somaValor > 0:
                    valores.append(somaValor + 1)

            plt.plot(nomeProdutos, valores)  # passa os eixos x e y no gráfico
            plt.xlabel('produtos')  # escreve no gráfico indicando o que é o eixo x
            plt.ylabel('quantidade vendida em reais')  # escreve no gráfico indicando o que é o eixo y
            plt.show()  # mostra o gráfico na tela

        if decisao3 == 2:
            grupoUnico = []
            grupoUnico.clear()

            try:
                with conexao.cursor() as cursor:
                    cursor.execute('select * from produtos')
                    grupo = cursor.fetchall()
            except:
                print('erro na consulta')

            try:
                with conexao.cursor() as cursor:
                    cursor.execute('select * from estatisticavendido')
                    vendidoGrupo = cursor.fetchall()
            except:
                print('erro na consulta')

            for i in grupo:
                grupoUnico.append(i['grupo'])

            grupoUnico = sorted(set(grupoUnico))

            qntFinal = []
            qntFinal.clear()

            for h in range(0, len(grupoUnico)):
                qntUnitaria = 0
                for i in vendidoGrupo:
                    if grupoUnico[h] == i['grupo']:
                        qntUnitaria += 1
                qntFinal.append(qntUnitaria)

            plt.plot(grupoUnico, qntFinal)
            plt.ylabel('quantidade unitaria vendida')
            plt.xlabel('produtos')
            plt.show()

while not autentico:
    decisao = int(input('[1] - Login | [2] - Cadastrar\n'))

    try:
        with conexao.cursor() as cursor:
            cursor.execute('SELECT * FROM cadastros')
            resultado = cursor.fetchall()
    except:
        print('Erro ao conectar o banco de dados')

    autentico, usuarioSupremo = logarCadastrar()


if autentico == True:
    print('Autenticado')

    if usuarioSupremo == True:
        decisaoUsuario = 1

        while decisaoUsuario != 0:
            decisaoUsuario = int(input('[0] - Sair | [1] - Cadastrar Produtos | [2] - Listar Produtos | [3] - Excluir Produto | [4] - Editar Produto | [5] - Listar Pedidos | [6] - Visualizar as estatísticas\n'))
            if decisaoUsuario == 1:
                cadastrarProdutos()
            elif decisaoUsuario == 2:
                listarProdutos()
            elif decisaoUsuario == 3:
                excluirProduto()
            elif decisaoUsuario == 4:
                editarProduto()
            elif decisaoUsuario == 5:
                listarPedidos()
            elif decisaoUsuario == 6:
                gerarEstatistica()
            else:
                print('Digite uma opção válida!')
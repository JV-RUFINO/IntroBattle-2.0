from sys import path as caminho
from pathlib import Path as Caminhozão

arquivo = Caminhozão(__file__).resolve()
parente , raiz = arquivo.parent, arquivo.parents[1]
caminho.append(str(raiz))

try:
    from repetidor                         import repetidor_de_func
except ModuleNotFoundError:
    from codigo_compartilhado.repetidor    import repetidor_de_func


" === CÓDIGO REAL === "


@repetidor_de_func( hablitar_func = False )
def acao_classe( classe , *args , **kwargs ):
    funcao_expecifica = eval( 'classe' + '.' + args[0] )

    funcao_expecifica( args[1] )


" === TESTE === "


if __name__ == '__main__':
    class A:
        def __init__( self , nome ):
            self.nome = nome

        def printar_nome( self , extra ):
            print( self.nome + ' ' + extra )

    acao_classe( [ A('A') , A('B') , A('C') ] ,'printar_nome' , 'extra' )

from sys import path as caminho
from pathlib import Path as Caminhozão

arquivo = Caminhozão(__file__).resolve()
parente , raiz = arquivo.parent, arquivo.parents[1]
caminho.append(str(raiz))

try:
    from repetidor                          import repetidor_de_func
except ModuleNotFoundError:
    from codigo_compartilhado.repetidor     import repetidor_de_func


" === CÓDIGO REAL === "


@repetidor_de_func( filter )
def filtrar_classe( classe , func_extra , *args , **kwargs ):
    return classe


" === TESTE === "


if __name__ == '__main__':
    class A:
        def __init__( self , nome ):
            self.nome = nome


    print( filtrar_classe( [ A('A') , A('A') , A('C') ] , lambda x: x.nome == 'A' ) )
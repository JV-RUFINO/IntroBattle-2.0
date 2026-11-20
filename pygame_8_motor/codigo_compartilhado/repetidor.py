from sys import path as caminho
from pathlib import Path as Caminhozão

arquivo = Caminhozão(__file__).resolve()
parente , raiz = arquivo.parent, arquivo.parents[1]
caminho.append(str(raiz))

'''
OBJETIVO: 
        Criar um decorador que repita a execução de uma função para cada classe em um conjunto de classes, 
        permitindo a passagem de argumentos adicionais e a escolha do tipo de iteração (como map ou filter). 
        O decorador também permite habilitar ou desabilitar a função extra que será aplicada às classes.
'''

def repetidor_de_func( tipo = map , hablitar_func : bool = True):
    def dec(func):
        if hablitar_func:
            def wrapper( conjunto_classes , func_extra , *args , **kwargs ):
                r = []
                for classe in tipo( func_extra , conjunto_classes ):
                    r.append( func( classe , func_extra , *args , **kwargs ) )

                return r
        else:
            def wrapper( conjunto_classes , *args , **kwargs ):
                r = []
                for classe in tipo( lambda x:x ,conjunto_classes ):
                    r.append( func( classe , *args , **kwargs ) )

                return r

        return wrapper
    return dec
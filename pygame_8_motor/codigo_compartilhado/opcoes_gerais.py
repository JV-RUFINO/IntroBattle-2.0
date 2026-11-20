from sys import path as caminho
from pathlib import Path as Caminhozão

arquivo = Caminhozão(__file__).resolve()
parente , raiz = arquivo.parent, arquivo.parents[1]
caminho.append(str(raiz))

# IMPORTAÇOES GERAIS
from abc             import ABC , abstractmethod


"=== CÓDIGO REAL ==="


class Opcoes_Geral(ABC):
    def __init__( _ , original : ...):
        _.original      = original
        _.moldavel      = _.original_reproduzida

        _.alternativo   = False

    @property
    @abstractmethod
    def original_reproduzida( _ ) -> ...:
        ...

    @abstractmethod
    def resetar( _ ):
        ...

    def __call__( _ ):
        ...

    def __repr__( _ ) -> str:
        return f"{type(_).__name__}( original = {_.original} , moldavel = {_.moldavel} , alternativo = {_.alternativo} )"


"=== TESTES ==="


if __name__ == "__main__":
    ...

    
      

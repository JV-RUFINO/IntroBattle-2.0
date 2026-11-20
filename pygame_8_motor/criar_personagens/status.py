from sys import path as caminho
from pathlib import Path as Caminhozão

arquivo = Caminhozão(__file__).resolve()
parente , raiz = arquivo.parent, arquivo.parents[1]
caminho.append(str(raiz))


# EXTERIOR
from codigo_compartilhado        import Stat
from codigo_compartilhado        import Condicao

from codigo_compartilhado        import Linkzin
from codigo_compartilhado        import Imagem_Opcoes

# IMPORTAÇÕES GERAIS
from abc                    import ABC , abstractmethod 
from os                     import getcwd


'=== CÓDIGO REAL ==='


class Status(ABC):
    def __init__( _ , numero : int ):
        _.caminho  : str      = Linkzin(getcwd(),'banco_dados','Icones','Representadores')
        _.condicao : Condicao = Condicao.Estavel

        _.__conteudo = [ numero , numero ]

    @property
    def numero( _ ) -> int:
        return _.__conteudo[0]

    @numero.getter
    def backup( _ ) -> int:
        return _.__conteudo[1]

    @numero.setter
    def numero( _ , novo_numero) -> int:
        if novo_numero >= len(_.niveis_status):
            novo_numero = len(_.niveis_status) - 1
        elif novo_numero < 0:
            novo_numero = 0

        nova_condicao = Condicao.Estavel
        if novo_numero   > _.backup:
            nova_condicao = Condicao.Buffado
        elif novo_numero < _.backup:
            nova_condicao = Condicao.Nerfado

        _.__conteudo[0] = novo_numero
        _.condicao      = nova_condicao

    @staticmethod
    @abstractmethod
    def TIPO() -> Stat:
        ...

    @property
    @abstractmethod
    def niveis_status( _ ) -> list[ str , str , str , str , str ]:
        return [ 'muito_baixa' , 'baixa' , 'media' , 'alta' , 'muito_alta' ]

    @property
    @abstractmethod
    def mostrar_imagem( _ ) -> Imagem_Opcoes:
        return Imagem_Opcoes( Linkzin( _.caminho , _.niveis_status[_.numero] + '.png' ) )
    
    @abstractmethod
    def resetar_status( _ ) -> int:
        _.numero = _.backup

        return _.numero

    def __eq__( _ , objeto) -> bool:
        if type(objeto) == int:
            return True if objeto == _.numero else False
        elif type(objeto) == Status:
            return True if objeto == _ else False 

    def __add__( _ , numero: int):
        _.numero += numero 

    def __sub__( _ , numero: int):
        _.numero -= numero

    def __int__( _ ):
        return _.numero

    def __repr__( _ ) -> str:
        return f'{type(_).__name__}(status = {_.condicao} & numero = {_.numero})'

    
'=== TESTES ==='


if __name__ == "__main__":
    ...
    
    
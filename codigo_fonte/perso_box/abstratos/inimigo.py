from sys import path as caminho
from pathlib import Path as Caminhozão

arquivo = Caminhozão(__file__).resolve()
parente , raiz = arquivo.parent, arquivo.parents[1]
caminho.append(str(raiz))


# ESSENCIAIS
from box_exterior                import Perso

# PERSONAGEM
from motor_exterior                 import Personagem 

try:
    from introbattle_perso          import Perso_geral
except ModuleNotFoundError:
    from .introbattle_perso         import Perso_geral

# STATUS
from box_exterior                   import Status

# PYGAME
from pygame                         import Surface  as Superficie 


'=== CÓDIGO REAL ==='


class Inimigo(Perso_geral):
    def __init__( _ , classe_inimiga : tuple[str] , posicao_roteiro : tuple[str] , coordenadas: tuple[int, int] = [0, 0] ):
        if type(classe_inimiga) == str:
            classe_inimiga = (classe_inimiga,)
        if type(posicao_roteiro) == str:
            posicao_roteiro = (posicao_roteiro,)

        super().__init__( ( "inimigos" , *classe_inimiga ) , ( 1 , *posicao_roteiro ) , None , coordenadas )

        _.todas_falas = None

    @staticmethod
    def TIPO( ) -> Perso:
        return None

    @property
    def magia_imagem( _ ):
        return None

    @property
    def dano_magia( _ ) -> int:
        return None

    def adcionar_status( _ , classe_status : Status , chave_str: tuple ):
        return super().adcionar_status( classe_status , chave_str )

    def retorna_path( _ , caminho_desejado : tuple[str] ) -> list:
        return super().retorna_path( caminho_desejado )
    
    def adc_img( _ , conjunto_caminhos : tuple[Caminhozão] , chaves = None ) -> dict:
        return super().adc_img( conjunto_caminhos , chaves )

    def reducao_dano( _ , dano_recebido : int ) -> int: # aplicando DEFESA sobre o dano recebido
        return super().reducao_dano( dano_recebido )

    def buff_debuff( _ , efeito , buff = True ):
        return super().buff_debuff( efeito , buff )

    def ataque_basico( _ , alvo: Personagem): # ataca o alvo .Conta apenas o ATAQUE
        return super().ataque_basico( alvo )

    def mostrar_animacao(_, screen: Superficie, escala: tuple = None):
        return super().mostrar_animacao(screen, escala)

    def __hash__(_) -> int:
        return super().__hash__()

    def __sub__( _ , valor: ...):
        super().__sub__( valor )

    def __add__( _ , valor: ...):
        super().__add__( valor )

    def repr_inimigo( _ , genero : str , texto_convencional: str , texto_derrota: str ):
        return super().repr_personagem( f'{genero} {texto_convencional}' , f'{texto_derrota} :)' , ( f"Derrote-{genero.lower()}!" , "De pé.Continue atacando!" ))
       
        

'=== TESTES ==='


if __name__ == "__main__":
    a = Inimigo( "caveira" , "E" )

    print(a.imagens)

    

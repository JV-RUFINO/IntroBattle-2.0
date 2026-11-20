from sys import path as caminho
from pathlib import Path as Caminhozão


arquivo = Caminhozão(__file__).resolve()
parente , raiz = arquivo.parent, arquivo.parents[1]
caminho.append(str(raiz))


# EXTERIOR
from box_exterior                import Perso
from box_exterior                import Linkzin

# PERSONAGEM
from motor_exterior                 import Personagem 

try:
    from introbattle_perso          import Perso_geral
except ModuleNotFoundError:
    from .introbattle_perso         import Perso_geral

# STATUS
from box_exterior                   import Status

# MAGIAS
from box_exterior                   import Magias

# PYGAME
from pygame                         import Surface  as Superficie , Color as Cor

# IMPORTAÇÕES GERAIS
from os                             import getcwd
from json                           import load     as carregar_json


'=== CÓDIGO REAL ==='


class Aliado(Perso_geral):
    def __init__( _ , classe_aliada : tuple[str] , posicao_roteiro : tuple[str] , magia : Magias , coordenadas: tuple[int, int] = [0, 0]):
        if type(classe_aliada) == str:
            classe_aliada = (classe_aliada,)
        if type(posicao_roteiro) == str:
            posicao_roteiro = (posicao_roteiro,)

        super().__init__( ( "aliados" , *classe_aliada ) , ( 0 , *posicao_roteiro ) , magia , coordenadas )

        # DIALOGOS DO PERSONAGEM
        with open(Linkzin( getcwd() , 'roteiro' , 'dialogos_perso.json' ) , 'r' , encoding= "utf-8" ) as status:
            _.todas_falas = carregar_json(status)[0]

        for posicao in posicao_roteiro:
            _.todas_falas = _.todas_falas[posicao]

    @staticmethod
    def TIPO( ) -> Perso:
        return None

    @property
    def magia_imagem( _ ):
        return _.magias()

    @property
    def dano_magia( _ ) -> int:
        'return super().dano_magia'
        _.magias.dano_magia( _.STATUS )
    
    def adcionar_status( _ , classe_status: Status , chave_str: tuple ):
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

    def falar( _ , frase: str, cor: tuple): # abre a caixa de texto e faz o personagem falar
        ...

    def dialogo_combate( _ , cor = Cor( 0 , 100 , 0 ) ):
        return _.falar( _.todas_falas , cor )

    def magia( _ , alvo: Personagem):
        return super().magia( alvo )

    def mostrar_animacao(_, screen: Superficie, escala: tuple = None):
        return super().mostrar_animacao(screen, escala)

    def __hash__(_) -> int:
        return super().__hash__()

    def __sub__( _ , valor: ...):
        super().__sub__( valor )

    def __add__( _ , valor: ...):
        super().__add__( valor )

    def repr_aliado( _ , genero : str , texto_convencional: str , nome_derrota: str ):
        return super().repr_personagem( f'{genero} {texto_convencional}' , f'{genero} {nome_derrota} caiu :(' , ( "Saudavel!" , f"Ferid{genero.lower()}, mas de pé!" ))
        

'=== TESTES ==='


if __name__ == "__main__":
    A = Aliado( "paladino" , "P" , 0 )

    '''A + Vida( 1 )
    A - Ataque( 1 )
    A + Defesa( 1 )

    print(A.STATUS)'''

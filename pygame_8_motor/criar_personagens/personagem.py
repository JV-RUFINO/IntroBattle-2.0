from __future__ import annotations

from sys import path as caminho
from pathlib import Path as Caminhozão

arquivo = Caminhozão(__file__).resolve()
parente , raiz = arquivo.parent, arquivo.parents[1]
caminho.append(str(raiz))


# EXTERIOR
from codigo_compartilhado    import Projetil
from codigo_compartilhado    import Imagem_Opcoes
from codigo_compartilhado    import Linkzin

try:
    from magias              import Magias
    from status              import Status
except ImportError:
    from .magias             import Magias
    from .status             import Status

# PYGAME
from pygame                 import Surface  as Superficie , Color as Cor
from pygame.image           import load     as carregar_imagem

# IMPORTAÇÕES GERAIS
from json                   import load     as carregar_json
from abc                    import ABC , abstractmethod


'=== CÓDIGO REAL ==='


class Personagem(ABC):
    '### Classe abstrata que representa um personagem do jogo. ###'
    def __init__( _ , coordenadas : tuple[ int , int ] = [ 0 , 0 ] ):
        ''' EXEMPLO DE CAMINHO IMAGENS
        [   
            ["banco_dados","Personagens"],
            ".png",
            {
                "aliados":  {
                    "paladino"          : ["down","escolhivel","idle","selecionada"],
                    "wizard"            : ["down","escolhivel","idle","selecionada"],
                    "hunter"            : ["down","escolhivel","idle","selecionada"],
                    "curandeiro"        : ["down","escolhivel","idle","selecionada"],
                    "rougue 2nd version": ["down","escolhivel","idle","selecionada"]
                },
                "inimigos": {
                    "caveira"           : ["down","escolhivel","idle","selecionada"],
                    "Lady Medusa"       : ["down","escolhivel","idle","selecionada"]
                }}
        ]
        '''

        ''' EXEMPLO DE CAMINHO STATUS
        [{
            "C":{ 
                "ATAQUE"    : 2 ,
                "DEFESA"    : 2 ,
                "VELOCIDADE": 2 , 
                "CARGA"     : 2 ,
                "VIDA"      : 2
            },
            "P":{
                "VIDA"      : 4 ,
                "ATAQUE"    : 2 ,
                "DEFESA"    : 4 ,
                "VELOCIDADE": 0 , 
                "CARGA"     : 0 
            },
            ...},
            
            {
            "E":{
                "VIDA"      : 1 ,
                "ATAQUE"    : 1 ,
                "DEFESA"    : 0 ,
                "VELOCIDADE": 1 , 
                "CARGA"     : 0 
            },

            "B":{
                "VIDA"      : 4 ,
                "ATAQUE"    : 4 ,
                "DEFESA"    : 4 ,
                "VELOCIDADE": 4 , 
                "CARGA"     : 4 
            },
            ...}]
        '''

        # posicao do personagem na tela
        _.coordenadas : list[ int , int ] = list(coordenadas)


        # caminho que a classe usa para procurar os scripts/roteiros necessarios para carregar as imagens e status do personagem
        _.caminho_imagens = ( 'roteiro' , 'caminho_imagens.json' )
        _.caminho_status  = ( 'roteiro' , 'status_personagens.json' )

        # IMAGENS DO PERSONAGEM
        _.imagens : dict[ Imagem_Opcoes ] = {}

        # STATUS DO PERSONAGEM
        _.status  : dict[ Status ]        = {}

        # MAGIAS / HABS
        _.magias : Magias   = ...

        # estado do personagem (Idle , Down , Escolhivel , Selecionada)
        _.estado_atual      = ...

        # vida do personagem
        _.vida   : int      = ...

    @staticmethod
    @abstractmethod
    def TIPO( ) -> ...:
        '* retorna um enumerador que representa o personagem (soldado ,mago , dragao , etc)'
        ...

    @staticmethod
    @abstractmethod
    def cor_assinatura( ) -> Cor:
        '* retorna a cor que representa o personagem (soldado ,mago , dragao , etc)'
        ...

    @property
    @abstractmethod
    def escala( _ ) -> dict:
        if _.imagens == {}:
            return None
        else:
            return _.imagens[ list(_.imagens.keys())[0] ].dimensoes

    @escala.setter
    @abstractmethod
    def escalar_imagens( _ , nova_escala : tuple[int,int] ):
        for imagem in _.imagens:
            resultado : Imagem_Opcoes = _.imagens[imagem]

            resultado.dimensoes = nova_escala

    @property
    @abstractmethod
    def imagem_atual( _ ) -> Imagem_Opcoes:
        '* retorna a imagem atual do personagem seguindo o estado atual'
        return _.imagens[_.estado_atual]

    @property
    @abstractmethod
    def magia_imagem( _ ) -> ...:
        '* retorna a imagem da magia do personagem'
        return None

    @property
    @abstractmethod
    def STATUS( _ ) -> dict:
        '* retorna todos os status do personagem'
        return _.status

    @property
    @abstractmethod
    def dano_basico( _ ) -> int:
        '* retorna o dano mais comum que o personagem pode causar'
        #'return int( _.ATAQUE )'
        ...

    @property
    @abstractmethod
    def dano_magia( _ ) -> int:
        '* retorna o dano da magia do personagem'
        #'return _.magias.dano_magia( _.STATUS )'
        ...

    @property
    @abstractmethod
    def calculo_VidaTotal( _ ):
        '* retorna o cálculo da vida total do personagem'
        #'return int(_.VIDA) + 1'
        ...

    @abstractmethod
    def adcionar_status( _ , novo_status: Status , chave_str: tuple , nome_status : ... ) -> Status:
        '* adiciona um novo status para o personagem, carregando os valores do arquivo JSON de status'
        # self.adcionar_status( Exemplo , ( "E" , "EXEMPLO" ) , "Hello" )
        # -> { "Hello" : Exemplo( valores do json com base no _.caminho_status  e ( "E" , "EXEMPLO" ) ) }
        with open(Linkzin( *_.caminho_status , act_dir= True ) , 'r' ) as status:
            resultado = carregar_json(status) 
        
        for nn in chave_str:
            resultado = resultado[nn]

        novo_status = novo_status( resultado )

        _.status.update( { nome_status : novo_status } )

        return novo_status # Exemplo( resultado )

    @abstractmethod
    def retorna_path( _ , caminho_desejado : tuple[str] ) -> list:
        '* retorna uma lista de caminhos para as imagens do personagem, com base no arquivo JSON de caminho_imagens'
        with open( Linkzin( *_.caminho_imagens , act_dir=True ) , 'r' ) as status:
            resultado = carregar_json(status)

            cc               : tuple[str] = tuple(resultado[0]) # Exemplo : ( 'banco_dados' , 'Personagens' )
            tipo_imagem      : str        = resultado[1]        # Exemplo : '.png'
            conjunto_imagens : dict       = resultado[2]        # Exemplo : {"aliado": { "paladino": ["down" , "idle", ...]}}

        info = caminho_desejado
        for caminho in caminho_desejado:
            conjunto_imagens = conjunto_imagens[caminho] 
        # Exemplo : ["down" , "idle", ...]

        for numero in range(len(conjunto_imagens)):
            conjunto_imagens[numero] = Linkzin( *cc , *info , conjunto_imagens[numero] + tipo_imagem , act_dir = True )
        # ['...\\Exemplo\\banco_dados\\Personagens\\aliados\\paladino\\down.png', 
        #       '...\\Exemplo\\banco_dados\\Personagens\\aliados\\paladino\\escolhivel.png', 
        #           '...\\Exemplo\\banco_dados\\Personagens\\aliados\\paladino\\idle.png', 
        #               '...\\Exemplo\\banco_dados\\Personagens\\aliados\\paladino\\selecionada.png']

        return [Caminhozão(img) for img in conjunto_imagens]
        # [WindowsPath('Exemplo/banco_dados/Personagens/aliados/paladino/down.png'), 
        #       WindowsPath('Exemplo/banco_dados/Personagens/aliados/paladino/escolhivel.png'), 
        #               WindowsPath('Exemplo/banco_dados/Personagens/aliados/paladino/idle.png'), 
        #                       WindowsPath('Exemplo/banco_dados/Personagens/aliados/paladino/selecionada.png')]

    @abstractmethod
    def adc_img( _ , caminho_fornecido : tuple[str] , estado_img ) -> dict:
        '* adciona uma quantidade n de imagem para o personagem, com base no caminho fornecido'
        for numero in range(len(caminho_fornecido)):
            chave = caminho_fornecido if estado_img == None else estado_img

            _.imagens.update({ chave[numero] : Imagem_Opcoes( carregar_imagem( caminho_fornecido[numero] ) ) })
            # Exemplo : { <Estado.Down: 4>: Imagem_Opcoes( ... ) }

        return _.imagens
        # Exemplo : {
        #   <Estado.Down: 4>: Imagem_Opcoes( ... ), 
        #       <Estado.Escolhivel: 2>: Imagem_Opcoes( ... ), 
        #               <Estado.Idle: 1>: Imagem_Opcoes( ... ), 
        #                       <Estado.Selecionada: 3>: Imagem_Opcoes( ... )}

    @abstractmethod
    def reducao_dano( _ , dano_recebido : int , reducao_dano : int ) -> int: # aplicando DEFESA sobre o dano recebido
        '* aplica uma reducao de dano sobre o dano recebido'
        dano_real = dano_recebido - reducao_dano

        if dano_real < 1:
            dano_real = 1 # dano nunca menor que 0

        return dano_real

    @abstractmethod
    def buff_debuff( _ , efeito : Status , buff = True) -> Status:
        '* aplica um buff ou debuff sobre o personagem, alterando os valores do status'
        for status in _.STATUS:
            if type(efeito) == type(_.STATUS[status]):
                st_desalmado : Status = _.STATUS[status]
                
                st_desalmado.numero = st_desalmado.numero + int(efeito) if buff else st_desalmado.numero - int(efeito) 

                return st_desalmado
        
        return efeito

    @abstractmethod
    def ataque_basico( _ , alvo: Personagem): # ataca o alvo .Conta apenas o ATAQUE
        '* aplica o ataque basico do personagem sobre o alvo / outro Personagem'
        alvo - _.dano_basico

        return ( None , _.dano_basico )

    @abstractmethod
    def magia( _ , alvo: Personagem) -> Projetil:
        '* aplica a magia do personagem sobre o alvo / outro Personagem'
        alvo - _.dano_magia
        _.magias.aplicar_efeitos( _ , alvo ) # faça você mesmo!

        return ( Projetil , _.dano_magia )
    
    @abstractmethod
    def falar( _ , frase: str, cor: tuple): # abre a caixa de texto e faz o personagem falar
        '* abre a caixa de texto e faz o personagem falar'
        ...

    @abstractmethod
    def mostrar_animacao( _ , screen: Superficie , escala: tuple = None):
        '* mostra a animação do personagem na tela, com base no estado atual e na escala fornecida'
        if escala != None:
            _.escalar_imagens = escala
        
        return _.imagem_atual.printar_imagem( screen , _.coordenadas )

    def __hash__(_) -> int:
        return super().__hash__()

    @abstractmethod
    def __sub__( _ , valor ):
        ...

        return _

    @abstractmethod
    def __add__( _ , valor ):
        ...
            
        return _

    def __textinho_adcional(_, con):
        reportar_status = ""

        for status in _.STATUS:
            if _.STATUS[status].condicao == con:
                reportar_status += f"{status}"
                reportar_status += " , "
        
        return reportar_status[:-3] 

    @abstractmethod
    def repr_personagem( _ , print_convencional : str , para_derrota : str , vida_status : tuple ):
        ...


'=== TESTES ==='


if __name__ == "__main__":
    caminho = Caminhozão(__file__).resolve().parent.parent / 'roteiro' / 'caminho_imagens.json'

    '''with open(caminho , 'r' ) as status:
        resultado = carregar_json(status)

        cc               : tuple[str] = tuple(resultado[0]) # Exemplo : ( 'banco_dados' , 'Personagens' )
        tipo_imagem      : str        = resultado[1]        # Exemplo : '.png'
        conjunto_imagens : dict       = resultado[2]        # Exemplo : {"aliado": { "paladino": ["down" , "idle", ...]}}

    print(caminho)'''


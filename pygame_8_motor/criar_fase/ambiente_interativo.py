from __future__ import annotations

from sys import path as caminho
from pathlib import Path as Caminhozão

arquivo = Caminhozão(__file__).resolve()
parente , raiz = arquivo.parent, arquivo.parents[1]
caminho.append(str(raiz))

# COMPARTILHADO 
from codigo_compartilhado import Imagem_Opcoes as IOp

# PARENTE
try:
    from micro_cena                 import Micro_Cena           as MC
    from rolo_cenas                 import Rolo_Cenas           as RC
    from rodar_cenas                import Rodar_Cenas          as RR
except ModuleNotFoundError:
    from .micro_cena                 import Micro_Cena           as MC
    from .rolo_cenas                 import Rolo_Cenas           as RC
    from .rodar_cenas                import Rodar_Cenas          as RR
    
# ESSENCIAIS
from codigo_compartilhado    import Linkzin

# PYGAME
import pygame
from pygame             import Surface          as Superficie , KEYDOWN as TECLA_SEGURADA , KEYUP as TECLA_APERTADA , K_LEFT as ESQUERDA , K_RIGHT as DIREITA , K_RETURN as ENTER
from pygame.image       import load             as carregar_imagem
from pygame.event       import Event            as Evento 
from pygame             import Clock            as Relogio

# IMPORTAÇÕES GERAIS
from os import getcwd
from json import load as carregar_json


' === CÓDIGO REAL === '


class Criar_Fase:
    '### Decorador que transforma funções em Ambientes Interativos'
    def __init__( _ , *background: str , centralizar = True , ev_chave = None , ev_tipo = None , caminho_comum = True , tipo = ".png" , fps_limit = 60 , auto_X = True ):
        cc            = "" if caminho_comum == False else Ambiente_Interativo.caminho_comum()

        _.background  = IOp(carregar_imagem( Linkzin( cc , *background ) + tipo )) #
        _.centralizar = centralizar

        _.fps_limit   = fps_limit
        _.auto_X      = auto_X

        _.ev_chave , _.ev_tipo = ev_chave , ev_tipo

    def criar_MC( _ , funcao : function , posicao : int ):
        # O primeiro MC tem posição 0
        return MC( funcao , _.background , posicao , _.ev_chave , _.ev_tipo )

    def __call__(_ , funcao):
        '''
        receber_screen -> argumento auto-inserido pelo decorador. É a Surface do pygame
        novo_evento    -> evento(EX: teclado do jogador) capturado. Pode ser util para a fase
            EX: () = nenhum evento
            EX: (pygame.K_ENTER) -> jogador pressionou o ENTER
        TODA FASE DEVE RETORNAR TRUE OU FALSE
        '''

        return Ambiente_Interativo( RC( _.criar_MC( funcao , 0 ) ) , _.centralizar , _.fps_limit , _.auto_X  )

class Adicionar_Fase(Criar_Fase):
    '### Decorador que Adciona mais uma micro cena a outro Ambiente Interativo'
    def __init__( _ , *background: str, fonte: Ambiente_Interativo , ev_chave = None , ev_tipo = None, caminho_comum=True, tipo= ".png" ):
        super().__init__( *background , 
                                caminho_comum = caminho_comum , tipo = tipo , 
                                    ev_chave= ev_chave , ev_tipo= ev_tipo ,
                                        fps_limit = fonte.fps_limit , auto_X = fonte.auto_X )

        _.fonte  = fonte

    def __call__( _ , funcao ) -> Ambiente_Interativo:
        _.fonte.fases_normais + _.criar_MC( funcao , len( _.fonte.fases_normais ) )

        return _.fonte
    
class Adicionar_Auxiliar:
    '### Decorador especalizado para fases auxiliares'
    def __init__( _ , chave: int , tipo: int , fonte: Ambiente_Interativo ):
        _.chave = chave
        _.tipo  = tipo
        _.fonte = fonte

    def criar_MC( _ , funcao : function ):
        # O primeiro MC tem posição 0
        return MC( funcao , None , len( _.fonte.auxiliares ) , ev_chave = _.chave , ev_tipo = _.tipo )

    def __call__( _ , funcao : function ) -> Ambiente_Interativo:
        _.fonte.auxiliares + _.criar_MC( funcao )

        return _.fonte


class Ambiente_Interativo(RR):
    '### Transforme funções em fases pygame!'
    def __init__( _ , fases : RC , centralizar = True , fps_limit : int = 60 , auto_X = True ):
        super().__init__( fases )

        _.fps_limit   : int     = fps_limit
        _.auto_X      : bool    = auto_X
        _.relogio     : Relogio = Relogio()
        _.centralizar : bool    = centralizar

    @staticmethod
    def caminho_comum():
        return Linkzin( getcwd() , 'banco_dados' , 'Cenarios' )

    def Fase_Adicional( _ , *background: str , ev_chave = None , ev_tipo = None, caminho_comum = True , tipo = ".png" ):
        def Second_Decorator( funcao_extra : function ):
            @Adicionar_Fase( *background , fonte= _ , ev_chave= ev_chave , ev_tipo= ev_tipo , caminho_comum= caminho_comum , tipo= tipo )
            def Third_Last( *args , **kwargs ) -> bool:
                result = funcao_extra( *args , **kwargs )

                return result

            return Third_Last
        
        return Second_Decorator

    def Fase_Auxiliar( _ , evento : int = None , tipo_evento = TECLA_APERTADA ):
        def Second( funcao_extra: function ):
            @Adicionar_Auxiliar( evento , tipo_evento , _ )
            def Third( *args , **kwargs ):
                result = funcao_extra( *args , **kwargs )
                
                return result

            return Third
        
        return Second

    def criacao_fase( _ , receber_screen : Superficie , info_extra = None ) -> None:
        '* parte especializada em criar a fase'
        if len(_.auxiliares) > 0:
            _.auxiliar( receber_screen , info_extra , _.ultimo_evento )

        _.running = _.rodar_tradicional( receber_screen , info_extra , _.ultimo_evento ) 

        if _.centralizar:
            _.running = _.retornar_origem( _.running )
        
        pygame.display.flip()

    def rodar_corrente( _ , receber_screen : Superficie , info_extra = None ):
        '* provém um game loop pra fase'
        # receber_screen -> superficie pygame
        # info_extra     -> pode ser qualquer coisa, como por exemplo, um objeto de jogador, ou um objeto de inimigo, ou um objeto de fase, etc. É apenas um argumento extra que pode ser passado para as fases.'
        # novo_evento    -> caso o jogador queira inserir a lista de eventos

        while _.running:
            _.ultimo_evento = _.novo_evento( )

            # FASE SENDO CRIADA

            _.criacao_fase( receber_screen , info_extra )
            
            # FASE SENDO CRIADA

            if _.auto_X:
                _.running = _.AUTO_X( _.ultimo_evento , _.running )

            _.relogio.tick( _.fps_limit )  # limits FPS to 60
        
        return _.ultimo_evento

    def chamar_ambiente( _ , receber_screen : Superficie , info_extra = None ) -> bool:
        '* redmenciona o background , reseta e roda a corrente'
        
        _.fases_normais.redimencionar_backg_all( receber_screen )
        
        _.resetar_corrente()

        resultado = _.rodar_corrente( receber_screen , info_extra )
        
        return resultado

    def __call__( _ , receber_screen : Superficie , info_extra = None , parente : RC = None , novo_evento: list = None ):
        '''
        receber_screen -> argumento auto-inserido pelo decorador. É a Surface do pygame
        novo_evento    -> evento(EX: teclado do jogador) capturado. Pode ser util para a fase
            EX: () = nenhum evento
            EX: (pygame.K_ENTER) -> jogador pressionou o ENTER
        TODA FASE DEVE RETORNAR TRUE OU FALSE
        '''
        
        return _.chamar_ambiente( receber_screen , info_extra )

    
' === TESTES === '


if __name__ == '__main__':
    import pygame
    from os                     import getcwd
    from pygame.event           import get      as capturar_evento
    from pygame.time            import Clock    as Relogio
    from codigo_compartilhado   import Linkzin
    from pygame.image           import load     as carregar_imagem 
    from pygame                 import Surface  as Superficie , KEYDOWN as TECLA_SEGURADA , KEYUP as TECLA_APERTADA , K_LEFT as ESQUERDA , K_RIGHT as DIREITA , K_RETURN as ENTER

    # pygame setup
    pygame.init()
    screen = pygame.display.set_mode((1280, 720))

    @Criar_Fase( "salão" )
    def fase(
        screen :Superficie, 
            info_extra : ...        = None,
                parente : Ambiente_Interativo       = None,
                    eventos:list    = None):
        
        for evento in eventos:
            if evento.type == TECLA_SEGURADA:
                if evento.key == ENTER:
                    print('Entrou na fase 2')
                    parente.index = 1

        print(eventos)

        return True

    @fase.Fase_Adicional( "cena_battle" , ev_chave= ENTER , ev_tipo= TECLA_APERTADA )
    def fase_2(
        screen :Superficie, 
            info_extra : ...        = None,
                parente : Ambiente_Interativo        = None,
                    eventos:Evento    = None):
        
        '''for evento in eventos:
            if evento.type == TECLA_SEGURADA:
                if evento.key == ENTER:
                    print('Entrou na fase original')
                    return False

        print('222222222222')'''

        '''if len(eventos) > 0:
            return False'''

        print(eventos)

        return True

    @fase.Fase_Auxiliar( ENTER )
    def fase_3(
        screen :Superficie, 
            info_extra : ...        = None,
                parente : Ambiente_Interativo        = None,
                    eventos:list    = None):

        print(3333333333)

    imagem = carregar_imagem('banco_dados/Cenarios/cena_battle.png')
    
    A = MC( fase   , imagem , 0 )
    B = MC( fase_2 , imagem , 1 , ENTER )

    C = RC( [A , B] )

    'D = Rodar_Cenas( C , 60 , True )'

    #  GAME LOOP

    evento = capturar_evento()

    print(evento)

    fase( screen )
    

    pygame.quit()
      


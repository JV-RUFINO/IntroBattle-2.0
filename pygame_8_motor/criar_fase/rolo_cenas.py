from __future__ import annotations

from sys import path as caminho
from pathlib import Path as Caminhozão

arquivo = Caminhozão(__file__).resolve()
parente , raiz = arquivo.parent, arquivo.parents[1]
caminho.append(str(raiz))

# COMPARTILHADO
from    codigo_compartilhado    import filtrar_classe
from    codigo_compartilhado    import acao_classe
from    codigo_compartilhado    import Imagem_Opcoes    as Iop 

# PARENTE
try:
    from micro_cena              import Micro_Cena       as MC
except ModuleNotFoundError:
    from .micro_cena              import Micro_Cena       as MC

# PYGAME
from    pygame.image            import load             as carregar_imagem
from    pygame.event            import Event            as Evento 


' === CÓDIGO REAL === '

    
class Rolo_Cenas: # RC = Conjunto de Fases / Micro_Cenas(MC)
    '### Conjunto de Fases'
    posicao_Corrente = 0 # Micro_Cena atual que está sendo executado    

    def __init__( _ , *elos : list[MC] ):
        try:
            _.estoque = list(*elos) # [ MC(), MC(), ... ]
        except TypeError:
            _.estoque = list(elos)  # [ MC(), MC(), ... ]

    def __filtrar_micro_cena( _ , funcao : function ) -> MC | None :
        '* com base no estoque de MCs , retorna o primeiro MC que corresponda as exigencias definidas pela função.'
        res = filtrar_classe( _.estoque , funcao )
        return None if len(res) == 0 else res[0] # MC() / None

    def __acao_geral_mc( _ , funcao_mc : str , parametro: ... ) -> None:
        '* repete a mesma ação para todos os MCs guardados'
        acao_classe( _.estoque , funcao_mc , parametro )

    @property
    def atual( _ ) -> MC | None: 
        '* retorna o MC que está sendo/será executado'
        return _.__filtrar_micro_cena( lambda x: x.posicao_Corrente == _.posicao_Corrente ) 

    @property
    def principal( _ ) -> MC | None:
        '* retorna o primeiro MC dentro da lista' 
        return _.__filtrar_micro_cena( lambda y: y.principal )

    @property
    def funcoes_originais( _ ) -> list[function]:
        '* retorna as funções dentro dos MCs'
        return [ fun.função_original for fun in _.estoque if type(fun) == MC ]

    @property
    def backgrounds( _ ) -> list[Iop] | None:
        '* retorna a imagem/background dentro dos MCs'
        return [ elo.background for elo in _.estoque if type(elo) == MC ]

    def procurar( _ , parametro : ... ) -> MC | None:
        '''
        int     = a posição diante do estoque   / Ex: procurar(0)    -> primeiro elo no estoque
        str     = nome da função desejada       / Ex: procurar("ex") -> MC com nome "ex"
        Evento  = procura se existe um elo com esse evento / Ex: procurar( K_RETURN ) -> MC com evento gravado K_RETURN
        '''
        
        tipo = [int , str , Evento]
        acao = [ lambda z: z.posicao_Corrente == parametro , 
                    lambda w: w.nome == parametro , 
                        lambda ç: ç.verificar_evento( parametro ) ]

        for numero in range(len(tipo)):
            if type(parametro) == tipo[numero]:
                return _.__filtrar_micro_cena( acao[numero] )
    
    def eventos_gravados( _ , tipo = list ) -> list[tuple[Evento,Evento]]:
        '* retorna todos os eventos gravados dentro dos MCs'
        if tipo == dict:
            return { elo.nome : elo.evs for elo in _.estoque if any([ev != None for ev in elo.evs]) }

        return tipo([ elo.evs for elo in _.estoque if any([ev != None for ev in elo.evs]) ])
    
    def converter_para_int( _ , parametro : ... ) -> int | None:
        '* retorna a posição da micro_cena de acordo com o parametro utilizado'
        micro_cena = _.procurar( parametro )

        if micro_cena != None:
            return micro_cena.posicao_Corrente
        
    def redimencionar_backg_all( _ , superficie ):
        '* redimenciona todos os backgrounds'
        _.__acao_geral_mc( 'redimensionar_backg' , superficie )

    def definir_posicao_geral( _ ) -> None:  
        '* posiciona todos os MCs'
        _.__acao_geral_mc( 'posicionar' , _ )

    def adc_elo( _ , elo : MC ) -> None:
        _.estoque.append( elo )

        elo.posicionar( _ )

    def rmv_elo( _ , elo_existente : MC) -> None:
        _.estoque.remove( elo_existente )

        _.definir_posicao_geral()

    def __add__( _ , novo_elo : MC ):
        _.adc_elo( novo_elo )

    def __sub__( _ , elo_extrair : MC ):
        _.rmv_elo( elo_extrair )

    def __contains__( _ , elo : MC ) -> bool:
        return elo in _.estoque

    def __getitem__( _ , posicao ) -> ...:
        return _.procurar( posicao )

    def __len__( _ ):
        return len(_.estoque)

    def __repr__( _ ):
        return f'Rolo_Cenas({_.estoque})'


' === TESTES === '


if __name__ == '__main__':
    import pygame
    from os                     import getcwd
    from pygame.event           import get      as capturar_evento
    from pygame.time            import Clock    as Relogio
    from codigo_compartilhado   import Linkzin
    from pygame.image           import load     as carregar_imagem 
    from pygame                 import Surface  as Superficie , KEYDOWN as TECLA_SEGURADA , KEYUP as TECLA_APERTADA , K_LEFT as ESQUERDA , K_RIGHT as DIREITA , K_RETURN as ENTER

    def fase(
        screen :Superficie, 
            info_extra : ... = None,
                index : int = None,
                    eventos:list = None):
            '''for evento in eventos:
                if evento.type == TECLA_APERTADA:
                    if evento.key == ENTER:
                        index[1]'''
    
            "print('Fase rodando')"
    
            return True

    def fase_2(
            screen :Superficie, 
                info_extra : ... = None,
                    index : int = None,
                        eventos:list = None):
                """for evento in eventos:
                    if evento.type == KEYUP:
                        '''if evento.key == ENTER:
                            C = Caçadora()
                            index.CT = C.dialogo_combate()
        
                            index[1]'''"""
        
                print('222222222222')
        
                return True

    imagem = Iop(carregar_imagem('banco_dados/Cenarios/cena_battle.png'))
    
    A = MC( fase   , imagem , 0 )
    B = MC( fase_2 , imagem , 1 , ENTER )

    C = Rolo_Cenas( A , B )

    # Example file showing a basic pygame "game loop"
    import pygame

    # pygame setup
    pygame.init()
    screen = pygame.display.set_mode((1280, 720))
    clock = pygame.time.Clock()
    running = True


    C.definir_posicao_geral()
    C.redimencionar_backg_all( screen )

    print(C[0])

    while running:
        # poll for events
        # pygame.QUIT event means the user clicked X to close your window

        'print(type(pygame.event.get()))'
        eventos = pygame.event.get()

        'print(eventos)'

        '''if A.verificar_evento(eventos):
            print(":)")'''
        
        for event in eventos:
            event : Evento

            if event.type == pygame.QUIT:
                running = False

                break

            '''if event.type == TECLA_APERTADA:
                if event.key == ENTER:
                    running = False

                    break'''
            screen.fill("purple")
            
            C.atual( screen )

        # fill the screen with a color to wipe away anything from last frame
        ''

        # RENDER YOUR GAME HERE
        'C( screen , novo_evento = eventos ,index= C.estoque_elos)'

        # flip() the display to put your work on screen
        pygame.display.flip()

        clock.tick(60)  # limits FPS to 60

    pygame.quit()
      


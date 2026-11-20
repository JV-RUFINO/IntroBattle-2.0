from __future__ import annotations

from sys import path as caminho
from pathlib import Path as Caminhozão

arquivo = Caminhozão(__file__).resolve()
parente , raiz = arquivo.parent, arquivo.parents[1]
caminho.append(str(raiz))

# CODIGO COMPARTILHADO
from codigo_compartilhado import Imagem_Opcoes as IOp

# PYGAME
from pygame.image       import load     as carregar_imagem
from pygame.transform   import scale    as imagem_escala
from pygame.event       import Event    as Evento 

# IMPORTAÇÕES GERAIS
from dataclasses        import dataclass


' === CÓDIGO REAL === '


@dataclass
class Micro_Cena:   # MC = Fase Individual
    '### Representa uma fase singular // Deve apenas retornar True ou False'
                            
    função_original  : function          # essa função será repetida infinitamente enquanto a fase não for concluída
    background       : IOp               # Imagem_Opcoes( Superficie('caminho/para/imagem.png') ) 
    posicao_Corrente : int        = -1   # caso dado, informa a posição desse MC dentro da corrente

    ev_chave         : int        = None # "ENTER"      / "RIGHT"   / ...
    ev_tipo          : int        = None # "KEYDOWN"    / "KEYUP"   / ...

    @property
    def nome( _ ) -> str:
        '* retorna o nome da função'
        return _.função_original.__name__ # "exemplo" / "nome_da_funcao"

    @property
    def evs( _ ) -> tuple[ int , int ] | tuple[ None , None ]:
        '* retorna o conjunto dos eventos gravados, tanto eventos chave quanto de tipo'
        return _.ev_chave , _.ev_tipo   # ( ENTER , KEYDOWN )

    @property
    def conteudo_essencial( _ ) -> tuple[ function , Superficie , int , tuple ]:
        '* retorna todo o conteúdo da Micro_Cena'
        return _.função_original , _.background , _.posicao_Corrente , _.evs

    @property
    def principal( _ ) -> bool | None:
        '* retorna a hierarquia da Micro_Cena diante de um conjunto superior'
        if _.posicao_Corrente == -1:  # posição não-definida
            return None
        elif _.posicao_Corrente == 0: # principal
            return True
        elif _.posicao_Corrente > 0:  # não
            return False
        
    def verificar_evento( _ , captura_evento : Evento ) -> bool | None: # caso o MC possua um evento, verifica se ele está presente na lista de eventos capturados no loop principal do jogo
        '''
        * True  = evento presente na lista de eventos
        False = evento não presente na lista de eventos
        None  = MC sequer possui um evento gravado
        '''

        if all([ ev != None for ev in _.evs ]):
            return      captura_evento.type == _.ev_tipo and captura_evento.key == _.ev_chave
        elif _.ev_tipo != None:
            return      captura_evento.type == _.ev_tipo
        else:
            try:
                return  captura_evento.key  == _.ev_chave
            except AttributeError:
                return False

    def redimensionar_backg( _ , superficie : Superficie ) -> IOp:
        '* altera a imagem original para cobrir toda a superficie da fase'
        # NAO ALTERAR SEM VERIFICAR ROLO_CENAS

        _.background.tela_cheia( superficie )

        # não preciso mais. RIP codigo anterior xD
        '_.background = imagem_escala( _.background , ( superficie.get_width() , superficie.get_height() ))'

        return _.background

    def posicionar( _ , rolo_cenas ) -> None:
        '* automaticamente verifica a posição dentro de um conjunto superior'
        # NAO ALTERAR SEM VERIFICAR ROLO_CENAS
        if _ in rolo_cenas:
            _.posicao_Corrente = rolo_cenas.estoque.index( _ )

    def printar_background( _ , screen : Superficie ) -> None: # 
        '* printa a imagem(background) na superficie'
        _.background( screen , ( 0 , 0 ) )

        # mais uma vitima do powercreep. RIP codigo anterior
        'screen.blit( _.background , ( 0 , 0 ) )'

    def rodar_elo( _ , receber_screen : Superficie , info_extra : ... = None , parente = None , novo_evento: list = None ) -> ...:
        '* executa a função original e retorna o resultado'
        # receber screen = tela do jogo / Surface do pygame
        # info_extra     = espaço extra para passar informações únicas e à gosto do criador
        # index          = caso o MC(Micro Cena) esteja dentro de um conjunto maior, esse tal conjunto deve entrar aqui
        # novo_evento    = lista de eventos que foram capturados no loop principal do jogo, e que podem ser usados para interagir com a fase

        resultado = _.função_original( receber_screen , info_extra , parente , novo_evento )

        return resultado

    def __str__( _ ):
        return _.nome

    def __int__( _ ):
        return _.posicao_Corrente

    def __call__( _ , receber_screen : Superficie , info_extra : ... = None , parente = None , novo_evento: list = None ):
        _.printar_background( receber_screen )

        return _.rodar_elo( receber_screen , info_extra , parente , novo_evento )


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
    clock = pygame.time.Clock()
    running = True

    def fase(
        screen :Superficie, 
            info_extra : ... = None,
                index = None,
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
                    index = None,
                        eventos:list = None):
                """for evento in eventos:
                    if evento.type == KEYUP:
                        '''if evento.key == ENTER:
                            C = Caçadora()
                            index.CT = C.dialogo_combate()
        
                            index[1]'''"""
        
                print('222222222222')
        
                return True

    imagem = IOp(carregar_imagem('banco_dados/Cenarios/cena_battle.png'))
    
    A = Micro_Cena( fase   , imagem , 0 )
    B = Micro_Cena( fase_2 , imagem , 1 , ENTER )

    # Example file showing a basic pygame "game loop"
    while running:
        # poll for events
        # pygame.QUIT event means the user clicked X to close your window
        eventos = pygame.event.get()
        
        for event in eventos:
            event : Evento

            if event.type == pygame.QUIT:
                running = False

                break

        # fill the screen with a color to wipe away anything from last frame
        screen.fill("purple")

        # RENDER YOUR GAME HERE
        'C( screen , novo_evento = eventos ,index= C.estoque_elos)'

        # flip() the display to put your work on screen
        pygame.display.flip()

        clock.tick(60)  # limits FPS to 60

    pygame.quit()
      


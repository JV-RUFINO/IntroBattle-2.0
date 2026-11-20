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
    from micro_cena         import Micro_Cena       as MC
    from rolo_cenas         import Rolo_Cenas       as RC
except ModuleNotFoundError:
    from .micro_cena         import Micro_Cena       as MC
    from .rolo_cenas         import Rolo_Cenas       as RC

# PYGAME
import pygame
from pygame             import Surface          as Superficie , KEYDOWN as TECLA_SEGURADA , KEYUP as TECLA_APERTADA , K_LEFT as ESQUERDA , K_RIGHT as DIREITA , K_RETURN as ENTER
from pygame.image       import load             as carregar_imagem
from pygame.event       import get              as capturar_evento
from pygame.time        import Clock            as Relogio
from pygame.event       import Event            as Evento 


' === CÓDIGO REAL === '

    
class Rodar_Cenas: # RR = Auxilia Na execução das Fases
    '### Parte do Ambiente_Interativo que cuida da execução de Fases'

    running             = True                  # define se a Fase deve continuar rodando
    ultimo_evento       = None                  # variavel dedicada a guardar eventos

    def __init__( _ , fases_totais : RC ) -> None:
        _.fases_normais = fases_totais          # Destinado as fases principais. Afetam o loop
        _.auxiliares    = RC([])                # rolo especializado em eventos instantaneos, que não afetam o loop.'
    
    @staticmethod
    def novo_evento( ) -> list:
        '* retorna uma lista de eventos capturados pelo pygame'
        return capturar_evento() 

    @staticmethod
    def AUTO_X( todos_eventos , res ):
        '* verifica se foi apertado o botão de "X" da superficie'
        for evento in todos_eventos:
            if evento.type == pygame.QUIT:
                return False

        return res
    
    @property
    def index( _ ) -> int:
        '* retorna a posição das fases principais / normais'
        return _.fases_normais.posicao_Corrente
    
    @index.setter
    def index( _ , novo_index ):
        if novo_index >= 0:
            _.fases_normais.posicao_Corrente = novo_index

        elif type(novo_index) == Evento or type(novo_index) == list:
            if type(novo_index) == Evento:
                novo_index = [ novo_index ]

            _.posic_via_ev( _.fases_normais ,novo_index )

    @property
    def fase_atual( _ ) -> MC:
        '* retorna a fase que coincida com a posição da corrente'
        return _.fases_normais.atual

    @property
    def fase_original( _ ) -> MC:
        '* retorna a fase primeira/original'
        return _.fases_normais.principal

    @property
    def background_atual( _ ) -> str:
        '* retorna a imagem usada dentro da fase/MC'
        return _.fases_normais.backgrounds[_.index]

    def resetar_corrente( _ ):
        '* volta a posição da corrente para 0 e (re)ativa o running'
        _.index     = 0
        _.running   = True

    def avançar( _ , distancia: int = 1 ) -> int:
        _.index += distancia

        return distancia

    def retroceder( _ , distancia: int = 1 ) -> int:
        _.index -= distancia

        return distancia

    def rodar_tradicional( _ , receber_screen : Superficie , info_extra = None , novo_evento: list = None ) -> bool:
        '* roda a fase alem de filtrar os eventos caso essa fase contenha eventos gravados'
        # receber screen = tela do jogo / Surface do pygame
        # info_extra     = espaço extra para passar informações únicas e à gosto do criador
        # index          = ...
        # novo_evento    = lista de eventos que foram capturados no loop principal do jogo, e que podem ser usados para interagir com a fase

        if any( [ev != None for ev in _.fase_atual.evs] ) and type(novo_evento) != None:
            novo_evento = [ ev for ev in novo_evento if _.fase_atual.verificar_evento( ev )]

        return _.fase_atual( receber_screen , info_extra , _ , novo_evento )


    def retornar_origem( _ , resultado : bool ) -> bool:
        '* se existir elo principal -> False volta ao elo principal. Loop será encerrado apenas quando o elo principal retornar False'
        
        teste = _.fase_atual != _.fase_original
        if teste and resultado == False:
            _.index = _.fase_original.posicao_Corrente

        return True if teste else resultado
            
    def posic_via_ev( _ , rolo_cenas : RC , varios_eventos: list , auto_posic = True ) -> int | None:
        '* altera a posicao da corrente caso o Evento coincida com algum dos eventos gravados no Rolo_Cenas.'
        posicao_elo = None
        for evento in varios_eventos:
            evento : Evento

            posicao_elo = rolo_cenas.converter_para_int(evento)

            if type(posicao_elo) == int:
                rolo_cenas.posicao_Corrente = posicao_elo if auto_posic else rolo_cenas.posicao_Corrente

                break

        return posicao_elo
    
    def auxiliar( _ , receber_screen : Superficie , info_extra : ... = None , novo_evento: list = None ) -> bool:
        '* focado para cenas/eventos que não alteram o loop principal. Sempre retorna True'
        pos = _.posic_via_ev( _.auxiliares , novo_evento , auto_posic = False )

        aux : MC = _.auxiliares[pos]

        if type(aux) == MC:
            aux.rodar_elo( receber_screen , info_extra , _ , novo_evento ) # True e False são irrelevantes
        
        return True

    
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
            info_extra : ...        = None,
                parente : RC        = None,
                    eventos:list    = None):
        
        for evento in eventos:
            if evento.type == TECLA_SEGURADA:
                if evento.key == ENTER:
                    print('Entrou na fase 2')
                    parente.posicao_Corrente = 1

        return True

    def fase_2(
        screen :Superficie, 
            info_extra : ...        = None,
                parente : RC        = None,
                    eventos:list    = None):
        
        for evento in eventos:
            if evento.type == TECLA_SEGURADA:
                if evento.key == ENTER:
                    print('Entrou na fase original')
                    parente.posicao_Corrente = 0

        print('222222222222')

        return True

    imagem = IOp(carregar_imagem('banco_dados/Cenarios/cena_battle.png'))
    
    A = MC( fase   , imagem , 0 )
    B = MC( fase_2 , imagem , 1 , ENTER )

    C = RC( [A , B] )

    D = Rodar_Cenas( C )

    #  GAME LOOP

    'D.resetar_corrente()'
    while running:
        # poll for events
        # pygame.QUIT event means the user clicked X to close your window

        eventos = pygame.event.get()
        for event in eventos:
            event : Evento

            if event.type == pygame.QUIT:
                running = False

                break

        D.rodar_tradicional( screen , novo_evento = eventos)
    

    pygame.quit()
      


from sys import path as caminho
from pathlib import Path as Caminhozão

arquivo = Caminhozão(__file__).resolve()
parente , raiz = arquivo.parent, arquivo.parents[1]
caminho.append(str(raiz))

# CRIADORES -- BATALHA
from motor_exterior import Ambiente_Interativo as AI , Criar_Fase 

from motor_exterior import Seleção_Horizontal

from motor_exterior import Botao

from motor_exterior import Cor_Opcoes , Imagem_Opcoes

# CODIGO ANTIGO MEU COPIADO
'from battle_exterior import Menu_Conjunto'

# PYGAME
from pygame             import Surface as Superficie, QUIT as SAIR_X , Color as Cor , Rect as Retangulo
import pygame


'=== CÓDIGO REAL ==='


class Criar_Menu_inicial(Seleção_Horizontal):
    def __init__( _ , screen : Superficie ):
        super().__init__( "FACIL" , "MEDIO" , "DIFICIL" , 
                                dimensao_geral = ( screen.get_width()/6 , screen.get_height()/2 ) , 
                                        espaçamento= 100 , 
                                                base = Cor(50,0,0) )

        cores = [ Cor_Opcoes( Cor(0 , 180 , 0) ) , Cor_Opcoes( Cor(0 , 100 , 100) ) , Cor_Opcoes( Cor(180 , 0 , 0) )]
        n = 0
        for bt in _.botoes:
            bt.botao = cores[n]

            n += 1

        _.jogo          = True
        _.dificuldade   = 0

    @staticmethod
    def fonte():
        return Botao.fonte()

    def verificar_menu( _ , evento ):
        if _.botao_focado.verificar_evento( evento )[1] != None:
            for ev in evento:
                if ev.type == pygame.KEYUP:
                    _.dificuldade = _.foco
                    _.jogo = False

        return _.jogo

    def mudar_selecionado( _ , evento : list ):
        if _.botao_focado.verificar_evento( evento )[0] != None:
            for ev in evento:
                if ev.type == pygame.KEYUP:
                    if ev.key == pygame.K_RIGHT:
                        _.foco += 1
                    elif ev.key == pygame.K_LEFT:
                        _.foco -= 1

    def __call__( _ , screen , evs ):
        _.verificar_menu( evs )

        _.mudar_selecionado( evs )

        for bt in _.botoes:
            bt.desenhar_botão( screen , evs )


@Criar_Fase( 'salão' )
def Menu_Inicial(
        screen :Superficie, 
            info_extra : ...        = None,
                parente : AI        = None,
                    eventos:list    = None):
    
    Menu : Criar_Menu_inicial = info_extra

    screen.blit( 
                Menu.fonte().render( f'BEM VINDO AO INTROBATTLE', 
                            False , Cor(250,0,0) ) , Retangulo(screen.get_width()/4,200,0,0))

    Menu( screen , eventos )
        
    return Menu.jogo
    

'=== TESTES ==='


if __name__ == "__main__":
    from   pygame.display     import set_mode as definir_janela , set_caption as definir_titulo
    import pygame

    # pygame setup
    pygame.init()
    
    screen = definir_janela((1280, 720))
    definir_titulo("IntroBattle")

    B = Criar_Menu_inicial(screen)

    A = Menu_Inicial(screen, B)

    '''if any([a.type == SAIR_X for a in A]):
        print(":0")'''

    print(B.dificuldade)
    pygame.quit()

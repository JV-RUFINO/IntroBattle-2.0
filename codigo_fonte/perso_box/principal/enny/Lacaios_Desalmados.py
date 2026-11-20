from sys import path as caminho
from pathlib import Path as Caminhozão

arquivo = Caminhozão(__file__).resolve()
parente , raiz = arquivo.parent, arquivo.parents[1]
caminho.append(str(raiz))


# CODIGO COPIADO
from perso_exterior     import imagem_unica
from perso_exterior     import Linkzin

# ESSENCIAIS
from perso_exterior     import Caixa_Texto , texto_decorador

from perso_exterior     import Status

# ALIADOS
from perso_exterior     import Inimigo

# PYGAME
from pygame             import Surface  as Superficie , Color as Cor , Rect as Retangulo
from pygame.image       import load     as carregar_imagem
from pygame.transform   import scale    as imagem_escala

# IMPORTAÇÕES GERAIS
from os                 import getcwd


'== CÓDIGO REAL =='


class Lacaios_Desalmados(Inimigo):
    def __init__( _ , especializacao : str , elite = False , coordenadas: tuple[int, int] = [0, 0]):
        _.__especializacao = especializacao # arqueiros , brutos , espadachins , lanceiros , soldados
        palavra_chave = 'cinza' if elite == False else 'elite'

        super().__init__( ('lacaios_desalmados', especializacao , palavra_chave) , f"L-{especializacao}" , coordenadas )

        # STATUS DO PERSONAGEM
        if elite:
            for stat in _.STATUS:
                buff_elite : Status = type( _.STATUS[stat] )( 1 ) 

                _.buff_debuff( buff_elite , buff = True )

    @staticmethod
    def cor_assinatura() -> Cor:
        return Cor( 100 , 100 , 100 )

    @texto_decorador(carregar_imagem(Linkzin( getcwd() , 'banco_dados' , 'Personagens' , 'inimigos' , 'Lady Medusa' , 'idle.png')),Cor(135, 135, 135))
    def falar( _ , frase: str, cor: tuple) -> Caixa_Texto:
        return frase , cor

    def mostrar_animacao( _ , screen: Superficie , escala: tuple = None ):
        numero_escala = escala if escala != None else ( 30 , 30 )

        nova_imagem = imagem_escala( 
                imagem_unica( _.imagem_atual.moldavel , Retangulo( 126 , 0 , 18 , 20 ) , -1 ) ,
                        numero_escala )
        
        return screen.blit(nova_imagem , _.coordenadas)

    def __repr__( _ ):
        return super().repr_inimigo( "Os" , f"{_.__especializacao} sem alma nem coração" , "Lacaio bom é lacaio morto" )


'== TESTES =='


if __name__ == "__main__":
    # Example file showing a basic pygame "game loop"
    import pygame
    from pygame.event   import get as capturar_evento
    from pygame.time    import Clock as Relogio
    from pygame.display import set_mode as definir_janela , set_caption as definir_titulo
    from perso_exterior import Estado
    
    # pygame setup
    pygame.init()
    L = Lacaios_Desalmados( 'lanceiros' , True , [ 100 , 100 ] )
    CC: Caixa_Texto = L.falar('aaaaaaaaaaaaaa',Cor(100,100,100))
    L.estado_atual = Estado.Idle
    print(L)

    screen = definir_janela((1280, 720))
    definir_titulo("IntroBattle")

    clock = Relogio()
    running = True

    'L.escalar_imagens = ( 300 , 100 )'

    '''# arqueiros , brutos , espadachins , lanceiros , soldados
    L = Lacaios_Desalmados('soldados' , False)
    L2= Lacaios_Desalmados('espadachins' , True)
    print("cinzas: ",L.status)
    print("elite: ",L2.status)'''

    while running:
        # poll for events
        # pygame.QUIT event means the user clicked X to close your window
        for event in capturar_evento():
            if event.type == pygame.QUIT:
                running = False

            '''if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    CC.alt[2] = True
                    
                if event.key == pygame.K_LEFT:
                    CC.alt[1] = True
                
                if event.key == pygame.K_RETURN:
                    CC.alt[0] = True

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT:
                    CC.index += 1
                    
                if event.key == pygame.K_LEFT:
                    CC.index -= 1
    
                if event.key == pygame.K_RETURN:
                    CC.rodando = False
                    
                CC.resetar_cores()'''

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    L.coordenadas[0] += 10
                    
                    
                if event.key == pygame.K_LEFT:
                    L.coordenadas[0] -= 10

            
        # fill the screen with a color to wipe away anything from last frame
        screen.fill("purple")

        # RENDER YOUR GAME HERE
        
        L.mostrar_animacao(screen,(200,300))

        'print(L.imagem_atual(screen))'
        'CC(screen)'
        
        # RENDER YOUR GAME HERE

        # flip() the display to put your work on screen
        pygame.display.flip()

        clock.tick(60)  # limits FPS to 60

    pygame.quit()


    




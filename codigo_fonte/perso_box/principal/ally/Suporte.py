from sys import path as caminho
from pathlib import Path as Caminhozão

arquivo = Caminhozão(__file__).resolve()
parente , raiz = arquivo.parent, arquivo.parents[1]
caminho.append(str(raiz))


# ESSENCIAIS
from perso_exterior         import Perso
from perso_exterior         import Caixa_Texto , texto_decorador
from perso_exterior         import Linkzin

# ALIADOS
from perso_exterior         import Aliado

# MAGIAS
from perso_exterior         import JatoDAgua

# PYGAME
from pygame                 import Color    as Cor
from pygame.image           import load     as carregar_imagem

# IMPORTAÇÕES GERAIS
from os                     import getcwd


'== CÓDIGO REAL =='


class Suporte(Aliado):
    def __init__( _ , coordenadas: tuple[int, int] = [0, 0]):
        super().__init__( 'curandeiro' , "S" , JatoDAgua , coordenadas )

    @staticmethod
    def TIPO() -> Perso:
        return Perso.Suporte 

    @staticmethod
    def cor_assinatura() -> Cor:
        return Cor( 40 , 40 , 150 )

    @texto_decorador(carregar_imagem(Linkzin( getcwd() , 'banco_dados' , 'Personagens' , 'aliados' , 'curandeiro' , 'idle.png')),Cor(40,40,150))
    def falar( _ , frase: str, cor: tuple):
        return frase , cor

    @property
    def dano_magia( _ ) -> int:
        return int(_.CARGA)
    
    def dialogo_combate( _ , cor = Cor( 0 , 0 , 150 )) -> Caixa_Texto:
        return _.falar( _.todas_falas , cor )

    def __repr__( _ ):
        return super().repr_aliado( "O" , "curador de almas" , "Clérigo" )


'== TESTES =='


if __name__ == "__main__":
    # Example file showing a basic pygame "game loop"
    import pygame
    from pygame.event   import get as capturar_evento
    from pygame.time    import Clock as Relogio
    from pygame.display import set_mode as definir_janela , set_caption as definir_titulo
    
    # pygame setup
    pygame.init()
    S = Suporte()
    SS: Caixa_Texto = S.dialogo_combate()

    screen = definir_janela((1280, 720))
    definir_titulo("IntroBattle")

    clock = Relogio()
    running = True


    while running:
        # poll for events
        # pygame.QUIT event means the user clicked X to close your window
        for event in capturar_evento():
            if event.type == pygame.QUIT:
                running = False

            '''if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    SS.alt[2] = True
                    
                if event.key == pygame.K_LEFT:
                    SS.alt[1] = True
                
                if event.key == pygame.K_RETURN:
                    SS.alt[0] = True

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT:
                    SS.index += 1
                    
                if event.key == pygame.K_LEFT:
                    SS.index -= 1
    
                if event.key == pygame.K_RETURN:
                    SS.rodando = False
                    
                SS.resetar_cores()'''
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    S.coordenadas[0] += 10
                    
                    
                if event.key == pygame.K_LEFT:
                    S.coordenadas[0] -= 10

            
        # fill the screen with a color to wipe away anything from last frame
        screen.fill("purple")

        # RENDER YOUR GAME HERE
        
        'SS(screen)'

        print(S.imagem_atual)
        'S.mostrar_animacao( screen , (200,200) )'
        
        # RENDER YOUR GAME HERE

        # flip() the display to put your work on screen
        pygame.display.flip()

        clock.tick(60)  # limits FPS to 60

    pygame.quit()
    
    

    




from sys import path as caminho
from pathlib import Path as Caminhozão

arquivo = Caminhozão(__file__).resolve()
parente , raiz = arquivo.parent, arquivo.parents[1]
caminho.append(str(raiz))

# ESSENCIAIS
from box_exterior            import Stat
from box_exterior            import Linkzin

# ABSTRATOS
from box_exterior            import Status


'=== CÓDIGO REAL ==='


class Defesa(Status):
    def __init__( _ , numero: int ):
        super().__init__( numero )

        _.caminho = Linkzin( _.caminho , 'DEFESA' )

    @staticmethod
    def TIPO() -> Stat:
        return Stat.DEFESA

    @property
    def niveis_status( _ ) -> list:
        return super().niveis_status

    @property
    def mostrar_imagem( _ ):
        return super().mostrar_imagem
    
    def resetar_status(_):
        return super().resetar_status()


'=== TESTES ==='


if __name__ == "__main__":
    # Example file showing a basic pygame "game loop"
    import pygame
    from box_exterior import Linkzin

    from pygame import image
    from os import getcwd

    # pygame setup
    pygame.init()
    screen = pygame.display.set_mode((1280, 720))

    pygame.display.set_caption("IntroBattle")

    clock = pygame.time.Clock()
    running = True

    A = Defesa(2)

    while running:
        # poll for events
        # pygame.QUIT event means the user clicked X to close your window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT:
                    A.numero += 1

                elif event.key == pygame.K_LEFT:
                    A.numero -= 1

                elif event.key == pygame.K_SPACE:
                    A.resetar_status()

        # fill the screen with a color to wipe away anything from last frame
        screen.fill("purple")
        # RENDER YOUR GAME HERE

        'screen.blit(A.mostrar_imagem(),(100,100))'
        A.mostrar_imagem( screen , (100,100))

        print(A)

        # flip() the display to put your work on screen
        pygame.display.flip()

        clock.tick(60)  # limits FPS to 60

    pygame.quit()
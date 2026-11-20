from sys import path as caminho
from pathlib import Path as Caminhozão

arquivo = Caminhozão(__file__).resolve()
parente , raiz = arquivo.parent, arquivo.parents[1]
caminho.append(str(raiz))

# CODIGO COPIADO
from codigo_compartilhado   import Linkzin
from codigo_compartilhado   import Cor_Opcoes
from codigo_compartilhado   import Imagem_Opcoes

# PARENTE
try:
    from dimensoes              import Dimensoes
except ModuleNotFoundError:
    from .dimensoes              import Dimensoes

# PYGAME
from pygame                 import Color   as Cor , Surface as Superficie , Rect as Retangulo
from pygame                 import Surface as Superficie 
from pygame                 import KEYDOWN as TECLA_SEGURADA , KEYUP as TECLA_APERTADA 

from pygame.draw            import rect    as desenhar_retangulo
from pygame.font            import Font    as Fonte
from pygame.event           import Event


"=== CÓDIGO REAL ==="


class Botao(Dimensoes):
    def __init__( _ , retangulo                         : Retangulo , 
                        botao                           : Cor_Opcoes | Imagem_Opcoes , 
                            ev_gravado                  : int ,
                                texto                   : str = " " , 
                                    cor_texto           : Cor_Opcoes = Cor_Opcoes( Cor( 255, 255, 255) )  , 
                                        cor_texto_fixo  : bool = True ):
        super().__init__( retangulo )

        botao       = _.transformador( botao )
        cor_texto   = _.transformador( cor_texto )

        _.botao           : Cor_Opcoes | Imagem_Opcoes = botao # Cor_Opcoes( {_.cor_moldavel} // Original: {_.__cor_original} ) ou Imagem_Opcoes( {_.dimensoes} )
        _.cor_texto       : Cor_Opcoes  = cor_texto         # Cor_Opcoes( {_.cor_moldavel} // Original: {_.__cor_original} )

        _.ev_gravado      : int         = ev_gravado        # ENTER , K_LEFT , K_RIGHT , ... 
        
        _.texto           : str         = texto             # "ATACAR" , "DEFENDER" , "SAIR" , etc...
        _.cor_texto_fixo  : bool        = cor_texto_fixo    # Se a cor do texto é fixo ou se muda de acordo com a opção escolhida

        _.foco            : bool        = True              # Se o botão está em foco ou não

    def __decorador( extra : function ) -> function:
        def nova_funcao( *args , **kwargs  ) -> ...:
            _      : Botao          = args[0]
            screen : Superficie     = args[1]
            evs    : list[Evento]   = args[2]

            _.ativar_alt( evs ) 

            resultado = extra( *args , **kwargs )

            _.desenhar_texto( screen )

            return resultado

        return nova_funcao

    def __trava_foco( func: function ) -> function:
        def nova_func( *args , **kwargs ) -> ...:
            _ : Botao = args[0]

            if _.foco:
                res = func( *args , **kwargs )

                return res 

            return None

        return nova_func

    @staticmethod
    def fonte():
        return Fonte(Linkzin('fonte_jogo',"fontePygame.ttf", act_dir= True),32)
    
    @staticmethod
    def transformador( valor: ... ) -> Cor_Opcoes | Imagem_Opcoes:
        if type( valor ) == tuple or type( valor ) == Cor:
            valor = Cor_Opcoes( valor )
        elif type( valor ) == str or type( valor ) == Superficie:
            valor = Imagem_Opcoes( valor )
        elif type(valor) == Cor_Opcoes:
            valor = Cor_Opcoes( valor.moldavel )

        return valor
    
    @property
    def alternativo( _ ) -> bool:
        return _.botao.alternativo
    
    @alternativo.setter
    def alternativo( _ , novo : bool ):
        _.botao.alternativo = novo

        if _.cor_texto_fixo == False:
            _.cor_texto.alternativo = novo

    def verificar_evento( _ , eventos : list ) -> list[int, int] | list[None, None]:
        res = [ None , None ]
        for ev in eventos:
            ev: Event

            if ev.type == TECLA_APERTADA or ev.type == TECLA_SEGURADA:
                res[0] = ev.type

                if ev.key == _.ev_gravado:
                    res[1] = ev.key

        return res

    @__trava_foco
    def ativar_alt( _ , eventos : list ) -> None:
        res = _.verificar_evento( eventos )

        if res[1] == _.ev_gravado:
            if _.alternativo == False and res[0] == TECLA_SEGURADA:
                _.alternativo = True

            elif _.alternativo == True and res[0] == TECLA_APERTADA:
                _.alternativo = False

    def desenhar_retangulo( _ , screen : Superficie , cor : Cor , espaçamento : int = None ):
        _.botao : Cor_Opcoes

        valores = ( screen , cor , _.dimensoes )
        if espaçamento == None:
            desenhar_retangulo( *valores )
        else:
            desenhar_retangulo( *valores , width= espaçamento )

    def desenhar_imagem( _ , screen : Superficie ):
        _.botao : Imagem_Opcoes

        _.botao.dimensoes = ( _.largura , _.altura )

        _.botao( screen , _.ponto_inicial )

    def desenhar_texto( _ , screen : Superficie ):
        screen.blit( _.fonte().render( _.texto , False , _.cor_texto.cor ) , 
                            _.pos_frase( _.fonte( ), _.texto) ) # texto da caixa

    @__decorador
    def desenhar_botão( _ , screen : Superficie , evs : list ):
        _.botao : Cor_Opcoes 

        cor_principal = _.botao.cor_foco if _.foco else _.botao.cor
        _.desenhar_retangulo( screen , cor_principal          )
        _.desenhar_retangulo( screen , _.botao.cor_borda , 14 )  

    @__decorador
    def botao_via_imagem( _ , screen : Superficie , evs : list ):
        _.botao : Imagem_Opcoes

        _.desenhar_imagem( screen )

    def __call__( _ , screen : Superficie , evs: list ):
        valores = ( screen , evs )

        if type( _.botao ) == Cor_Opcoes:
            _.desenhar_botão( *valores )

        elif type( _.botao ) == Imagem_Opcoes:
            _.botao_via_imagem( *valores )

        else:
            raise TypeError(f"Tipo de botão inválido: {type(_.botao)}")

    def __repr__( _ ) -> str:
        return f"{type(_).__name__}( nome = {_.texto} , dim = {_.dimensoes} , ev = {_.ev_gravado} )"
    


'=== TESTES ==='


if __name__ == "__main__":
    from codigo_compartilhado.linkzin  import Linkzin
    import pygame
    from os                     import getcwd
    from pygame.event           import get      as capturar_evento
    from pygame.time            import Clock    as Relogio
    from pygame.image           import load     as carregar_imagem 
    from pygame                 import Surface  as Superficie , KEYDOWN as TECLA_SEGURADA , KEYUP as TECLA_APERTADA , K_LEFT as ESQUERDA , K_RIGHT as DIREITA , K_RETURN as ENTER
    from pygame                 import Event as Evento

    # pygame setup
    pygame.init()
    screen = pygame.display.set_mode((1280, 720))
    clock = pygame.time.Clock()
    running = True

    imagem      = carregar_imagem( Linkzin('banco_dados','Cenarios','introcomp_menu.png', act_dir= True) )
    cores       = Cor( 150 , 100 , 100 ) 


    conteudo = Botao(
                    Retangulo(500,550,200,100),
                        cores,
                            ENTER,
                                "SAIR",
                                    (255, 255, 255) ,
                                        True
                                        )

    'print(conteudo.botao)'
    'print(conteudo.altura)'
    '''print('PONTO_INICIAL: ',conteudo.ponto_inicial)
    print(f'LARGURA: {conteudo.largura} // LARGURA(DIV): {conteudo.largura / 2}')
    print(f'ALTURA: {conteudo.altura} // ALTURA(DIV): {conteudo.altura / 4}')
    print(f'FONTE: {conteudo.fonte().size( conteudo.texto )} // FONTE(DIV): {(conteudo.fonte().size( conteudo.texto )[0] / 4,conteudo.fonte().size( conteudo.texto )[1])}')
    print(f'FORMULA FINAL: {14 + conteudo.ponto_inicial[0] + (conteudo.largura / 4) - (conteudo.fonte().size( conteudo.texto )[0] / 4) , conteudo.ponto_inicial[1] + conteudo.altura / 4}')
    print(f'FORMULA FINAL(-ponto inicial): {(conteudo.largura / 2) - (conteudo.fonte().size( conteudo.texto )[0] ) , conteudo.altura / 4}')
'''

    print(conteudo.botao)
    # Example file showing a basic pygame "game loop"
    while running:
        # poll for events
        # pygame.QUIT event means the user clicked X to close your window
        eventos = pygame.event.get()
        
        for event in eventos:
            event : Evento

            '''if eventos != []:
                print(eventos)'''

            if event.type == pygame.QUIT:
                running = False

                break

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT:
                    conteudo.x += 5
                if event.key == pygame.K_LEFT:
                    conteudo.x -= 5

                if event.key == pygame.K_RETURN:
                    conteudo.largura += 5

        # fill the screen with a color to wipe away anything from last frame
        screen.fill("purple")

        conteudo(screen , eventos )

        'print(conteudo)'

        # flip() the display to put your work on screen
        pygame.display.flip()

        clock.tick(60)  # limits FPS to 60

    pygame.quit()
        
    
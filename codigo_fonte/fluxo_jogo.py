from sys import path as caminho
from pathlib import Path as Caminhozão

arquivo = Caminhozão(__file__).resolve()
parente , raiz = arquivo.parent, arquivo.parents[1]
caminho.append(str(raiz))

try:
    # MOTOR PYGAME
    from motor_exterior         import  Seleção_Horizontal , Seleção_Vertical
    from motor_exterior         import  Macro_ambiente
    from motor_exterior         import  Personagem

    # CELEBRO -- CRIADORES
    from criadores_batalha      import Criar_Batalha
    from criadores_batalha      import Printar_Seleção_Perso as PSP
    from criadores_batalha      import Printar_Combatentes
    from criadores_batalha      import Printar_Chefao
    from criadores_batalha      import Printar

    # PERSONAGENS
    from perso_box              import Paladino,Ladino,Suporte,Caçadora,Maga
    from perso_box              import Esqueleto, Lady_Medusa

    # FASES BATTLE
    from fases_battle           import Menu_Inicial , Criar_Menu_inicial
    from fases_battle           import Selecionar_Personagens 
    from fases_battle           import Enfrentar_Inimigos , criar_chefona , criar_esqueletos , criar_lacaios , Menu_Batalha
    from fases_battle           import Conclusao
except ModuleNotFoundError:
    # MOTOR PYGAME
    from .motor_exterior        import  Seleção_Horizontal , Seleção_Vertical
    from .motor_exterior        import  Macro_ambiente
    from .motor_exterior        import  Personagem

    # CELEBRO -- CRIADORES
    from .criadores_batalha     import Criar_Batalha
    from .criadores_batalha     import Printar_Seleção_Perso as PSP
    from .criadores_batalha     import Printar_Combatentes
    from .criadores_batalha     import Printar_Chefao
    from .criadores_batalha     import Printar

    # PERSONAGENS
    from .perso_box             import Paladino,Ladino,Suporte,Caçadora,Maga
    from .perso_box             import Esqueleto, Lady_Medusa

    # FASES BATTLE
    from .fases_battle          import Menu_Inicial , Criar_Menu_inicial
    from .fases_battle          import Selecionar_Personagens 
    from .fases_battle          import Enfrentar_Inimigos , criar_chefona , criar_esqueletos , criar_lacaios , Menu_Batalha
    from .fases_battle          import Conclusao

# PYGAME
import pygame
from pygame                     import Surface  as Superficie, Color as Cor, Rect as Retangulo
from pygame                     import QUIT as SAIR_X , K_RETURN as ENTER , KEYUP
from pygame.event               import Event 


'=== CÓDIGO REAL ==='

class Fluxo_Jogo:
    def __init__( _ , screen : Superficie ) -> None:
        _.macro_ambiente = Macro_ambiente( Menu_Inicial , Selecionar_Personagens , Enfrentar_Inimigos , Conclusao , screen= screen )

        _.rodando_jogo : bool = True
        
        _.lista_acoes_aliadas = [[],[]] # armazen das acoes que os aliados vão fazer
        
        _.batalha   = Criar_Batalha( tuple() , tuple() )
        _.CMI       = Criar_Menu_inicial( _.screen )
        _.MB        = Menu_Batalha( _.screen , Paladino() ) 

    @staticmethod
    def cor_placeholder():
        return Cor( 80 , 80 , 80 ) # só existe para ser trocado por outra cor

    @property
    def screen( _ ):
        return _.macro_ambiente.screen

    @property
    def dificuldade_jogo( _ ):
        return _.CMI.dificuldade
    
    @property
    def aliados_escolhidos( _ ):
        return _.batalha.aliados

    @aliados_escolhidos.setter
    def aliados_escolhidos( _ , novos_aliados):
        _.batalha.aliados = novos_aliados

    @property
    def inimigos_escolhidos( _ ):
        return _.batalha.aliados

    @inimigos_escolhidos.setter
    def inimigos_escolhidos( _ , novos_inimigos ):
        _.batalha.boss = False if len(novos_inimigos) > 1 else True
    
        _.batalha.inimigos = novos_inimigos 

    def X_ou_nao( _ , evento : list[Event] ):
        return all([ a.type != SAIR_X for a in evento ])

    def criar_batalha( _ , modo_printar : Printar , primeiro_perso : Personagem ):
        _.MB.base    = primeiro_perso.cor_assinatura()
        escolher     = modo_printar()

        return escolher

    def Molde_Fluxos( fase ):
        def decorator( _ ) -> bool:
            resultado : Event = fase( _ )

            continuar_rodando = _.X_ou_nao( resultado ) # True / False

            _.rodando_jogo    = continuar_rodando

            return continuar_rodando
            
        return decorator

    def Molde_Fluxo_Battle( inimigos ):
        def segundo_decorador( fase ):
            def decorator( _ ) -> bool:
                _.macro_ambiente.reativar_amb_solo( 2 )

                _.inimigos_escolhidos = inimigos()

                resultado : Event = fase( _ )

                _.lista_acoes_aliadas[0].clear() # só para garantir
                _.lista_acoes_aliadas[1].clear() # só para garantir

                return resultado

            return decorator
            
        return segundo_decorador


    @Molde_Fluxos
    def tela_menu( _ ) -> bool:
        fase : list = _.macro_ambiente( _.CMI , index = 0 )

        _.CMI.jogo = True # caso o loop volte

        return fase

    @Molde_Fluxos
    def selecionando_aliados( _ ) -> bool:
        q       = tuple([ str(a) for a in range( len(PSP.posicao()[0]) ) ])

        opcoes  = Seleção_Horizontal(
                    *q , 
                        base= _.cor_placeholder() , 
                                dimensao_geral = Retangulo( *PSP.posicao()[1][0] , *PSP.tamanho_estrutura() ) , 
                                        espaçamento = 50 ,
                                            cor_texto = Cor(60,60,60))
        psp     = PSP()
        aliados_escolhidos = []

        fase : Event = _.macro_ambiente( [ 
                opcoes  ,
                psp , 
                aliados_escolhidos ]
            , index = 1 )

        _.aliados_escolhidos = tuple(aliados_escolhidos)

        return fase

    @Molde_Fluxos
    @Molde_Fluxo_Battle( inimigos= criar_esqueletos )
    def inimigos_easy( _ ) -> bool:
        escolher = _.criar_batalha( Printar_Combatentes , _.batalha.aliados[0] )
        
        fase : Event = _.macro_ambiente( ( 
                    _.batalha                   ,
                    _.MB                      ,
                    _.lista_acoes_aliadas[0]    , 
                    escolher )
                , index= 2)

        return fase

    @Molde_Fluxos
    @Molde_Fluxo_Battle( inimigos = criar_lacaios )
    def inimigos_medio( _ ) -> bool:
        escolher = _.criar_batalha( Printar_Combatentes , _.batalha.aliados[0] )
                
        fase : Event = _.macro_ambiente( ( 
                    _.batalha                   ,
                    _.MB                      ,
                    _.lista_acoes_aliadas[0]    , 
                    escolher )
                , index= 2)

        return fase

    @Molde_Fluxos
    @Molde_Fluxo_Battle( inimigos = criar_chefona )
    def chefao_hard( _ ) -> bool:
        escolher = _.criar_batalha( Printar_Chefao , _.batalha.aliados[0] )
                
        fase : Event = _.macro_ambiente( ( 
                    _.batalha                   ,
                    _.MB                      ,
                    _.lista_acoes_aliadas[0]    , 
                    escolher )
                , index= 2)

        return fase

    def tela_final( _ , vitoria = True ) -> bool:
        fase = _.macro_ambiente( ( 
                    _.aliados_escolhidos , 
                    vitoria              , 
                    _.dificuldade_jogo ) 
                , index= 3)

        resultado_fase = [fases.type for fases in fase]

        if KEYUP in resultado_fase:
            return None

        return _.X_ou_nao( fase )

    def __call__( _ ) -> None:
        fases_iniciais = [ _.tela_menu , _.selecionando_aliados ]
        fases_batalha  = [ _.inimigos_easy , _.inimigos_medio , _.chefao_hard ]

        _.macro_ambiente.reativar_ambientes()
        continuar = False
        while _.macro_ambiente.running_geral( False ):
            for fase in fases_iniciais:
                continuar = fase()

                if continuar == False:
                    break
        
            limite_dificuldade = -1 if continuar else 999
            for fase in fases_batalha:
                limite_dificuldade += 1

                if _.dificuldade_jogo >= limite_dificuldade:
                    continuar = fase()

                    if _.batalha.vitoria:
                        continue

                    break
                            
            if continuar == True:
                continuar = _.tela_final( vitoria = _.batalha.vitoria )

            if continuar == None:
                continue
            elif continuar == False:
                break
            

'=== TESTES ==='


if __name__ == "__main__":
    from   pygame.display     import set_mode as definir_janela , set_caption as definir_titulo
    import pygame

    # pygame setup
    pygame.init()
    

    screen = definir_janela((1280, 720))
    definir_titulo("IntroBattle")

    fluxo = Fluxo_Jogo(screen)

    'fluxo.selecionando_aliados()'

    'fluxo.tela_final()'

    fluxo()

    pygame.quit()
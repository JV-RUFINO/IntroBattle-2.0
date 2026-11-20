from sys import path as caminho
from pathlib import Path as Caminhozão

arquivo = Caminhozão(__file__).resolve()
parente , raiz = arquivo.parent, arquivo.parents[1]
caminho.append(str(raiz))

# CRIADORES BATALHA
from motor_exterior     import Criar_Fase, Ambiente_Interativo as AI
from criadores_batalha  import Printar_Seleção_Perso as PSP
from motor_exterior     import Seleção_Horizontal
from motor_exterior     import Cor_Opcoes

# PERSONAGENS
from perso_box import Caçadora
from perso_box import Ladino
from perso_box import Maga
from perso_box import Paladino
from perso_box import Suporte

# ESSENCIAIS
from motor_exterior import Perso

# PYGAME
import pygame
from pygame             import Surface  as Superficie, Color as Cor, Rect as Retangulo
from pygame             import KEYUP    as TECLA_APERTADA, K_LEFT as ESQUERDA , K_RIGHT as DIREITA, QUIT as SAIR_X , K_RETURN as ENTER
from pygame.event       import Event
from pygame             import Font as Fonte


'=== CÓDIGO REAL ==='


def criar_dict_perso():
    return {
        Perso.Paladino: Paladino()  ,
        Perso.Ladino  : Ladino()    ,
        Perso.Caçadora: Caçadora()  ,
        Perso.Maga    : Maga()      ,
        Perso.Suporte : Suporte()
        }

@Criar_Fase( 'teste 7' , ev_tipo= TECLA_APERTADA )
def Selecionar_Personagens(
        screen :Superficie, 
            info_extra : ...        = None,
                parente : AI        = None,
                    eventos:list    = None):
    
    opcoes  : Seleção_Horizontal = info_extra[0]
    psp     : PSP                = info_extra[1]
    armazen : list               = info_extra[2]
    
    if len(armazen) >= 3:
        return False
    else:
        parente.index = 1
    

@Selecionar_Personagens.Fase_Adicional( 'teste 7' , ev_tipo= TECLA_APERTADA )
def Pausa_Personagens(
    screen :Superficie, 
        info_extra : ...        = None,
            parente : AI        = None,
                eventos:list    = None):

    opcoes  : Seleção_Horizontal = info_extra[0]
    psp     : PSP                = info_extra[1]
    armazen : list               = info_extra[2]

    combatente = criar_dict_perso()

    fonte               = opcoes.botao_focado.fonte()
    todos_retangulos    = ( Retangulo( 150 , n , 0 , 0 ) for n in range( 200 , 501 , 100 ) )
    frase               = 'APERTE QUALQUER TECLA PARA CONTINUAR'

    psp(screen      ,
        combatente  ,
        opcoes.foco ,
        armazen)

    for rec in todos_retangulos:
        screen.blit( 
            fonte.render( f'{frase}', 
                True , opcoes.cor_texto.cor , opcoes.cor_texto.cor_alternativa ) , rec )

    return True

@Pausa_Personagens.Fase_Adicional( 'teste 3 ps' , ev_tipo= TECLA_APERTADA )
def Escolher_Personagens(
    screen :Superficie, 
        info_extra : ...        = None,
            parente : AI        = None,
                eventos:list    = None):

    opcoes  : Seleção_Horizontal = info_extra[0]
    psp     : PSP                = info_extra[1]
    armazen : list               = info_extra[2]

    if len(armazen) >= 3:
        parente.index = 0 # RETORNA PRA CENTRAL DE CONTROLE E FINALIZA A FASE
    
    # AGORA SIM VEM O CÓDIGO
    combatente        = criar_dict_perso()
    opcoes_combatente = [ c for c in combatente.keys() ]
    fonte : Fonte     = opcoes.botao_focado.fonte()

    # PRINTANDO NA TELA
    cor_assinatura : Cor      = combatente[opcoes_combatente[opcoes.foco]].cor_assinatura()
    opcoes.cor_texto.moldavel = cor_assinatura
    
    screen.blit( 
            fonte.render( f'ESCOLHA SEUS ALIADOS: {len(armazen)}', 
                        False , cor_assinatura ) , Retangulo(380,50,0,0))

    opcoes(screen , eventos)

    psp(screen,
        combatente,
        opcoes.foco,
        armazen)

    # PRINTANDO NA TELA

    return True
    

@Selecionar_Personagens.Fase_Auxiliar()
def Eventos_Perso(
            screen :Superficie, 
                info_extra : ...        = None,
                    parente : AI        = None,
                        eventos:list    = None):
    
    if parente.index == 1:
        parente.index = 2

    elif parente.index == 2:
        opcoes  : Seleção_Horizontal = info_extra[0]
        psp     : PSP                = info_extra[1]
        armazen : list               = info_extra[2]

        combatente        = criar_dict_perso()
        opcoes_combatente = [ c for c in combatente.keys() ]
        
        for ev in eventos:
            ev : Event
    
            dupla = [ESQUERDA,DIREITA] # [ pygame.K_LEFT , pygame.K_RIGHT ]  
            if ev.key in dupla:     
                if ev.key   == dupla[0]:
                    opcoes.foco -= 1 
                elif ev.key == dupla[1]:
                    opcoes.foco += 1
    
                cor_assinatura : Cor = combatente[opcoes_combatente[opcoes.foco]].cor_assinatura() # Cor( int ,int , int)
                opcoes.base          = type(opcoes.base)(cor_assinatura)                           # Cor_Opcoes( Cor(...) )
    
            elif ev.key == ENTER:      # pygame.RETURN          
                personagem_escolhido : Perso = opcoes_combatente[opcoes.foco] # Paladino , Maga , ...
    
                if all(personagem.TIPO() != personagem_escolhido for personagem in armazen):
                    armazen.append(combatente[personagem_escolhido])

    
'=== TESTES ==='


if __name__ == "__main__":
    from   pygame.display     import set_mode as definir_janela , set_caption as definir_titulo
    import pygame

    # pygame setup
    pygame.init()
    

    screen = definir_janela((1280, 720))
    definir_titulo("IntroBattle")


    opcoes  = Seleção_Horizontal("1",'2','3','4','5',dimensao_geral=Retangulo(50,100,200,500), base= Cor(100,100,175), cor_texto= (100,0,0), espaçamento= 50)
    
    print(opcoes.base)
    
    psp     = PSP()
    armazen = []


    Selecionar_Personagens( screen , [opcoes , psp , armazen] )

    print(armazen)

    pygame.quit()
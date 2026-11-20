from __future__ import annotations

from sys import path as caminho
from pathlib import Path as Caminhozão

arquivo = Caminhozão(__file__).resolve()
parente , raiz = arquivo.parent, arquivo.parents[1]
caminho.append(str(raiz))

# ESSENCIAIS
from motor_exterior import Caixa_Texto


# CELEBRO -- CRIADORES
from motor_exterior       import Criar_Fase , Ambiente_Interativo as AI, Botao
from motor_exterior       import Seleção_Horizontal

# PERSONAGENS
from motor_exterior                    import Personagem
from perso_box                           import Lady_Medusa


# ETIQUETAS
from motor_exterior                    import Estado

# PYGAME
from pygame import Surface as Superficie, QUIT as SAIR_X,Color as Cor , Rect as Retangulo
from pygame import K_RETURN as ENTER , KEYUP as TECLA_APERTADA , KEYDOWN as TECLA_SEGURADA , K_RIGHT as DIREITA , K_LEFT as ESQUERDA
from pygame.event import Event


'=== CÓDIGO REAL ==='


def decidir_conclusao(vitoria : bool , dificuldade : int ):
    if vitoria:
        if dificuldade == 2:
            texto       = ["HORA DE COMEMORAR!", 'VITORIA :D']
            dimensoes   = [Retangulo(380,550,540,100),Retangulo(500,100,100,100)]
            cor         = [Cor(60,175,60),(0, 200, 0)]
        else:
            texto       = ["CONTINUE A LUTAR!" , "AINDA NÃO É O FIM!"]
            dimensoes   = [Retangulo(400,550,515,100),Retangulo(400,100,100,100)]
            cor         = [Cor(180,180,0),(200, 200, 0)]

    else:
        texto           = ["ACEITAR A DERROTA", 'VOCÊ PERDEU :(']
        dimensoes       = [Retangulo(400,550,510,100),Retangulo(480,100,100,100)]
        cor             = [Cor(175,30,0),(200, 0, 0)]

    return [Seleção_Horizontal(texto[0], base=cor[0], dimensao_geral=dimensoes[0]),
                [Botao.fonte().render( texto[1] , False , cor[1] ) , dimensoes[1]]]

def printar_perso_conclu( screen : Superficie ,perso : list , vitoria: bool ):
    aumento = 300
    if len(perso) == 1:
        posicao = [555,200]
        tamanho = (185,345)

    elif len(perso) == 3:
        posicao = [250,200]
        tamanho = (200,200)

    for perso in perso:
        perso : Personagem

        perso.estado_atual = Estado.Escolhivel if vitoria else Estado.Down
        perso.coordenadas  = posicao

        perso.mostrar_animacao( screen,  tamanho )

        posicao[0] += aumento

@Criar_Fase( 'teste 7' , ev_tipo= TECLA_APERTADA , ev_chave= ENTER )
def Conclusao(
            screen :Superficie, 
                            info_extra : ...        = None,
                                parente : AI        = None,
                                    eventos:list    = None
                ):

    aliados     : tuple = info_extra[0] # ( Personagem , Personagem , Personagem )
    vitoria     : bool  = info_extra[1]
    dificuldade : int   = info_extra[2] # 0 / 1 / 2

    if len(eventos) >= 1:
        if vitoria:
            Julgamento( screen , Lady_Medusa().julgamento_final(dificuldade) )

        return False

    conclu = decidir_conclusao( vitoria , dificuldade )

    # ESCREVER EM CIMA 
    screen.blit( conclu[1][0] , conclu[1][1] ) # texto da caixa
    # ESCREVER EM CIMA 

    # PRINTAR O BOTÃO NA TELA 
    voltar_opcao = conclu[0] # Printar_Opções(cor_geral=(int,int,int),opcoes = (str), _Printar_Opções__CONTAGEM=0)
    voltar_opcao(screen, eventos)
    # PRINTAR O BOTÃO NA TELA 

    # MOSTRAR OS COMBATENTES VENCEDORES
    if dificuldade < 2 and vitoria:
        perso = [Lady_Medusa()]
    else:
        perso = aliados 

    printar_perso_conclu( screen ,perso , vitoria )
    # MOSTRAR OS COMBATENTES VENCEDORES
    
    return True


@Criar_Fase( 'teste 7' )
def Julgamento(
            screen :Superficie, 
                            info_extra : ...        = None,
                                parente : AI        = None,
                                    eventos:list    = None):

    CC : Caixa_Texto = info_extra

    for event in eventos:
        event : Event

        if event.type == TECLA_SEGURADA:
            if event.key == DIREITA:
                CC.alt[2] = True
                
            if event.key == ESQUERDA:
                CC.alt[1] = True
            
            if event.key == ENTER:
                CC.alt[0] = True

        if event.type == TECLA_APERTADA:
            if event.key == DIREITA:
                CC.index += 1
                
            if event.key == ESQUERDA:
                CC.index -= 1

            if event.key == ENTER:
                CC.rodando = False
                
            CC.resetar_cores()
    
    if CC.rodando:
        CC( screen )

        printar_perso_conclu( screen , [Lady_Medusa()] , True)
    
    return CC.rodando


'=== TESTE ==='


if __name__ == "__main__":
    from   pygame.display     import set_mode as definir_janela , set_caption as definir_titulo
    import pygame

    from perso_box import Paladino,Ladino,Suporte,Caçadora,Maga
    
    # pygame setup
    pygame.init()
    
    screen = definir_janela((1280, 720))
    definir_titulo("IntroBattle")
    
    aliados     = (Paladino(),Caçadora(),Maga()) 

    
    Conclusao( screen ,  ( aliados , True , 2 ) )

    pygame.quit()

    


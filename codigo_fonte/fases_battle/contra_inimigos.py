from __future__ import annotations

from sys import path as caminho
from pathlib import Path as Caminhozão

arquivo = Caminhozão(__file__).resolve()
parente , raiz = arquivo.parent, arquivo.parents[1]
caminho.append(str(raiz))

# ESSENCIAIS
from motor_exterior         import Caixa_Texto

# CELEBRO -- CRIADORES
from motor_exterior         import Criar_Fase , Ambiente_Interativo as AI
from criadores_batalha      import Criar_Batalha
from motor_exterior         import Seleção_Horizontal
from criadores_batalha      import Printar_Chefao as BP_chefao , Printar
from criadores_batalha      import Anim_AtkBasico , Anim_Magia , Animacao

# PERSONAGENS
from motor_exterior         import Personagem
from perso_box              import Esqueleto , Lady_Medusa , Lacaios_Desalmados
from perso_box              import Aliado

# ETIQUETAS
from motor_exterior         import Combate , Estado

# PYGAME
import pygame
from pygame import Surface as Superficie, QUIT as SAIR_X,Color as Cor
from pygame import K_LEFT as ESQUERDA , K_RIGHT as DIREITA , K_UP as CIMA , K_DOWN as BAIXO , K_RETURN as ENTER, KEYUP as TECLA_APERTADA , KEYDOWN as TECLA_SEGURADA
from pygame.event import Event

# IMPORTAÇÕES GERAIS
import random


'=== CÓDIGO REAL ==='


class Menu_Batalha(Seleção_Horizontal):
    def __init__( _ , screen : Superficie , primeiro_perso : Personagem ):
        super().__init__( "LUTAR" , "MAGIA" , "FALAR" , "PULAR" , 
                            dimensao_geral = ( screen.get_width()/7 , screen.get_height()/1.3 ) , 
                                espaçamento = 50 , 
                                    base = primeiro_perso.cor_assinatura() )

    @property
    def menu_nome_atual( _ ):
        return _.botao_focado.texto

    @property
    def opcao_traduzida( _ ) -> Combate:
        tt    = _.todos_focos
        todos = ( Combate.Atacar , Combate.Magia , Combate.Falar , Combate.Pular )

        for numero in range(len(tt)):
            if tt[numero]:
                return todos[numero]

    @opcao_traduzida.getter
    def atacar_magia( _ ):
        return _.opcao_traduzida in ( Combate.Atacar , Combate.Magia )

    @opcao_traduzida.getter
    def falar_ou_nao( _ ):
        return _.opcao_traduzida == Combate.Falar

    @opcao_traduzida.getter
    def pular_ou_nao( _ ):
        return _.opcao_traduzida ==  Combate.Pular

    def retornar_animacao( _ , personagens : tuple , inverter = False ) -> Animacao:
        # !HORA DA CENA DE BATALHA!
        if _.atacar_magia:
            res = ( _.opcao_traduzida == Combate.Atacar , _.opcao_traduzida == Combate.Magia )
            if res[0]:
                aliado = personagens[0] ; inimigo = personagens[1]
                especialidade   = aliado if inverter else inimigo
                versão_animacao = Anim_AtkBasico

            elif res[1]:
                especialidade   = None
                versão_animacao = Anim_Magia

            return versão_animacao( *personagens , especialidade ) 

        return None

    def mudar_selecionado( _ , evento : list ):
        if _.botao_focado.verificar_evento( evento )[0] != None:
            for ev in evento:
                if ev.type == TECLA_APERTADA:
                    if ev.key == DIREITA:
                        _.foco += 1
                    elif ev.key == ESQUERDA:
                        _.foco -= 1
        return None

    def selecionar( _ , evento : list ):
        if _.botao_focado.verificar_evento( evento )[1] != None:
            for ev in evento:
                if ev.type == TECLA_APERTADA:
                    return _.opcao_traduzida
        return None

    def __call__( _ , screen : Superficie , eventos : list , perso : Personagem ):
        _.base = perso.cor_assinatura()

        _.mudar_selecionado( eventos )

        resultado = _.selecionar( eventos )

        _.rodar_todos( screen , eventos )

        return resultado

def criar_esqueletos(quantidade = 3):
    return tuple([ Esqueleto() for n in range(quantidade) ])

def criar_lacaios(elites = (False, True, False)) -> tuple:
    return tuple([
        Lacaios_Desalmados(
                random.choice(['arqueiros','brutos','espadachins','lanceiros','soldados']),
                elitezin) 
        for elitezin in elites])

def criar_chefona():
    return (Lady_Medusa(),)

def printar_batalha( screen : Superficie , batalha : Criar_Batalha , escolha : Printar ):
    if batalha.boss:
        escolha(
                screen,                 # <Surface(...x...x.. SW)>
                batalha.aliados,        # (Ladino(),Maga(),Suporte()) :.Exemplo
                *batalha.inimigos)      # (Lady_Medusa())
    else:
        escolha(
                screen,                 # <Surface(...x...x.. SW)>
                batalha.aliados,        # (Ladino(),Maga(),Suporte()) :.Exemplo
                batalha.inimigos)      # ((Esqueleto(),Esqueleto(),Esqueleto()))

def forcar_fechamento( batalha : Criar_Batalha , ev : list ):
    if any([resul.type == SAIR_X for resul in ev]):
        for ally in batalha.aliados:
            ally.vida = 0

        return True
    
    return False

@Criar_Fase( 'salão' )
def Enfrentar_Inimigos(
    screen :Superficie, 
        info_extra : ...        = None,
            parente : AI        = None,
                eventos:list    = None):
    # INSIRA O CÓDIGO AQUI
    
    batalha : Criar_Batalha     = info_extra[0] # Criar_Batalha(aliados=(...) , inimigos=(...), boss = False)
    opcoes  : Menu_Batalha      = info_extra[1] # Printar_Opções(cor_geral=(int,int,int),opcoes = (str,str,...), _Printar_Opções__CONTAGEM=0)
    armazen : list              = info_extra[2] # [(0, <Combate.Atacar: 1>, 0),(1, <Combate.Falar: 3>, None),(2, <Combate.Magia: 2>, 2)] :.Exemplo
    escolha : BP_chefao         = info_extra[3] # BPN([False,0])

    # PRINTAR OS PERSONAGENS NA TELA
    
    printar_batalha( screen , batalha , escolha )

    # PRINTAR OS PERSONAGENS NA TELA

    if batalha.vitoria == None:
        if len(armazen) < 3: 
            parente.index = 1
        else:
            parente.index = 3

    return batalha.vitoria == None

@Enfrentar_Inimigos.Fase_Adicional( 'salão' )
def Escolha_Primaria(
    screen :Superficie, 
        info_extra : ...        = None,
            parente : AI        = None,
                eventos:list    = None):
    # INSIRA O CÓDIGO AQUI

    batalha : Criar_Batalha     = info_extra[0] # Criar_Batalha(aliados=(...) , inimigos=(...), boss = False)
    opcoes  : Menu_Batalha      = info_extra[1] # Printar_Opções(cor_geral=(int,int,int),opcoes = (str,str,...), _Printar_Opções__CONTAGEM=0)
    armazen : list              = info_extra[2] # [(0, <Combate.Atacar: 1>, 0),(1, <Combate.Falar: 3>, None),(2, <Combate.Magia: 2>, 2)] :.Exemplo
    escolha : Printar           = info_extra[3] # BPN([False,0])

    # PRINTAR OS PERSONAGENS NA TELA

    printar_batalha( screen , batalha , escolha )

    # PRINTAR OS PERSONAGENS NA TELA

    aliado_escolhido : Personagem = batalha.aliados[len(armazen)]
    if aliado_escolhido.estado_atual != Estado.Down:
        AtacarMagiaFalarPular : bool = escolha.alvos_idle # True ou False

        if AtacarMagiaFalarPular:
            # PRINTAR OPCOES NA TELA

            teste_enter = opcoes( screen , eventos , aliado_escolhido )

            # PRINTAR OPCOES NA TELA

            if teste_enter != None:
                if any([ opcoes.falar_ou_nao , opcoes.pular_ou_nao ]):
                    opcao_escolhida  : Combate = opcoes.opcao_traduzida
                    adição = ( opcao_escolhida , len(armazen) , escolha.index_selecionada ) # ( Combate , int , int )

                    armazen.append( adição )

                if opcoes.atacar_magia:
                    escolha.alterar_escolha()
        else:
            parente.index = 2

    else:
        armazen.append(( Combate.Pular , len(armazen)  , escolha.index_selecionada )) # morto não age 

    # INSIRA O CÓDIGO AQUI

    return len(armazen) < 3


@Enfrentar_Inimigos.Fase_Adicional( 'salão' , ev_tipo= TECLA_APERTADA )
def Escolha_Secundaria(
    screen :Superficie, 
        info_extra : ...        = None,
            parente : AI        = None,
                eventos:list    = None):
    # INSIRA O CÓDIGO AQUI

    batalha : Criar_Batalha     = info_extra[0] # Criar_Batalha(aliados=(...) , inimigos=(...), boss = False)
    opcoes  : Menu_Batalha      = info_extra[1] # Printar_Opções(cor_geral=(int,int,int),opcoes = (str,str,...), _Printar_Opções__CONTAGEM=0)
    armazen : list              = info_extra[2] # [(0, <Combate.Atacar: 1>, 0),(1, <Combate.Falar: 3>, None),(2, <Combate.Magia: 2>, 2)] :.Exemplo
    escolha : Printar           = info_extra[3] # BPN([False,0])

    # PRINTAR OS PERSONAGENS NA TELA
    
    printar_batalha( screen , batalha , escolha )
    
    # PRINTAR OS PERSONAGENS NA TELA

    for ev in eventos:
        if ev.key == CIMA or ev.key == BAIXO:
            escolha.mudar_selecionado( ev.key )
        elif ev.key == ENTER:
            opcao_escolhida  : Combate = opcoes.opcao_traduzida
            adição = ( opcao_escolhida , len(armazen) , escolha.index_selecionada )

            armazen.append( adição )

            escolha.alterar_escolha( None )

            return False

@Enfrentar_Inimigos.Fase_Adicional( 'cena_battle' )
def Battle(
        screen :Superficie, 
            info_extra : ...        = None,
                parente : AI        = None,
                    eventos:list    = None):

    batalha : Criar_Batalha     = info_extra[0] # Criar_Batalha(aliados=(...) , inimigos=(...), boss = False)
    opcoes  : Menu_Batalha      = info_extra[1] # Printar_Opções(cor_geral=(int,int,int),opcoes = (str,str,...), _Printar_Opções__CONTAGEM=0)
    armazen : list              = info_extra[2] # [(0, <Combate.Atacar: 1>, 0),(1, <Combate.Falar: 3>, None),(2, <Combate.Magia: 2>, 2)] :.Exemplo
    escolha : Printar           = info_extra[3] # BPN([False,0])

    # RENOMEANDO AS VARIAVEIS
    dec_ali : list = armazen                   # [(Combate.Atacar,0,1),(Combate.Falar,1,None),(Combate.Pular,1,None)]
    dec_ini : list = batalha.decisao_inimiga   # [(Combate.Atacar,0,2),(Combate.Atacar,1,1),(Combate.Atacar,2,0)]
    # RENOMEANDO AS VARIAVEIS

    anim = []
    for individual in batalha.fila: # [Personagem , Personagem , ...] -> EX: [Caçadora , Esqueleto , Paladino, ...]
        individual : Personagem

        if individual.vida > 0:
            # PROCESSANDO A AÇÃO
            inverter           : bool = True if individual in batalha.inimigos else False

            index_autor        : int  = batalha.inimigos.index(individual) if inverter else batalha.aliados.index(individual)
            decisao_individual : list = dec_ini[index_autor]               if inverter else dec_ali[index_autor]

            if decisao_individual[0] == Combate.Falar:
                individual : Aliado
                CC = individual.dialogo_combate()

                a = Falar( screen , ( CC , batalha , escolha ) )

                if forcar_fechamento( batalha , a ):
                    return False

                continue

            resul = batalha.combate( decisao_individual , inverter = inverter )
            # PROCESSANDO A AÇÃO

            # ADICIONANDO A NOVA ANIMAÇÃO PRO "ANIM"
            aliado  : Personagem = batalha.aliados[ decisao_individual[2]] if inverter else batalha.aliados[ decisao_individual[1]]
            inimigo : Personagem = batalha.inimigos[decisao_individual[1]] if inverter else batalha.inimigos[decisao_individual[2]]

            nova_anim : Animacao = opcoes.retornar_animacao( (aliado , inimigo) , inverter )

            if nova_anim != None:
                anim.append(nova_anim)
            # ADICIONANDO A NOVA ANIMAÇÃO PRO "ANIM"

        for anim_expecifica in anim:
            b = Cena_Battle( screen , ( anim_expecifica , batalha.boss ) ) # os que estiverem running.false não vão rodar

            if forcar_fechamento( batalha , b ):
                return False
        
        # !HORA DA CENA DE BATALHA!

    # LIMPANDO AS AÇÕES
    armazen.clear()
    # LIMPANDO AS AÇÕES

    return False

@Criar_Fase( 'cena_battle' )
def Cena_Battle(
    screen :Superficie, 
        info_extra : ...        = None,
            parente : AI        = None,
                eventos:list    = None):

    animacao : Animacao = info_extra[0]
    boss     : bool     = info_extra[1]

    if animacao.running:
        animacao(screen , boss = boss)

        return True
    else:
        return False

@Criar_Fase( 'salão' )
def Falar(
    screen :Superficie, 
        info_extra : ...        = None,
            parente : AI        = None,
                eventos:list    = None):

    CC      : Caixa_Texto    = info_extra[0]
    batalha : Criar_Batalha  = info_extra[1]
    printar : Printar        = info_extra[2]
    
    if CC.rodando:
        CC( screen )

        printar_batalha( screen , batalha , printar )

    return CC.rodando

@Falar.Fase_Auxiliar( tipo_evento= TECLA_SEGURADA )
def Brilhar_Caixa(
    screen :Superficie, 
        info_extra : ...        = None,
            parente : AI        = None,
                eventos:list    = None):

    CC      : Caixa_Texto    = info_extra[0]
    batalha : Criar_Batalha  = info_extra[1]
    printar : BP_chefao      = info_extra[2]

    for event in eventos:
        event : Event

        if event.key == DIREITA:
            CC.alt[2] = True
            
        if event.key == ESQUERDA:
            CC.alt[1] = True
        
        if event.key == ENTER:
            CC.alt[0] = True

@Falar.Fase_Auxiliar( tipo_evento= TECLA_APERTADA )
def Mover_Caixa(
    screen :Superficie, 
        info_extra : ...        = None,
            parente : AI        = None,
                eventos:list    = None):
    
    CC      : Caixa_Texto    = info_extra[0]
    batalha : Criar_Batalha  = info_extra[1]
    printar : BP_chefao      = info_extra[2]

    for event in eventos:
        event : Event

        if event.key == DIREITA:
            CC.index += 1
            
        if event.key == ESQUERDA:
            CC.index -= 1

        if event.key == ENTER:
            CC.rodando = False

        CC.resetar_cores()


'=== TESTES ==='


if __name__ == "__main__":
    from   pygame.display     import set_mode as definir_janela , set_caption as definir_titulo
    import pygame
    from perso_box import Paladino,Ladino,Suporte,Caçadora,Maga

    from criadores_batalha.printar_personagens import Printar_Combatentes as PC

    # pygame setup
    pygame.init()
    

    screen = definir_janela((1280, 720))
    definir_titulo("IntroBattle")
    

    aliados     = (Paladino(),Ladino(),Maga()) 
    inimigos    = criar_esqueletos()
    
    batalha     = Criar_Batalha(aliados,inimigos)
    opcoes      = Menu_Batalha( screen , aliados[0] )

    armazen     = []
    escolher    = BP_chefao()
    escolher    = PC()

    'batalha.boss = False'

    Enfrentar_Inimigos( screen,
                                (batalha,
                                        opcoes,
                                                armazen, 
                                                        escolher))

    'Falar( screen , ( aliados[1].dialogo_combate() , batalha , escolher ))'
    
    pygame.quit()
    

from sys import path as caminho
from pathlib import Path as Caminhozão

arquivo = Caminhozão(__file__).resolve()
parente , raiz = arquivo.parent, arquivo.parents[1]
caminho.append(str(raiz))


# EXTERIOR
from box_exterior                 import Estado , Stat , Perso, Condicao
from box_exterior                 import Imagem_Opcoes

# STATUS
from status.Vida                    import Vida
from status.Ataque                  import Ataque
from status.Velocidade              import Velocidade
from status.Defesa                  import Defesa
from status.Carga                   import Carga

# PERSONAGEM
from box_exterior                 import Personagem 

# STATUS
from box_exterior                 import Status

# MAGIAS
from box_exterior                 import Magias

# PYGAME
from pygame                         import Surface  as Superficie , Color as Cor


'=== CÓDIGO REAL ==='


class Perso_geral(Personagem):
    def __init__( _ , classe_geral : tuple[str] , posicao_roteiro : tuple[str] , magia : Magias , coordenadas : tuple[ int , int ] = [ 0 , 0 ] ):
        super().__init__( coordenadas )

        if type(classe_geral) == str:
            classe_geral = (classe_geral,)
        if type(posicao_roteiro) == str:
            posicao_roteiro = (posicao_roteiro,)

        caminho = _.retorna_path( classe_geral )
        # ['...\\Exemplo\\banco_dados\\Personagens\\...\\...\\down.png', 
        #       '...\\Exemplo\\banco_dados\\Personagens\\...\\...\\escolhivel.png', 
        #           ... ]

        _.adc_img( caminho )
        # {<Estado.Down: 4>: Imagem_Opcoes( ... ), 
        #       <Estado.Escolhivel: 2>: Imagem_Opcoes( ... ), 
        #               <Estado.Idle: 1>: Imagem_Opcoes( ... ), 
        #                       <Estado.Selecionada: 3>: Imagem_Opcoes( ... )}

        todos_status = [ Ataque , Defesa , Vida , Carga , Velocidade ]
        todos_str    = [ "ATAQUE" , "DEFESA" , "VIDA" , "CARGA" , "VELOCIDADE" ]

        for numero in range(len(todos_status)):
            _.adcionar_status( todos_status[numero] , ( *posicao_roteiro , todos_str[numero] ))
        #   {<Stat.ATAQUE: 2>: Ataque(status = ... & numero = ...), 
        #       <Stat.DEFESA: 3>: Defesa(status = ... & numero = ...), 
        #           <Stat.VIDA: 5>: Vida(status = ... & numero = ...), 
        #               <Stat.CARGA: 4>: Carga(status = ... & numero = ...), 
        #                   <Stat.VELOCIDADE: 1>: Velocidade(status = ... & numero = ...)}

        # VIDA TOTAL
        _.vida          = int(_.VIDA) + 1
        
        # MAGIAS / HABS
        _.magias        = magia

        # ESTADO ATUAL
        _.estado_atual  = Estado.Idle

    @staticmethod
    def TIPO(  ) -> Perso:
        return None

    @staticmethod
    def cor_assinatura( cor ) -> Cor:
        return Cor( r=cor[0] , g=cor[1] , b=cor[2] )
    
    @property
    def escala( _ ) -> dict:
        if _.imagens == {}:
            return None
        else:
            return _.imagens[ list(_.imagens.keys())[0] ].dimensoes

    @escala.setter
    def escalar_imagens( _ , nova_escala : tuple[int,int] ):
        for imagem in _.imagens:
            resultado : Imagem_Opcoes = _.imagens[imagem]

            resultado.dimensoes = nova_escala
            
    @property
    def imagem_atual( _ ):
        return super().imagem_atual

    @property
    def magia_imagem( _ ):
        return None

    @property
    def STATUS(_) -> dict:
        return super().STATUS

    @STATUS.getter
    def VIDA(_) -> Vida:
        return _.status[Stat.VIDA]

    @STATUS.getter
    def ATAQUE(_) -> Ataque:
        return _.status[Stat.ATAQUE]

    @STATUS.getter
    def DEFESA(_) -> Defesa:
        return _.status[Stat.DEFESA]

    @STATUS.getter
    def VELOCIDADE(_) -> Velocidade:
        return _.status[Stat.VELOCIDADE]

    @STATUS.getter
    def CARGA(_) -> Carga:
        return _.status[Stat.CARGA]
    
    @property
    def calculo_VidaTotal( _ ):
        return int(_.VIDA) + 1
        
    @property
    def dano_basico( _ ) -> int:
        return int( _.ATAQUE )

    @property
    def dano_magia( _ ) -> int:
        return None
    
    def adcionar_status( _ , classe_status: Status , chave_str: tuple ):
        return super().adcionar_status( classe_status , chave_str , classe_status.TIPO() )

    def retorna_path( _ , caminho_desejado : tuple[str] ) -> list:
        return super().retorna_path( caminho_desejado )

    def adc_img( _ , caminho_fornecido : tuple[Caminhozão] , estado_img = None) -> dict:
        if estado_img == None:
            nome_caminhos = [ caminho.name[:-4].upper() for caminho in caminho_fornecido ]

            cc = []
            for nome in nome_caminhos:
                if nome == "DOWN":
                    cc.append(Estado.Down)
                elif nome == "ESCOLHIVEL":
                    cc.append(Estado.Escolhivel)
                elif nome == "IDLE":
                    cc.append(Estado.Idle)
                elif nome == "SELECIONADA":
                    cc.append(Estado.Selecionada)

            estado_img = cc

        ss = [ str(smg) for smg in caminho_fornecido ] 

        return super().adc_img( ss , estado_img )

    def reducao_dano( _ , dano_recebido : int) -> int: # aplicando DEFESA sobre o dano recebido
        return super().reducao_dano( dano_recebido , int( _.DEFESA ) )

    def buff_debuff( _ , efeito , buff = True ):
        return super().buff_debuff( efeito , buff )

    def ataque_basico( _ , alvo: Personagem): # ataca o alvo .Conta apenas o ATAQUE
        return super().ataque_basico( alvo )

    def falar( _ , frase: str, cor: tuple): # abre a caixa de texto e faz o personagem falar
        ...

    def magia( _ , alvo: Personagem):
        return None

    def mostrar_animacao(_, screen: Superficie, escala: tuple = None):
        return super().mostrar_animacao(screen, escala)
    
    def repr_personagem( _ , print_convencional : str , para_derrota : str , vida_status : tuple ):
        if _.vida == 0:
            return para_derrota

        index_status = 1 if _.vida <= _.calculo_VidaTotal / 2 else 0

        reportar_status = ""

        bbb = [(Condicao.Nerfado , Condicao.Buffado),
                    (" Nerfados & " , " Buffados")]
        for aaa in range(0,len(bbb)):
            if bbb[0][aaa] in [_.STATUS[status].condicao for status in _.STATUS]:
                reportar_status += _.__textinho_adcional(bbb[0][aaa])
            else:
                reportar_status += "0"

            reportar_status += bbb[1][aaa]

        return f"{print_convencional} : {vida_status[index_status]}({reportar_status})"

    def __hash__(_) -> int:
        return super().__hash__()

    def __sub__( _ , valor ):
        if type(valor) == int:
            valor : int

            _.vida -= _.reducao_dano( valor ) # reduzindo o dano conforme a DEFESA

            if _.vida < 0:
                _.vida = 0

        elif type(valor) in [type(_.STATUS[status]) for status in _.STATUS]:
            valor : Status

            _.buff_debuff( valor , buff = False)

        return _

    def __add__( _ , valor ):
        if type(valor) == int:
            valor : int

            _.vida += valor

        elif type(valor) in [type(_.STATUS[status]) for status in _.STATUS]:
            valor : Status

            _.buff_debuff( valor , buff = True)
            
        return _

'=== TESTES ==='


if __name__ == "__main__":
    A = Perso_geral( ("aliados","paladino") , (0,"P"), 0)

    '''A + Vida( 1 )
    A - Ataque( 1 )
    A + Defesa( 1 )'''

    print(A.imagens)

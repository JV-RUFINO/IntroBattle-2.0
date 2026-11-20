from sys import path as caminho
from pathlib import Path as Caminhozão

arquivo = Caminhozão(__file__).resolve()
parente , raiz = arquivo.parent, arquivo.parents[1]
caminho.append(str(raiz))

# CODIGO COMPARTILHADO  
from pygame_8_motor.codigo_compartilhado   import Cor_Opcoes , Imagem_Opcoes
from pygame_8_motor.codigo_compartilhado   import Caixa_Texto , texto_decorador
from pygame_8_motor.codigo_compartilhado   import repetidor , acao_classe , filtrar_classe
from pygame_8_motor.codigo_compartilhado   import Linkzin
from pygame_8_motor.codigo_compartilhado   import carregar_tira , porcao_imagens , imagem_unica
from pygame_8_motor.codigo_compartilhado   import Projetil
from pygame_8_motor.codigo_compartilhado   import Combate , Condicao , Estado , Magi , Perso , Stat
from pygame_8_motor.codigo_compartilhado   import repetidor_de_func

# PERSONAGENS
from pygame_8_motor.criar_personagens      import Personagem , Magias , Status
from pygame_8_motor.criador_botoes         import Dimensoes , Botao , Conjunto_Botoes , Seleção_Horizontal , Seleção_Vertical
from pygame_8_motor.criar_fase             import Micro_Cena , Rolo_Cenas , Rodar_Cenas , Criar_Fase , Ambiente_Interativo , Macro_ambiente
    

if __name__ == "__main__":
    print("Este arquivo não é para ser executado diretamente.")
    A = Personagem
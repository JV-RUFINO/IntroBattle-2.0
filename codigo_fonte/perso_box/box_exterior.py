from sys import path as caminho
from pathlib import Path as Caminhozão

arquivo = Caminhozão(__file__).resolve()
parente , raiz = arquivo.parent, arquivo.parents[1]
caminho.append(str(raiz))

# CODIGO COMPARTILHADO  
from motor_exterior   import Cor_Opcoes , Imagem_Opcoes
from motor_exterior   import Caixa_Texto , texto_decorador
from motor_exterior   import repetidor , acao_classe , filtrar_classe
from motor_exterior   import Linkzin
from motor_exterior   import carregar_tira , porcao_imagens , imagem_unica
from motor_exterior   import Projetil
from motor_exterior   import Combate , Condicao , Estado , Magi , Perso , Stat

# PERSONAGENS
from motor_exterior   import Personagem , Magias , Status
from motor_exterior   import Dimensoes , Botao , Conjunto_Botoes , Seleção_Horizontal , Seleção_Vertical
from motor_exterior   import Micro_Cena , Rolo_Cenas , Rodar_Cenas , Ambiente_Interativo , Macro_ambiente


if __name__ == "__main__":
    print("Este arquivo não é para ser executado diretamente.")

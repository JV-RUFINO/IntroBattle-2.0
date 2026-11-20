from sys import path as caminho
from pathlib import Path as Caminhozão

arquivo = Caminhozão(__file__).resolve()
parente , raiz = arquivo.parent, arquivo.parents[1]
caminho.append(str(raiz))

# CODIGO COMPARTILHADO  
from box_exterior               import Cor_Opcoes , Imagem_Opcoes
from box_exterior               import Caixa_Texto , texto_decorador
from box_exterior               import repetidor , acao_classe , filtrar_classe
from box_exterior               import Projetil
from box_exterior               import Linkzin
from box_exterior               import carregar_tira , porcao_imagens , imagem_unica

# ETIQUETAS
from box_exterior               import Combate , Condicao , Estado , Magi , Perso , Stat

# STATUS
from box_exterior               import Status
from status.Vida                import Vida
from status.Ataque              import Ataque
from status.Velocidade          import Velocidade
from status.Defesa              import Defesa
from status.Carga               import Carga

# MAGIAS
from magias.BolaDeFogo          import BolaDeFogo
from magias.Ventania            import Ventania
from magias.Fumaca              import Fumaça
from magias.JadoDAgua           import JatoDAgua

# LAYERS_ASBSTRATO
from abstratos.aliado           import Aliado 
from abstratos.inimigo          import Inimigo

if __name__ == "__main__":
    ...
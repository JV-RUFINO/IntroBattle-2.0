from sys import path as caminho
from pathlib import Path as Caminhozão

arquivo = Caminhozão(__file__).resolve()
parente , raiz = arquivo.parent, arquivo.parents[1]
caminho.append(str(raiz))

try:
    from anim_batalha           import Animacao , Anim_AtkBasico , Anim_Magia
    from criar_batalha          import Criar_Batalha
    from printar_personagens    import Printar , Printar_Combatentes , Printar_Chefao , Printar_Seleção_Perso
except ModuleNotFoundError:
    from .anim_batalha           import Animacao , Anim_AtkBasico , Anim_Magia
    from .criar_batalha          import Criar_Batalha
    from .printar_personagens    import Printar , Printar_Combatentes , Printar_Chefao , Printar_Seleção_Perso
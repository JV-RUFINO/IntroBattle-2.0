from __future__ import annotations

from sys import path as caminho
from pathlib import Path as Caminhozão

arquivo = Caminhozão(__file__).resolve()
parente , raiz = arquivo.parent, arquivo.parents[1]
caminho.append(str(raiz))

try:
    from menu_inicial       import Menu_Inicial , Criar_Menu_inicial
    from seleção_perso      import Selecionar_Personagens
    from contra_inimigos    import Enfrentar_Inimigos , Menu_Batalha , criar_chefona , criar_esqueletos , criar_lacaios
    from conclusao          import Conclusao
except ModuleNotFoundError:
    from .menu_inicial       import Menu_Inicial , Criar_Menu_inicial
    from .seleção_perso      import Selecionar_Personagens
    from .contra_inimigos    import Enfrentar_Inimigos , Menu_Batalha , criar_chefona , criar_esqueletos , criar_lacaios
    from .conclusao          import Conclusao
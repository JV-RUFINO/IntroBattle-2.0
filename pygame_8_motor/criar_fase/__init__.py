from __future__ import annotations

from sys import path as caminho
from pathlib import Path as Caminhozão

arquivo = Caminhozão(__file__).resolve()
parente , raiz = arquivo.parent, arquivo.parents[1]
caminho.append(str(raiz))

try:
    from micro_cena             import Micro_Cena       
    from rolo_cenas             import Rolo_Cenas
    from rodar_cenas            import Rodar_Cenas
    from ambiente_interativo    import Ambiente_Interativo , Criar_Fase
    from macro_ambiente         import Macro_ambiente
except ModuleNotFoundError:
    from .micro_cena             import Micro_Cena       
    from .rolo_cenas             import Rolo_Cenas
    from .rodar_cenas            import Rodar_Cenas
    from .ambiente_interativo    import Ambiente_Interativo , Criar_Fase 
    from .macro_ambiente         import Macro_ambiente
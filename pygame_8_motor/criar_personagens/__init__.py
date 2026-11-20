from __future__ import annotations

from sys import path as caminho
from pathlib import Path as Caminhozão

arquivo = Caminhozão(__file__).resolve()
parente , raiz = arquivo.parent, arquivo.parents[1]
caminho.append(str(raiz))

try:
    from personagem     import Personagem
    from magias         import Magias
    from status         import Status
except ModuleNotFoundError:
    from .personagem     import Personagem
    from .magias         import Magias
    from .status         import Status

from sys import path as caminho
from pathlib import Path as Caminhozão

arquivo = Caminhozão(__file__).resolve()
parente , raiz = arquivo.parent, arquivo.parents[1]
caminho.append(str(raiz))

try:
    from fluxo_jogo import Fluxo_Jogo
except ModuleNotFoundError:
    from .fluxo_jogo import Fluxo_Jogo
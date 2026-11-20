from sys import path as caminho
from pathlib import Path as Caminhozão

arquivo = Caminhozão(__file__).resolve()
parente , raiz = arquivo.parent, arquivo.parents[1]
caminho.append(str(raiz))

try:
    from dimensoes          import Dimensoes
    from botao              import Botao
    from conjunto_botoes    import Conjunto_Botoes
    from criar_selecoes     import Seleção_Horizontal , Seleção_Vertical
except ModuleNotFoundError:
    from .dimensoes          import Dimensoes
    from .botao              import Botao
    from .conjunto_botoes    import Conjunto_Botoes
    from .criar_selecoes     import Seleção_Horizontal , Seleção_Vertical
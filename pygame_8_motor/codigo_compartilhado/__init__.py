from sys import path as caminho
from pathlib import Path as Caminhozão

arquivo = Caminhozão(__file__).resolve()
parente , raiz = arquivo.parent, arquivo.parents[1]
caminho.append(str(raiz))

try:
    # funcoes compartilhadas
    from acao_classe        import acao_classe
    from filtrar_classe     import filtrar_classe
    from repetidor          import repetidor_de_func
    from linkzin            import Linkzin
    from spritesheet        import porcao_imagens, imagem_unica , carregar_tira

    # classes compartilhadas
    from cor_opcoes         import Cor_Opcoes
    from opcoes_gerais      import Opcoes_Geral
    from imagem_opcoes      import Imagem_Opcoes
    from projetil           import Projetil
    from enumeradores       import Condicao , Magi , Stat, Perso , Estado , Combate
    from caixa_texto        import Caixa_Texto , texto_decorador
except ModuleNotFoundError:
    # funcoes compartilhadas
    from .acao_classe        import acao_classe
    from .filtrar_classe     import filtrar_classe
    from .repetidor          import repetidor_de_func
    from .linkzin            import Linkzin
    from .spritesheet        import porcao_imagens, imagem_unica , carregar_tira

    # classes compartilhadas
    from .cor_opcoes         import Cor_Opcoes
    from .opcoes_gerais      import Opcoes_Geral
    from .imagem_opcoes      import Imagem_Opcoes
    from .projetil           import Projetil
    from .enumeradores       import Condicao , Magi , Stat, Perso , Estado , Combate
    from .caixa_texto        import Caixa_Texto , texto_decorador
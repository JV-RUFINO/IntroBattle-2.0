from sys import path as caminho
from pathlib import Path as Caminhozão


arquivo = Caminhozão(__file__).resolve()
parente , raiz = arquivo.parent, arquivo.parents[1]
caminho.append(str(raiz))

try:
    # ABSTRATOS
    from abstratos.aliado           import Aliado
    from abstratos.inimigo          import Inimigo

    # MAGIAS
    from magias.BolaDeFogo          import BolaDeFogo
    from magias.Ventania            import Ventania
    from magias.Fumaca              import Fumaça
    from magias.JadoDAgua           import JatoDAgua

    # STATUS
    from status.Vida                import Vida
    from status.Ataque              import Ataque
    from status.Velocidade          import Velocidade
    from status.Defesa              import Defesa
    from status.Carga               import Carga

    # PRINCIPAL
    from principal.ally.Caçadora    import Caçadora
    from principal.ally.Ladino      import Ladino
    from principal.ally.Maga        import Maga
    from principal.ally.Paladino    import Paladino
    from principal.ally.Suporte     import Suporte

    from principal.enny.Esqueleto   import Esqueleto
    from principal.enny.Lady_Medusa import Lady_Medusa
    from principal.enny.Lacaios_Desalmados import Lacaios_Desalmados
except ModuleNotFoundError:
    # ABSTRATOS
    from .abstratos.aliado           import Aliado
    from .abstratos.inimigo          import Inimigo

    # MAGIAS
    from .magias.BolaDeFogo          import BolaDeFogo
    from .magias.Ventania            import Ventania
    from .magias.Fumaca              import Fumaça
    from .magias.JadoDAgua           import JatoDAgua

    # STATUS
    from .status.Vida                import Vida
    from .status.Ataque              import Ataque
    from .status.Velocidade          import Velocidade
    from .status.Defesa              import Defesa
    from .status.Carga               import Carga

    # PRINCIPAL
    from .principal.ally.Caçadora    import Caçadora
    from .principal.ally.Ladino      import Ladino
    from .principal.ally.Maga        import Maga
    from .principal.ally.Paladino    import Paladino
    from .principal.ally.Suporte     import Suporte

    from .principal.enny.Esqueleto   import Esqueleto
    from .principal.enny.Lady_Medusa import Lady_Medusa
    from .principal.enny.Lacaios_Desalmados import Lacaios_Desalmados
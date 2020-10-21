from SimpleNegamax import SimpleNegamax
from RandomPlayer import RandomPlayer
from SimpleNegamaxalphabeta import Negamaxalphabeta
from Basic import Basic
from StockFishEngine import StockFishEngine
from Monte_Carlo_Easy import MonteCarloEasy
from Monte_Carlo_Noam import MonteCarlo


class AIPlayerFactory:
    def __init__(self):
        wrp = RandomPlayer('w')
        wsnmp = SimpleNegamax('w')
        brp = RandomPlayer('b')
        bsnmp = SimpleNegamax('b')
        wnab = Negamaxalphabeta('w')
        bnab = Negamaxalphabeta('b')
        bbep = Basic('b')
        wbep = Basic('w')
        wsf = StockFishEngine('w')
        bsf = StockFishEngine('b')
        wmclp = MonteCarloEasy('w')
        bmclp = MonteCarloEasy('b')
        wmcp = MonteCarlo('w')
        bmcp = MonteCarlo('b')
        self.__players = {"0w": wrp, "1w": wsnmp, "0b": brp, "1b": bsnmp, "2w": wnab, "2b": bnab, "3b": bbep,
                          "3w": wbep, "sfw": wsf, "sfb": bsf, "4w": wmclp, "4b": bmclp, "4.5w": wmcp, "4.5b": bmcp}

    def get_player(self, level):
        return self.__players.get(level)

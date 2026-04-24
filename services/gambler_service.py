from models.gambler import Gambler
from repositories.gambler_repository import GamblerRepository
from services.input_validator import InputValidator

class GamblerService:
    MIN_STAKE = 100
    @staticmethod
    def create_gambler(name, initial_balance, win_threshold, loss_threshold):
        InputValidator.validate_initial_stake(GamblerService.MIN_STAKE)
        InputValidator.validate_limits(win_threshold,loss_threshold)
        gambler = Gambler(
            name=name,
            initial_balance=initial_balance,
            current_balance=initial_balance,
            total_winnings=0,
            total_bets=0,
            min_balance=initial_balance,
            win_threshold=win_threshold,
            loss_threshold=loss_threshold
        )

        return GamblerRepository.create(gambler)
    
    @staticmethod
    def get_gambler(gambler_id):
        gambler = GamblerRepository.find_by_id(gambler_id)
        if not gambler:
            raise ValueError("Gambler not found")
        return gambler
    
    @staticmethod
    def update_gambler(gambler_id, **kwargs):
        gambler = GamblerService.get_gambler(gambler_id)

        for key, value in kwargs.items:
            if hasattr(gambler,key):
                setattr(gambler, key, value)

        GamblerRepository.update(gambler)
        return gambler
    
    @staticmethod
    def validate_eligibility(gambler_id):
        gambler = GamblerService.get_gambler(gambler_id)

        if gambler.current_balance < GamblerService.MIN_STAKE:
            return False
        if gambler.current_balance >= gambler.win_threshold:
            return False
        if gambler.current_balance <= gambler.loss_threshold:
            return False
        return True
    
    @staticmethod
    def reset_gambler(gambler_id):
        gambler = GamblerService.get_gambler(gambler_id)

        #proportional reset

        gambler.current_balance = gambler.initial_balance
        gambler.win_threshold = gambler.initial_balance * 2
        gambler.loss_threshold = gambler.initial_balance * 0.5

        GamblerRepository.update(gambler)
        return gambler
    
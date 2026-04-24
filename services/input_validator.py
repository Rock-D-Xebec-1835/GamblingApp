import math
from exceptions.validation_exceptions import *
from models.validation_config import ValidationConfig
from models.validation_error_type import ValidationErrorType

class InputValidator:
    @staticmethod
    def validate_initial_stake(stake):
        if stake is None:
            raise StakeValidationException(
                "Stake cannot be null",
                ValidationErrorType.NULL_ERROR,
                "stake",stake
            )
        if not isinstance(stake, (int, float)):
            raise StakeValidationException(
                "Stake must be numeric",
                ValidationErrorType.NUMERIC_ERROR,
                "stake", stake
            )
        if math.isnan(stake) or math.isinf(stake):
            raise StakeValidationException(
                "Invalid numeric value",
                ValidationErrorType.NUMERIC_ERROR,
                "stake",stake
            )
        if stake <= 0:
            raise StakeValidationException(
                "Stake must be positive",
                ValidationErrorType.RANGE_ERROR,
                "stake",stake
            )
        if stake < ValidationConfig.MIN_STAKE or stake > ValidationConfig.MAX_STAKE:
            raise StakeValidationException(
                "Stake out of alowed range",
                ValidationErrorType.RANGE_ERROR,
                "stake",stake
            )
    
    @staticmethod
    def validate_bet_amount(amount, current_balance):
        if amount <= 0:
            raise BetValidationException(
                "Bet must be positive",
                ValidationErrorType.BET_ERROR,
                "amount", amount
            )
        if amount > current_balance:
            raise BetValidationException(
                "Bet exceeds current balance",
                ValidationErrorType.BET_ERROR,
                "amount", amount
            )
        if amount < ValidationConfig.MIN_BET or amount > ValidationConfig.MAX_BET:
            raise BetValidationException(
                "Bet out of allowed range",
                ValidationErrorType.RANGE_ERROR,
                "amount", amount
            )
    
    @staticmethod
    def validate_limits(win_threshold, loss_threshold):
        if win_threshold <= loss_threshold:
            raise LimitValidationException(
                "Win threshold must be greater than loss threshold",
                ValidationErrorType.LIMIT_ERROR
            )
    
    @staticmethod
    def validate_probability(prob):
        if prob is None:
            return
        if not isinstance(prob, (int, float)):
            raise ProbabilityValidationException(
                "Probability must be numeric",
                ValidationErrorType.NUMERIC_ERROR
            )
        if math.isnan(prob) or math.isinf(prob):
            raise ProbabilityValidationException(
                "Invalid probability value",
                ValidationErrorType.NUMERIC_ERROR
            )
        if prob < 0 or prob > 1:
            raise ProbabilityValidationException(
                "Probability must be between 0 and 1",
                ValidationErrorType.PROBABILITY_ERROR
            )
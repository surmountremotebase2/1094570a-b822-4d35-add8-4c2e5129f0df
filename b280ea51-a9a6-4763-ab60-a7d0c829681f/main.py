from surmount.base_class import Strategy, TargetAllocation
from surmount.logging import log

class TradingStrategy(Strategy):
    
    def __init__(self):
        self.tickers = ["DFEN"]
        # No need to add OHLCV data to data_list, it's automatically included
        self.data_list = []  # Placeholder, as OHLCV is included by default

    @property
    def interval(self):
        return "1day"

    @property
    def assets(self):
        return self.tickers

    @property
    def data(self):
        return self.data_list

    def run(self, data):
        # Initialize allocation with no exposure
        allocation_dict = {"DFEN": 0}
        
        # Accessing the daily OHLCV data for DFEN
        dfen_data = data["ohlcv"][-1]["DFEN"]  # Latest available data
        
        # Calculate volatility as the difference between high and low of the day
        daily_volatility = dfen_data["high"] - dfen_data["low"]
        
        # Normalize or scale daily volatility to determine allocation
        # This simplistic approach increases allocation linearly with increased volatility,
        # capped at a maximum allocation of 1 (or 100% of the portfolio)
        scaled_volatility = min(daily_volatility / dfen_data["low"], 1)  # Normalizing with low price as a simple example
        
        # Update allocation based on calculated volatility
        # Assuming a higher volatility implies higher opportunity (and risk)
        allocation_dict["DFEN"] = scaled_volatility
        
        log(f"Setting DFEN allocation based on daily volatility: {scaled_volatility}")
        
        return TargetAllocation(allocation_dict)
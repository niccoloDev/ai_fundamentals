class Asset:
    def __init__(self, ticker, data, weight=None):
        self.ticker = ticker
        self.data = data
        self.weight = weight

    def to_dict(self):
        return {
            'ticker': self.ticker,
            'weight': self.weight
        }


class Portfolio:
    def __init__(self, assets=None):
        if assets is None:
            self.assets = []
        else:
            self.assets = assets
        self.fitness = None

    def to_string(self):
        str_template = 'Ticker: {} Weight: {} \n'
        ret_str = ''
        for asset in self.assets:
            ret_str += str_template.format(asset.ticker, asset.weight)
        return ret_str

    def __str__(self):
        return self.to_string()

    def __repr__(self):
        return self.to_string()

    def to_dict(self):
        return {
            'assets': [asset.to_dict() for asset in self.assets],
            'fitness': self.fitness
        }

    def add_asset(self, asset):
        self.assets.append(asset)
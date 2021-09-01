import pandas as pd


class TokenLockupModel:
    def __init__(self,
                 opening_price=None,
                 token_freeze_period=None,
                 token_thaw_period=None):
        self.opening_price = opening_price if opening_price is not None else 100
        self.token_freeze_period = token_freeze_period if token_freeze_period is not None else 10
        self.token_thaw_period = token_thaw_period if token_thaw_period is not None else 30
        self.output_dict = {}
        self.output_dict['Input'] = {
            'OpeningPrice': self.opening_price,
            'TokenFreeze': self.token_freeze_period,
            'TokenThaw': self.token_thaw_period
        }

    def get_data(self):
        # Chart Data
        weekly_token_thaw = self.opening_price / self.token_thaw_period
        df = pd.DataFrame(
            {
                'Week': [
                    1,
                    self.token_freeze_period,
                    self.token_freeze_period + self.token_thaw_period,
                    52 if self.token_freeze_period + self.token_thaw_period <= 52 else 260
                ]
            })
        df['Price'] = 0
        df.loc[df['Week'] <= self.token_freeze_period, 'Price'] = self.opening_price
        df.loc[df['Week'] > self.token_freeze_period, 'Price'] = (self.opening_price - (df['Week'] - self.token_freeze_period) * weekly_token_thaw)
        df.loc[df['Price'] < 0, 'Price'] = 0

        self.output_dict['Output'] = {'Chart' : df.to_dict(orient='list')}

        # Table Data
        weeks_table_1_year = [5, 10, 20, 30, 40, 52]
        weeks_table_5_years = [10, 50, 100, 150, 200, 260]
        df = pd.DataFrame(
            {
                'Week': weeks_table_1_year if self.token_freeze_period + self.token_thaw_period <= 52 else weeks_table_5_years
            })
        df['Price'] = 0
        df.loc[df['Week'] <= self.token_freeze_period, 'Price'] = self.opening_price
        df.loc[df['Week'] > self.token_freeze_period, 'Price'] = (self.opening_price - (df['Week'] - self.token_freeze_period) * weekly_token_thaw)
        df.loc[df['Price'] < 0, 'Price'] = 0
        df['TokensReleased'] =  df['Price'] / self.opening_price

        self.output_dict['Output']['Table'] = df.to_dict(orient='list')


        return self.output_dict

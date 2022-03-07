from curses.panel import top_panel
import pandas as pd
import argparse
import plotly.express as px
from kats.consts import TimeSeriesData
from kats.models.prophet import ProphetModel, ProphetParams

DATASET_PATH = './datasets/trends1.csv'

class ProphetForecaster:
    
    
    def __init__(
        self,df_path:str,
        date_col:str,
        value_col:str,
        prophet_params: dict
    ):
        
        self.date_col_name = date_col
        self.value_col_name = value_col
        self.prophet_params = prophet_params
        
        self.df = pd.read_csv(df_path,parse_dates=[self.date_col_name])
        
        self.ts_df = TimeSeriesData(
            self.df[
                [
                    self.date_col_name,
                    self.value_col_name
                ]
            ],
            time_col_name=self.date_col_name
        )
    
    
    def fit(self,pick_last_datapoints_num:int = None):
        
        train_data = None
        self.pick_last_datapoints_num = None
        
        if pick_last_datapoints_num is not None:
            
            self.pick_last_datapoints_num = pick_last_datapoints_num
            train_data = self.ts_df[-pick_last_datapoints_num:]
            
        else:
            
            train_data = self.ts_df
            
        self.prophet_model = ProphetModel(
            data=train_data,
            params=self.prophet_params
        )
        
        self.prophet_model.fit()
        
    def predict(self,step=48):
        
        self.forecast_df = self.prophet_model.predict(steps=step,include_history=True)
        
    def plot_predictions(self):
        
        identifier_col_name = 'label'
        input_df = self.df
        
        input_df[identifier_col_name] = 'unused'
        
        if self.pick_last_datapoints_num is not None:
            
            input_df[identifier_col_name].iloc[-self.pick_last_datapoints_num:] = 'train'
        
        # forecast_renamed = self.forecast_df.rename(
        #     columns={
        #         'time': self.date_col_name,
        #         'fcst' : self.value_col_name
        #     }
        # )
        
        # forecast_renamed[identifier_col_name] = 'forecasted'
        
        new_df = pd.concat(
            [
                input_df,
                self.forecast_df
            ],
            axis=1
        )
    
        fig = px.line(
            new_df,
            x='time',
            y=[self.value_col_name,'fcst']
        )
      
        fig.show()

    
if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--top_name', help='name of the top')
    parser.add_argument('--seasonality_mode', help='either "additive" or "multiplicative" seasonality mode')
    parser.add_argument('--predict_step_size', help='how many steps to predict in future')
    parser.add_argument('--pick_last_datapoints_num', help='number of sequential data point to include for fitting the model',default=None)
    args = parser.parse_args()

    top_name = args.top_name
    seasonality_mode = args.seasonality_mode
    predict_step_size = int(args.predict_step_size)
    pick_last_datapoints_num = int(args.pick_last_datapoints_num) if args.pick_last_datapoints_num is not None else None

    print(seasonality_mode)
    prophet_params = ProphetParams(
        seasonality_mode=seasonality_mode,
        yearly_seasonality=True
    )

    forecaster = ProphetForecaster(
        df_path= DATASET_PATH,
        date_col='date',
        value_col=top_name,
        prophet_params=prophet_params
    )

    forecaster.fit(pick_last_datapoints_num=pick_last_datapoints_num)
    forecaster.predict(step=predict_step_size)
    forecaster.plot_predictions()


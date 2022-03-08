from curses.panel import top_panel
from statistics import mean
import pandas as pd
import argparse
import plotly.express as px
from kats.consts import TimeSeriesData
from kats.models.prophet import ProphetModel, ProphetParams
from sklearn.metrics import mean_squared_error,mean_absolute_error

DATASET_PATH = './datasets/trends1.csv'

class ProphetForecaster:
    """Time Series Forecaster with plotting functionalities
    """
    
    
    def __init__(
        self,df_path:str,
        date_col:str,
        value_col:str,
        prophet_params: ProphetParams
    ):
        """

        Args:
            df_path (str): path to csv file
            date_col (str): name of date column to be used for time series
            value_col (str): name of value column to be forecasted
            prophet_params (ProphetParams): parameters that will be passed to prophet model
        """
        
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
        """fit the prophet model on training data

        Args:
            pick_last_datapoints_num (int, optional): index of the first data points to be chosen for the training.
            For now, model is fitted 
            on the entire training set. Defaults to None.
        """
        
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
        """predict using the fitted model

        Args:
            step (int, optional): number of steps to predict in future. Defaults to 48.
        """
        self.prediction_step = step
        self.forecast_df = self.prophet_model.predict(steps=step,include_history=True)
        
    def plot_predictions(self):
        """plot the prediction along with the historical data 
        """
        
        identifier_col_name = 'label'
        input_df = self.df
        
        input_df[identifier_col_name] = 'unused'
        
        if self.pick_last_datapoints_num is not None:
            
            input_df[identifier_col_name].iloc[-self.pick_last_datapoints_num:] = 'train'
        
        new_df = pd.concat(
            [
                input_df,
                self.forecast_df
            ],
            axis=1
        )
        history_df = new_df.iloc[:-self.prediction_step]

        rmse = mean_squared_error(history_df[self.value_col_name],history_df['fcst'],squared=False)
        mae = mean_absolute_error(history_df[self.value_col_name],history_df['fcst'])
        
        fig = px.line(
            new_df,
            x='time',
            y=[self.value_col_name,'fcst'],
            title= f'Using FBProphet RMSE {rmse} and MAE {mae}'
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


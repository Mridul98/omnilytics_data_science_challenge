from time import time
import pandas as pd
from kats.consts import TimeSeriesData
from kats.models.linear_model import LinearModel, LinearModelParams
from kats.tsfeatures.tsfeatures import TsFeatures

TREND_DATASET_PATH = 'datasets/trends1.csv'


class Result:

    def __init__(
        self,df_path,
        date_column_name='date',
        top_column_names=['top 1','top 2','top 3']
    ) -> None:

        self.time_series_df = pd.read_csv(df_path,
                                          parse_dates=[date_column_name],
                                          low_memory=False)

        self.top_column_name_list = top_column_names
        self.date_column_name = date_column_name
        self.feature_model = TsFeatures(
            selected_features=[
                'linearity',
                'trend_strength'
            ]
        )

    @property
    def preprocessed_dataset(self):
    

        convert_dtype_dict = {i: float for i in self.top_column_name_list}
        
        self.time_series_df.astype(convert_dtype_dict)
        self.time_series_df.sort_values(by=self.date_column_name,
                                        ascending=True,inplace=True)
        
        time_series_df_resampled = self.time_series_df.set_index('date')\
                                            .resample('M').mean().reset_index()
        
        return time_series_df_resampled

        
    
    def last_12m(self,top_name:str) -> None:
        
        if top_name not in self.top_column_name_list:
            raise ValueError('top name not found in the dataframe')
        else:
            last_year_df = self.preprocessed_dataset[[self.date_column_name,top_name]].iloc[-12:]

            ts_last_year_data = TimeSeriesData(
                df=last_year_df,
                time_col_name=self.date_column_name
            )
            linear_model = LinearModel(
                data=ts_last_year_data,
                params=LinearModelParams()
            )
            linear_model.fit()

            slope,intercept = linear_model.model.params['x1'], linear_model.model.params['const']

            ts_features = self.feature_model.transform(ts_last_year_data)
            
            trend_strength, linearity = ts_features['trend_strength'], ts_features['linearity']

            return f'the slope of the model for {top_name} is {slope} and intercept {intercept} and trend strength {trend_strength} with linearity {linearity}'


if __name__ == '__main__':

    result = Result(df_path=TREND_DATASET_PATH)
    
    for x in ['top 1','top 2','top 3']:
        print(result.last_12m(top_name=x))

    


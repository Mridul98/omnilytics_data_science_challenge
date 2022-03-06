import pandas as pd
from kats.consts import TimeSeriesData
from kats.models.linear_model import LinearModel, LinearModelParams
from kats.tsfeatures.tsfeatures import TsFeatures


TREND_DATASET_PATH = 'datasets/trends1.csv'


class Result:

    def __init__(
        self,df_path:str,
        date_column_name='date',
        top_column_names=['top 1','top 2','top 3']
    ) -> None:
        """

        Args:
            df_path (str): path to csv trend csv files
            date_column_name (str, optional): name of the date column of the corresponding 
            csv files containing time series data. Defaults to 'date'.
            top_column_names (list, optional): list of column name 
            that represents name of different tops . Defaults to ['top 1','top 2','top 3'].
        """

        self.time_series_df = pd.read_csv(df_path,
                                          parse_dates=[date_column_name],
                                          low_memory=False)

        self.top_column_name_list = top_column_names
        self.date_column_name = date_column_name

        ## stl features
        self.feature_model = TsFeatures(
            selected_features=[
                'linearity',
                'trend_strength'
            ]
        )

    @property
    def preprocessed_dataset(self) -> pd.DataFrame:
        """preprocessed time series dataset with resampled values
        from weekly to monthly total

        Returns:
            pd.DataFrame: time series data with resampled monthly values
        """

        convert_dtype_dict = {i: float for i in self.top_column_name_list}
        
        self.time_series_df.astype(convert_dtype_dict)
        self.time_series_df.sort_values(by=self.date_column_name,
                                        ascending=True,inplace=True)
        
        time_series_df_resampled = self.time_series_df.set_index('date')\
                                            .resample('M').sum().reset_index()
        
        return time_series_df_resampled

    @property
    def preprocessed_dataset_cumsum(self) -> pd.DataFrame:
        """preprocessed cumulative sum time series of 
        tops trends dataset

        Returns:
            pd.DataFrame: dataframe containing monthly cumulative sum of tops values
        """

        trend_cumsum_df = self.preprocessed_dataset.set_index(self.date_column_name)\
                              .cumsum().reset_index()

        return trend_cumsum_df


    def __get_time_series_stats(self,top_name:str,month_lag:int) -> dict:
        """get stl features for the time series of the given top name
        For now it returns only time series regresssiong coefficients, linearity and trend strength

        Args:
            top_name (str): _description_
            month_lag (int): _description_

        Raises:
            ValueError: _description_

        Returns:
            dict: _description_
        """
        if top_name not in self.top_column_name_list:
            raise ValueError('top name not found in the dataframe')
        else:

            month_lag_df = self.preprocessed_dataset[[self.date_column_name,top_name]].iloc[-month_lag:]
            
            ts_last_year_data = TimeSeriesData(
                df=month_lag_df,
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

            return {

                'slope' : slope,
                'intercept' : intercept,
                'trend_strength' : trend_strength,
                'linearity' : linearity
            }
    
    def __get_descriptive_stats(self,top_name:str,month_lag:int) -> dict:
        """get descriptive stats about the tops performance.
        For now, it is only cumulative growth rate

        Args:
            top_name (str): _description_
            month_lag (int): _description_

        Returns:
            dict: _description_
        """
        month_lag_cumsum_df = self.preprocessed_dataset_cumsum.iloc[-month_lag:]

        monthly_cumulative_growth_rate = (
            (
                month_lag_cumsum_df[top_name].values[-1]
                /
                month_lag_cumsum_df[top_name].values[0]
            ) 
            ** (1 / month_lag) - 1
        ) * 100

        return {
            "monthly_cumulative_growth_rate" : monthly_cumulative_growth_rate
        }


    def __get_trend_verb(self,slope:float) -> str:
        """get appropriate string for 
        representing trend behaviour

        Args:
            slope (float): slope coefficient of linear regression
            of univariate time series

        Returns:
            str: _description_
        """
        if slope == 0:
            return 'no trending'

        if slope < 0:
            return 'downward trending'

        if slope > 0:
            return 'upward trending'


    def last_12m(self,top_name:str) -> dict:
        """calculate performance related stats for the given top
        and return results

        Args:
            top_name (str): _description_

        Raises:
            ValueError: raised when the top name is not in the 
            preprocessed dataframe

        Returns:
            dict: dictionary containing performance related stats
        """
        
        if top_name not in self.top_column_name_list:
            raise ValueError('top name not found in the dataframe')
        else:
            stl_features = self.__get_time_series_stats(top_name=top_name,month_lag=12)
            descriptive_stats = self.__get_descriptive_stats(top_name=top_name,month_lag=12)

            final_result = {**stl_features, **descriptive_stats}
            
            return final_result


    def perf_12m(self,top_name:str):
        
        perf_result = self.last_12m(top_name=top_name)

        slope = perf_result['slope']
        slope_str = "{:.2f}".format(slope)
        cmgr = "{:.2f}".format(perf_result['monthly_cumulative_growth_rate'])

        result_string = f'''{top_name}'s last year cumulative monthly growth rate is: {cmgr} % with {self.__get_trend_verb(slope)} of co-efficient {slope_str} approx.'''
        return {
            top_name : result_string
        }


if __name__ == '__main__':

    result = Result(df_path=TREND_DATASET_PATH)
    
    for x in ['top 1','top 2','top 3']:
        print(result.perf_12m(top_name=x))

    


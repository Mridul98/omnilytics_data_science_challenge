## Before running any program, please consider installing 
## packages defined in 'solutions/requirements.txt'
## please install the packages in a python virtual environment
    1. Run pip3 install -r 'solutions/requirements.txt'

## Part - 1
## Performance were evaluated based on 3 criteria
    1. Cumulative monthly growth rate (it is the indicator of the last years growth)
    2. Trend estimation using Linear Regression (it is the indicator whether the trend is downward or upward)
    3. Linearity Strength of the time series (indicator of how the linear the time series is. Value close to 0 means the time series is fairly non-linear)

    (most of the time, cumulative monthly growth rate is enough to measure the performance of different tops)
### Performance measured using CMGR (Cumulative Monthly Growth Rate): 

    ((t_s/t_e)^(1/window_length)) - 1

### where, t_s is total sales up until timestamp s from the beginning and t_e is total sales up until timestamp  e from s.
### and the window_length = |s-e| (for this purpose, it is equal to 12, since we are calculating based on the cumulative performance of the last year only)

### 2 and 3. the corresponding code of these part can be found in solutions/results.py module.

#### how to run the code related to part 1

    1. change directory to solutions/
    2. run 'python3 results.py'

## Part - 2 

### Evaluation of the different fit for different tops using RMSE

    fit top1  = 2.14929
    fit2 top1 = 1.7787
    fit3 top1 = 1.7579
    
    best fit for top1 (best to worst): fit3 > fit2 > fit 1 

    fit top2  = 8.3345
    fit2 top2 = 4.4031
    fit3 top2 = 3.6099

    best fit for top2 (best to worst): fit3 > fit2 > fit

    fit top3  = 2.9793
    fit2 top3 = 2.4637
    fit3 top3 = 2.3682

    best fit for top3 (best to worst): fit3 > fit2 > fit

    prophet top 1 = 1.7560
    prophet top 2 = 3.8190
    prophet top 3 = 2.4147



### forecasting using prophet model with yearly seasonality

### top 1
![forecasted top 1](/solutions/plot_images/prophet_top1.png)
### top 2
![forecasted top 2](/solutions/plot_images/prophet_top2.png)
### top 3
![forecasted top 2](/solutions/plot_images/prophet_top3.png)

    prophet top 1 = 1.7560
    prophet top 2 = 3.8190
    prophet top 3 = 2.4147
    
## How to run prophet forecasting:

    1. Run 'cd solutions/'
    2. run 'python3 forecast.py --top_name 'top 1' --seasonality_mode 'multiplicative' --predict_step_size 144

    Here, (predict_step_size / 4) = the number of weeks to be forecasted



## Overall performance ranking (Best to worst): 

### top 1:

    prophet top 1 > fit3 top 1 > fit2 top 1 > fit top 1

### top 2:

    fit3 top2 > prophet top 2 > fit2 top 2 > fit top 1

### top 3:

    fit3 top3 > prophet top 3 > fit2 top 3 > fit top 1
    


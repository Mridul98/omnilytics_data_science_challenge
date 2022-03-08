## Part - 1

1. ### Performance measured using CMGR (Cumulative Monthly Growth Rate): 

    (t_s/t_e)**(1/window_length) - 1

### where, t_s is total sales up until timestamp s from the beginning and t_e is total sales up until timestamp  e from s.
### and the window_length = |s-e|

2 and 3. ### the corresponding code of this part can be found in solutions/results.py module.

## Part - 2 

### forecasting using prophet model with yearly seasonality

![forecasted top 1](/solutions/plot_images/prophet_top1.png)
![forecasted top 2](/solutions/plot_images/prophet_top2.png)
![forecasted top 2](/solutions/plot_images/prophet_top3.png)

# RMSE:
    fit top1  = 2.14929
    fit2 top1 = 1.7787
    fit3 top1 = 1.7579
    
    fit top2  = 8.3345
    fit2 top2 = 4.4031
    fit3 top2 = 3.6099

    fit top3  = 2.9793
    fit2 top3 = 2.4637
    fit3 top3 = 2.3682

    prophet top 1 = 1.7560
    prophet top 2 = 3.8190
    prophet top 3 = 2.4147
    

## Overall performance ranking (Best to worst): 

### top 1:

    prophet top 1 > fit3 top 1 > fit2 top 1 > fit top 1

### top 2:

    fit3 top2 > prophet top 2 > fit2 top 2 > fit top 1

### top 3:

    fit3 top3 > prophet top 3 > fit2 top 3 > fit top 1
    


# from https://medium.com/@emredjan/emulating-r-regression-plots-in-python-43741952c034
# and https://data.library.virginia.edu/diagnostic-plots/


def diagnostic_plot(model_fit, df_name, response_variable):
    import numpy as np
    import pandas as pd

    import seaborn as sns
    import matplotlib.pyplot as plt

    import statsmodels.formula.api as smf
    from statsmodels.graphics.gofplots import ProbPlot

    plt.style.use('seaborn') # pretty matplotlib plots
    plt.rc('font', size=14)
    plt.rc('figure', titlesize=18)
    plt.rc('axes', labelsize=15)
    plt.rc('axes', titlesize=18)


    # Calculations required for some of the plots
    # fitted values (need a constant term for intercept)
    model_fitted_y = model_fit.fittedvalues

    # model residuals
    model_residuals = model_fit.resid

    # normalized residuals
    model_norm_residuals = model_fit.get_influence().resid_studentized_internal

    # absolute squared normalized residuals
    model_norm_residuals_abs_sqrt = np.sqrt(np.abs(model_norm_residuals))

    # absolute residuals
    model_abs_resid = np.abs(model_residuals)

    # leverage, from statsmodels internals
    model_leverage = model_fit.get_influence().hat_matrix_diag

    # cook's distance, from statsmodels internals
    model_cooks = model_fit.get_influence().cooks_distance[0]



    #### Residual plot
    '''This plot shows if residuals have non-linear patterns. There could be a non-linear
    relationship between predictor variables and an outcome variable and the pattern could
    show up in this plot if the model doesn’t capture the non-linear relationship.
    If you find equally spread residuals around a horizontal line with distinct patterns,
    that is a good indication you don’t have non-linear relationships.
    '''

    #Draws a scatterplot of fitted values against residuals, with a
    #“locally weighted scatterplot smoothing (lowess)”
    #regression line showing any apparent trend.
    plot_lm_1 = plt.figure(1)
    plot_lm_1.set_figheight(4)
    plot_lm_1.set_figwidth(6)

    plot_lm_1.axes[0] = sns.residplot(model_fitted_y, response_variable, data=df_name,
                                      lowess=True,
                                      scatter_kws={'alpha': 0.5},
                                      line_kws={'color': 'red', 'lw': 1, 'alpha': 0.8})

    plot_lm_1.axes[0].set_title('Residuals vs Fitted')
    plot_lm_1.axes[0].set_xlabel('Fitted values')
    plot_lm_1.axes[0].set_ylabel('Residuals')


    # annotations
    abs_resid = model_abs_resid.sort_values(ascending=False)
    abs_resid_top_3 = abs_resid[:3]

    for i in abs_resid_top_3.index:
        plot_lm_1.axes[0].annotate(i,
                                   xy=(model_fitted_y[i],
                                       model_residuals[i]));



    #### QQ plot
    '''This plot shows if residuals are normally distributed. Do residuals follow
    a straight line well or do they deviate severely? It’s good if residuals are
    lined well on the straight dashed line.
    '''

    #This one shows how well the distribution of residuals fit the normal
    #distribution. This plots the standardized (z-score) residuals against
    #the theoretical normal quantiles. Anything quite off the diagonal
    #lines may be a concern for further investigation.
    QQ = ProbPlot(model_norm_residuals)
    plot_lm_2 = QQ.qqplot(line='45', alpha=0.5, color='#4C72B0', lw=1)

    plot_lm_2.set_figheight(4)
    plot_lm_2.set_figwidth(6)

    plot_lm_2.axes[0].set_title('Normal Q-Q')
    plot_lm_2.axes[0].set_xlabel('Theoretical Quantiles')
    plot_lm_2.axes[0].set_ylabel('Standardized Residuals');

    # annotations
    abs_norm_resid = np.flip(np.argsort(np.abs(model_norm_residuals)), 0)
    abs_norm_resid_top_3 = abs_norm_resid[:3]

    for r, i in enumerate(abs_norm_resid_top_3):
        plot_lm_2.axes[0].annotate(i,
                                   xy=(np.flip(QQ.theoretical_quantiles, 0)[r],
                                       model_norm_residuals[i]));

    #### Scale-Location Plot
    '''It’s also called Spread-Location plot. This plot shows if residuals
    are spread equally along the ranges of predictors. This is how you can
    check the assumption of equal variance (homoscedasticity). It’s good if
    you see a horizontal line with equally (randomly) spread points.
    '''
    #This is another residual plot, showing their spread,
    #which you can use to assess heteroscedasticity.
    #It’s essentially a scatter plot of absolute square-rooted normalized
    #residuals and fitted values, with a lowess regression line.
    plot_lm_3 = plt.figure(3)
    plot_lm_3.set_figheight(4)
    plot_lm_3.set_figwidth(6)

    plt.scatter(model_fitted_y, model_norm_residuals_abs_sqrt, alpha=0.5)
    sns.regplot(model_fitted_y, model_norm_residuals_abs_sqrt,
                scatter=False,
                ci=False,
                lowess=True,
                line_kws={'color': 'red', 'lw': 1, 'alpha': 0.8})

    plot_lm_3.axes[0].set_title('Scale-Location')
    plot_lm_3.axes[0].set_xlabel('Fitted values')
    plot_lm_3.axes[0].set_ylabel('$\sqrt{|Standardized Residuals|}$');

    # annotations
    abs_sq_norm_resid = np.flip(np.argsort(model_norm_residuals_abs_sqrt), 0)
    abs_sq_norm_resid_top_3 = abs_sq_norm_resid[:3]

    for i in abs_norm_resid_top_3:
        plot_lm_3.axes[0].annotate(i,
                                   xy=(model_fitted_y[i],
                                       model_norm_residuals_abs_sqrt[i]));


    #### Leverage plot
    '''This plot helps us to find influential cases (i.e., subjects) if any.
    Not all outliers are influential in linear regression analysis (whatever outliers mean).
    Even though data have extreme values, they might not be influential to determine a
    regression line. That means, the results wouldn’t be much different if we either
    include or exclude them from analysis. They follow the trend in the majority of cases
    and they don’t really matter; they are not influential. On the other hand, some cases
    could be very influential even if they look to be within a reasonable range of the values.
    They could be extreme cases against a regression line and can alter the results if we
    exclude them from analysis. Another way to put it is that they don’t get along with
    the trend in the majority of the cases.

    Unlike the other plots, this time patterns are not relevant. We watch out for outlying
    values at the upper right corner or at the lower right corner. Those spots are the places
    where cases can be influential against a regression line. Look for cases outside of a
    dashed line, Cook’s distance. When cases are outside of the Cook’s distance (meaning
    they have high Cook’s distance scores), the cases are influential to the regression
    results. The regression results will be altered if we exclude those cases.
    '''

    #This plot shows if any outliers have influence over the regression fit.
    #Anything outside the group and outside “Cook’s Distance” lines,
    # may have an influential effect on model fit.
    plot_lm_4 = plt.figure(4)
    plot_lm_4.set_figheight(4)
    plot_lm_4.set_figwidth(6)

    plt.scatter(model_leverage, model_norm_residuals, alpha=0.5)
    sns.regplot(model_leverage, model_norm_residuals,
                scatter=False,
                ci=False,
                lowess=True,
                line_kws={'color': 'red', 'lw': 1, 'alpha': 0.8})

    plot_lm_4.axes[0].set_xlim(0, 0.20)
    plot_lm_4.axes[0].set_ylim(-3, 5)
    plot_lm_4.axes[0].set_title('Residuals vs Leverage')
    plot_lm_4.axes[0].set_xlabel('Leverage')
    plot_lm_4.axes[0].set_ylabel('Standardized Residuals')

    # annotations
    leverage_top_3 = np.flip(np.argsort(model_cooks), 0)[:3]

    for i in leverage_top_3:
        plot_lm_4.axes[0].annotate(i,
                                   xy=(model_leverage[i],
                                       model_norm_residuals[i]))

    # shenanigans for cook's distance contours
    def graph(formula, x_range, label=None):
        x = x_range
        y = formula(x)
        plt.plot(x, y, label=label, lw=1, ls='--', color='red')

    p = len(model_fit.params) # number of model parameters

    graph(lambda x: np.sqrt((0.5 * p * (1 - x)) / x),
          np.linspace(0.001, 0.200, 50),
          'Cook\'s distance') # 0.5 line

    graph(lambda x: np.sqrt((1 * p * (1 - x)) / x),
          np.linspace(0.001, 0.200, 50)) # 1 line

    plt.legend(loc='upper right');

    plt.show()
    sns.reset_orig()

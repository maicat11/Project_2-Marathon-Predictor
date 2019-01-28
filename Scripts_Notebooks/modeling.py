import numpy as np
import seaborn as sns; sns.set()
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score


# Split the data into train, val, test
def split_data(df, X_cols):
    '''Split the data into train, validate, test data by columns provided.'''

    X = df[X_cols]
    y = df[['finish_time']]

    # split the model into train-validation and test sets
    X, X_test, y, y_test = train_test_split(X, y, test_size=.2, random_state=11)
    # further split data for train and validation
    X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=.2, random_state=11)
    return X_train, y_train, X_val, y_val, X_test, y_test


def model_results(model, X_train, y_train, X_val, y_val):
    '''Create a pipeline for linear regression. Return R^2 and RMSE values.'''
    model.fit(X_train, y_train)
    predictions = model.predict(X_val)
    RMSE = np.sqrt(mean_squared_error(y_val, predictions))
    r2_squared = r2_score(y_val, predictions)
    residuals = y_val - predictions
    return r2_squared, RMSE, residuals, predictions


def plot_learning_curves(model, X_train, y_train, X_val, y_val):
    '''Graph learning curves.'''
    train_errors, val_errors = [], []
    for m in range(1, len(X_train)):
        model.fit(X_train[:m], y_train[:m])
        y_train_predict = model.predict(X_train[:m])
        y_val_predict = model.predict(X_val)
        train_errors.append(np.sqrt(mean_squared_error(y_train_predict, y_train[:m])))
        val_errors.append(np.sqrt(mean_squared_error(y_val_predict, y_val)))
    sns.set(style="darkgrid")
    plt.figure(num=1, figsize=(15, 5))
    plt.plot(np.sqrt(train_errors), 'r-+', linewidth=2, label='train', color='red', )
    plt.plot(np.sqrt(val_errors), 'r-+', linewidth=2, label='val', color='royalblue')
    plt.title('Learning Curves', size=20)
    plt.xlabel('Training Set Size', size=15)
    plt.ylabel('RMSE', size=15)
    plt.legend()
    plt.xscale('log')
    plt.yscale('log');


def residuals_plot(predictions, residuals, X_val):
    sns.set(style="whitegrid")
    plt.figure(figsize=(15, 5))
    sns.scatterplot(x=list(predictions), y=list(residuals), legend='full',
                    hue=X_val['Gender_F'], palette={1: 'red', 0: 'royalblue'})
    plt.title('Residuals Plot', size=20)
    plt.xlabel('Predictions', size=15)
    plt.ylabel('Residuals', size=15);

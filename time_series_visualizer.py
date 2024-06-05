import calendar
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()
import matplotlib.dates as mdates

global df
df = pd.read_csv("fcc-forum-pageviews.csv", index_col='date', parse_dates=True)
df = df[(df['value'] > df['value'].quantile(0.025)) & (df['value'] < df['value'].quantile(0.975))]


def draw_line_plot():
    df1 = df.copy()
    # Draw line plot
    fig, ax = plt.subplots(figsize=(18,7))

    ax.plot(df1.index, df1['value'])
    ax.set_xlabel('Date')
    ax.set_ylabel('Page Views')
    ax.set_title('Daily freeCodeCamp Forum Page Views 5/2016-12/2019')
    ax.set_ylim([0, df1['value'].max() * 0.17])



    # Save image and return fig (don't change this part)
    fig.savefig('line_plot.png')
    return fig

def draw_bar_plot():
    # Copy and modify data for monthly bar plot
    df_bar = df.copy()
    # Draw bar plot
    df_bar = df_bar.groupby([df_bar.index.year, df_bar.index.month_name()]).mean().value.unstack()
    # Sort columns by month names
    df_bar = df_bar[list(calendar.month_name)[1:]]
    df_bar.columns.name = "Months"
    fig = df_bar.plot(kind="bar", figsize=(12, 6), xlabel="Years", ylabel="Average Page Views").get_figure()
    fig.savefig('bar_plot.png')
    return fig

def draw_box_plot():
    # Prepare data for box plots (this part is done!)
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = [d.year for d in df_box.date]
    df_box['month'] = [d.strftime('%b') for d in df_box.date]

    # Draw box plots (using Seaborn)

    month_dict = {'Jan': 1, 'Feb': 2, 'Mar': 3, 'Apr': 4, 'May': 5, 'Jun': 6, 'Jul': 7, 'Aug': 8, 'Sep': 9, 'Oct': 10, 'Nov': 11, 'Dec': 12}

    # Create a new column 'month_num' that maps the 'month' column to month numbers using the dictionary
    df_box['month_num'] = df_box['month'].map(month_dict)

    # Sort df_box by 'month_num'
    df_box.sort_values('month_num', inplace=True)

    fig, ax= plt.subplots(ncols=2,figsize=(15,7))
    sns.boxplot(data=df_box,x='year',y='value', ax=ax[0])
    ax[0].set_title('Year-wise Box Plot (Trend)')
    ax[0].set_xlabel('Year')
    ax[0].set_ylabel('Page Views')

    sns.boxplot(data=df_box, x='month', y='value', ax=ax[1])
    ax[1].set_title('Month-wise Box Plot (Seasonality)')
    ax[1].set_xlabel('Month')
    ax[1].set_ylabel('Page Views')




    # Save image and return fig (don't change this part)
    fig.savefig('box_plot.png')
    return fig
    
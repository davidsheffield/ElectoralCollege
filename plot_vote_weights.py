import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


color_democratic = '#0044c9'
color_republican = '#e81b23'
color_other = '#F2DF0A'


def get_data():
    """
    Load and preprocess voting data for multiple years.

    This function reads CSV files containing voting data for specified years,
    calculates the electoral vote weights for each state, and returns the
    processed data in a dictionary.

    Returns:
        dict: A dictionary where keys are years (as strings) and values are
              DataFrames containing the processed voting data for each year.
    """
    years = ['2000', '2004', '2008', '2012', '2016', '2020']

    data = {}
    for year in years:
        print(year)
        tmp_data = pd.read_csv(f'data/{year}.csv')
        data[year] = calculate_weights(tmp_data)

    return data


def calculate_weights(data):
    """
    Calculate weights.
    Electoral College votes per vote
    Weight = (Electoral College votes per vote) / (Average Electoral College votes per vote)
    Vote percentage = (Number of votes in state) / (Number of national votes for that party)
    """

    data['Democratic EV per vote'] = data['Democratic EV'] / data['Democratic Vote']
    data['Republican EV per vote'] = data['Republican EV'] / data['Republican Vote']
    data.loc[data['State'] == 'ME-1', 'Democratic EV per vote'] = (data.loc[data['State'] == 'Maine','Democratic EV per vote'].to_numpy()
                                                                   + data.loc[data['State'] == 'ME-1', 'Democratic EV per vote'].to_numpy())
    data.loc[data['State'] == 'ME-2', 'Democratic EV per vote'] = (data.loc[data['State'] == 'Maine','Democratic EV per vote'].to_numpy()
                                                                   + data.loc[data['State'] == 'ME-2', 'Democratic EV per vote'].to_numpy())
    data.loc[data['State'] == 'ME-1', 'Republican EV per vote'] = (data.loc[data['State'] == 'Maine','Republican EV per vote'].to_numpy()
                                                                   + data.loc[data['State'] == 'ME-1', 'Republican EV per vote'].to_numpy())
    data.loc[data['State'] == 'ME-2', 'Republican EV per vote'] = (data.loc[data['State'] == 'Maine','Republican EV per vote'].to_numpy()
                                                                   + data.loc[data['State'] == 'ME-2', 'Republican EV per vote'].to_numpy())
    data.loc[data['State'] == 'NE-1', 'Democratic EV per vote'] = (data.loc[data['State'] == 'Nebraska','Democratic EV per vote'].to_numpy()
                                                                   + data.loc[data['State'] == 'NE-1', 'Democratic EV per vote'].to_numpy())
    data.loc[data['State'] == 'NE-2', 'Democratic EV per vote'] = (data.loc[data['State'] == 'Nebraska','Democratic EV per vote'].to_numpy()
                                                                   + data.loc[data['State'] == 'NE-2', 'Democratic EV per vote'].to_numpy())
    data.loc[data['State'] == 'NE-3', 'Democratic EV per vote'] = (data.loc[data['State'] == 'Nebraska','Democratic EV per vote'].to_numpy()
                                                                   + data.loc[data['State'] == 'NE-3', 'Democratic EV per vote'].to_numpy())
    data.loc[data['State'] == 'NE-1', 'Republican EV per vote'] = (data.loc[data['State'] == 'Nebraska','Republican EV per vote'].to_numpy()
                                                                   + data.loc[data['State'] == 'NE-1', 'Republican EV per vote'].to_numpy())
    data.loc[data['State'] == 'NE-2', 'Republican EV per vote'] = (data.loc[data['State'] == 'Nebraska','Republican EV per vote'].to_numpy()
                                                                   + data.loc[data['State'] == 'NE-2', 'Republican EV per vote'].to_numpy())
    data.loc[data['State'] == 'NE-3', 'Republican EV per vote'] = (data.loc[data['State'] == 'Nebraska','Republican EV per vote'].to_numpy()
                                                                   + data.loc[data['State'] == 'NE-3', 'Republican EV per vote'].to_numpy())

    # Filter out Maine and Nebraska to use the congressional districts for those states instead
    # no_ME_NE = ~data['State'].isin(['Maine', 'Nebraska'])
    data = data.loc[~data['State'].isin(['Maine', 'Nebraska'])].reset_index(drop=True)

    # mean_EV_per_vote = (((data.loc[no_ME_NE, 'Democratic EV per vote']
    #                       * data.loc[no_ME_NE, 'Democratic Vote']).sum()
    #                      + (data.loc[no_ME_NE, 'Republican EV per vote']
    #                         * data.loc[no_ME_NE, 'Republican Vote']).sum())
    #                     / (data.loc[no_ME_NE, 'Democratic Vote'].sum()
    #                        + data.loc[no_ME_NE, 'Republican Vote'].sum()
    #                        + data.loc[no_ME_NE, 'Other Vote'].sum()))
    mean_EV_per_vote = (((data['Democratic EV per vote'] * data['Democratic Vote']).sum()
                         + (data['Republican EV per vote'] * data['Republican Vote']).sum())
                        / (data['Democratic Vote'].sum()
                           + data['Republican Vote'].sum()
                           + data['Other Vote'].sum()))
    print('Mean EV per vote:', mean_EV_per_vote)

    data['Democratic Weight'] = data['Democratic EV per vote'] / mean_EV_per_vote
    data['Republican Weight'] = data['Republican EV per vote'] / mean_EV_per_vote

    # data['Democratic Vote Percentage'] = data['Democratic Vote'] / data.loc[no_ME_NE, 'Democratic Vote'].sum()
    # data['Republican Vote Percentage'] = data['Republican Vote'] / data.loc[no_ME_NE, 'Republican Vote'].sum()
    data['Democratic Vote Percentage'] = data['Democratic Vote'] / data['Democratic Vote'].sum()
    data['Republican Vote Percentage'] = data['Republican Vote'] / data['Republican Vote'].sum()

    # data.loc[~data['State'].isin(['Maine', 'Nebraska'])].groupby('Democratic EV per vote')['Democratic Vote'].sum()

    return data


def plot_weight_vs_votes_by_year(data, year):
    """
    Scatter plot for one year of the electoral votes per vote vs number of votes
    """

    democratic = data[year].groupby('Democratic EV per vote')['Democratic Vote'].sum().reset_index()
    republican = data[year].groupby('Republican EV per vote')['Republican Vote'].sum().reset_index()
    other_votes = data[year]['Other Vote'].sum()

    plt.scatter(democratic['Democratic Vote'],
                democratic['Democratic EV per vote'],
                color=color_democratic)
    plt.scatter(republican['Republican Vote'],
                republican['Republican EV per vote'],
                color=color_republican)
    plt.scatter(other_votes,
                0,
                color=color_other)

    plt.tick_params(axis='both', direction='in')

    plt.xlim(0, 4e7)
    plt.ylim(0, 1.6e-5)

    plt.xlabel(f'Votes in {year}')
    plt.ylabel('Electoral votes per vote')

    plt.show()

    breakpoint()
    pass


def plot_weight_bars_by_year(data, year):
    """
    Plot for one year of the electoral votes per vote with bar widths equal to the number of votes
    """

    # democratic = data[year].groupby('Democratic EV per vote')['Democratic Vote'].sum().reset_index()
    # democratic['Cumulative Vote'] = democratic['Democratic Vote'].cumsum()
    # democratic['Vote Fraction'] = democratic['Cumulative Vote'] / democratic['Cumulative Vote'].tail(1).to_numpy()
    # republican = data[year].groupby('Republican EV per vote')['Republican Vote'].sum().reset_index()
    # republican['Cumulative Vote'] = republican['Republican Vote'].cumsum()
    # republican['Vote Fraction'] = republican['Cumulative Vote'] / republican['Cumulative Vote'].tail(1).to_numpy()

    vote_fraction = 0
    democratic_x = []
    democratic_y = []
    for idx, row in data.sort_values('Democratic Weight').iterrows():
        democratic_x.append(vote_fraction)
        democratic_y.append(row['Democratic Weight'])
        vote_fraction += row['Democratic Vote Percentage']
        democratic_x.append(vote_fraction)
        democratic_y.append(row['Democratic Weight'])
    
    vote_fraction = 0
    republican_x = []
    republican_y = []
    for idx, row in data.sort_values('Republican Weight').iterrows():
        republican_x.append(vote_fraction)
        republican_y.append(row['Republican Weight'])
        vote_fraction += row['Republican Vote Percentage']
        republican_x.append(vote_fraction)
        republican_y.append(row['Republican Weight'])

    fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True)

    # ax1.plot(democratic_x, democratic_y)
    ax1.fill_between(democratic_x, democratic_y, color=color_democratic)
    ax1.set_xlim(0, 1)
    ax1.set_ylim(0, 5)
    ax1.set_ylabel('Democratic voters')
    ax1.set_title(f'Vote weights in {year} election')

    # ax2.plot(republican_x, republican_y)
    ax2.fill_between(republican_x, republican_y, color=color_republican)
    ax2.set_xlim(0, 1)
    ax2.set_ylim(0, 5)
    ax2.set_xlabel('Percentage of votes')
    ax2.set_ylabel('Republican voters')

    plt.tick_params(axis='both', direction='in')

    plt.tight_layout()
    plt.subplots_adjust(hspace=0)

    plt.show()


def plot_bubbles(data, years):
    """
    Bubble plot of vote weight with bubbles equal to the number of votes
    """

    fig, axs = plt.subplots(len(years), 1, sharex=True) # , figsize=(15, 5 * len(years)))

    divisor = 30000

    for i, year in enumerate(reversed(years)):
        democratic = data[year].groupby('Democratic Weight')['Democratic Vote'].sum() / divisor
        axs[i].scatter(democratic.index, np.zeros_like(democratic), s=democratic, alpha=0.5, c=color_democratic, edgecolors='w')
        republican = data[year].groupby('Republican Weight')['Republican Vote'].sum() / divisor
        axs[i].scatter(republican.index, np.zeros_like(republican), s=republican, alpha=0.5, c=color_republican, edgecolors='w')
        axs[i].scatter([0], [0], s=data[year]['Other Vote'].sum() / divisor, alpha=0.5, c=color_other, edgecolors='w')
        axs[i].set_ylabel(year)
    axs[-1].set_xlabel("Weight of vote relative to election's average")

    plt.tight_layout()
    plt.subplots_adjust(hspace=0)
    plt.show()


if __name__ == '__main__':
    data = get_data()
    # plot_weight_vs_votes_by_year(data, '2020')

    years = ['2000', '2004', '2008', '2012', '2016', '2020']
    # years = ['2016', '2020']

    for year in years:
         plot_weight_bars_by_year(data[year], year)

    plot_bubbles(data, years)

from __future__ import print_function, unicode_literals

if __name__ == "__main__":
    # Import Matplotlib
    import matplotlib.pyplot as plt

    plt.rcParams.update({'font.size': 20, 'figure.figsize': (10, 8)})  # set font and plot size to be larger

    # Import pandas as "pd"
    import pandas as pd

    # Import PyInquirer to use as user input library
    from PyInquirer import style_from_dict, Token, prompt, Separator, print_json

    # Import plotly for graphs
    import plotly.graph_objects as go

    round_data = pd.read_csv("data/round_data.csv", index_col="round_name")
    popular_armor_data = pd.read_csv("data/popular_armor_stats.csv", index_col="armor_class")

    health_dataframe = {
        'body_part': ['head', 'thorax', 'stomach', 'left_arm', 'right_arm', 'left_leg', 'right_leg'],
        'body_part_hp': [35, 80, 70, 60, 60, 65, 65],
        'body_part_overshoot_mult': [1000, 1000, 1.5, 0.7, 0.7, 1, 1]
    }
    health_data = pd.DataFrame(health_dataframe)
    health_data.set_index("body_part", inplace=True)
    #print(health_data)

    total_health = 435

    armor_penthrough_perc_dmg_reduction = 28


    def get_round_types(round_input_answer):
        options = round_data.round_type.unique()
        # if answers['size'] == 'jumbo':
        # options.append('helicopter')
        return options


    # Calculate stats from sheet
    round_data['armor_pen_rating'] = round_data['pen_power'] / round_data['pen_power'].max()
    round_data['armor_damage_rating'] = round_data['armor_dmg_perc'] / round_data['armor_dmg_perc'].max()
    round_data['armor_stat_rating_totals'] = round_data['armor_pen_rating'] + round_data['armor_damage_rating']
    round_data['armor_stat_efficiency_rating'] = round_data['armor_stat_rating_totals'] / \
        round_data['armor_stat_rating_totals'].max()
    round_data['health_damage_rating'] = round_data['damage'] / round_data['damage'].max()
    round_data['health_stat_efficiency_rating'] = round_data['health_damage_rating'] / round_data[
        'health_damage_rating'].max()
    round_data['stat_rating_totals'] = round_data['armor_pen_rating'] + round_data['armor_damage_rating'] + \
        round_data['health_damage_rating']
    round_data['stat_efficiency_rating'] = round_data['stat_rating_totals'] / round_data['stat_rating_totals'].max()
    round_data['total_health_damage'] = round_data['projectiles'] * round_data['damage']
    round_data['total_armor_damage'] = round_data['projectiles'] * round_data['armor_dmg_perc']
    round_data['armor_stat_price_efficiency'] = round_data['armor_stat_rating_totals'] / round_data['price']
    round_data['health_stat_price_efficiency'] = round_data['health_damage_rating'] / round_data['price']
    round_data['total_stat_price_efficiency'] = (round_data['armor_stat_rating_totals'] +
                                                 round_data['health_damage_rating']) / round_data['price']
    round_data['armor_stat_price_efficiency_ratio'] = (round_data['armor_stat_price_efficiency'] / round_data[
        'armor_stat_price_efficiency'].max()) * 100
    round_data['health_stat_price_efficiency_ratio'] = (round_data['health_stat_price_efficiency'] / round_data[
        'health_stat_price_efficiency'].max()) * 100
    round_data['total_stat_price_efficiency_ratio'] = (round_data['total_stat_price_efficiency'] / round_data[
        'total_stat_price_efficiency'].max()) * 100

    # Show plot of data
    round_data.plot(kind='scatter', x='health_stat_price_efficiency', y='armor_stat_price_efficiency',
                    title='Health Stat Price Efficiency vs Armor Stat Price Efficiency')
    # plt.show()

    # Calculate kill stats

    # print(round_data.head())

    # print(round_data.round_type.unique())

    round_input_question = [
        {
            'type': 'list',
            'name': 'round_input',
            'message': 'Which round would you like to visualize?',
            'choices': get_round_types,
        }
    ]

    round_input_answer = prompt(round_input_question)
    selected_round_type = round_input_answer.get("round_input", "")
    selected_rounds = round_data.loc[round_data['round_type'] == selected_round_type]
    #print(selected_rounds[["round_display_name"]])

    selected_rounds_health_stat_price_efficiency = selected_rounds.health_stat_price_efficiency_ratio.tolist()
    selected_rounds_armor_stat_price_efficiency = selected_rounds.armor_stat_price_efficiency_ratio.tolist()
    selected_rounds_total_stat_price_efficiency = selected_rounds.total_stat_price_efficiency_ratio.tolist()
    #print(selected_rounds_total_stat_price_efficiency)
    #print(round_data.total_stat_price_efficiency.describe())

    #fig = go.Figure(data=go.Scatter(
        #x=selected_rounds_health_stat_price_efficiency,
        #y=selected_rounds_armor_stat_price_efficiency,
        #mode='markers',
        #marker=dict(size=selected_rounds_total_stat_price_efficiency)
        #)
    #)

    fig = go.Figure()

    fig.add_trace(go.Scatter(x=selected_rounds_health_stat_price_efficiency,
                             y=selected_rounds_armor_stat_price_efficiency,
                             mode='markers',
                             marker=dict(size=selected_rounds_total_stat_price_efficiency),
                             name='selected_rounds'))
    fig.add_trace(go.Scatter(x=list(set(round_data['health_stat_price_efficiency_ratio'])),
                             y=list(set(round_data['armor_stat_price_efficiency_ratio'])),
                             mode='markers',
                             #marker=dict(size=list(set(round_data['total_stat_price_efficiency_ratio']))),
                             name='round_data'))

    fig.update_layout(
        xaxis=go.layout.XAxis(
            #tickangle=90,
            title_text="Health Stat Efficiency",
            title_font={"size": 20},
            title_standoff=25),
        yaxis=go.layout.YAxis(
            title_text="Armor Stat Efficiency",
            title_standoff=25)
    )

    fig.update_xaxes(range=[1, 100])
    fig.update_yaxes(range=[1, 100])

    fig.show()

    # input()

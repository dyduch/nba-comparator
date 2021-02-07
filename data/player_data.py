import numpy as np
import matplotlib.pyplot as plt

from data.scrapper import get_stats_for_player, get_name_for_player, get_image_link_for_player


def show_stat_plot(stats_dict, stat_name):
    stat_values = get_stat_values(stat_name, stats_dict)
    plt.plot(stat_values.keys(), stat_values.values(), c='red')

    plt.xlabel("Season")
    plt.ylabel(stat_name)

    plt.title("Stats")

    plt.show()


def get_averages_for_stats(stats_dict):
    result_dict = {}
    possible_stats = list(stats_dict.values())[0]
    for stat_name in possible_stats:
        if stat_name == 'g' or stat_name == 'gs':
            result_dict[stat_name] = get_total_stat_value(stats_dict, stat_name)
        else:
            result_dict[stat_name] = get_average_stat_value(stats_dict, stat_name)
    return result_dict


def get_total_stat_value(stats_dict, stat_name):
    stat_values = get_stat_values(stat_name, stats_dict)
    return int(np.sum([value for key, value in stat_values.items()]))


def get_average_stat_value(stats_dict, stat_name):
    stat_values = get_stat_values(stat_name, stats_dict)
    if 'pct' in stat_name:
        return round(np.mean([value for key, value in stat_values.items()]) * 100, 2)
    return round(np.mean([value for key, value in stat_values.items()]), 2)


def get_stat_values(stat_name, stats_dict):
    stat_values = {}
    for key, value in stats_dict.items():
        if value[stat_name]:
            stat_values[key] = (float(value[stat_name]))
        else:
            stat_values[key] = 0.0
    return stat_values


def get_nba_data(player_name, seasons):
    stats = get_stats_for_player(player_name, seasons)
    result = get_averages_for_stats(stats)
    name = get_name_for_player(player_name)
    img = get_image_link_for_player(player_name)
    result['name'] = name
    result['img'] = img

    result['first_season'] = get_full_season(seasons[0])
    result['last_season'] = get_full_season(seasons[-1])
    return result


# 2008 -> 2007-08
def get_full_season(season):
    int_season = int(season)
    prev_season = str(int_season - 1)
    return "{0}-{1}".format(prev_season, season[2::])

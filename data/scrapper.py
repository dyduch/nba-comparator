import bs4
import requests

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X x.y; rv:42.0) Gecko/20100101 Firefox/42.0'}
base_url = 'https://www.basketball-reference.com'
search_url = 'https://www.basketball-reference.com/search/search.fcgi?search='


def get_image_link_for_player(player_name):
    player_url = get_player_url(player_name)
    return get_image(player_url)


def get_image(player_url):
    soup = get_soup_page(player_url)
    meta_div = soup.find('div', {'id': 'meta'})
    img = meta_div.find('img')
    return img['src']


def get_name_for_player(player_name):
    player_url = get_player_url(player_name)
    return get_name(player_url)


def get_name(player_url):
    soup = get_soup_page(player_url)
    name_header = soup.find('h1', {'itemprop': 'name'})
    return name_header.find('span').text


def get_stats_for_player(player_name, seasons):
    player_url = get_player_url(player_name)
    return get_data_for_seasons(player_url, seasons)


def get_player_url(player_name):
    player_search_url = search_url
    name_parts = player_name.split()
    suffix = '+'.join(name_parts)
    player_search_url += suffix
    soup = get_soup_page(player_search_url)
    players = soup.find('div', {'id': 'players'})

    if not players:
        return player_search_url

    search_items = players.findAll('div', {'class': 'search-item-name'})

    player_links = []
    matching_player_index = 0

    for item in search_items:
        a = item.find('a', href=True)
        if "{0} ".format(player_name) in a.text:
            matching_player_index = search_items.index(item)
        player_links.append(a['href'])

    return "{0}{1}".format(base_url, player_links[matching_player_index])


def get_data_for_seasons(player_url, seasons):
    soup = get_soup_page(player_url)

    per_game_table = soup.find('div', {'id': 'div_per_game'})
    result_dict = {}
    for season in seasons:
        per_game_row = per_game_table.find('tr', {'id': 'per_game.{0}'.format(season), 'class': 'full_table'})
        stat_dict = {}
        if per_game_row:
            for stat in per_game_row.findAll('td', {'class': 'right'}):
                stat_name = stat['data-stat']
                stat_value = stat.text
                stat_dict[stat_name] = stat_value
            result_dict[season] = stat_dict

    return result_dict


def get_soup_page(url):
    result = requests.get(url, headers=headers)
    bkref_page = result.text
    soup = bs4.BeautifulSoup(bkref_page, features='html.parser')
    return soup

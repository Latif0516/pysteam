import json
import pandas as pd
from steamwebapi.api import IPlayerService, ISteamUserStats, ISteamWebAPIUtil
import steamfront

playerserviceinfo = IPlayerService()
steamuserstats = ISteamUserStats()
client = steamfront.Client()

features = [
    'steamid',
    'appid',
    'playtime_forever'
]


def achievementprocentage(ach):
    achieved = [i for i in ach if i['achieved'] == 1]
    return len(achieved) / len(ach)


iddict = dict()

# json_data = [76561198048730871, 76561198180821795, 76561198008911412]
json_file = open('Resources/steamkey10000.json', 'r')
json_data = json.loads(json_file.read())
json_file.close()

print(len(json_data))

df = pd.DataFrame(columns=features)
df.index.names = ['steamID/appID']
id = -1;
for index, steamid in enumerate(json_data):
    response = playerserviceinfo.get_owned_games(steamid)['response']
    if len(response) > 1:
        games = response['games']
        id = id + 1
        iddict[id] = steamid
        for game in games:
            df = df.append(pd.DataFrame([[int(id), int(game['appid']), int(game['playtime_forever'])]],columns=features))
        print('\r{0}%'.format(round((index + 1) / len(json_data) * 100)), end="", flush=True)
df.to_csv('Resources/dataset10000.csv', mode='w+')

            # try:
            #     currentGame = client.getApp(name=game['name'])
            #     currentGenres = (list(currentGame.genres))
            #     currentGenres.extend(list(currentGame.categories))
            #     df.set_value(jointid, 'genres', currentGenres)
            # except:
            #     continue

            # try:
            #    achievements = steamuserstats.get_player_achievements(steamid, game['appid'])['playerstats'][
            #        'achievements']
            #   df.set_value(jointid, 'achievements', achievementprocentage(achievements))
            # except:
            #   df.set_value(jointid, 'achievements', None)
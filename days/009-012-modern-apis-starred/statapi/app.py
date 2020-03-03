import csv

from apistar import App, Route, types, validators
from apistar.http import JSONResponse

DATA = 'Batting.csv'


def convert_csv_to_dict(data=DATA):
    '''Converts lehman data into a dictionary of dictionaries for API use.'''
    with open(data) as csvfile:
        reader = csv.DictReader(csvfile)
        batters = {}
        for row in reader:
            if row['IBB'] == '':
                row['IBB'] = 0
            if row['HBP'] == '':
                row['HBP'] = 0
            if row['SH'] == '':
                row['SH'] = 0
            if row['SF'] == '':
                row['SF'] = 0
            if row['SB'] == '':
                row['SB'] = 0
            if row['CS'] == '':
                row['CS'] = 0
            if row['GIDP'] == '':
                row['GIDP'] = 0
            if row['RBI'] == '':
                row['RBI'] = 0
            if row['SO'] == '':
                row['SO'] = 0
            batter = {'playerID': row['playerID'],
                      'yearID': int(row['yearID']),
                      'stint': int(row['stint']),
                      'teamID': row['teamID'],
                      'G': int(row['G']),
                      'AB': int(row['AB']),
                      'R': int(row['R']),
                      'H': int(row['H']),
                      'DO': int(row['DO']),
                      'TR': int(row['TR']),
                      'HR': int(row['HR']),
                      'RBI': int(row['RBI']),
                      'SB': int(row['SB']),
                      'CS': int(row['CS']),
                      'BB': int(row['BB']),
                      'SO': int(row['SO']),
                      'IBB': int(row['IBB']),
                      'HBP': int(row['HBP']),
                      'SH': int(row['SH']),
                      'SF': int(row['SF']),
                      'GIDP': int(row['GIDP'])}
            batters[str((row['playerID']) +
                    str(row['yearID']) +
                    str(row['stint']))] = batter
        return batters


batters = convert_csv_to_dict()

ALL_TEAMS = set([batter[1]['teamID'] for batter in batters.items()])

SEASON_NOT_FOUND = 'Season not found'


class Season(types.Type):
    playerID = validators.String(max_length=9)
    yearID = validators.Integer(minimum=1871)
    stint = validators.Integer(minimum=1)
    teamID = validators.String(enum=list(ALL_TEAMS))
    G = validators.Integer(minimum=1)
    AB = validators.Integer(minimum=0, default=0)
    R = validators.Integer(minimum=0, default=0)
    H = validators.Integer(minimum=0, default=0)
    DO = validators.Integer(minimum=0, default=0)
    TR = validators.Integer(minimum=0, default=0)
    HR = validators.Integer(minimum=0, default=0)
    RBI = validators.Integer(minimum=0, default=0)
    SB = validators.Integer(minimum=0, default=0)
    CS = validators.Integer(minimum=0, default=0)
    BB = validators.Integer(minimum=0, default=0)
    SO = validators.Integer(minimum=0, default=0)
    IBB = validators.Integer(minimum=0, default=0)
    HBP = validators.Integer(minimum=0, default=0)
    SH = validators.Integer(minimum=0, default=0)
    SF = validators.Integer(minimum=0, default=0)
    GIDP = validators.Integer(minimum=0, default=0)


def list_seasons():
    return [Season(batter[1]) for batter in sorted(batters.items())]


def get_season(season_id: str):
    batter = batters.get(season_id)
    if not batter:
        error = {'error': SEASON_NOT_FOUND}
        return JSONResponse(error, status_code=404)
    return JSONResponse(Season(batter), status_code=200)


def update_season(season_id: str, season: Season):
    batter = batters.get(season_id)
    if not batter:
        error = {'error': SEASON_NOT_FOUND}
        return JSONResponse(error, status_code=404)

    batters[season_id] = season
    return JSONResponse(Season(season), 200)


def delete_season(season_id: str):
    batter = batters.get(season_id)
    if not batter:
        error = {'error': SEASON_NOT_FOUND}
        return JSONResponse(error, status_code=404)

    del batters[season_id]
    return JSONResponse({}, 204)


def create_season(season: Season):
    season_id = season['playerID'] + str(season['yearID']) + str(season['stint'])
    batters[season_id] = season
    return JSONResponse(Season(season), 201)


routes = [
    Route('/', method='GET', handler=list_seasons),
    Route('/', method='POST', handler=create_season),
    Route('/{season_id}/', method='GET', handler=get_season),
    Route('/{season_id}/', method='PUT', handler=update_season),
    Route('/{season_id}/', method='DELETE', handler=delete_season),
]

app = App(routes=routes)


if __name__ == '__main__':
    app.serve('127.0.0.1', 5000, debug=True)

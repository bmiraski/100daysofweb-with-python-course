from apistar import test

from app import app, batters, SEASON_NOT_FOUND, ALL_TEAMS

client = test.TestClient(app)


def test_all_teams():
    assert len(ALL_TEAMS) == 149
    assert "CHN" in ALL_TEAMS
    assert "ABQ" not in ALL_TEAMS


def test_list_seasons():
    response = client.get('/')
    assert response.status_code == 200

    resp_list = response.json()
    num_seasons = len(batters)
    assert len(resp_list) == num_seasons

    first_bat = 'aardsda01'
    assert resp_list[0]['playerID'] == first_bat


def test_get_season():
    response = client.get('/pujolal0120201')
    assert response.status_code == 404
    assert response.json() == {'error': SEASON_NOT_FOUND}

    response = client.get('/pujolal0120071')
    expected = {"playerID": "pujolal01", "yearID": 2007, "stint": 1, "teamID": "SLN",
                "G": 158, "AB": 565, "R": 99, "H": 185, "DO": 38, "TR": 1, "HR": 32,
                "RBI": 103, "SB": 2, "CS": 6, "BB": 99, "SO": 58, "IBB": 22, "HBP": 7,
                "SH": 0, "SF": 8, "GIDP": 27}
    assert response.status_code == 200
    assert response.json() == expected


def test_delete_season():
    response = client.delete('/pujolal0120201/')
    assert response.status_code == 404
    assert response.json() == {'error': SEASON_NOT_FOUND}

    response = client.delete('/pujolal0120071/')
    assert response.status_code == 204
    assert response.json() == {}

    response = client.get('/pujolal0120071/')
    assert response.status_code == 404
    assert response.json() == {'error': SEASON_NOT_FOUND}

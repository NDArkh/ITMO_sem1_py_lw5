import requests
from time import sleep


def get(url: str, max_retries: int = 3) -> requests.Response:
    retries_cnt = 0
    while (_req := requests.get(url)).status_code != 200 \
            and retries_cnt < max_retries:
        sleep(1 + 2 * retries_cnt)
    return _req


if __name__ == '__main__':
    # task: part 1
    req = get('http://open-notify.org')
    if req.status_code == 200:
        print(f'done! result\'s headers:\n{req.headers}')
    else:
        print(f'{req.status_code=}')

    # task: part 2
    with open('apikey_openweathermap', 'r', encoding='utf-8') as f:
        api_key = f.read()
        print('\n\nNow you can write a city name to get weather info.\nUse empty '
              'input to go next...')
        while (city_name := input('city_name=')) != '':
            geo_req = get(
                f'http://api.openweathermap.org/geo/1.0/direct'
                f'?q={city_name}'
                f'&limit=1'
                f'&appid={api_key}'
            )
            if geo_req.status_code == 200:
                if len((res := geo_req.json())) > 0:
                    lat, lon = res[0]['lat'], res[0]['lon']
                    find_name = res[0]['name']
                    weather_req = get(
                        f'https://api.openweathermap.org/data/2.5/weather'
                        f'?lat={lat}'
                        f'&lon={lon}'
                        f'&lang=ru'
                        f'&appid={api_key}'
                        f'&units=metric'
                    ).json()
                    print(f'Now at {find_name}: '
                          f'{weather_req["weather"][0]["main"]} '
                          f'({weather_req["weather"][0]["description"]}), '
                          f'{weather_req["main"]["temp"]} C dg.')
                else:
                    print(f'Can\'t find the "{city_name}", sorry...')
            else:
                print(f'Request error: {geo_req.status_code=}')

    # task: part 3
    req_iss_pos = get('http://api.open-notify.org/iss-now.json') \
        .json()["iss_position"]
    req_space_ppl = get('http://api.open-notify.org/astros.json').json()
    data = dict()
    ppl_cnt = 0
    for person_dict in req_space_ppl['people']:
        name, craft = person_dict['name'], person_dict['craft']
        if craft not in data:
            data[craft] = [name]
        else:
            data[craft].append(name)
        ppl_cnt += 1
    print(f'\n\nThere are {len(data)} spacecrafts with {ppl_cnt} people (at sum) '
          f'in space right now!')
    for cft in data:
        if cft == 'ISS':
            print(f'ISS (located at {req_iss_pos["latitude"]} lat., {req_iss_pos["longitude"]} '
                  f'lon. right now)')
        else:
            print(cft)
        for ppl in data[cft]:
            print('\t' + ppl)

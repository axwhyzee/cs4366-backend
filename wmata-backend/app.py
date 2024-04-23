from flask import Flask, request

from api import (
    get_bus_positions,
    get_routes,
    get_stop_predictions,
    get_stop_schedule,
    get_waypoints
)
from utils import logger, name_to_dir, stem_route


WAYPOINTS = {}

app = Flask(__name__)

@app.route('/')
def root():
    return '/'

@app.route('/path', methods=['GET'])
def query_path():
    """Fetch path for a given route
    Example: /path?route_id=S2&route_dir=SOUTH
    Response: {"coords":[[-77.030187,38.993366],[-77.03009,38.993429], ...],"stops":[...]}
    """
    route_id = request.args.get('route_id')
    route_dir = request.args.get('route_dir')

    if route_id not in WAYPOINTS or route_dir not in WAYPOINTS[route_id]:
        WAYPOINTS[route_id] = WAYPOINTS.get(route_id, {})
        WAYPOINTS[route_id][route_dir] = get_waypoints(route_id)
    return WAYPOINTS[route_id][route_dir]

@app.route('/positions', methods=['GET'])
def query_positions():
    """Fetch bus positions for an array of given routes
    Example:  /positions?route_ids=S2*1&route_ids=S2*2&route_ids=S2*3&route_ids=S2*5&route_dirs=SOUTH&route_dirs=SOUTH&route_dirs=SOUTH&route_dirs=SOUTH&stop_lon=-77.036528&stop_lat=38.943053
    Response: {"S2":[[-77.03491592407227,38.90253067016602],[-77.03646850585938,38.92841637351296],[-77.03646704491149,38.93128082600046],[-77.02902725995597,38.98177835496806]]}
    """
    route_ids = request.args.getlist('route_ids')
    route_dirs = request.args.getlist('route_dirs')
    stop_lon = request.args.get('stop_lon')
    stop_lat = request.args.get('stop_lat')
    res = {}

    for raw_route_id, route_dir in zip(route_ids, route_dirs):
        route_id = stem_route(raw_route_id)
        if res.get(route_id):
            continue

        pos = get_bus_positions(route_id, route_dir, stop_lon, stop_lat)
        res[route_id] = []
        res_pos = res[route_id]

        for bus in pos.get('BusPositions', []):
            if bus.get('DirectionText') == route_dir:
                res_pos.append({"longitude": bus.get('Lon'), "latitude": bus.get('Lat')})
    return res

@app.route('/stop', methods=['GET'])
def query_stop():
    """Fetch bus info for a given stop ID + routes served by the stop
    Example: /stop?stop_id=1002864
    Response: {"stop_id":"1002864","stop_lat":38.943053,"stop_lon":-77.036528,"stop_name":"16TH ST NW + VARNUM ST NW","stop_routes":{"D33":{"dir":"","times":[],"variations":["D33"]},"S2":{"dir":"SOUTH","times":[10,35],"variations":["S2*1","S2*2","S2*3","S2*5"]},"W45":{"dir":"","times":[],"variations":["W45"]}}}
    """
    stop_id = request.args.get('stop_id')
    res = {}
    stop_schedules = get_stop_schedule(stop_id)

    if 'Stop' not in stop_schedules:
        print('Invalid stop ID')
        return res

    stop_info = stop_schedules['Stop']
    stop_id = stop_info.get('StopID')
    stop_name = stop_info.get('Name')
    stop_lon = stop_info.get('Lon')
    stop_lat = stop_info.get('Lat')
    stop_routes = stop_info.get('Routes')

    res['stop_id'] = stop_id
    res['stop_name'] = stop_name
    res['stop_lon'] = stop_lon
    res['stop_lat'] = stop_lat
    res['stop_routes'] = {}

    for raw_route_id in stop_routes:
        route_id = stem_route(raw_route_id)
        if route_id in res['stop_routes']:
            res['stop_routes'][route_id]['variations'].append(raw_route_id)
        else:
            res['stop_routes'][route_id] = {
                'dir': '', 'variations': [raw_route_id], 'times': []}

    timings = get_stop_predictions(stop_id)
    visited = set()

    for pred in timings.get('Predictions', []):
        route_id = pred.get('RouteID')
        route_dir_text_full = pred.get('DirectionText')
        route_dir_text = name_to_dir(route_dir_text_full)
        route_time = pred.get('Minutes')
        print(f'{route_id=} {route_time=} {route_dir_text_full=}')

        route = res['stop_routes'][route_id]
        route['times'].append(route_time)

        if route_id in visited:
            continue

        route['dir'] = route_dir_text
        visited.add(route_id)

    return res

@logger
def init_paths():
    routes = get_routes()

    for route in routes.get('Routes', []):
        raw_route_id = route.get('RouteID')
        wps = get_waypoints(raw_route_id)

        for key, val in wps.items():

            if 'Direction' not in key or not val:
                continue

            route_dir = val['DirectionText']
            route_id = stem_route(raw_route_id)

            if route_id in WAYPOINTS and route_dir in WAYPOINTS[route_id]:
                continue

            WAYPOINTS[route_id] = WAYPOINTS.get(route_dir, {route_dir: {}})
            WAYPOINTS[route_id][route_dir]['coords'] = list(
                map(lambda x: {"longitude": x['Lon'], "latitude": x['Lat']}, val['Shape']))
            WAYPOINTS[route_id][route_dir]['stops'] = list(
                map(lambda x: {"longitude": x['Lon'], "latitude": x['Lat']}, val['Stops']))
    print('init_paths() finished')

if __name__ == '__main__':
    init_paths()
    app.run(port=5002)
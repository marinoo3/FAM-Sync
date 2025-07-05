from flask import Blueprint, current_app, request, abort, jsonify
from functools import wraps




endpoints = Blueprint('api', __name__)





def check_api_key(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        
        api_key = request.headers.get('X-API-Key')
        if api_key and api_key == current_app.secret_key:
            return f(*args, **kwargs)
        
        return jsonify({"message": "Unauthorized"}), 401
        
    return wrapper




@endpoints.route('/sync_clickandboat', methods=['POST'])
@check_api_key
def sync_clickandboat():

    print('Synconizing Click&Boat...')

    # collect token from body
    data = request.get_json(silent=True) or {}
    token = data.get('token')

    # raise 400 if token not provided
    if not token:
        abort(400, 'token missing')

    # load calendar from Notion
    response_json = current_app.calendar.load_calendar()
    print(response_json)

    bookings = current_app.parser.get_bookings(platforms=['clickandboat'], cookies={'authToken': token})

    new_bookings = {
        'count': 0,
        'names': []
    }

    for event in bookings:
        if not current_app.calendar.match_event(event):
            response = current_app.calendar.add_event(event)
            print(response)
            new_bookings['count'] += 1
            new_bookings['names'].append(event.client)

    return jsonify({'status': 'success', 'content': new_bookings})


@endpoints.route('/check_auth', methods=['GET'])
@check_api_key
def check_auth():
    print('ACCESS ALLOWED')
    return jsonify({'status': 'success'})
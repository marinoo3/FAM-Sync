from flask import Blueprint, jsonify, current_app, request, abort




endpoints = Blueprint('api', __name__)




@endpoints.route('/sync_clickandboat/', methods=['POST'])
def sync_clickandboat():

    # collect token from body
    data = request.get_json(silent=True) or {}
    token = data.get('token')

    # raise 400 if token not provided
    if not token:
        abort(400, 'token missing')

    current_app.calendar.load_calendar()
    bookings = current_app.parser.get_bookings(platforms=['clickandboat'], cookies={'authToken': token})

    for event in bookings:
        if not current_app.calendar.match_event(event):
            current_app.calendar.add_event(event)

    return jsonify({'status': 'success'})


@endpoints.route('/test_endpoint/<token>', methods=['GET'])
def test_endpoint(token):

    # raise 400 if token not provided
    if not token:
        abort(400, 'token missing')

    current_app.calendar.load_calendar()
    bookings = current_app.parser.get_bookings(platforms=['clickandboat'], cookies={'authToken': token})

    for event in bookings:
        if not current_app.calendar.match_event(event):
            current_app.calendar.add_event(event)

    return jsonify({'status': 'success'})
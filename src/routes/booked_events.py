from flask.views import MethodView
from flask_smorest import Blueprint
from controllers.book_events_controller.book_event_controller import BookEventsController
from controllers.book_events_controller.view_booked_event_controller import ViewBookEventsController
from flask_jwt_extended import get_jwt, jwt_required
from flask import request, jsonify

blp = Blueprint("BookedEvents", "bookedevents", description="BookedEvents operations")


@blp.route('/bookevents/<event_id>')
class BookEventsView(MethodView):
    
    @jwt_required()
    @blp.doc(parameters=[{'name': 'Authorization', 'in': 'header', \
        'description': 'Authorization: Bearer <access_token>', 'required': 'true'}])
   
    def post(self, event_id):
        payload = get_jwt()
        user_id = payload['id']
      
        event_data = request.get_json()
        if 'ticket_qty' in event_data:
            events = BookEventsController()
            response = events.book_event(event_id, user_id, event_data['ticket_qty'])
            return response
        else:
            failure_result = {
                    'status': 400,
                    'error': 'BadRequest',
                    'message': 'Invalid request data, Please try again!'}
            
            return jsonify(failure_result),failure_result["status"]
            
            
        
    
@blp.route('/bookevents')
class ListBookedEventsView(MethodView):
    
    @jwt_required()
    @blp.doc(parameters=[{'name': 'Authorization', 'in': 'header', \
        'description': 'Authorization: Bearer <access_token>', 'required': 'true'}])
    def get(self):
        payload = get_jwt()
        user_id = payload['id']
        event = ViewBookEventsController()
        response = event.view_booked_event(user_id)
        return response

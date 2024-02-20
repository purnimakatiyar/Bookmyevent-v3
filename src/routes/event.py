from flask.views import MethodView
from flask_smorest import Blueprint
from flask import jsonify
from controllers.event_controller.remove_event_controller import RemoveEventController
from controllers.event_controller.view_event_controller import ViewEventController
from controllers.event_controller.add_event_controller import AddEventController
from controllers.event_controller.remove_event_controller import RemoveEventController
from controllers.event_controller.update_event_controller import UpdateEventController
from utils.rbac import role_access
from flask_jwt_extended import get_jwt, jwt_required
from schema import EventSchema, UpdateEventSchema
from flask import request

blp = Blueprint("Event", "event", description="Event operations")


@blp.route('/event')
class EventView(MethodView):
    
    @jwt_required()
    @role_access(['Manager'])
    @blp.doc(parameters=[{'name': 'Authorization', 'in': 'header', \
        'description': 'Authorization: Bearer <access_token>', 'required': 'true'}])
    @blp.arguments(EventSchema)
    def post(self, event_data):
        payload = get_jwt()
        
        event = AddEventController()
        response = event.add_event(payload["id"], event_data)
        return response
        
    
@blp.route('/events/<event_id>')
class ShowEventView(MethodView):
    
    def get(self, event_id):
        event = ViewEventController()
        result = event.view_event(event_id)
        return result
    
    
    @jwt_required()
    @role_access(['Manager'])
    @blp.doc(parameters=[{'name': 'Authorization', 'in': 'header', \
                    'description': 'Authorization: Bearer <access_token>', 'required': 'true'}])
    @blp.arguments(UpdateEventSchema)
    def put(self, event_data, event_id):
        payload = get_jwt() 
        event = UpdateEventController()
        response = event.update_event_details(payload["id"], event_id, event_data)
        return response
    
    
    @jwt_required()
    @role_access(['Manager'])
    @blp.doc(parameters=[{'name': 'Authorization', 'in': 'header', \
                    'description': 'Authorization: Bearer <access_token>', 'required': 'true'}])
    def delete(self, event_id):
        payload = get_jwt()
        event = RemoveEventController()
        result = event.remove_event(payload["id"], event_id)
        return result

        
@blp.route('/events')
class EventsView(MethodView):
    
    def get(self):
        price = request.args.get("price")
        category = request.args.get('category')
        location = request.args.get('location')
        eventname = request.args.get('eventname')
        event_data = {
            "price": price,
            "category": category,
            "location": location,
            "eventname": eventname
        }
        
        
        if price is None and category is None and location is None and eventname is None:
            event = ViewEventController()
            return event.list_all_events()

        if eventname is not None:
            event = ViewEventController()
            return event.search_event(eventname)
            
        if price is not None:
            event = ViewEventController()
            return event.filter_event(event_data)
        
        if category is not None:
            event = ViewEventController()
            return event.filter_event(event_data)
        
        if location is not None:
            event = ViewEventController()
            return event.filter_event(event_data)
        
        
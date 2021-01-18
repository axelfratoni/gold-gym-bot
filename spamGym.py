import sys
import requests
import time
from datetime import timedelta, datetime, date

################################# Data #################################

EVENT_NAME = "Workout Reservation"
CLUB_NUMBER = "08898"
HOURS_TO_SINGUP = 72
DESIRED_CLASSES = [
    {
        "dayOfWeek" : "MON",
        "eventStartTime" : "06:30 pm"
    }
]

################################# Helper Functions #################################

def create_time_interval(hours_interval):
    from_time = datetime.now()
    from_time_string = "{}%2F{}%2F{}".format(from_time.month, from_time.day, from_time.year)
    to_time = from_time + + timedelta(hours=hours_interval)
    to_time_string = "{}%2F{}%2F{}".format(to_time.month, to_time.day, to_time.year)
    return from_time_string, to_time_string

def calculate_sleep_interval():
    shortest_sleep_interval = timedelta(hours=24)
    nearest_time = datetime.now() + shortest_sleep_interval
    for desired_class in DESIRED_CLASSES:
        now = datetime.now()
        desired_time = datetime.combine(date.today(), datetime.strptime(desired_class["eventStartTime"], "%I:%M %p").time())
        remaining_time = timedelta(hours=0)
        if(desired_time > datetime.now()):
            remaining_time = desired_time - now
        else:
            remaining_time = desired_time - datetime.combine(date.today(), datetime.strptime("00", "%H").time()) + \
                (datetime.combine(date.today(), datetime.strptime("00", "%H").time()) + timedelta(days=1)) - now        
        if(remaining_time < shortest_sleep_interval and remaining_time > timedelta(hours=0)):
            shortest_sleep_interval = remaining_time
            nearest_time = desired_class["eventStartTime"]
    return shortest_sleep_interval, nearest_time

def find_events(session):
    classes = []
    try:
        classes = get_available_classes(session, CLUB_NUMBER, HOURS_TO_SINGUP)
    except:
        print("Could not retrieve your gym information")
        sys.exit()
    events_found = []
    for event in classes:
        if(not EVENT_NAME in event["eventName"]):           
            continue
        for desired_class in DESIRED_CLASSES:
            if(event["dayOfWeek"] == desired_class["dayOfWeek"]
                and event["eventStartTime"] == desired_class["eventStartTime"]
                and int(event["maxEnrollment"]) > int(event["enrolled"])
                and event["allowEnroll"]):
                events_found.append(event)    
    if(len(events_found) == 0):
        print("No available events found\n")
    else:
        event_count = len(events_found)
        print("Found {} available event{}\n".format(event_count, "s" if(event_count > 1) else ""))
    return events_found

def suscribe_to_events(session, events):
    if(len(events) == 0):
        return
    for event in events:
        try:
            sign_up_to_class(session, CLUB_NUMBER, event["eventItemId"])
            print("Suscribed to event! (date: {} | time: {})".format(event["eventDate"], event["eventStartTime"]))
        except:
            print("Failed to suscribe to event (date: {} | time: {})".format(event["eventDate"], event["eventStartTime"]))
    print()

def show_upcomming_classes(session):
    schedule = []
    try:
        schedule = get_schedule(session, HOURS_TO_SINGUP)        
    except:
        print("Could not retrieve your gym information")
        sys.exit()
    print("Your upcomming classes:")
    for event in schedule:
        print("{}) Date: {} | Time: {}".format(event["id"], event["eventDate"], event["eventStartTime"]))
    print()

################################# API Calls #################################

def new_session(user, password):
    session = requests.session()
    url = "https://www.myiclubonline.com/iclub/performLogin"
    header = { "Content-Type" : "application/x-www-form-urlencoded" }
    payload = "spring-security-redirect=&username=" + user + "&password=" + password
    session.post(url, headers=header, data=payload)
    return session

def get_schedule(session, hours_interval):
    from_time, to_time = create_time_interval(hours_interval)
    url = "https://www.myiclubonline.com/iclub/scheduling/memberSchedule?lowDate=" + from_time + "&highDate=" + to_time + "&_=1606449552639"
    result = session.get(url)
    return result.json()

def get_available_classes(session, club_number, hours_interval):
    from_time, to_time = create_time_interval(hours_interval)
    url = "https://www.myiclubonline.com/iclub/scheduling/classSchedule?club=" + club_number + "&lowDate=" + from_time + "&highDate=" + to_time + "&_=1606449633761"
    result = session.get(url)
    return result.json()

def sign_up_to_class(session, club_number, event_id):
    url = "https://www.myiclubonline.com/iclub/scheduling/addMemberToEvent?club=" + club_number + "&eventItemId=" + event_id + "&_=1606449483813"
    result = session.get(url)
    return result.json()

def sign_out_from_class(session, club_number, event_id):
    url = "https://www.myiclubonline.com/iclub/scheduling/removeMemberFromEvent?club=" + club_number + "&eventItemId=" + event_id + "&_=1606449483813"
    result = session.get(url)
    return result.json()

################################# Main #################################

user, password = sys.argv[1], sys.argv[2]
session = new_session(user, password)

show_upcomming_classes(session)

while(True):
    available_events = find_events(session)
    previous_schedule = get_schedule(session, HOURS_TO_SINGUP)
    if(len(available_events) > 0):
        suscribe_to_events(session, available_events)    
    if(len(get_schedule(session, HOURS_TO_SINGUP)) > len(previous_schedule)):
        print("Job done")
        sys.exit()
    else:
        print("Failed to sign up")
    time.sleep(60)
    session = new_session(user, password)

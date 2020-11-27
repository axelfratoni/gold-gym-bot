import requests
from datetime import timedelta, datetime

def create_time_interval(hours_interval):
    from_time = datetime.now()
    from_time_string = "{}%2F{}%2F{}".format(from_time.month, from_time.day, from_time.year)
    to_time = from_time + + timedelta(hours=hours_interval)
    to_time_string = "{}%2F{}%2F{}".format(to_time.month, to_time.day, to_time.year)
    return from_time_string, to_time_string

def new_session(user, password):
    session = requests.session()
    url = "https://www.myiclubonline.com/iclub/performLogin"
    header = { "Content-Type" : "application/x-www-form-urlencoded" }
    payload = "spring-security-redirect=&username=" + user + "&password=" + password
    result = session.post(url, headers=header, data=payload)
    return session, result.status_code

def get_schedule(session, hours_interval):
    from_time, to_time = create_time_interval(hours_interval)
    url = "https://www.myiclubonline.com/iclub/scheduling/memberSchedule?lowDate=" + from_time + "&highDate=" + to_time + "&_=1606449552639"
    result = session.get(url)
    return result.json(), result.status_code

def get_available_classes(session, club_number, hours_interval):
    from_time, to_time = create_time_interval(hours_interval)
    url = "https://www.myiclubonline.com/iclub/scheduling/classSchedule?club=" + club_number + "&lowDate=" + from_time + "&highDate=" + to_time + "&_=1606449633761"
    result = session.get(url)
    return result.json(), result.status_code

def sign_up_to_class(session, club_number, event_id):
    url = "https://www.myiclubonline.com/iclub/scheduling/addMemberToEvent?club=" + club_number + "&eventItemId=" + event_id + "&_=1606449483813"
    result = session.get(url)
    return result.json(), result.status_code

def sign_out_from_class(session, club_number, event_id):
    url = "https://www.myiclubonline.com/iclub/scheduling/removeMemberFromEvent?club=" + club_number + "&eventItemId=" + event_id + "&_=1606449483813"
    result = session.get(url)
    return result.json(), result.status_code

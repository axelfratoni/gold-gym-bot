# Gold Gym Suscriber Bot

This bot automatically subscribes you to the next desired available class.

## Installation
1. Clone the repository
1. Install *Virtualenv*\
`sudo apt-get install virtualenv`
1. Create an enviroment\
`virtualenv gym-env`
1. Load the enviroment\
`source gym-env/bin/activate`
1. Install Python dependencies\
`pip3 install. -r requirements.txt`

## Set up
On the `gymBot.py` file, edit the **Data** section with the corresponding data:

```
EVENT_NAME = "Workout Reservation"
CLUB_NUMBER = "08898"
HOURS_TO_SINGUP = 72
DESIRED_CLASSES = [
    {
        "dayOfWeek" : "MON",
        "eventStartTime" : "08:00 pm"
    },
    {
        "dayOfWeek" : "WED",
        "eventStartTime" : "08:00 pm"
    },
    {
        "dayOfWeek" : "FRI",
        "eventStartTime" : "08:00 pm"
    }
]
```

## Execution
1.  Load the enviroment\
`virtualenv gym-env`
1. Run the script entering your gym credentials\
`python3 gymBot.py <user> <password>`

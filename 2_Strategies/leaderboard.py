import sys
import json 

try:
    with open('algo_event.config', 'r') as f:
        event_config = json.load(f)
        print(event_config['leaderboard'])
except:
  print("No leaderboard for this event")

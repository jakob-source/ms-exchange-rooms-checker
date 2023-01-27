import datetime
from datetime import datetime, timedelta
from pytz import timezone
from exchangelib import Credentials, Account, Configuration, EWSDateTime
from exchangelib.protocol import BaseProtocol, NoVerifyHTTPAdapter
from exchangelib.properties import CalendarEvent
BaseProtocol.HTTP_ADAPTER_CLS = NoVerifyHTTPAdapter
import urllib3
import json
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

credentials = Credentials('<username>', '<password>')
config = Configuration(server='<server_name>', credentials=credentials)
account = Account('<email_address>', credentials=credentials, autodiscover=False, config=config)

list={}
now = datetime.now()

'''
roomlist = account.protocol.get_roomlists()
for list in roomlist:
    print (list)
    rooms = account.protocol.get_rooms(list.email_address)
'''
start = datetime.now(account.default_timezone)
end = start + timedelta(hours=1)

for room in account.protocol.get_rooms('<rooms_group_email_address>'):
    account = Account(room.email_address, credentials=credentials, autodiscover=False, config=config)
    accounts = [(account, 'Organizer', False)]
    for busy_info in account.protocol.get_free_busy_info(
            accounts=accounts, start=start, end=end, merged_free_busy_interval=60, requested_view="DetailedMerged"
    ):
        list[room.name]=[]
        if busy_info.calendar_events:
            for event in busy_info.calendar_events:
                list[room.name].append(('{} from {} to {}'.format(event.busy_type,event.start.strftime('%H:%M'),event.end.strftime('%H:%M'))))
        else:
            list[room.name].append("Not Busy")
json_data = json.dumps(list, indent=2)
print (json_data)

import sched, time
import os
import logging
import requests

from twilio.rest import Client
from dotenv import load_dotenv

load_dotenv()

LOG = logging.getLogger('root')


def building_log():    
    log_format = "[%(asctime)s | %(filename)s:%(lineno)s - %(funcName)20s() ] %(message)s"
    file_for_log = os.path.join(os.path.dirname(__file__), 'chek_connection_server.log')
    logging.basicConfig(filename=file_for_log, format=log_format)
    LOG.setLevel(logging.INFO)

def init_data():
    TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
    TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    LOG.info('Data for connecting to the mail server initiated')
    init_connect_to_server(client)    

def init_connect_to_server(client):
    try:
        response = requests.get('https://python101.online')
        LOG.info('Server response received')
        s = sched.scheduler(time.time, time.sleep)
        check_connection_server(s, response, client) 
        s.run()        
    except Exception as e:
        LOG.error("No response has been received from the server, check your connection or server address: {}".format(e))
        exit(-1)

def check_connection_server(sc, response, client): 
    if response.status_code == 200:
        url = response.url
        message = client.messages.create(    
            body = f'Server connection - {url} disconnected',  # текст сообщения
            from_ = '+13613015329',  # номер, который был получен
            to = '+380997730476',  # твой номер, на который придёт sms
        )
        LOG.info('Message sent')
        exit(-1)
    sc.enter(10, 1, check_connection_server, (sc, response, client))

if __name__ == '__main__':
    building_log()
    init_data()
   
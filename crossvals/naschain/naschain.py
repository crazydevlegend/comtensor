import bittensor as bt
from base.synapse_based_crossval import SynapseBasedCrossval
from crossvals.naschain.protocol import *
import requests

class NaschainCrossVal(SynapseBasedCrossval):
    
    def __init__(self, netuid = 31, wallet_name = 'default', wallet_hotkey = 'default', network = "finney", topk = 1, subtensor = None):
        super().__init__(netuid, wallet_name, wallet_hotkey, network, topk, subtensor)
        self.dendrite = bt.dendrite( wallet = self.wallet )
        self.genomaster_ip = 'http://51.161.12.128'
        self.genomaster_port = '5000'
        self.genomaster_valid_endpoint = '/handle_valid_request'

    def forward(self):
        axons = [self.metagraph.axons[i['uid']] for i in self.top_miners]

        url = self.genomaster_ip + ':' + self.genomaster_port + self.genomaster_valid_endpoint
        response = requests.get(url)

        return response.json()

        # responses = self.dendrite.query(
        #     axons = axons,
        #     synapse = synapse,
        #     deserialize = False,
        #     timeout = timeout,
        # )
        # return responses

    def run(self):
        response = self.forward()
        return response
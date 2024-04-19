import bittensor as bt
from base.synapse_based_crossval import SynapseBasedCrossval
from crossvals.hivetrain.protocol import *
from bitarray import bitarray
import random

class HivetrainCrossVal(SynapseBasedCrossval):
    
    def __init__(self, netuid = 25, wallet_name = 'default', wallet_hotkey = 'default', network = "finney", topk = 1):
        super().__init__(netuid, wallet_name, wallet_hotkey, network, topk)
        self.dendrite = bt.dendrite( wallet = self.wallet )
        dataset_length = 968000015
        self.dataset_indices = bitarray(dataset_length)
        self.dataset_indices_train = self.dataset_indices
        self.datapoints_per_group = 500

    def get_dataset_indices(self, items_per_group):
        if self.dataset_indices_train.count(0) < items_per_group:
            print("Ran out of dataset indices. Resetting")
            self.dataset_indices_train.setall(0)
            # self.epoch += 1
            # self.set_dht("epoch", self.epoch)
            return self.get_dataset_indices(items_per_group)
        
        search_start = random.choice(range(len(self.dataset_indices_train) - items_per_group + 1))
        start = self.dataset_indices_train.index(bitarray('0'*items_per_group), search_start)
        group = [i for i in range(start, start + items_per_group)]
        self.dataset_indices_train[group] = True

        return [group]

    def forward(self, private_input, timeout: float):
        axons = [self.metagraph.axons[i['uid']] for i in self.top_miners]
        uid_dataset = self.get_dataset_indices(self.datapoints_per_group)

        synapse = Train( 
            dataset_indices = uid_dataset,
            run_id = private_input.run_id,
            batch_size = private_input.batch_size or 1,
            gradient_accumilation_steps = private_input.local_gradient or 4
        )

        responses = self.dendrite.query(
            axons = axons,
            synapse = synapse,
            deserialize = False,
            timeout = timeout,
        )
        return responses

    def run(self, private_input):
        response = self.forward(private_input, 150)
        return response
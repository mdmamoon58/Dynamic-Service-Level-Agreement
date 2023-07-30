import socket
import time
import random
import matplotlib.pyplot as plt
from web3 import Web3

provider = socket.socket()
print('Socket created')

provider.bind(('localhost', 9999))

provider.listen(3)
print('Waiting for connection')

# Connect to the Ethereum network and load the contract instance
web3 = Web3(Web3.HTTPProvider('http://localhost:7545'))

# Load the contract ABI and address
contract_abi = [
			{
				"anonymous": False,
				"inputs": [
					{
						"indexed": True,
						"internalType": "uint256",
						"name": "requestId",
						"type": "uint256"
					},
					{
						"indexed": False,
						"internalType": "string",
						"name": "consumerName",
						"type": "string"
					},
					{
						"indexed": False,
						"internalType": "uint256",
						"name": "allocatedResources",
						"type": "uint256"
					},
					{
						"indexed": False,
						"internalType": "uint256",
						"name": "usedResources",
						"type": "uint256"
					},
					{
						"indexed": False,
						"internalType": "uint256",
						"name": "unusedResources",
						"type": "uint256"
					}
				],
				"name": "InteractionData",
				"type": "event"
			},
			{
				"inputs": [],
				"name": "interactionCount",
				"outputs": [
					{
						"internalType": "uint256",
						"name": "",
						"type": "uint256"
					}
				],
				"stateMutability": "view",
				"type": "function"
			},
			{
				"inputs": [
					{
						"internalType": "uint256",
						"name": "",
						"type": "uint256"
					}
				],
				"name": "interactions",
				"outputs": [
					{
						"internalType": "uint256",
						"name": "requestId",
						"type": "uint256"
					},
					{
						"internalType": "string",
						"name": "consumerName",
						"type": "string"
					},
					{
						"internalType": "uint256",
						"name": "allocatedResources",
						"type": "uint256"
					},
					{
						"internalType": "uint256",
						"name": "usedResources",
						"type": "uint256"
					},
					{
						"internalType": "uint256",
						"name": "unusedResources",
						"type": "uint256"
					}
				],
				"stateMutability": "view",
				"type": "function"
			},
			{
				"inputs": [
					{
						"internalType": "uint256",
						"name": "_requestId",
						"type": "uint256"
					},
					{
						"internalType": "string",
						"name": "_consumerName",
						"type": "string"
					},
					{
						"internalType": "uint256",
						"name": "_allocatedResources",
						"type": "uint256"
					},
					{
						"internalType": "uint256",
						"name": "_usedResources",
						"type": "uint256"
					},
					{
						"internalType": "uint256",
						"name": "_unusedResources",
						"type": "uint256"
					}
				],
				"name": "storeInteraction",
				"outputs": [],
				"stateMutability": "nonpayable",
				"type": "function"
			}
		]   # Update with the ABI of your contract
contract_address = '0x5B38Da6a701c568545dCfcB03FcB875f56beddC4'  # Address of your deployed contract

# Load the contract instance
contract = web3.eth.contract(address=contract_address, abi=contract_abi)

# Lists to store data for plotting
time_list = []
allocated_resources_list = []
used_resources_list = []
unused_resources_list = []

# Set up the plot
plt.ion()  # Turn on interactive mode
fig, ax = plt.subplots()

# Main loop
while True:
    consumer, addr = provider.accept()
    name = consumer.recv(1024).decode()
    print("Connected with", addr, name)

    consumer.send(bytes('Welcome', 'utf-8'))

    try:
        for _ in range(10):
            # Request resources from the consumer
            consumer.send(bytes('request_resources', 'utf-8'))

            # Receive the number of resources requested from the consumer
            resource_request = consumer.recv(1024).decode()
            if resource_request == 'request_resources':
                continue  # Skip resource allocation if the consumer sent the request string

            try:
                resource_request = int(resource_request)
                print("Resource request:", resource_request)
            except ValueError:
                continue  # Skip resource allocation if the consumer sent an invalid request

            # Randomly decide whether to allocate all requested resources or less
            if random.random() < 0.5:
                allocated_resources = min(resource_request, 10)  # Allocate all or maximum of 10
            else:
                allocated_resources = random.randint(1, resource_request)  # Allocate randomly between 1 and requested resources

            # Send the allocated resources to the consumer
            consumer.send(bytes(str(allocated_resources), 'utf-8'))

            # Generate the number of used resources
            used_resources = random.randint(0, allocated_resources)
            unused_resources = allocated_resources - used_resources

            # Store the interaction on the blockchain
            interaction_data = {
                'requestId': int(time.time()),
                'consumerName': name,
                'allocatedResources': allocated_resources,
                'usedResources': used_resources,
                'unusedResources': unused_resources
            }

            # Append data to the lists
            time_list.append(interaction_data['requestId'])
            allocated_resources_list.append(interaction_data['allocatedResources'])
            used_resources_list.append(interaction_data['usedResources'])
            unused_resources_list.append(interaction_data['unusedResources'])

            # Plot the data
            ax.cla()  # Clear the current plot
            ax.plot(time_list, allocated_resources_list, label='Allocated Resources')
            ax.plot(time_list, used_resources_list, label='Used Resources')
            ax.plot(time_list, unused_resources_list, label='Unused Resources')
            ax.legend()

            plt.xlabel('Time')
            plt.ylabel('Resources')

            # Update the plot
            plt.draw()
            plt.pause(0.001)  # Pause to allow the plot to refresh

            time.sleep(1)  # Add a delay for demonstration purposes

            # Specify the "from" address
            from_address = '0x4b15D586fddE5da0e2e45b8DA3C4e0fA72550990'  # Update this with your desired Ethereum address

            # Send a transaction to the contract to store the interaction
            transaction = contract.functions.storeInteraction(
                interaction_data['requestId'],
                interaction_data['consumerName'],
                interaction_data['allocatedResources'],
                interaction_data['usedResources'],
                interaction_data['unusedResources']
            ).transact({'from': from_address})

    except ConnectionAbortedError:
        print("Connection with the consumer aborted.")
        consumer.close()

    consumer.close()

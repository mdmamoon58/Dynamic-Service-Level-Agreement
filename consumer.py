import socket
import random

consumer = socket.socket()
consumer.connect(('localhost', 9999))

name = input("Enter your name: ")
consumer.send(bytes(name, 'utf-8'))

# Receive the welcome message from the provider
welcome_message = consumer.recv(1024).decode()
print(welcome_message)

for _ in range(10):
    # Generate a random number for resource request
    resource_request = str(random.randint(1, 10))
    print("Requesting", resource_request, "resources")

    # Send the resource request to the provider
    consumer.send(bytes(resource_request, 'utf-8'))

    # Receive the allocated resources from the provider
    allocated_resources = consumer.recv(1024).decode()
    if allocated_resources == 'request_resources':
        continue  # Skip processing if the received message is 'request_resources'

    print("Allocated resources:", allocated_resources)

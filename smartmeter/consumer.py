from google.cloud import pubsub_v1

# Your Google Cloud project ID
project_id = "smartmeter-375900"

# The name of the subscription that you created
subscription_name = "pubsub"

consumer = pubsub_v1.SubscriberClient()
subscription_path = consumer.subscription_path(project_id, subscription_name)

def receive_message(callback):
    consumer.subscribe(subscription_path, callback=callback)

def callback(message):
    print(f'Received message: {message.data}')
    message.ack()

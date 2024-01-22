from google.cloud import pubsub_v1

# Your Google Cloud project ID
project_id = "smartmeter-375900"

# The name of the topic that you created
topic_name = "smartmeter"

producer = pubsub_v1.PublisherClient()
topic_path = producer.topic_path(project_id, topic_name)

def publish_message(data):
    data = data.encode('utf-8')
    producer.publish(topic_path, data=data)
    print(f'Published message: {data}')

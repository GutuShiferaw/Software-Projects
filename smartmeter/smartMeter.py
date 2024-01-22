class SmartMeter:

    def __init__(self, project_id, topic_name, subscription_name):

        self.producer = pubsub_v1.PublisherClient()
        self.topic_path = self.producer.topic_path(project_id, topic_name)
        self.consumer = pubsub_v1.SubscriberClient()
        self.subscription_path = self.consumer.subscription_path(project_id, subscription_name)

    def publish_data(self, data):
        data = data.encode('utf-8')
        self.producer.publish(self.topic_path, data=data)
        print(f'Published message: {data}')

    def receive_data(self, callback):
        self.consumer.subscribe(self.subscription_path, callback=callback)

    def callback(self, message):
        print(f'Received message: {message.data}')
        message.ack()
project_id = "smartmeter-375900"
topic_name = "smartmeter"
subscription_name = "smartmeter-375900"

meter = SmartMeter(project_id, topic_name, subscription_name)
meter.publish_data("Hello World!")
meter.receive_data(meter.callback)

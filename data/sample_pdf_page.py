sample_input_page = """
Stephane MaarekNOT FOR DISTRIBUTION © Stephane Maarek www.datacumulus.com Application: SNS to Amazon S3 through Kinesis Data Firehose
SNS TopicBuying Service
Kinesis DataFirehose
Amazon S3•SNS can send to Kinesis and therefore we can have the following solutions architecture:Any supported KDFDestination
© Stephane MaarekNOT FOR DISTRIBUTION © Stephane Maarek www.datacumulus.com Amazon SNS – FIFO T opic•FIFO = First In First Out (ordering of messages in the topic)ProducerSubscribersSQS FIFOSend messagesReceive messages12341234•Similar features as SQS FIFO:•Ordering by Message Group ID (all messages in the same group are ordered)•Deduplication using a Deduplication ID or Content Based Deduplication•Can have SQS Standard and FIFO queues as subscribers•Limited throughput (same throughput as SQS FIFO)

© Stephane MaarekNOT FOR DISTRIBUTION © Stephane Maarek www.datacumulus.com
"""

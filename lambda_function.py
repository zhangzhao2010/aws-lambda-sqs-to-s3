import boto3
import time
import json

def lambda_handler(event, context):
    # 初始化 AWS 客户端
    sqs = boto3.client('sqs')
    s3 = boto3.client('s3')

    # 设置 SQS 和 S3 的相关信息
    queue_url = 'SQS_URL'
    bucket_name = 'BUCKET_NAME'
    output_file = 'messages-{}.json'.format(time.time())
    
    messages = []
    finished = False

    while not finished:
        # 从 SQS 中获取一批消息
        response = sqs.receive_message(
            QueueUrl=queue_url,
            AttributeNames=['All'],
            MaxNumberOfMessages=10,
            VisibilityTimeout=0,  # 立即使消息可见
            WaitTimeSeconds=20  # 设置等待时间，最长为20秒
        )

        if 'Messages' in response:
            received_messages = response['Messages']

            for message in received_messages:
                messages.append(message)
                # print(json.dumps(message))

                # 删除已读取消息
                sqs.delete_message(
                    QueueUrl=queue_url,
                    ReceiptHandle=message['ReceiptHandle']
                )
        else:
            finished = True

    # 将消息保存为 JSON 文件
    with open('/tmp/{}'.format(output_file), 'w') as file:
        json.dump(messages, file)
    
    s3.upload_file('/tmp/{}'.format(output_file), bucket_name, output_file)

    return {
        'statusCode': 200,
        'body': 'Messages saved to S3',
        'bucket_name': bucket_name,
        'object_name': output_file
    }

if __name__ == '__main__':
    event = ''
    context = ''
    lambda_handler(event, context)

# aws-lambda-sqs-to-s3
receive messages from sqs, save all of messages to a file, upload the file to s3 bucket.

# Lambda 配置
Python 3.10

# TIPS
1. Lambda 执行超时时间设置到最长（15分钟）
2. Lambda 函数执行角色需要附加"AmazonSQSFullAccess"和"AmazonS3FullAccess"两个权限策略
3. 如果队列中消息数过多，建议自行增加消息数判断逻辑（例如读取超过1000条消息后立马退出循序）
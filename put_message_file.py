import boto3
import time
import random

FILE_NAME = "message.txt"


def main(log_group_name: str, aws_profile: str, aws_region: str, file_name: str):
    session = boto3.session.Session(region_name=aws_region, profile_name=aws_profile)
    client = session.client("logs")

    log_stream_name = str(int(time.time() * 1000))
    res = client.create_log_stream(
        logGroupName=log_group_name,
        logStreamName=log_stream_name,
    )

    timestamp = int(time.time() * 1000)
    with open(file_name) as f:
        message = f.read()
    log_events = []
    log_events.append(
        {
            "timestamp": timestamp,
            "message": message
        }
    )

    batch_size = 10000
    count = 0
    sequence_token = None
    while count < len(log_events):
        print(count)
        if sequence_token is None:
            res = client.put_log_events(
                logGroupName=log_group_name,
                logStreamName=log_stream_name,
                logEvents=log_events[count:count + batch_size],
            )
        else:
            res = client.put_log_events(
                logGroupName=log_group_name,
                logStreamName=log_stream_name,
                logEvents=log_events[count:count + batch_size],
                sequenceToken=sequence_token,
            )
        if "nextSequenceToken" in res:
            sequence_token = res["nextSequenceToken"]
        count += batch_size


if __name__ == "__main__":
    import sys

    args = sys.argv
    log_group_name = args[1]
    aws_profile = args[2]
    aws_region = args[3]
    main(log_group_name,
         aws_profile,
         aws_region,
         FILE_NAME,
         )


import boto3
import time
import random


LOG_MSG_TMP = """
abcdABCD123456$#!@あいうえおアイウエオ春夏秋冬 \　id[{}]
testtesttestaaaa

いろはにほへと
"""


def main(log_group_name: str, log_size: int, aws_profile: str, aws_region: str):
    session = boto3.session.Session(region_name=aws_region, profile_name=aws_profile)
    client = session.client("logs")

    log_stream_name = str(int(time.time() * 1000))
    res = client.create_log_stream(
        logGroupName=log_group_name,
        logStreamName=log_stream_name,
    )

    log_events = []
    for i in range(log_size):
        timestamp = int(time.time() * 1000)
        message = LOG_MSG_TMP.format(random.randint(0, 1000))
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
    log_size = int(args[2])
    aws_profile = args[3]
    aws_region = args[4]
    main(log_group_name,
         log_size,
         aws_profile,
         aws_region)

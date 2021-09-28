# CloudWatch Logs put dummy events
## Requirements
- Python 3.x (=>3.8)

## Run
### Prepare

```bash
pip install -r requirements.txt
```

### Run script (for random events)

```bash
python put_message.py <log_group_name> <log_size> <aws_profile> <aws_profile>
```


### Run script (for a single message in message.txt)
1. Create `message.txt` and Write a log text in.
2. Run a script

```bash
python put_message_file.py <log_group_name> <aws_profile> <aws_profile>
```

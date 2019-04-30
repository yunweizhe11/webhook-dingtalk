# AlertManager-webhook-dingtalk
Generating [DingTalk] notification from [Prometheus] [AlertManager] WebHooks

### Running

```bash
python webhook-dingtalk.py <flags>
```

## Usage

```
usage: webhook-dingtalk.py --ding.profile=DING.PROFILE [<flags>]

Flags:
  -h, --help              Show context-sensitive help (also try --help-long and --help-man).
      --web.listen-address=":8060"
                          The address to listen on for web interface.
      --ding.profile=DING.PROFILE ...
                          Custom DingTalk profile (can be given multiple times, <profile>=<dingtalk-url>).
      --filter_lables=label
```

## RUN Example


```
python webhook-dingtalk.py --ding_profile="webhook1=https://oapi.dingtalk.com/robot/send?access_token=xxxxxxxxxxx"  --listen_address=8060 --filter_lables=job --filter_lables=instance
python webhook-dingtalk.py --ding_profile="webhook1=https://oapi.dingtalk.com/robot/send?access_token=xxxxxxxxxxx,webhook2=https://oapi.dingtalk.com/robot/send?access_token=xxxxxxxxxxx"  --listen_address=8060 --filter_lables=job --filter_lables=instance
```

## Prometheus Example

```
- alert: alert_name
    expr: promQL
    for: 10m
    labels:
      severity: warning
    annotations:
      summary: alert_title
      description: alert_details
```
## ALertManager Example

```
receivers:
- name: 'dingtalk'
  webhook_configs:
  - send_resolved: false
    url: 'http://localhost:8060/dingtalk/webhook1/send'
```

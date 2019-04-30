# AlertManager-webhook-dingtalk
Generating [DingTalk] notification from [Prometheus] [AlertManager] WebHooks

### Running

```bash
python dingding-hook.py <flags>
```

## Usage

```
usage: dingding-hook.py --ding.profile=DING.PROFILE [<flags>]

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
python dingding-hook.py --ding_profile="webhook1=https://oapi.dingtalk.com/robot/send?access_token=xxxxxxxxxxx"  --listen_address=8060 --filter_lables=job --filter_lables=instance
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

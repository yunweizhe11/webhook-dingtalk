# coding: utf-8
import os
import sys
import json
import requests
import argparse
import pytz,datetime
from flask import Flask
from flask import request
reload(sys) 
sys.setdefaultencoding('utf8')
app = Flask(__name__)

@app.route('/dingtalk/<webhook>/send', methods=['POST', 'GET'])
def send(webhook):
    if request.method == 'POST':
        post_data = request.get_data()
        data,title = bytes2json(post_data)
        send_alert(data=data,title=title,webhook=webhook)
        return 'success'
    else:
        return 'weclome to use prometheus alertmanager dingtalk webhook server!'


def format_to_template(data):
    count = 0 
    code = 0
    if len(data['alerts']) == 1:
        result,title = assembly(data=data)
    else:
        result = ''
        for i in data['alerts']:
           res,title = assembly(data=data,count=count)
           result += '\n\n' + res
           count += 1
    return result,title
def assembly(data,count=0):
    code = 0
    if data['alerts'][count].get('status',None) == 'firing':
        status = u"告警"
    elif data['alerts'][count].get('status',None) == 'Resolved':
        status = u"恢复"
        code = 1
    else:
        status = u"空" 
    result = " **告警名称**: {alertname} \
             \n**当前状态**: {status}\
             \n**当前级别**: {severity}\
             \n**告警主题**: {summary}\
             \n**告警详情**: {description}".format(description=data['alerts'][count]['annotations'].get('description',None),summary=data['alerts'][count]['annotations'].get('summary',None),severity=data['alerts'][count]['labels'].get('severity',None),alertname=data['alerts'][count]['labels'].get('alertname',None),status=status) 
    for keys,value in data['alerts'][count]['labels'].items():
        if keys not in default_lables:
            result += "\n**{keys}**: {values}\n".format(keys=keys,values=value)
    result += "\n**触发时间**: {StartsAt}\n".format(StartsAt=utc_fromat_GMT(data=data['alerts'][count].get('startsAt',None)))
    if code == 1:
        result += "\n**结束时间**: {endsAt}\n".format(endsAt=utc_fromat_GMT(data=data['alerts'][count].get('endsAt',None)))
    title = "{status}.{alertname}".format(alertname=data['alerts'][count]['labels'].get('alertname',None),status=status) 
    return result,title 
def utc_fromat_GMT(data):
    if data is None:
        return None
    dates = data.split('.')[0]
    dates += 'Z'
    local_tz = pytz.timezone('Asia/Chongqing')
    local_format = "%Y-%m-%d %H:%M:%S"
    utc_format='%Y-%m-%dT%H:%M:%SZ'
    utc_dt = datetime.datetime.strptime(dates, utc_format) 
    local_dt = utc_dt.replace(tzinfo=pytz.utc).astimezone(local_tz)
    time_str = local_dt.strftime(local_format)
    return time_str
def bytes2json(data_bytes):
    data = data_bytes.decode('utf8').replace("'", '"')
    return format_to_template(json.loads(data))


def send_alert(data,webhook,title):
    dingdingurl = global_webhook.get(webhook,None) 
    if dingdingurl is None:
        return "webhook is Nond"
    send_data = {
        "msgtype": "markdown",
        "markdown": {"title":title,"text":data}
    }
    req = requests.post(dingdingurl,json=send_data)
    result = req.json()
    if result['errcode'] != 0:
        print('notify dingtalk error: %s' % result['errcode'])


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--ding_profile', type=str,help="ding.profile", default = None)
    parser.add_argument('--listen_address', type=int,help="HTTP PORT 8060", default = 8060)
    parser.add_argument('--filter_lables', action='append',default = None)
    args = parser.parse_args()
    if args.ding_profile is None:
        print "ding.profile is None"
        sys.exit(1)
    result = args.ding_profile
    port = args.listen_address
    filter_labels = args.filter_lables
    global_webhook = {}
    default_lables = ['alertname','severity']
    for i in result.split(','):
        global_webhook[i.split('=',1)[0]] = i.split('=',1)[1]
    if isinstance(filter_labels,list):
        default_lables = list(set(filter_labels) | set(default_lables))
    app.run(host='0.0.0.0', port=port)

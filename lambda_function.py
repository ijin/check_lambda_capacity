import os
import datetime
import boto3

region = os.getenv('AWS_REGION','ap-northeast-1')
client = boto3.client('lambda', region_name=region)
cloudwatch = boto3.client('cloudwatch', region_name=region)

def calculate_capacity(next_marker=None):
    if next_marker:
        r = client.list_functions(MaxItems=500, Marker=next_marker)
    else:
        r = client.list_functions(MaxItems=500)

    size = sum(calculate_versions_capacity(f['FunctionName']) for f in r['Functions'])

    if 'NextMarker' in r:
        return size + lambda_size_r(next_marker=r['NextMarker'])
    else:
        return size

def calculate_versions_capacity(function_name, next_marker=None):
    if next_marker:
        r = client.list_versions_by_function(
            FunctionName=function_name, MaxItems=500, Marker=next_marker)
    else:
        r = client.list_versions_by_function(
            FunctionName=function_name, MaxItems=500)

    size = sum((f['CodeSize']) for f in r['Versions'])

    if 'NextMarker' in r:
        return size + calculate_versions_capacity(function_name=function_name, next_marker=r['NextMarker'])
    else:
        return size


def put_cw(namespace, metric_name, value, unit):
    metric_data = {
        'MetricName': metric_name,
        'Timestamp': datetime.datetime.utcnow(),
        'Value': value,
        'Unit': unit
    }
    r = cloudwatch.put_metric_data(
        Namespace = namespace,
        MetricData = [metric_data]
    )
    return r

def lambda_handler(event, context):
    size = calculate_capacity()
    print(size)
    r = put_cw('lambda', 'size', size, 'Bytes')
    print(r)
    return size

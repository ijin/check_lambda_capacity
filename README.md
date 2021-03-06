# check_lambda_capacity

[![Build status](https://circleci.com/gh/ijin/check_lambda_capacity.svg?style=shield&circle-token=:circle-token)](https://circleci.com/gh/ijin/check_lambda_capacity)

AWS Lambda function which checks the total capacity of all Lambda functions in a specific region and publishes the metric to CloudWatch. A CloudFormation template is included to bootstrap the process.

<a href="https://console.aws.amazon.com/cloudformation/home?region=ap-northeast-1#/stacks/new?stackName=check-lambda-capacity&templateURL=https://s3-ap-northeast-1.amazonaws.com/ijin/aws/lambda/check_lambda_capacity/check_lambda_capacity.template">
<img src="https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png"></a>

## Why

[AWS Lambda Deployment Limits](http://docs.aws.amazon.com/lambda/latest/dg/limits.html#limits-list).
The total size of all the deployment packages that can be uploaded per region is **75GB**. If you are including libraries and utilizing versioning for you lambda functions, you might eventually reach this limit. Monitor the total usage size is a good idea. 

## How

This lambda function uses the `ListFunctions` and `ListVersionsByFunction` API iterating and summing up their `CodeSize`, and posts the value (in Bytes) to CloudWatch.

A CloudFormation template is provided to help with the creation of necessary resources, in addition to configuring an alarm.

## Notes

This lambda function should be run using [`Scheduled events`](http://docs.aws.amazon.com/lambda/latest/dg/with-scheduled-events.html), but CloudFormation support is currently unavailable so we need to explicitly configure this.

# License

MIT License (see [LICENSE](https://github.com/ijin/check_lambda_capacity/blob/master/LICENSE))

# check_lambda_capacity

[![Build status](https://circleci.com/gh/ijin/check_lambda_capacity.svg?style=shield&circle-token=:circle-token)](https://circleci.com/gh/ijin/check_lambda_capacity)

Lambda function (and CloudFormation template) which checks the total capacity of all Lambda functions in a region.

<a href="https://console.aws.amazon.com/cloudformation/home?region=ap-northeast-1#/stacks/new?stackName=check-lambda-capacity&templateURL=https://s3-ap-northeast-1.amazonaws.com/ijin/aws/lambda/check_lambda_capacity/check_lambda_capacity.template">
<img src="https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png"></a>

## Why

[AWS Lambda Deployment Limits](http://docs.aws.amazon.com/lambda/latest/dg/limits.html#limits-list) as of `2015/1/14`.
The total size of all the deployment packages that can be uploaded per region is a mere **1.5GB**, which is much too small if you are including libraries and utilizing versioning for you lambda functions. We need to monitor its total usage size. 

## How

This lambda function uses the `ListFunctions` and `ListVersionsByFunction` API iterating and summing up their `CodeSize`, and posts the value (in Bytes) to CloudWatch.

A CloudFormation template is provided to help with the creation of necessary resources, in addition to configuring an alarm.

## Notes

This lambda function should be run using [`Scheduled events`](http://docs.aws.amazon.com/lambda/latest/dg/with-scheduled-events.html), but currently configuration is only possible through the AWS managemnt console.

# License

MIT License (see [LICENSE](https://github.com/ijin/check_lambda_capacity/blob/master/LICENSE))

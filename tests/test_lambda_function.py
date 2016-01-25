from unittest import TestCase
from nose.tools import ok_, eq_
from nose.tools import assert_not_equal as neq_
#from lambda_function import lambda_size_r, put_cw
import os
import json
import boto3
import placebo
import lambda_function

class LambdaFunctionTestCase(TestCase):
    @classmethod
    def setup_class(self):
        self.data_path = os.path.join(os.path.dirname(__file__), 'responses')
        self.session = boto3.Session()
        self.pill = placebo.attach(self.session, data_path=self.data_path)
        self.pill.playback()
        lambda_function.client = self.session.client('lambda', region_name='us-east-1')
        lambda_function.cloudwatch = self.session.client('cloudwatch', region_name='us-east-1')

    def test_calculate_capacity(self):
        neq_(1236380, lambda_function.calculate_capacity())
        eq_(7379387, lambda_function.calculate_capacity())

    def test_calculate_capacity_paginate(self):
        self.pill.prefix = 'paginate'
        neq_(1236380, lambda_function.calculate_capacity(max_items=3))
        eq_(7379387, lambda_function.calculate_capacity(max_items=3))

    def test_calculate_versions_capacity(self):
        self.pill.prefix = 'single'
        f = 'hello_python'
        neq_(0, lambda_function.calculate_versions_capacity(function_name=f))
        eq_(6143382, lambda_function.calculate_versions_capacity(function_name=f))

    def test_calculate_versions_capacity_paginate(self):
        self.pill.prefix = 'single-paginate'
        f = 'hello_python'
        neq_(0, lambda_function.calculate_versions_capacity(function_name=f, max_items=1))
        eq_(6143382, lambda_function.calculate_versions_capacity(function_name=f, max_items=1))

    def test_put_cw(self):
        self.pill.prefix = ''
        service = 'monitoring'
        operation = 'PutMetricData'
        json_file = self.data_path + '/{}.{}_1.json'.format(service, operation)
        with open(json_file) as data_file:
            response = json.load(data_file)
        eq_(response['data'], lambda_function.put_cw('lambda', 'size', 123, 'Bytes'))


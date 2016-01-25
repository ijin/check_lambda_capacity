from unittest import TestCase
from nose.tools import ok_, eq_
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

    def test_lambda_size_r(self):
        self.pill.prefix = 'all'
        ok_(True)
        eq_(1236380, lambda_function.lambda_size_r())

    def test_put_cw(self):
        self.pill.prefix = ''
        service = 'monitoring'
        operation = 'PutMetricData'
        json_file = self.data_path + '/{}.{}_1.json'.format(service, operation)
        #json_file = self.pill.get_new_file_path(service,operation)
        with open(json_file) as data_file:
            response = json.load(data_file)
        eq_(response['data'], lambda_function.put_cw('lambda', 'size', 123, 'Bytes'))
#
#
#    def test_lambda_size_r_bits(self):
#        self.pill.prefix = 'bits'
#        ok_(True)
#        eq_(1236380, lambda_function.lambda_size_r(next_marker=3))
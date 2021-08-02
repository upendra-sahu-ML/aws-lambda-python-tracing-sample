import os
import logging
import jsonpickle
import requests
import elasticapm
import json
from sf_apm_lib import snappyflow as sf

logger = logging.getLogger()
logger.setLevel(logging.INFO)

project_name = os.environ['PROJECT_NAME']
app_name = os.environ['APP_NAME']
profile_key = os.environ['SF_PROFILE_KEY']
trace_config = snappyflow.get_trace_config(profile_key, project_name, app_name)

def test_func():
    sess = requests.Session()
    for url in [ 'https://www.elastic.co', 'https://benchmarks.elastic.co' ]:
        resp = sess.get(url)

def lambda_handler(event, context):
    # Tracing instrumentation
    client = elasticapm.Client(service_name="python-lambda",
        server_url=trace_config['SFTRACE_SERVER_URL'],
        verify_cert=trace_config['SFTRACE_VERIFY_SERVER_CERT'],
        global_labels=trace_config['SFTRACE_GLOBAL_LABELS']
        )
    elasticapm.instrument()
    # Create tracing transaction
    client.begin_transaction(transaction_type="script")
    # Lambda function code
    logger.info('Sample Application for Tracing')
    logger.info('## ENVIRONMENT VARIABLES\r' + str(os.environ))
    test_func()
    body = {
        "message": "AWS Lambda tracing sample app! Your function executed successfully!",
        "input": event,
    }

    response = {"statusCode": 200, "body": json.dumps(body)}
    
    # End of tracing transaction
    client.end_transaction(name=__name__, result="success")
    return response

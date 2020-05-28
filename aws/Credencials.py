import json
import os
import sys
import base64
import datetime
import hashlib
import hmac

access_key = ''
secret_key = ''
securityToken = ''

bucket = "distribui4"
bucketUrl = ""
region = 'us-east-1'
service = 's3'

t = datetime.datetime.utcnow()
amzDate = t.strftime('%Y%m%dT%H%M%SZ')
dateStamp = t.strftime('%Y%m%d')  # Date w/o time, used in credential scope

policy = """{"expiration": "2020-12-30T12:00:00.000Z",
"conditions": [
{"bucket": \"""" + bucket + """\"},
["starts-with", "$key", ""],
{"acl": "public-read"},
{"success_action_redirect": \"""" + bucketUrl + """success.html"},
    {"x-amz-credential": \"""" + access_key + "/" + dateStamp + "/" + region + """/s3/aws4_request"},
    {"x-amz-algorithm": "AWS4-HMAC-SHA256"},
    {"x-amz-date": \"""" + amzDate + """\" },
    {"x-amz-security-token": \"""" + securityToken + """\"  }
  ]
}"""


# Key derivation functions. See:
# http://docs.aws.amazon.com/general/latest/gr/signature-v4-examples.html#signature-v4-examples-python
def sign(key, msg):
    return hmac.new(key, msg.encode('utf-8'), hashlib.sha256).digest()


def getSignatureKey(key, datestamp, regionname, servicename):
    kdate = sign(('AWS4' + key).encode('utf-8'), datestamp)
    kregion = sign(kdate, regionname)
    kservice = sign(kregion, servicename)
    ksigning = sign(kservice, 'aws4_request')
    return ksigning


def getCredentials(event, context):
    # TODO implement
    stringToSign = b""
    stringToSign = base64.b64encode(bytes((policy).encode("utf-8")))
    signing_key = getSignatureKey(secret_key, dateStamp, region, service)
    signature = hmac.new(signing_key, stringToSign, hashlib.sha256).hexdigest()

    # print(dateStamp)
    # print(signature)
    print(policy)
    return {
        'statusCode': 200,
        'headers': {'Access-Control-Allow-Origin': '*'},
        'body': json.dumps({'stringSigned': signature, 'stringToSign': stringToSign.decode('utf-8'),
                            'xAmzCredential': access_key + "/" + dateStamp + "/" + region + "/s3/aws4_request",
                            'dateStamp': dateStamp, 'amzDate': amzDate, 'securityToken': securityToken})
    }



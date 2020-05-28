import json
import os, sys, base64, datetime, hashlib, hmac

access_key = 'ASIAVY64N4P5HWRW344C'
secret_key = 'qx1JAEhamaGp6VsQSJDgo6eDbaRk9VziPjPK4pF/'
securityToken = "FwoGZXIvYXdzEIL//////////wEaDFs91+NgtTFDtEJdTSLMAQDH680piwqXJeQODmlUErL88lQSUP7Lj9i17dlDt8LMfBjyX6zonMFugs3/FpdM3FPRCTKVXbf+Onx4JUOSlyi5uIapShwWWkAu3tjYncQBAqngdNfKTyyNOVPIAZyb3V8aIdhQlcPdz0FwEVgvaGaRPbW1DGOTDaZkv6pGydcn4lNywmxLfRYs87xkv39ltDJIjA7MkFyC0ZwIOQcjN3wZAR/ICwSK2JD8HTCZpTZq4pLnCx/xsLBvOJg7A6llgDrPUUX/KxRn5X1ilyj5lbz2BTItNxpKbAFDtTDKl07jlBrd/ps4gfZkhdOygjL+Zqo2d81Eth7bHL907ubHgESg"

bucket = "distribui4"
bucketUrl = "http://distribui4.s3-website-us-east-1.amazonaws.com/"
region = 'us-east-1'
service = 's3'

t = datetime.datetime.utcnow()
amzDate = t.strftime('%Y%m%dT%H%M%SZ')
dateStamp = t.strftime('%Y%m%d')  # Date w/o time, used in credential scope

policy = """
{
    "expiration": "2020-12-30T12:00:00.000Z",
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
}
"""


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


def lambda_handler(event, context):
    stringtosign = base64.b64encode(bytes(policy.encode("utf-8")))
    signing_key = getSignatureKey(secret_key, dateStamp, region, service)
    signature = hmac.new(signing_key, stringtosign, hashlib.sha256).hexdigest()
    return {'statusCode': 200, 'headers': {'Access-Control-Allow-Origin': '*'},
            'body': json.dumps({'stringSigned': signature, 'stringToSign': stringtosign.decode('utf-8'),
                                'xAmzCredential': access_key + "/" + dateStamp + "/" + region + "/s3/aws4_request",
                                'dateStamp': dateStamp, 'amzDate': amzDate, 'securityToken': securityToken})
            }



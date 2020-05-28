import json
import boto3

def suma(a, b):
   return a + b
   
def resta(a, b):
   return a - b
   
def default():
   return "Opcion Invalida"
   
def switch(case, a, b):
   sw = {
      "+": suma(a, b),
      "-": resta(a, b),
   }
   return sw.get(case, default())



def lambda_handler(event, context):
    # TODO implement

    metodo=event["queryStringParameters"]["method"]
    
    if metodo=="operacion" :
        op1=float(event["queryStringParameters"]["op1"])
        op2=float(event["queryStringParameters"]["op2"])
        op=(event["queryStringParameters"]["op"])
        res=0
    
        res=switch(op, op1, op2)
        return {
            'statusCode': 200,
            'headers': { 'Access-Control-Allow-Origin' : '*' },
            'body':json.dumps({ 'res' :  str(res) })
        }
    elif metodo=="escritura" :
            encoded_string = event["queryStringParameters"]["res"].encode("utf-8")
            bucket_name = "pruebacalculadora"
            file_name = "resultado.txt"
            
            s3 = boto3.resource("s3")
            s3.Bucket(bucket_name).put_object(Key=file_name, Body=encoded_string)
            
            return {
            'statusCode': 200,
            'headers': { 'Access-Control-Allow-Origin' : '*' },
            'body':json.dumps({ 'res' :  'ok' })
            }
        
    #return json.dumps({"statusCode": 200, "headers" : {"Access-Control-Allow-Origin" : "*"},    'body': { "res" : str(res) }})

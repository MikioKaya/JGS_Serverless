import boto3

dynamodb = boto3.resource('dynamodb') 

def lambda_handler(event, context):
    tableName = 'Point'
    primaryKeyName = 'UserId'
    userId = event['UserId']
    
    if userId == "all":
        return dynamodb.Table('Point').scan()['Items']
    else:
        return dynamodb.Table(tableName).get_item(Key={primaryKeyName: userId})['Item']
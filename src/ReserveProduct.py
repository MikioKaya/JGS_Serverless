import boto3

dynamodb = boto3.resource('dynamodb')

def lambda_handler(event, context):
    tableName = 'Stock'
    primaryKeyName = 'ProductId'
    purchaseProductId = int(event['ProductId'])
    purchaseCount = int(event['Count'])
    targetData = dynamodb.Table(tableName).get_item(Key={primaryKeyName: purchaseProductId})['Item']
    stockCount = targetData['Stock']
    reserveCount = targetData['Reserve']
    
    response = dynamodb.Table(tableName).update_item(
        Key={
            primaryKeyName: purchaseProductId
        },
        UpdateExpression="set Reserve=:r, Stock=:s",
        ExpressionAttributeValues={
            ':r': reserveCount - purchaseCount,
            ':s': stockCount - purchaseCount
        },
        ReturnValues="ALL_NEW"
    )
    return response
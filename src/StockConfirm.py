import boto3

dynamodb = boto3.resource('dynamodb')

class OutOfStockException(Exception):
    """購入時に在庫が不足している場合の例外クラス"""
    pass

def lambda_handler(event, context):
    tableName = 'Stock'
    primaryKeyName = 'ProductId'
    purchaseProductId = int(event['ProductId'])
    purchaseCount = int(event['Count'])
    targetData = dynamodb.Table(tableName).get_item(Key={primaryKeyName: purchaseProductId})['Item']
    stockCount = targetData['Stock']
    reserveCount = targetData['Reserve']
    
    #予約確認
    if (stockCount - reserveCount) - purchaseCount < 0:
        msg = '在庫数：' + str(stockCount) + '、予約数：' + str(reserveCount) + '、購入可能数：' + str(stockCount - reserveCount)
        raise OutOfStockException('在庫が不足しています。%s' % msg)
    
    response = dynamodb.Table(tableName).update_item(
        Key={
            primaryKeyName: purchaseProductId
        },
        UpdateExpression="set Reserve=:r",
        ExpressionAttributeValues={
            ':r': reserveCount + purchaseCount
        },
        ReturnValues="ALL_NEW"
    )
    return response
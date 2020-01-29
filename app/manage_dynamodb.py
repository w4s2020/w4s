import boto3

def get_dynamodb_client():
    dynamodb = boto3.client("dynamodb", region_name="eu-west-1", endpoint_url="http://dynamodb:8000")
    """ :type : pyboto3.dynamodb """
    return dynamodb

def get_dynamodb_resource():
    dynamodb = boto3.client("dynamodb", region_name="eu-west-1", endpoint_url="http://dynamodb:8000")
    """ :type : pyboto3.dynamodb """
    return dynamodb

def create_table():
    table_name = "Recipes"
    attribute_definition = [
        {
            'AttributeName': 'recipename',
            'AttributeType': 'S'

        },
        {
            'AttributeName': 'ingredients',
            'AttributeType': 'N'        
        }
    ]

    key_schema = [
        {
            'AttributeName': 'recipename',
            'KeyType': 'HASH'
        },
        {
            'AttributeName': 'ingredients',
            'KeyType': 'RANGE'
        }
    ]
    initial_iops = {
        'ReadCapacityUnits': 10,
        'WriteCapacityUnits': 10
    }

    dynamodb_table_response = get_dynamodb_client().create_table(
        AttributeDefinitions=attribute_definition,
        TableName=table_name,
        KeySchema=key_schema,
        ProvisionedThroughput=initial_iops
    )

    print("Created DynamoDB table:" + str(dynamodb_table_response))

    # if __name__ == '__main__':
# create_table()


import boto3
from botocore.exceptions import ClientError

class DynamoDB:
    def __init__(self, url, region):
        client = boto3.resource(
            'dynamodb',
            endpoint_url=url,
            region_name=region
        )
        self.tables = {
            "players": client.Table("players"),
        }


    def get_item_by_id(self, player_id):
        try:
            response = self.tables["players"].get_item(
                Key={
                    'player_id': player_id  # Replace with your primary key name
                }
            )
        except ClientError as e:
            print(f"Error getting item: {e.response['Error']['Message']}")
            return None
        else:
            return response.get('Item')  # Returns None if the item doesn't exist

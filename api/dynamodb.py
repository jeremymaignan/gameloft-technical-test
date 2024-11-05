import boto3
from botocore.exceptions import ClientError
from flask import current_app


class DynamoDB:
    def __init__(self, url, region):
        self.client = boto3.resource(
            'dynamodb',
            endpoint_url=url,
            region_name=region
        )
        self.tables = {
            "players": self.client.Table("players"),
        }

    def get_item_by_id(self, player_id):
        try:
            response = self.tables["players"].get_item(
                Key={
                    'player_id': player_id  # Replace with your primary key name
                }
            )
        except ClientError as e:
            current_app.logger.error(f"Error getting item: {e.response['Error']['Message']}")
            return None
        return response.get('Item')  # Returns None if the item doesn't exist

    def save_item(self, item):
        try:
            response = self.tables["players"].put_item(
                Item=item
            )
            current_app.logger.info(f"Item added: {item['player_id']}")
            return response
        except ClientError as e:
            current_app.logger.error(f"Error adding item: {e.response['Error']['Message']}")
            return None

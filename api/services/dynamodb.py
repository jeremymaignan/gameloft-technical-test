import boto3
from botocore.exceptions import ClientError
from flask import current_app


class DynamoDB:
    #TODO: Add apm around each ddb requests
    def __init__(self, url, region):
        self.client = boto3.resource(
            'dynamodb',
            endpoint_url=url,
            region_name=region
        )
        self.tables = {
            "players": self.client.Table("players"),
        }

    def get_item_by_id(self, tablename, key):
        try:
            response = self.tables[tablename].get_item(
                Key=key
            )
        except ClientError as e:
            current_app.logger.error("Error getting item: %s", e.response['Error']['Message'])
            return None
        return response

    def save_item(self, tablename, item):
        try:
            response = self.tables[tablename].put_item(Item=item)
            return response
        except ClientError as e:
            current_app.logger.error("Error adding item: %s", e.response['Error']['Message'])
            return None

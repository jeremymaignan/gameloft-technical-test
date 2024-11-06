import boto3
from botocore.exceptions import ClientError
from flask import current_app


class DynamoDB:
    #TODO: Add apm around each ddb requests
    def __init__(self, url, region, table_names):
        self.client = boto3.resource(
            'dynamodb',
            endpoint_url=url,
            region_name=region,
        )
        self.tables = {}
        for table_name in table_names:
            self.tables[table_name] = self.client.Table(table_name)

    def get_item_by_id(self, table_name, key):
        try:
            response = self.tables[table_name].get_item(
                Key=key
            )
        except ClientError as e:
            current_app.logger.error("Error getting item: %s", e.response['Error']['Message'])
            return None
        return response

    def save_item(self, table_name, item):
        try:
            response = self.tables[table_name].put_item(Item=item)
        except ClientError as e:
            current_app.logger.error("Error saving item: %s", e.response['Error']['Message'])
            return None

        if response['ResponseMetadata']['HTTPStatusCode'] != 200:
            current_app.logger.error("Error saving item: %s", response)
            return None
        return response

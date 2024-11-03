#!/bin/bash

#TODO: The table creation should be done as IaC (e.g terraform) and not here.

TABLE_NAME="players"

# Wait for DynamoDB Local to be ready
until aws dynamodb list-tables  --region $AWS_REGION --endpoint-url $DYNAMO_ENDPOINT > /dev/null 2>&1; do
    echo "Waiting for DynamoDB Local to be ready..."
    sleep 1
done

# Check if the table already exists
aws dynamodb describe-table --region $AWS_REGION --endpoint-url $DYNAMO_ENDPOINT --table-name $TABLE_NAME > /dev/null 2>&1
if [ $? -ne 0 ]; then
    # Table does not exist, so create it
    aws dynamodb create-table \
        --region $AWS_REGION \
        --table-name $TABLE_NAME \
        --attribute-definitions \
            AttributeName=player_id,AttributeType=S \
        --key-schema \
            AttributeName=player_id,KeyType=HASH \
        --provisioned-throughput ReadCapacityUnits=5,WriteCapacityUnits=5 \
        --endpoint-url $DYNAMO_ENDPOINT
    echo "DynamoDB table $TABLE_NAME created."
else
    echo "Table $TABLE_NAME already exists."
fi

# Start the Flask application
exec python3 api.py
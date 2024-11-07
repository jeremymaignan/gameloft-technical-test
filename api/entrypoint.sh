#!/bin/bash

#TODO: The table creation should be done as IaC (e.g terraform) and not here.
#TODO: In Prod, FLASK_DEBUG should be set at 0 (set in CI based on the env)

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

    # Insert the first player into the table
    aws dynamodb put-item \
        --region $AWS_REGION \
        --table-name $TABLE_NAME \
        --item '{
            "player_id": {"S": "97983be2-98b7-11e7-90cf-082e5f28d836"},
            "credential": {"S": "apple_credential"},
            "created": {"S": "2021-01-10 13:37:17Z"},
            "modified": {"S": "2021-01-23 13:37:17Z"},
            "last_session": {"S": "2021-01-23 13:37:17Z"},
            "total_spent": {"N": "400"},
            "total_refund": {"N": "0"},
            "total_transactions": {"N": "5"},
            "last_purchase": {"S": "2021-01-22 13:37:17Z"},
            "active_campaigns": {"L": []},
            "devices": {
                "L": [
                    {
                        "M": {
                            "id": {"N": "1"},
                            "model": {"S": "apple iphone 11"},
                            "carrier": {"S": "vodafone"},
                            "firmware": {"S": "123"}
                        }
                    }
                ]
            },
            "level": {"N": "3"},
            "xp": {"N": "1000"},
            "total_playtime": {"N": "144"},
            "country": {"S": "CA"},
            "language": {"S": "fr"},
            "birthdate": {"S": "2000-01-10 13:37:17Z"},
            "gender": {"S": "male"},
            "inventory": {
                "M": {
                    "cash": {"N": "123"},
                    "coins": {"N": "123"},
                    "item_1": {"N": "1"},
                    "item_34": {"N": "3"},
                    "item_55": {"N": "2"}
                }
            },
            "clan": {
                "M": {
                    "id": {"S": "123456"},
                    "name": {"S": "Hello world clan"}
                }
            },
            "_customfield": {"S": "mycustom"}
        }' \
        --endpoint-url $DYNAMO_ENDPOINT

    echo "DynamoDB table $TABLE_NAME created with one user."
else
    echo "Table $TABLE_NAME already exists."
fi


# Start the Flask application
export FLASK_DEBUG=1
exec python3 api.py
# Profile Matcher Service

## Purpose
This project is a simple user profile matcher that retrieves a player profile based on a unique client ID and matches it with active campaign settings. If a player's profile meets the conditions for any current campaign, the campaign name is added to the player's profile as an active campaign.

## Prerequisites

- `Docker`

## Quick Start

### 1. Start the service:
`docker-compose up`

This will start:

**gameloft-dynamodb:** DynamoDB Local instance for data storage.

Accessible at http://127.0.0.1:8000/

**gameloft-api:** Main profile matcher service.

This will:
1. Create the table `players` in database
2. Insert one player
3. Start the API. Accessible at http://127.0.0.1:5000/

**gameloft-dynamodb-admin:** UI tool to view and manage DynamoDB data.

Accessible at http://127.0.0.1:8001/

### 2. Send a request:

To test the profile matcher service, open the following URL in your browser:
http://127.0.0.1:5000/get_client_config/97983be2-98b7-11e7-90cf-082e5f28d836

In the response, you should see that the player's campaigns have been updated based on current campaign conditions.
To confirm that the player item has been updated in the database, navigate to: http://127.0.0.1:8001/tables/players/items/97983be2-98b7-11e7-90cf-082e5f28d836

## Development Workflow
Install dependencies: `make install`.

Run the application: `make run` or `docker-compose up`.

Run tests: `make test`.

Check linting: `make lint`.

List TODOs: `make todo`.

## Troubleshooting
**Port Conflicts:** Verify no other services are using ports 5000, 8000, or 8001 (Note: on macOS, AirPlay may also use port 5000.)
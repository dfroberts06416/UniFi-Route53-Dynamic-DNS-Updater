import json
import os
import boto3
import urllib3

# Initialize clients
route53 = boto3.client('route53')
http = urllib3.PoolManager()

def lambda_handler(event, context):
    """
    Lambda function to update Route53 with external IP from UniFi API
    
    Environment Variables Required:
    - UNIFI_API_KEY: Your UniFi API key
    - HOSTED_ZONE_ID: Route53 hosted zone ID
    - RECORD_NAME: DNS record to update (e.g., home.example.com)
    - TTL: DNS record TTL (default: 300)
    """
    
    # Get configuration from environment variables
    api_key = os.environ['UNIFI_API_KEY']
    hosted_zone_id = os.environ['HOSTED_ZONE_ID']
    record_name = os.environ['RECORD_NAME']
    ttl = int(os.environ.get('TTL', '300'))
    
    try:
        # Fetch external IP from UniFi API
        response = http.request(
            'GET',
            'https://api.ui.com/v1/hosts',
            headers={
                'X-API-KEY': api_key,
                'Accept': 'application/json'
            }
        )
        
        if response.status != 200:
            raise Exception(f"UniFi API returned status {response.status}")
        
        data = json.loads(response.data.decode('utf-8'))
        
        # Extract external IP address
        if not data.get('data') or len(data['data']) == 0:
            raise Exception("No hosts found in UniFi API response")
        
        external_ip = data['data'][0]['ipAddress']
        
        # Update Route53 record
        change_batch = {
            'Changes': [{
                'Action': 'UPSERT',
                'ResourceRecordSet': {
                    'Name': record_name,
                    'Type': 'A',
                    'TTL': ttl,
                    'ResourceRecords': [{'Value': external_ip}]
                }
            }]
        }
        
        route53_response = route53.change_resource_record_sets(
            HostedZoneId=hosted_zone_id,
            ChangeBatch=change_batch
        )
        
        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'DNS record updated successfully',
                'record': record_name,
                'ip': external_ip,
                'changeId': route53_response['ChangeInfo']['Id']
            })
        }
        
    except Exception as e:
        print(f"Error: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({
                'error': str(e)
            })
        }

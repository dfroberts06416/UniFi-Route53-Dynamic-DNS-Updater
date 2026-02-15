import json
import os
import boto3
import urllib3

# Initialize clients
route53 = boto3.client('route53')
http = urllib3.PoolManager()

def lambda_handler(event, context):
    """
    Lambda function to update Route53 with external IPs from UniFi Cloud API
    
    Supports both single and dual WAN configurations:
    - WAN1: Retrieved from gateway device in /v1/devices endpoint
    - WAN2: Retrieved from host information in /v1/hosts endpoint
    
    Environment Variables Required:
    - UNIFI_API_KEY: Your UniFi Cloud API key
    - HOSTED_ZONE_ID: Route53 hosted zone ID
    - RECORD_NAME: DNS record to update for WAN1 (e.g., home.example.com)
    - RECORD_NAME_WAN2: DNS record to update for WAN2 (optional, e.g., home-wan2.example.com)
    - TTL: DNS record TTL (default: 300)
    
    Returns:
    - 200: Success with updated IP addresses
    - 500: Error with details
    """
    
    # Get configuration from environment variables
    api_key = os.environ['UNIFI_API_KEY']
    hosted_zone_id = os.environ['HOSTED_ZONE_ID']
    record_name = os.environ['RECORD_NAME']
    record_name_wan2 = os.environ.get('RECORD_NAME_WAN2')
    ttl = int(os.environ.get('TTL', '300'))
    
    try:
        # Fetch WAN2 IP from UniFi Cloud API - /v1/hosts endpoint
        # This endpoint returns the host-level information including the external IP
        # that UniFi Cloud sees, which typically corresponds to WAN2
        response_hosts = http.request(
            'GET',
            'https://api.ui.com/v1/hosts',
            headers={
                'X-API-KEY': api_key,
                'Accept': 'application/json'
            }
        )
        
        if response_hosts.status != 200:
            raise Exception(f"UniFi API /v1/hosts returned status {response_hosts.status}")
        
        hosts_data = json.loads(response_hosts.data.decode('utf-8'))
        
        # Fetch WAN1 IP from UniFi Cloud API - /v1/devices endpoint
        # This endpoint returns device-level information including gateway devices
        # The gateway device IP typically corresponds to WAN1
        response_devices = http.request(
            'GET',
            'https://api.ui.com/v1/devices',
            headers={
                'X-API-KEY': api_key,
                'Accept': 'application/json'
            }
        )
        
        if response_devices.status != 200:
            raise Exception(f"UniFi API /v1/devices returned status {response_devices.status}")
        
        devices_data = json.loads(response_devices.data.decode('utf-8'))
        
        # Extract WAN1 IP from devices endpoint
        # Look for the gateway device (USG, UDM, etc.) in the devices list
        wan1_ip = None
        if devices_data.get('data'):
            for host in devices_data['data']:
                if 'devices' in host:
                    for device in host['devices']:
                        # Look for gateway devices (USG, UDM, etc.)
                        # These are identified by productLine='network' and model containing 'USG'
                        if device.get('productLine') == 'network' and 'USG' in device.get('model', ''):
                            wan1_ip = device.get('ip')
                            break
                if wan1_ip:
                    break
        
        if not wan1_ip:
            raise Exception("WAN1 IP address not found in UniFi devices API response")
        
        # Extract WAN2 IP from hosts endpoint
        # The top-level ipAddress field contains the external IP seen by UniFi Cloud
        wan2_ip = None
        if hosts_data.get('data') and len(hosts_data['data']) > 0:
            wan2_ip = hosts_data['data'][0].get('ipAddress')
        
        # Build changes for Route53
        changes = [{
            'Action': 'UPSERT',
            'ResourceRecordSet': {
                'Name': record_name,
                'Type': 'A',
                'TTL': ttl,
                'ResourceRecords': [{'Value': wan1_ip}]
            }
        }]
        
        # Add WAN2 record if configured and IP is available
        if record_name_wan2 and wan2_ip:
            changes.append({
                'Action': 'UPSERT',
                'ResourceRecordSet': {
                    'Name': record_name_wan2,
                    'Type': 'A',
                    'TTL': ttl,
                    'ResourceRecords': [{'Value': wan2_ip}]
                }
            })
        
        # Update Route53 records
        change_batch = {'Changes': changes}
        route53_response = route53.change_resource_record_sets(
            HostedZoneId=hosted_zone_id,
            ChangeBatch=change_batch
        )
        
        # Build response
        response_body = {
            'message': 'DNS record(s) updated successfully',
            'wan1': {
                'record': record_name,
                'ip': wan1_ip
            },
            'changeId': route53_response['ChangeInfo']['Id']
        }
        
        if record_name_wan2 and wan2_ip:
            response_body['wan2'] = {
                'record': record_name_wan2,
                'ip': wan2_ip
            }
        elif record_name_wan2 and not wan2_ip:
            response_body['warning'] = 'WAN2 record configured but IP not found in UniFi API'
        
        return {
            'statusCode': 200,
            'body': json.dumps(response_body)
        }
        
    except Exception as e:
        print(f"Error: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({
                'error': str(e)
            })
        }

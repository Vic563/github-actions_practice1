#!/usr/bin/env python3
"""
ServiceNow Integration Script

This script handles integration with ServiceNow for change request management.
It updates change request status based on GitHub Actions workflow results.
"""

import os
import sys
import requests
import json
from datetime import datetime


class ServiceNowIntegration:
    def __init__(self, instance_url, username, password):
        """
        Initialize ServiceNow integration
        
        Args:
            instance_url (str): ServiceNow instance URL
            username (str): ServiceNow username
            password (str): ServiceNow password
        """
        self.instance_url = instance_url
        self.auth = (username, password)
        self.headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
    
    def update_change_request(self, change_number, status, comments=""):
        """
        Update ServiceNow change request status
        
        Args:
            change_number (str): Change request number (e.g., CHG0123456)
            status (str): New status for the change request
            comments (str): Additional comments to add
            
        Returns:
            bool: True if update successful
        """
        try:
            # ServiceNow REST API endpoint for change requests
            url = f"{self.instance_url}/api/now/table/change_request"
            
            # Query parameters to find the change request
            params = {
                'sysparm_query': f'number={change_number}',
                'sysparm_limit': 1
            }
            
            # Get the change request
            response = requests.get(url, auth=self.auth, headers=self.headers, params=params)
            
            if response.status_code != 200:
                print(f"❌ Error retrieving change request: {response.status_code}")
                return False
            
            data = response.json()
            if not data.get('result'):
                print(f"❌ Change request {change_number} not found")
                return False
            
            # Get the sys_id of the change request
            sys_id = data['result'][0]['sys_id']
            
            # Update the change request
            update_data = {
                'state': status,
                'work_notes': f"GitHub Actions Update: {comments}\\n\\nTimestamp: {datetime.now().isoformat()}"
            }
            
            update_url = f"{url}/{sys_id}"
            update_response = requests.put(
                update_url, 
                auth=self.auth, 
                headers=self.headers, 
                data=json.dumps(update_data)
            )
            
            if update_response.status_code == 200:
                print(f"✅ Successfully updated change request {change_number}")
                return True
            else:
                print(f"❌ Error updating change request: {update_response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ Exception updating ServiceNow: {e}")
            return False
    
    def get_change_request_details(self, change_number):
        """
        Get details of a ServiceNow change request
        
        Args:
            change_number (str): Change request number
            
        Returns:
            dict: Change request details or None if not found
        """
        try:
            url = f"{self.instance_url}/api/now/table/change_request"
            params = {
                'sysparm_query': f'number={change_number}',
                'sysparm_limit': 1
            }
            
            response = requests.get(url, auth=self.auth, headers=self.headers, params=params)
            
            if response.status_code == 200:
                data = response.json()
                if data.get('result'):
                    return data['result'][0]
            
            return None
            
        except Exception as e:
            print(f"❌ Exception retrieving change request: {e}")
            return None


def main():
    """
    Main function for ServiceNow integration
    This would be called from GitHub Actions workflow
    """
    
    # Get environment variables (set in GitHub Actions secrets)
    instance_url = os.getenv('SERVICENOW_INSTANCE_URL')
    username = os.getenv('SERVICENOW_USERNAME') 
    password = os.getenv('SERVICENOW_PASSWORD')
    change_number = os.getenv('GITHUB_HEAD_REF', 'CHG0000000')  # Branch name
    workflow_status = os.getenv('WORKFLOW_STATUS', 'unknown')
    
    if not all([instance_url, username, password]):
        print("⚠️  ServiceNow credentials not configured - skipping integration")
        return
    
    # Initialize ServiceNow integration
    snow = ServiceNowIntegration(instance_url, username, password)
    
    # Map GitHub workflow status to ServiceNow status
    status_mapping = {
        'success': 'Review',
        'failure': 'Authorize', 
        'cancelled': 'Cancelled'
    }
    
    snow_status = status_mapping.get(workflow_status, 'Authorize')
    comments = f"GitHub Actions workflow completed with status: {workflow_status}"
    
    # Update the change request
    success = snow.update_change_request(change_number, snow_status, comments)
    
    if not success:
        sys.exit(1)
    
    print("🎉 ServiceNow integration complete!")


if __name__ == "__main__":
    main()

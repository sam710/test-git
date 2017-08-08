# -*- coding: utf8 -*-

import boto3
import time
import sys

# auto scaling group, ami
app_list_asg= [
                'doc-api',          
                 'erp',
                 'inseed',
                 'insolver',
                 'jain',
                 'midasinsight',
                 'mmsw',
                 'mrs',
                 'mrs-app',
                 'mrs-bigfile',
                 'product-site',
                 'web',
                ]

# not autoscaling group,  tag name : deploy 
app_list_not_asg= [
               'apm',          
               'batch',
               'erp-se',
               'intalk',
               'lgs-mongo',
               'mail-sms',
               'mit-api',
               'mrs-se',
               'mrs-chat',
                ]


APP_PREFIX = 'codedeploy-'
GROUP_PRODUCTION = 'production'
DEPLOYGROUP_STAGING = 'staging'
# DEPLOYGROUP_DEVELOPMENT = 'development'
AUTOSCALING_GROUP_NAME_POSTFIX = ''  # !!!!!!!!!!!!!!!!  example : "-20170622 ..  or "-01...

CONFIG_APP_PREFIX = 'codedeploy-config-'
GROUP_CONFIG_AMI = 'config-ami'
GROUP_CONFIG_PRODUCTION = 'config-production'

def main():
    client = boto3.client('codedeploy')

    
# 1. Delete DeployApplication . 
#     delete_all_codedeploy_applications(client)
#     delete_Codedeploy_config_applications(client)
   
#    sys.exit()
   
# 2. Create codedeploy applications
    # CODEDEPLOY_CONFIG_APP
    app_list_all = app_list_asg + app_list_not_asg
    create_codedploy_applications(client , CONFIG_APP_PREFIX, app_list_all )
    # CODEDEPLOY_APP
    create_codedploy_applications(client , APP_PREFIX, app_list_asg )
    create_codedploy_applications(client , APP_PREFIX, ['mit-api'] )

# 3. Create codedeploy config deploy group
 # DEPLOYGROUP_CONFIG_AMI
    create_codedploy_deploy_groups_by_tagname(client , app_list_asg, CONFIG_APP_PREFIX , GROUP_CONFIG_AMI, 'CodeDeployDefault.AllAtOnce')
 # DEPLOYGROUP_CONFIG_PRODUCTION
    # Autoscaling group
    create_codedploy_deploy_groups_by_tagname(client , app_list_asg, CONFIG_APP_PREFIX , GROUP_CONFIG_PRODUCTION, 'CodeDeployDefault.OneAtATime', True)
    # Not Autoscaling group
    create_codedploy_deploy_groups_by_tagname(client , app_list_not_asg, CONFIG_APP_PREFIX , GROUP_CONFIG_PRODUCTION, 'CodeDeployDefault.OneAtATime', False)
    
# 3. Create codedeploy config deploy group
 # DEPLOYGROUP_PRODUCTION
    create_codedploy_deploy_groups_by_autoscale(client , app_list_asg, APP_PREFIX , GROUP_PRODUCTION, 'CodeDeployDefault.OneAtATime',AUTOSCALING_GROUP_NAME_POSTFIX,  True)
    create_codedploy_deploy_groups_by_tagname(client , ['mit-api'], APP_PREFIX , GROUP_PRODUCTION, 'CodeDeployDefault.OneAtATime', False)
    
# 4. DEPLOYGROUP_STAGING
    staging_list = app_list_asg +['mit-api']
    create_codedploy_deploy_groups_by_tagname(client , staging_list, APP_PREFIX , DEPLOYGROUP_STAGING, 'CodeDeployDefault.AllAtOnce',False)
    

def delete_all_codedeploy_applications(_client):
    
    res = _client.list_applications( )
    app_list = res['applications']
    
    for app in app_list:
        _client.delete_application(applicationName = app)   

def delete_all_codedeploy_application(_client, _name):
    
    res = _client.list_applications( )
    app_list = res['applications']
    
    for app in app_list:
        if( app == _name ):
            _client.delete_application(applicationName = app)
            time.sleep(0.1)   # An error occurred (ThrottlingException) when calling the CreateApplication operation (reached max retries: 4): Rate exceeded

        else:
            print('not find applcation name')  
    

def delete_Codedeploy_config_applications(_client):
    res = _client.list_applications( )
    app_list = res['applications']
    
    for app in app_list:
        if( app.find('config-test') != -1 or  app.find('codedeploy-test') != -1 ) :
            _client.delete_application(applicationName = app)
            time.sleep(0.1)   # An error occurred (ThrottlingException) when calling the CreateApplication operation (reached max retries: 4): Rate exceeded

            print(app)   

def create_codedploy_applications(_client , _app_prefix, _app_list ):
    #Create Codedeploy Application
    for app_name in _app_list:
        response = _client.create_application(applicationName= _app_prefix +app_name)
        print ('create_application('+_app_prefix+app_name +')')
        time.sleep(0.1)   # An error occurred (ThrottlingException) when calling the CreateApplication operation (reached max retries: 4): Rate exceeded



def create_codedploy_deploy_groups_by_tagname(_client , _app_list, _app_prefix , _group_name, _config_name, _is_traffic_control = False):
        
    for app in _app_list :
       
        tag_name = app
        if _group_name is DEPLOYGROUP_STAGING :
            tag_name = 'staging'
        elif ( _group_name == GROUP_CONFIG_AMI ):
            tag_name = app+'-ami'
        
        if(_is_traffic_control == True ):
            deployment_style = {'deploymentType': 'IN_PLACE', 'deploymentOption': 'WITH_TRAFFIC_CONTROL' }
            elb_info= { 'elbInfoList': [{ 'name': 'pr-elb-'+app },] }
            response = _client.create_deployment_group(
                        applicationName= _app_prefix + app,
                        deploymentGroupName= _group_name,
                        deploymentConfigName=_config_name,   #CodeDeployDefault.AllAtOnce | CodeDeployDefault.HalfAtATime | CodeDeployDefault.OneAtATime
                        ec2TagFilters=[{'Key': 'deploy','Value': tag_name , 'Type': 'KEY_AND_VALUE'  }, ],
                        serviceRoleArn = 'arn:aws:iam::929815124819:role/role-deployment-20170410',
                        autoRollbackConfiguration={'enabled': False},
                        deploymentStyle= deployment_style,
                        loadBalancerInfo=elb_info, 
                         )
            time.sleep(0.1)   # An error occurred (ThrottlingException) when calling the CreateApplication operation (reached max retries: 4): Rate exceeded
            print ('create_deployment_group():no autoscale: retval=' +str(response))
        else:
            
            deployment_style = {'deploymentType': 'IN_PLACE', 'deploymentOption': 'WITHOUT_TRAFFIC_CONTROL' }
            response = _client.create_deployment_group(
                        applicationName= _app_prefix + app,
                        deploymentGroupName= _group_name,
                        deploymentConfigName=_config_name,   #CodeDeployDefault.AllAtOnce | CodeDeployDefault.HalfAtATime | CodeDeployDefault.OneAtATime
                        ec2TagFilters=[{'Key': 'deploy','Value': tag_name , 'Type': 'KEY_AND_VALUE'  }, ],
                        serviceRoleArn = 'arn:aws:iam::929815124819:role/role-deployment-20170410',
                        autoRollbackConfiguration={'enabled': False},
                        deploymentStyle= deployment_style,
                         )
            time.sleep(0.1)   # An error occurred (ThrottlingException) when calling the CreateApplication operation (reached max retries: 4): Rate exceeded
            print ('create_deployment_group():no autoscale: retval=' +str(response))
                  
        
def create_codedploy_deploy_groups_by_autoscale(_client , _app_list, _app_prefix , _group_name, _config_name, _autoscale_postfix, _is_traffic_control = False):
        
    for app in _app_list :
        if(_is_traffic_control == True ):
            deployment_style = {'deploymentType': 'IN_PLACE', 'deploymentOption': 'WITH_TRAFFIC_CONTROL' }
            elb_info= { 'elbInfoList': [{ 'name': 'pr-elb-'+app },] }
            response = _client.create_deployment_group(
                        applicationName= _app_prefix + app,
                        deploymentGroupName= _group_name,
                        deploymentConfigName=_config_name,   #CodeDeployDefault.AllAtOnce | CodeDeployDefault.HalfAtATime | CodeDeployDefault.OneAtATime
                        autoScalingGroups  = ['pr-asg-'+app+_autoscale_postfix],
                          serviceRoleArn = 'arn:aws:iam::929815124819:role/role-deployment-20170410',
                        autoRollbackConfiguration={'enabled': False},
                        deploymentStyle= deployment_style,
                        loadBalancerInfo=elb_info, 
                         )
            time.sleep(0.1)   # An error occurred (ThrottlingException) when calling the CreateApplication operation (reached max retries: 4): Rate exceeded
            print ('create_deployment_group():no autoscale: retval=' +str(response))
        else:
            deployment_style = {'deploymentType': 'IN_PLACE', 'deploymentOption': 'WITHOUT_TRAFFIC_CONTROL' }
            response = _client.create_deployment_group(
                        applicationName= _app_prefix + app,
                        deploymentGroupName= _group_name,
                        deploymentConfigName=_config_name,   #CodeDeployDefault.AllAtOnce | CodeDeployDefault.HalfAtATime | CodeDeployDefault.OneAtATime
                        autoScalingGroups  = ['pr-asg-'+app+_autoscale_postfix],
                        serviceRoleArn = 'arn:aws:iam::929815124819:role/role-deployment-20170410',
                        autoRollbackConfiguration={'enabled': False},
                        deploymentStyle= deployment_style,
                         )
            time.sleep(0.1)   # An error occurred (ThrottlingException) when calling the CreateApplication operation (reached max retries: 4): Rate exceeded
            print ('create_deployment_group():no autoscale: retval=' +str(response))
                

if __name__ == "__main__" :
    main()
    
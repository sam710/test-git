# -*- coding: utf8 -*-

import boto3
import sys
import time


deploy_app_list= [
#                 'doc-api',          
               'erp',
#                'inseed',
#                'insolver',
#                 'jain',
#                'midasinsight',
#                'mmsw',
#                'mrs',
#                'mrs-app',
#                'mrs-bigfile',
#                'product-site',
#                'web',
                ]


def main():
    deploy_group = 'staging'
    deploy_id_list = []
     
    for app in deploy_app_list :
        deploy_id_list.append( Create_Deployment( app, deploy_group ) )
    
    
    print (deploy_id_list)
    print ('end')
    



def Create_Deployment(_app_name,  _deploy_group='production'):
    
    print ('[Create_Deployment Start] ( _app_name : '+_app_name+ ', _deploy_group: '+_deploy_group +' )')
    
    client = boto3.client('codedeploy')
     
    deploy_group_name = _deploy_group # _deploy_group
    key_name ='deployment-descriptor/'+ _app_name+'/'+_app_name+'.zip'
        
    # create deployment
    response = client.create_deployment(
            applicationName= 'codedeploy-'+_app_name,
            deploymentGroupName=deploy_group_name,
            revision={
                'revisionType': 'S3',
                's3Location': {
                    'bucket': 'midasit-st-s3-deployment',
                  #  'key': 'deployment-descriptor/mrs/SampleApp_Linux.zip',
                    'key': key_name ,
                    'bundleType': 'zip',
                },
            },
                                            
            deploymentConfigName='CodeDeployDefault.OneAtATime',
            description= 'Deploy'+_app_name,
            ignoreApplicationStopFailures=False,
            autoRollbackConfiguration={ 'enabled': False,},  # 'events': [ 'DEPLOYMENT_FAILURE'|'DEPLOYMENT_STOP_ON_ALARM'|'DEPLOYMENT_STOP_ON_REQUEST', ]  },
            fileExistsBehavior='OVERWRITE'
        )
    
#     deploymentId = response['deploymentId']
#     waiter = client.get_waiter('deployment_successful')
#     print ('Wait For: Deployment-'+_app_name+', deploymentId ('+deploymentId+')')
#     waiter.wait(  deploymentId=deploymentId )   
#     print ('['+deploymentId+']['+_app_name+'] deployment successful')
    
    
if __name__ == '__main__':
    main()
       

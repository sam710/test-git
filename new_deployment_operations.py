# -*- coding: utf8 -*-

import boto3
import sys
import time

#web-group  (not-ami, not-autoscale)
deploy_app_list_not_ami= [
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


#ami
deploy_app_list_ami= [
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
#                'web',
                ]

DEPLOY_TARGET = [
#                                 'production',
#                                'operations_ami',
#                                     'config-ami',
                                 'config-production'
                                ]

def main():
    deploy_id_list = []
    deploy_app_list = ['intalk']  #deploy_app_list_ami
    
    for target in DEPLOY_TARGET:
        print ('deployment group : '+target)
        for app in deploy_app_list :
            #if(app == 'web'):
           
            deploy_id_list.append( Create_Deployment( app, target)) #'operations_ami' ) )
            #deploy_id_list.append( Create_Deployment( app, 'production' ) )
        
        print (deploy_id_list)
 
    
    
def Create_Deployment(_app_name,  _deploy_group='production'):
    
    print ('[Create_Deployment Start] ( _app_name : '+_app_name+ ', _deploy_group: '+_deploy_group +' )')
    
    client = boto3.client('codedeploy')
     
    deploy_group_name = _deploy_group # _deploy_group
    key_name ='deployment-descriptor/'+ _app_name+'/'+_app_name+'.zip'

    print( 'codedeploy-config-'+_app_name)        
    # create deployment
    response = client.create_deployment(
            applicationName= 'codedeploy-config-'+_app_name,
            deploymentGroupName=deploy_group_name,
            revision={
                'revisionType': 'S3',
                's3Location': {
                    'bucket': 'midasit-pr-s3-configuration-management',
                  #  'key': 'deployment-descriptor/mrs/SampleApp_Linux.zip',
                    'key': key_name ,
                    'bundleType': 'zip',
                },
            },
                                            
            deploymentConfigName='CodeDeployDefault.OneAtATime',
            description= 'Deploy'+_app_name,
            ignoreApplicationStopFailures=False,
            autoRollbackConfiguration={ 'enabled': False,},  # 'events': [ 'DEPLOYMENT_FAILURE'|'DEPLOYMENT_STOP_ON_ALARM'|'DEPLOYMENT_STOP_ON_REQUEST', ]  },
       #     fileExistsBehavior='OVERWRITE'
        )
#     
#     deploymentId = response['deploymentId']
#     waiter = client.get_waiter('deployment_successful')
#     print ('Wait For: Deployment-'+_app_name+', deploymentId ('+deploymentId+')')
#     waiter.wait(  deploymentId=deploymentId )   
#     print ('['+deploymentId+']['+_app_name+'] deployment successful')



    
if __name__ == '__main__':
    main()
       

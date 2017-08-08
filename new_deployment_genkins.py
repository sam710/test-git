# -*- coding: utf8 -*-

import boto3
import sys
import time


def Upload_WAR(_app_name, _war_path ):
    print ('[Upload_WAR Start] ( _app_name : '+_app_name+', _war_path: '+_war_path +' )')

    s3 = boto3.resource('s3')
    bucket = s3.Bucket('midasit-pr-s3-deployment' )

       # upload war file
    if(_war_path != None):
        bucket.upload_file( _war_path, 'src/'+_app_name+'/ROOT.war' )
        time.sleep(3)

        print ('[Create_Deployment End]   return True')
        return True    #updoad_file, no return value,, Required check Upload file

    else:
        print ('[Create_Deployment End]   return False')
        return False


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
                    'bucket': 'midasit-pr-s3-deployment',
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
    
    deploymentId = response['deploymentId']
    waiter = client.get_waiter('deployment_successful')
    
    print ('Wait For: Deployment-'+_app_name+', deploymentId ('+deploymentId+')')
    
    waiter.wait(  deploymentId=deploymentId )   
    
    print ('['+deploymentId+']['+_app_name+'] deployment successful')

   
if __name__ == '__main__':

    if len(sys.argv) < 4:
        print ('Require parameter: _app_name,_war_file_path,  _deploy_group')
        sys.exit()

    app_name = sys.argv[1]
    war_file_path = sys.argv[2]
    deploy_group = sys.argv[3]

    if(deploy_group != 'production'): #  and _deploy_group != 'staging' _deploy_group != 'development'):
        print ('wrong parameter : deploy group (production or staging or development')
        print ('Before open on AWS Envrionment, Only support "production"')
        sys.exit()

    if (Upload_WAR( app_name, war_file_path ) is 0 ):
        print ('Upload fail... check _war_path and war file...')
        sys.exit()

    Create_Deployment( app_name, deploy_group )


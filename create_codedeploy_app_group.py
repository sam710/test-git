# -*- coding: utf8 -*-

import boto3
import time

deploy_app_list= [
                 'doc-api',          
                 'erp',
                 'erp-se',       # tag name = deploy : erp-se
                 'inseed',
                 'insolver',
                 'jain',
                 'midasinsight',
                'mit-api',
                 
                 'mmsw',
                 'mrs',
                 'mrs-app',
                 'mrs-bigfile',
                 'mrs-se',              # tag name = deploy : mrs-se
                 'product-site',
                 'web',
                ]
#                'erp-scheduler',
#                'inseed-fire',             #war 
#                'inseed-scheduler',   #jar
#                'las',
#                'lgs',
#                'mit-common-scheduler',
#                'mit-intra-scheduler',
#                'mmsw-fire',
#                'mrs-chat',
#                'mrs-scheduler',





if __name__ == "__main__" :

    client = boto3.client('codedeploy')
    # CodeDeployConnection(        aws_access_key_id=aws_access_key_id,        aws_secret_access_key=aws_secret_access_key,        **kwargs    )
    
# 1. Delete DeployApplication .  (except codedeploy-mrs)
    response = client.list_applications( )
    print (response) 
    app_list = response['applications']
    for app in app_list:
            client.delete_application(applicationName = app)
    
    
# 2. Create deploy application
    for app_name in deploy_app_list:
      #  if(app_name != 'mrs'):
        response = client.create_application(applicationName='codedeploy-'+app_name)
        print ('create_application(codedeploy-'+app_name +') : retval =')
        print (response)
        time.sleep(0.1)   # An error occurred (ThrottlingException) when calling the CreateApplication operation (reached max retries: 4): Rate exceeded
    
     
    # Create deployment group
    deploy_group_name = 'production'
    deploy_group_name_for_ami = 'operations_ami'
    
    response = client.list_applications( )
    app_list = response['applications']
    
    for app in app_list :
     #   if( app != 'codedeploy-mrs'):
        print ('deploy group'+app)
        
        # not autoscale group
        if(app[11:] == 'erp-se' or app[11:] == 'mrs-se'  or app[11:] == 'mit-api'):         
            response = client.create_deployment_group(
                        applicationName= app,
                        deploymentGroupName=deploy_group_name,
                        deploymentConfigName='CodeDeployDefault.OneAtATime',   #CodeDeployDefault.AllAtOnce | CodeDeployDefault.HalfAtATime | CodeDeployDefault.OneAtATime
                            # 
     #                   autoScalingGroups  = ['as-group-'+app[11:]],
                        ec2TagFilters=[{'Key': 'deploy','Value': app[11:], 'Type': 'KEY_AND_VALUE'  }, ],
                        serviceRoleArn = 'arn:aws:iam::929815124819:role/role-deployment-20170410',
                        autoRollbackConfiguration={'enabled': False},
                        deploymentStyle={'deploymentType': 'IN_PLACE', 'deploymentOption': 'WITHOUT_TRAFFIC_CONTROL' },
     #                   loadBalancerInfo={ 'elbInfoList': [{ 'name': 'pr-elb-'+app[11:]},] }, 
                         )
            print ('create_deployment_group():no autoscale: retval=' )
            print (response) 
            
            if( app[11:] == 'mit-api'):
                response = client.create_deployment_group(
                            applicationName= app,
                            deploymentGroupName=deploy_group_name_for_ami,
                            deploymentConfigName='CodeDeployDefault.AllAtOnce',   #CodeDeployDefault.AllAtOnce | CodeDeployDefault.HalfAtATime | CodeDeployDefault.OneAtATime
                                # 
         #                   autoScalingGroups  = ['as-group-'+app[11:]],
                           ec2TagFilters=[{'Key': 'deploy','Value': app[11:], 'Type': 'KEY_AND_VALUE'  }, ],
                            serviceRoleArn = 'arn:aws:iam::929815124819:role/role-deployment-20170410',
                            autoRollbackConfiguration={'enabled': False},
                            deploymentStyle={'deploymentType': 'IN_PLACE', 'deploymentOption': 'WITHOUT_TRAFFIC_CONTROL' },
         #                   loadBalancerInfo={ 'elbInfoList': [{ 'name': 'pr-elb-'+app[11:]},] }, 
                             )         
                        
                    
        else :
            response = client.create_deployment_group(
                        applicationName= app,
                        deploymentGroupName=deploy_group_name,
                        deploymentConfigName='CodeDeployDefault.OneAtATime',   #CodeDeployDefault.AllAtOnce | CodeDeployDefault.HalfAtATime | CodeDeployDefault.OneAtATime
                        autoScalingGroups  = ['as-group-'+app[11:]],
                        serviceRoleArn = 'arn:aws:iam::929815124819:role/role-deployment-20170410',
                        autoRollbackConfiguration={'enabled': False},
                        deploymentStyle={'deploymentType': 'IN_PLACE', 'deploymentOption': 'WITHOUT_TRAFFIC_CONTROL' },

#                        deploymentStyle={'deploymentType': 'IN_PLACE', 'deploymentOption': 'WITH_TRAFFIC_CONTROL' },
#                        loadBalancerInfo={ 'elbInfoList': [{ 'name': 'pr-elb-'+app[11:]},] }, 
                         )
            print (response) 
                    
            # for ami group        
            response = client.create_deployment_group(
                        applicationName= app,
                        deploymentGroupName=deploy_group_name_for_ami,
                        deploymentConfigName='CodeDeployDefault.AllAtOnce',   #CodeDeployDefault.AllAtOnce | CodeDeployDefault.HalfAtATime | CodeDeployDefault.OneAtATime
                            # 
     #                   autoScalingGroups  = ['as-group-'+app[11:]],
                        ec2TagFilters=[{'Key': 'deploy','Value': app[11:]+'-ami', 'Type': 'KEY_AND_VALUE'  }, ],
                        serviceRoleArn = 'arn:aws:iam::929815124819:role/role-deployment-20170410',
                        autoRollbackConfiguration={'enabled': False},
                        deploymentStyle={'deploymentType': 'IN_PLACE', 'deploymentOption': 'WITHOUT_TRAFFIC_CONTROL' },
     #                   loadBalancerInfo={ 'elbInfoList': [{ 'name': 'pr-elb-'+app[11:]},] }, 
                         )
           
            print (response) 





 


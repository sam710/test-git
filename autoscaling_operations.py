# -*- coding: utf8 -*-

import os
import shutil
import sys
import time
import autoscaling_class 
import boto3
#from sentrysample.DeployDesc import DeployDesc



app_list22= [
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

app_list= [
                'doc-api',
#           
                       
            ]

#pr-ami-ec2-mrs-20170601
#pr-ami-ec2-mrs-20170601

DEPLOY_BUCKET_PATH = 'D:\\02_Workspace\\AWS\\Deploy_S3_bucket_Operations'
BUCKET_NAME = 'midasit-pr-s3-configuration-management'



def main():
#     CreateAllAutoScaleGroup('20170702-01')
    UpdateAutoScaleGroup('20170702-01')





def UpdateAutoScaleGroup(_ami_date):
    print('call UpdateAutoScaleGroup')
    as_manager = autoscaling_class.autoscale_manager_class()
    
    for app in app_list:
        as_name = 'pr-asg-'+app
        lc_data = autoscaling_class.lauch_config_class(app ,_ami_date, ['sg-50352037'], 'c4.large', 'Role-WAS-0329','aws_ec2_key_tokyo'  ) 
        lc_name_old = as_manager.Get_lcName_From_ASGroup(as_name)
        
        if( lc_name_old == lc_data.lc_name ) :
           lc_data.lc_name = lc_data.lc_name +'_1'
        
        as_manager.Update_AutoScalingGroup_NewLaunchConfig(as_name, lc_data )
        
        as_manager.Delete_LounchConfig(lc_name_old)
        
    

def CreateAllAutoScaleGroup(_date):
    as_health_check_type = 'EC2'  # or 'ELB'
    lc_data_list  = list()
    as_data_list  = list()
    
    delete_as_list = list()
    cnt = 0
    
    for app in app_list :
     # Seoul  
        instance_type =  't2.small'
        if( app == 'doc-api' or app == 'erp' or app == 'insolver' or app == 'inseed' ):
            instance_type =  't2.medium'
        elif ( app == 'web' or app == 'mrs' or app == 'mrs-app' or app == 'mrs-bigfile' ):
            instance_type =  'm4.large'
            
        lc_data_list.append( autoscaling_class.lauch_config_class(app ,_date,['sg-8bc645e3', 'sg-68c44700'], instance_type, 'Role-WAS-0329','aws_ec2_key'  ) )
        as_data_list.append( autoscaling_class.autoscale_class(app , 'subnet-b13e0ad8, subnet-6e9bf723',  0, 4, 2, 300,as_health_check_type,300 ) )

    # Tokyo
    #    lc_data_list.append( autoscaling_class.lauch_config_class(app ,'20170601', ['sg-50352037'], 't2.small', 'Role-WAS-0329','aws_ec2_key_tokyo'  ) )
     #   as_data_list.append( autoscaling_class.autoscale_class(app , "subnet-870929f1,subnet-1a224042",  0, 4, 1, 300,as_health_check_type,300 ) )
        print (lc_data_list)
        
    
    
    for lc_data in lc_data_list:
        
        as_manager = autoscaling_class.autoscale_manager_class( lc_data, as_data_list[cnt] )
    
        if(as_manager.IsExist_ASGroup( as_data_list[cnt].as_name) is 1) :
            as_manager.Delete_AutoScalingGroup( as_data_list[cnt].as_name )
            delete_as_list.append(as_data_list[cnt].as_name )
        #   as_manager.waitfor_delete_autosacling_group( as_data_list[cnt].as_name)
            
        if(as_manager.IsExist_LounchConfig( lc_data.lc_name) is 1) :
            as_manager.Delete_LounchConfig( lc_data.lc_name )   
        cnt +=1

    print(delete_as_list)
    if( len(delete_as_list) >0 ):
        as_wait = autoscaling_class.autoscale_manager_class()
        as_wait.waitfor_delete_autosacling_groups(delete_as_list)
    
    cnt =0
    for lc_data in lc_data_list:   
        as_manager = autoscaling_class.autoscale_manager_class( lc_data, as_data_list[cnt] )
        as_manager.Create_LaunchConfig()
        as_manager.Create_AutoScalingGroup()
        cnt +=1    
        
 



if __name__ == "__main__" :
    main()

   
    

    
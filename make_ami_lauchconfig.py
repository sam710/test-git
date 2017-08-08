# -*- coding: utf8 -*-

import boto3
from datetime import datetime
import os, shutil, sys, time
import autoscaling_class 


app_list= [
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


def main():
    

# Create AMI
    date = datetime.today().strftime("%Y%m%d")
 
    print (date)
  
    CreateAMI_ByAppList(date+'-01')
#     print ('End - Create AMIs')
       
      
#     UpdateAutoScaleGroup('20170622')
#     print ('End - UpdateAutoScaleGroup')

   
#     as_manager = autoscaling_class.autoscale_manager_class()
#       
#     for app in app_list:
#         as_name = 'as-group-'+app
#                
#         as_manager.Update_AutoScalingGroup_DesiredCapacity(as_name,2 )
       

def CreateAMI_ByAppList( _ami_date):
    image_list=[]
          
    for app in app_list:
        print (app)
        instance = GetInstanceByTagName(app)
        
        print (instance)
        if(instance != None):# and instance.state['Name'] == 'running'):
            tag = CreateTag( instance,  'deploy',  app+'-ami' )
            image = CreateAMI(  instance, app,  _ami_date)
            print (image.id)
            if image != None :
                image_list.append(image.id)
        else:
            print ('instance (pr-ec2-%s-ami) is not running' %  (app) )
    
    client = boto3.client('ec2')
    waiter = client.get_waiter('image_available')
    print ('Wait For:')
    print(image_list)    

    waiter.wait(   ImageIds= image_list )   
    

def UpdateAutoScaleGroup(_ami_date):
    print('call UpdateAutoScaleGroup')
    as_manager = autoscaling_class.autoscale_manager_class()
    
    for app in app_list:
        as_name = 'as-group-'+app
        lc_data = autoscaling_class.lauch_config_class(app ,_ami_date, ['sg-8bc645e3', 'sg-68c44700'], 'c4.large', 'Role-WAS-0329','aws_ec2_key'  ) 
        lc_name_old = as_manager.Get_lcName_From_ASGroup(as_name)
        
        if( lc_name_old == lc_data.lc_name ) :
           lc_data.lc_name = lc_data.lc_name +'_1'
        
        as_manager.Update_AutoScalingGroup_NewLaunchConfig(as_name, lc_data )
        
        as_manager.Delete_LounchConfig(lc_name_old)
        


def GetInstanceByTagName( _app_name):
    ec2 = boto3.resource('ec2', region_name='ap-northeast-2')
    
    filters = [{'Name':'tag:Name', 'Values':['pr-ec2-'+_app_name+'-ami']}]
        
    instance_list  = list(ec2.instances.filter(Filters=filters))
    
    if( len(instance_list) == 0):
        print ('[error] not found ami-instance')
        return None    
   
    return instance_list[0]

def CreateTag( _ec2_instance, _key, _value ):
    tag = _ec2_instance.create_tags(
                                            DryRun=False,
                                            Tags=[
                                                {
                                                    'Key': _key,
                                                    'Value': _value
                                                },
                                            ]
                                        )
    return tag

def CreateAMI( _ec2_instance, _app_name, _date ):

    image = _ec2_instance.create_image(
        DryRun=False,
    #    Name='pr-ami-ec2-'+_app_name+ '-'+_date,
        Name='pr-ami-ec2-'+_app_name+ '-'+_date,
        Description='',
        NoReboot=False
        )
    print (image)
    return image


    
if __name__ == '__main__':
    main()
       

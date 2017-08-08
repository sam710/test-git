# -*- coding: utf8 -*-
import boto3
import os, sys, time
from datetime import datetime


class lauch_config_class:
#variable
    app_name =''
    lc_name = ''
    lc_image_id = ''
    lc_security_groups = ''
    lc_instance_type = ''
    lc_instance_profile_name = ''
    lc_key_name = ''
    lc_instance_monitoring = True
    lc_userdata = ''

    def __init__( self, _app_name ,_ami_date, _security_groups,_instance_type, _instance_profile_name, _key_name, _userdata ='',  _instance_monitoring = True ):
        self.app_name = _app_name
        self.lc_name = 'pr-lc-'+ _app_name +'-'+_ami_date  # datetime.today().strftime("%Y%m%d")
        self.lc_security_groups = _security_groups
        self.lc_instance_type = _instance_type
        self.lc_instance_profile_name = _instance_profile_name
        self.lc_key_name = _key_name
        self.lc_instance_monitoring = _instance_monitoring
    #    self.lc_image_id = self.get_image_id('pr-ami-ec2-'+_app_name+'-'+_ami_date)
        print(_ami_date)
        self.lc_image_id = self.get_image_id('pr-ami-ec2-'+_app_name+'-'+_ami_date)  #test
        self.lc_userdata = _userdata

    def get_image_id(self, _ami_name ):
        ec2 = boto3.resource('ec2', region_name='ap-northeast-2')
        filter = {'Name': 'name', 'Values' : [_ami_name]}
        ami_list = list(ec2.images.filter(Filters = [filter]))

        if( len(ami_list) == 0):
            print ('[error] not found ami-instance')
            return None
        else:
            print (ami_list[0].id)
            return ami_list[0].id
    def set_userdata(self, _userdata):
        self.lc_userdata = _userdata

    def print_data(self):
        print( '***print lc class data **********')
        print( '[app_name] : ' + self.app_name )
        print( '[lc_name] : ' + self.lc_name )
        print( '[lc_image_id] : ' + self.lc_image_id )
        print( '[lc_security_groups] : ' + str(self.lc_security_groups) )
        print( '[lc_instance_type] : ' + self.lc_instance_type )
        print( '[lc_instance_profile_name] : ' + self.lc_instance_profile_name )
        print( '[lc_key_name] : ' + self.lc_key_name )
        print( '[lc_instance_monitoring] : ' + str(self.lc_instance_monitoring ) )
        print( '*********************************')


class autoscale_class:
# variable
    app_name =''
    as_name = ''
    as_tags_name = ''
    as_load_balancers = ''
    as_vpc_zone_identifier = ''
    as_min_size = 0
    as_max_size = 0
    as_desired_capacity = 0
    as_default_cooldown = 300
    as_health_check_type = ''
    as_health_check_period = 300

# initialize
    def __init__(self, _app_name,_vpc_zone_identifier,_min_size ,_max_size, _desired_capacity,_default_cooldown, _health_check_type, _health_check_period):
        self.app_name = _app_name
        self.as_name = self.get_as_name_by_app_name(_app_name)
        self.as_tags_name =  'pr-ec2-'+_app_name+'-autoscale'
        self.as_load_balancers = [ 'pr-elb-'+_app_name ]
        self.as_vpc_zone_identifier = _vpc_zone_identifier
        self.as_min_size = _min_size
        self.as_max_size = _max_size
        self.as_desired_capacity = _desired_capacity
        self.as_default_cooldown = _default_cooldown
        self.as_health_check_type = _health_check_type
        self.as_health_check_period = _health_check_period

# method
    def get_as_name_by_app_name(self, _app_name):
        return 'pr-asg-'+_app_name

    def print_data(self):
        print( '***print as class data **********')
        print( '[app_name] : ' + self.app_name )
        print( '[as_name] : ' + self.as_name )
        print( '[as_tags_name] : ' + str( self.as_tags_name) )
        print( '[as_load_balancers] : ' + str(self.as_load_balancers) )
        print( '[as_vpc_zone_identifier] : ' + str(self.as_vpc_zone_identifier) )
        print( '[as_min_size] : ' + str(self.as_min_size) )
        print( '[as_max_size] : ' + str(self.as_max_size) )
        print( '[as_desired_capacity] : ' + str(self.as_desired_capacity) )
        print( '[as_default_cooldown] : ' + str(self.as_default_cooldown) )
        print( '[as_health_check_type] : ' + self.as_health_check_type )
        print( '[as_health_check_period] : ' + str(self.as_health_check_period) )
        print( '*********************************')



class autoscale_manager_class:
#variable
    lc_data = None
    as_data = None
    aws_client = None

#initialize
    def __init__(self, _lc_data = None , _as_data = None  ):
        self.lc_data = _lc_data
        self.as_data = _as_data
        if self.lc_data is not None:
            self.lc_data.print_data()
        if self.as_data is not None:
            self.as_data.print_data()

        self.aws_client = boto3.client('autoscaling', region_name='ap-northeast-2')


#method
    def Create_LaunchConfig(self, _lc_data = None):
        print ('call autoscale_manager_class::Create_LauchConfig')

        #if(self.IsExist_LounchConfig(self.lc_data.lc_name) is 1) :
        #    self.Delete_LounchConfig(self.lc_data.lc_name)
        if _lc_data != None :
            self.lc_data = _lc_data

        response = self.aws_client.create_launch_configuration(
                                            LaunchConfigurationName=self.lc_data.lc_name ,
                                            ImageId=self.lc_data.lc_image_id,
                                            KeyName=self.lc_data.lc_key_name,
                                            SecurityGroups=self.lc_data.lc_security_groups,      #list
                                            UserData=self.lc_data.lc_userdata,
                                            InstanceType=self.lc_data.lc_instance_type,
                                            InstanceMonitoring={'Enabled': self.lc_data.lc_instance_monitoring },
                                            IamInstanceProfile= self.lc_data.lc_instance_profile_name,
                                        )
        print(response)

    def Create_AutoScalingGroup(self, _as_data = None):
        print ('call autoscale_manager_class::Create_AutoScalingGroup')
        
        if _as_data != None :
            self.as_data = _as_data       
        
        response = self.aws_client.create_auto_scaling_group(
                                            AutoScalingGroupName= self.as_data.as_name,
                                            LaunchConfigurationName=self.lc_data.lc_name,
                                            MinSize=self.as_data.as_min_size,
                                            MaxSize=self.as_data.as_max_size,
                                            DesiredCapacity=self.as_data.as_desired_capacity,
                                            DefaultCooldown=self.as_data.as_default_cooldown,
                                            LoadBalancerNames= self.as_data.as_load_balancers, #['string', ],
                                            HealthCheckType=self.as_data.as_health_check_type,
                                            HealthCheckGracePeriod=self.as_data.as_health_check_period,
                                            VPCZoneIdentifier=self.as_data.as_vpc_zone_identifier,   #['string', ],
                                            Tags=[{
                                                    'ResourceId': self.as_data.as_name,
                                                    'Key': 'Name',
                                                    'Value': self.as_data.as_tags_name,
                                                    'PropagateAtLaunch': True
                                                    },
                                                   {
                                                    'ResourceId': self.as_data.as_name,
                                                    'Key': 'deploy',
                                                    'Value': self.as_data.app_name,
                                                    'PropagateAtLaunch': True
                                                    },
                                                ]
                                            )

        #conn_autoscale.enable_metrics_collection(asGroup['name'], '1Minute')    #Enable Monitoring
        #conn_autoscale.enable_metrics_collection(ag, '1Minute')    #Enable Monitoring
        self.aws_client.enable_metrics_collection(AutoScalingGroupName=self.as_data.as_name,Granularity = '1Minute')
        notification_type_list = ['autoscaling:EC2_INSTANCE_LAUNCH',
                                            'autoscaling:EC2_INSTANCE_LAUNCH_ERROR',
                                            'autoscaling:EC2_INSTANCE_TERMINATE',
                                            'autoscaling:EC2_INSTANCE_TERMINATE_ERROR'
                                            ]
        res1 = self.aws_client.put_notification_configuration(AutoScalingGroupName=self.as_data.as_name, TopicARN='arn:aws:sns:ap-northeast-2:929815124819:autoscaling_email',NotificationTypes=notification_type_list)
#        res2 = self.aws_client.put_notification_configuration(AutoScalingGroupName=self.as_data.as_name, TopicARN='arn:aws:sns:ap-northeast-2:929815124819:autoscaling_slack',NotificationTypes=notification_type_list)

#        put_notification_configuration

        print (response)
        print ('End autoscale_manager_class::Create_AutoScalingGroup')



    def Update_AutoScalingGroup_DesiredCapacity(self,_as_name, _desired_capacity):
        print ('call autoscale_manager_class::Update_AutoScalingGroup_DesiredCapacity : '+_as_name )
        response = self.aws_client.update_auto_scaling_group(
                                            AutoScalingGroupName=_as_name,
                                            DesiredCapacity=_desired_capacity,
                                            )
        print(response)
        print ('End autoscale_manager_class::Update_AutoScalingGroup_DesiredCapacity') 

    def Update_AutoScalingGroup_NewLaunchConfig(self,_as_name, _new_lc_data):
        print ('call autoscale_manager_class::Update_AutoScalingGroup_NewLaunchConfig : '+_as_name )
        self.lc_data = _new_lc_data

        if(self.IsExist_LounchConfig(self.lc_data.lc_name) is 1) :
            self.Delete_LounchConfig(self.lc_data.lc_name)

        self.aws_client.create_launch_configuration(
                                            LaunchConfigurationName=self.lc_data.lc_name ,
                                            ImageId=self.lc_data.lc_image_id,
                                            KeyName=self.lc_data.lc_key_name,
                                            SecurityGroups=self.lc_data.lc_security_groups,      #list
                                            UserData=self.lc_data.lc_userdata,
                                            InstanceType=self.lc_data.lc_instance_type,
                                            InstanceMonitoring={'Enabled': self.lc_data.lc_instance_monitoring },
                                            IamInstanceProfile= self.lc_data.lc_instance_profile_name,
                                        )


        response = self.aws_client.update_auto_scaling_group(
                                            AutoScalingGroupName=_as_name,
                                            LaunchConfigurationName=self.lc_data.lc_name,
                                            )
        print(response)
        print ('End autoscale_manager_class::Update_AutoScalingGroup_NewLaunchConfig')

    def Get_lcName_From_ASGroup(self,_as_name):
        print ('call autoscale_manager_class::Get_lcName_From_ASGroup : '+_as_name)

        res = self.aws_client.describe_auto_scaling_groups(  AutoScalingGroupNames =[_as_name]  )
        print (res)
        if( len(res['AutoScalingGroups']) > 0):
            asg =res['AutoScalingGroups'][0]
            print('Return autoscale_manager_class::Get_lcName_From_ASGroup :'+ asg['LaunchConfigurationName'] )
            return asg['LaunchConfigurationName']
        else:
            print('Return autoscale_manager_class::Get_lcName_From_ASGroup : not find autoscale group' )
            return None

        return



    def IsExist_ASGroup(self,_as_name):
        print ('call autoscale_manager_class::IsExist_ASGroup : '+_as_name)

        res = self.aws_client.describe_auto_scaling_groups(  AutoScalingGroupNames =[_as_name]  )
    #    print (res)
        print('Return autoscale_manager_class::IsExist_ASGroup : ' + str(len(res['AutoScalingGroups'])) )
        return len(res['AutoScalingGroups'])


    def IsExist_LounchConfig(self, _lc_name):
        print ('call autoscale_manager_class::IsExist_LounchConfig : '+_lc_name)

        res = self.aws_client.describe_launch_configurations(  LaunchConfigurationNames=[_lc_name]  )
    #    print (res)
        print('Return autoscale_manager_class::IsExist_LounchConfig : ' + str(len(res['LaunchConfigurations'])) )
        return len(res['LaunchConfigurations'])


    def Delete_AutoScalingGroup(self, _as_name):
        print ('call autoscale_manager_class::Delete_AutoScalingGroup')

        response = self.aws_client.delete_auto_scaling_group(AutoScalingGroupName=_as_name, ForceDelete=True )
    #    print(response)
        print ('End autoscale_manager_class::Delete_AutoScalingGroup')

    def Delete_LounchConfig(self,_lc_name ):
        print ('call autoscale_manager_class::Delete_LounchConfig')
        #LaunchConfigurationName = self.lc_data.lc_name

        response = self.aws_client.delete_launch_configuration( LaunchConfigurationName=_lc_name )
        #print(response)
        print ('End autoscale_manager_class::Delete_LounchConfig')

    def waitfor_delete_autosacling_group(self, _as_name):
        while True:
            res = self.aws_client.describe_auto_scaling_groups(  AutoScalingGroupNames =[_as_name]  )
            print(len(res['AutoScalingGroups']))
            if( len(res['AutoScalingGroups']) == 0 ):
                break;
            else:
                asg =res['AutoScalingGroups'][0]
                print (_as_name +': ' +asg['Status'])
            time.sleep(10)

    def waitfor_delete_autosacling_groups(self, _as_name_list):

        if( _as_name_list == None or len(_as_name_list) ==0 ) : return

        while True:
            res = self.aws_client.describe_auto_scaling_groups(  AutoScalingGroupNames =_as_name_list  )
            print('as num for wating: '+ str(len(res['AutoScalingGroups']))  )
            if( len(res['AutoScalingGroups']) == 0 ):
                break;
            else:
                asg =res['AutoScalingGroups'][0]
                print ('wait for Delete autoscale group')
            time.sleep(15)



#    def delete_all_AutoScalingGroup_LounchConfig(self):

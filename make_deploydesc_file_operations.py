# -*- coding: utf8 -*-

import os
import shutil
import sys
import time
import deploydesc_operations_class
import boto3
from datetime import datetime 

#from sentrysample.DeployDesc import DeployDesc

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
#                  'product-site-kst',
                ]

#web-group  (not-ami, not-autoscale)
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

#web-group  (not-ami, not-autoscale)
app_list_not_asg_was= [
               'erp-se',
               'mit-api',
               'mrs-se',
                ]

DEPLOY_BUCKET_PATH = 'D:\\02_Workspace\\AWS\\Deploy_S3_bucket_Operations'
#DEPLOY_BUCKET_PATH = '/Users/st/workplace/Deploy_folder/deploy_operation'

BUCKET_NAME = 'midasit-pr-s3-configuration-management'


def main():
#Initialize -  delete desc files (local)
    shutil.rmtree(DEPLOY_BUCKET_PATH+'\\deployment-descriptor\\',True)
#     shutil.rmtree(DEPLOY_BUCKET_PATH+'/deployment-descriptor/',True)

    app_list = app_list_asg

#make deploy-descriptor & repository (config-files)
    deploy = deploydesc_operations_class.DeployDescOperations( DEPLOY_BUCKET_PATH, BUCKET_NAME, 'windows' )
    for app_name in app_list:
        deploy.make_desc_zip_file(app_name)
        deploy.make_repository_file(app_name)

    
    print ("\n\n\nCheck Deploy descriptor file & Repository...")
    
    


if __name__ == "__main__" :
    main()
    
    
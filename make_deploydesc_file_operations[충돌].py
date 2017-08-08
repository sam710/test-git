# -*- coding: utf8 -*-

import os
import shutil
import sys
import time
import deploydesc_operations_class
import boto3
from datetime import datetime 

#from sentrysample.DeployDesc import DeployDesc

app_list= [
                'doc-api',          
                 'erp',
                 'erp-se',       # tag name = deploy : erp-se
                 'inseed',
                 'insolver',
                 'jain',
                 'midasinsight',
                 'mit-api',
                 'mit-job',
                 'mmsw',
                 'mrs',
                 'mrs-app',
                 'mrs-bigfile',
                 'mrs-se',              # tag name = deploy : mrs-se
                 'product-site',
                 'web',
#                  'product-site-kst',
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
DEPLOY_BUCKET_PATH = 'D:\\02_Workspace\\AWS\\Deploy_S3_bucket_Operations'
BUCKET_NAME = 'midasit-pr-s3-configuration-management'
#BUCKET_NAME = 'midasit-pr-s3-deployment'


def main():
#Initialize -  delete desc files (local)
    shutil.rmtree(DEPLOY_BUCKET_PATH+'\\deployment-descriptor\\',True)

#make deploy-descriptor & repository (config-files)
    deploy = deploydesc_operations_class.DeployDescOperations( DEPLOY_BUCKET_PATH, BUCKET_NAME )
    for app_name in app_list:
        deploy.make_desc_zip_file(app_name)
        deploy.make_repository_file(app_name)

    
    print ("\n\n\nCheck Deploy descriptor file & Repository...")
    
    


if __name__ == "__main__" :
    main()
    
    
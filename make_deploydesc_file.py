# -*- coding: utf8 -*-

import os
import shutil
import sys
import time
import deploydesc_class 
import deploydesc_staging_class 


deploy_app_list= [

                'doc-api',          
                'erp',
#                 'erp-se',       # tag name = deploy : erp-se
                'inseed',
                'insolver',
                'jain',
                'midasinsight',
                'mit-api',
                'mmsw',
                'mrs',
                'mrs-app',
                'mrs-bigfile',
#                 'mrs-se',              # tag name = deploy : mrs-se
                'product-site',
                'web',
                ]



PRODUCTION_DEPLOY_BUCKET_PATH = 'D:\\02_Workspace\\AWS\\Deploy_S3_bucket'
STAGING_DEPLOY_BUCKET_PATH = 'D:\\02_Workspace\\AWS\\Deploy_S3_bucket_staging'
PR_BUCKET_NAME = 'midasit-pr-s3-deployment'
ST_BUCKET_NAME = 'midasit-st-s3-deployment'

DEPLOY_TARGET = 'staging'     # or 'production' 

if __name__ == "__main__" :
    
    if DEPLOY_TARGET is 'staging':
        shutil.rmtree(STAGING_DEPLOY_BUCKET_PATH+'\\deployment-descriptor\\',True)
        deploy = deploydesc_staging_class.DeployDescStaging( STAGING_DEPLOY_BUCKET_PATH, ST_BUCKET_NAME )
        for app_name in deploy_app_list:
            deploy.make_desc_zip_file(app_name)
        
    
    elif DEPLOY_TARGET is 'production':
        shutil.rmtree(PRODUCTION_DEPLOY_BUCKET_PATH+'\\deployment-descriptor\\',True)
        
        deploy = deploydesc_class.DeployDesc( PRODUCTION_DEPLOY_BUCKET_PATH, PR_BUCKET_NAME )
 
        
        for app_name in deploy_app_list:
            deploy.make_desc_zip_file(app_name)    

        
        
    #
# -*- coding: utf8 -*-

import boto3
import os, sys, time, shutil
import zipfile
import deploydesc_class


class DeployDescStaging(deploydesc_class.DeployDesc):
#variable
    repository_path = ''
    
#initialize
    def __init__(self, _root_dir ,_bucket_name, _platform = 'windows' ):
       
        parent_class = super(DeployDescStaging, self)
        parent_class.__init__( _root_dir , _bucket_name, _platform)
    
#method    
    def set_app_name (self, _app_name):
        
        parent_class = super(DeployDescStaging, self)
        parent_class.set_app_name( _app_name)
       
    def make_yml_file(self):     
               
        with open(self.yml_file_path  ,'w', newline='\n') as f:
            f.write("version: 0.0\n")
            f.write("os: linux\n")
            f.write("files:\n")
            f.write("hooks:\n")
            f.write("  BeforeInstall:\n")
            f.write("    - location: scripts/install_dependencies\n")
            f.write("      timeout: 300\n")
            f.write("      runas: webuser\n")
            f.write("  ApplicationStart:\n")
            f.write("    - location: scripts/start_server\n")
            f.write("      timeout: 300\n")
            f.write("      runas: root\n")
            f.write("  ValidateService:\n")
            f.write("    - location: scripts/validate_service\n")
            f.write("      timeout: 600\n")
            f.write("      runas: root\n")
            
    def make_validate_service_file(self):
        app_list= [
                 {'name':'erp-se',          'http':'8342'  },
                 {'name':'mit-api',         'http':'8242' },
                 {'name':'doc-api',         'http':'8282' },
                 {'name':'inseed',           'http':'8172' },
                 {'name':'insolver',         'http':'8182'  },
                 {'name':'jain',               'http':'8262'  },
                 {'name':'midasinsight',  'http':'8222' },
                 {'name':'mit-job',          'http':'8442' },
                 {'name':'mmsw',           'http':'8232' },
                 {'name':'mrs-app',         'http':'8122'  },
                 {'name':'mrs-bigfile',     'http':'8162'  },
                 {'name':'mrs-se',           'http':'8132'  },
                 {'name':'product-site',    'http':'8212' },
                 {'name':'erp',                 'http':'8352'  },         
                 {'name':'mrs',                'http':'8112' },        
               ]
        
        
        
        app_info = None
        
        if self.app_name != 'web' :
            for app in app_list :
                if self.app_name == app['name'] : 
                    app_info = app;
                    break
            
            print(app_info)
            if app_info == None:
                print ('not find app info')
                return 
          
      
        with open(self.validate_service_file_path  ,'w', newline = '\n') as f:
            f.write('#!/usr/bin/env python')
            f.write('\n')
                
            if self.app_name != 'web' :
                f.write("import os, time, sys, subprocess \n")
                
                f.write("cnt = 0\n")
                f.write("while(1):\n")
     
                f.write("    if( os.popen('curl -iksL  127.0.0.1:"+app_info['http']+"/health.html |grep \"HTTP/1.1 200\" |wc -l').read() == '1\\n' ): \n")
                f.write("        break\n")
                f.write("    time.sleep(1)\n")
                f.write("    if(cnt == 500 ):\n")
                f.write('        raise AssertionErrorFail ("Fail- heatcheck.html  ["+res+"]" )\n')
               
                f.write("        break\n")
                f.write("    cnt +=1\n")               

    
    def make_start_server_file(self):
      
        with open(self.start_server_file_path  ,'w', newline = '\n') as f:
            f.write('#!/usr/bin/env python\n')
            f.write('\n')
            f.write("import os, time \n")
          
            if self.app_name != 'web' :
                f.write("os.system ('service tomcat-"+self.app_name+" start > /dev/null 2> /dev/null < /dev/null ')\n")
                f.write('\n')

       

                
    def make_install_dependencies_file(self):
               
        with open(self.install_dependencies_file_path ,'w', newline = '\n') as f:

            f.write('#!/usr/bin/env python\n')
            f.write('\n')
            f.write("import os, time, sys, subprocess \n")
 
            
            if self.app_name != 'web' :
                
                f.write("os.system ('service tomcat-"+self.app_name+" stop > /dev/null 2> /dev/null < /dev/null ')\n")
                f.write("time.sleep(1)\n")
                f.write("os.system ('rm -rf /data/inst/src/"+self.app_name+"/ROOT.war') \n")
                f.write("os.system ('rm -rf /data/inst/tomcat_webapp/"+self.app_name+"/ROOT')  \n")
                f.write("os.system ('rm -rf /data/inst/src_properties/"+self.app_name+"/*') \n")
                f.write("os.system ('aws s3 cp --region ap-northeast-2  s3://midasit-st-s3-deployment/src/"+self.app_name+"/ROOT.war /data/inst/src/"+self.app_name+"/ROOT.war 2> /data/inst/codedeploy/beforeinstall.log') \n")
                f.write("os.system ('aws s3 cp --region ap-northeast-2  s3://midasit-st-s3-deployment/src_properties/"+self.app_name+"  /data/inst/src_properties/"+self.app_name+"/ --recursive') \n")
                f.write("time.sleep(2)\n")

                

 
 
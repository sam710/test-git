# -*- coding: utf8 -*-
import boto3
import os, sys, time, shutil
import zipfile


class DeployDesc:
#variable
    root_dir =''
    iterator = ''
    app_name = ''
 #   s3obj = ''#boto3.resource('s3')
 #   bucket = ''#boto3.s3.bucket()
    bucket_name=''
    yml_file_path = ''
    start_server_file_path = ''
    stop_server_file_path = ''
    install_dependencies_file_path = ''
    desc_zip_file_path = ''
    validate_service_file_path = ''
    
#initialize
    def __init__(self, _root_dir ,_bucket_name, _platform = 'windows' ):
        if(_platform == 'windows'):
            self.iterator ='\\'
        else: 
            self.iterator ='/'
            
        self.root_dir = _root_dir
        self.bucket_name = _bucket_name
  
    
#method    
    def set_app_name (self, _app_name):
        self.app_name = _app_name
        
        desc_path = self.root_dir+self.iterator+'deployment-descriptor'+self.iterator+self.app_name
        script_path = desc_path+self.iterator+'scripts'
        
        self.yml_file_path = desc_path + self.iterator+'appspec.yml'
        self.start_server_file_path = script_path+self.iterator+'start_server'
        self.stop_server_file_path = script_path+self.iterator+'stop_server'
        self.install_dependencies_file_path = script_path+self.iterator+'install_dependencies'
        self.validate_service_file_path = script_path+self.iterator+'validate_service'
        self.desc_zip_file_path =  desc_path+self.iterator+self.app_name+'.zip'
        print(self.yml_file_path)
        print(self.start_server_file_path)
#         print(self.stop_server_file_path)
        print(self.install_dependencies_file_path)
        print(self.validate_service_file_path)
        print(self.desc_zip_file_path)  
        
        
        #windows.. error...
       # print(self.root_dir+self.iterator+'deployment-descriptor')
        if not os.path.isdir(self.root_dir):
            os.mkdir(self.root_dir)

        time.sleep(1) 
        if not os.path.isdir(self.root_dir+self.iterator+'deployment-descriptor'):
            os.mkdir(self.root_dir+self.iterator+'deployment-descriptor')
             
        time.sleep(0.1)
        if not os.path.isdir(desc_path):
            os.mkdir(desc_path)
            
        time.sleep(0.1)     
        if not os.path.isdir(script_path):
            os.mkdir(script_path) 
        time.sleep(0.1)    
      
    def make_desc_zip_file(self, _app_name ):
        self.set_app_name(_app_name)
        
        self.make_yml_file()
        self.make_start_server_file()
        self.make_install_dependencies_file()
        self.make_validate_service_file()
        
        print('make desc files')
        
        desc_zip_file = zipfile.ZipFile( self.desc_zip_file_path  , 'w')
        desc_zip_file.write( self.yml_file_path , 'appspec.yml',  compress_type=zipfile.ZIP_DEFLATED )
        desc_zip_file.write( self.start_server_file_path ,'scripts/start_server' ,compress_type=zipfile.ZIP_DEFLATED )
        desc_zip_file.write( self.install_dependencies_file_path , 'scripts/install_dependencies'  ,compress_type=zipfile.ZIP_DEFLATED )
        desc_zip_file.write( self.validate_service_file_path , 'scripts/validate_service'  ,compress_type=zipfile.ZIP_DEFLATED )
           
        desc_zip_file.close()
      
        time.sleep(0.2) 
        
        #upload S3
        s3obj = boto3.resource('s3')
        bucket = s3obj.Bucket( self.bucket_name )
        bucket.upload_file( self.desc_zip_file_path, 'deployment-descriptor/'+_app_name+'/'+_app_name+'.zip' )
       
        print ('\nmake '+_app_name+'.zip file to /deployment-descriptor/'+_app_name+'/'+_app_name+'.zip')
        
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
  
  
                f.write("def is_service_running(name):\n")
                f.write("    with open(os.devnull, 'wb') as hide_output:\n")
                f.write("        exit_code = subprocess.Popen(['service', name, 'status'], stdout=hide_output, stderr=hide_output).wait()\n")
                f.write("        return exit_code == 0\n\n\n")
   
                    
                f.write("if ( is_service_running('zabbix-agent')==False ):\n")
                f.write("    os.system ('service zabbix-agent start')\n")
                f.write("    time.sleep(2)\n") 
                f.write("    if ( is_service_running('zabbix-agent')==False ):\n")
                f.write("        raise AssertionError('Fail - zabbix-agnet is not running')\n\n\n")
                
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
          
# zabbix agent conf (az)
            f.write("process = os.popen('wget -q -O - http://169.254.169.254/latest/meta-data/placement/availability-zone') \n")
            f.write("region = process.read() \n")
            f.write("process.close() \n")

            f.write("if( region == 'ap-northeast-2c' ):\n")
            f.write("    os.system(\"sed -i 's/Server=10.0.6.218/Server=10.0.141.142/g' /etc/zabbix/zabbix_agentd.conf\")\n")
            f.write("    os.system(\"sed -i 's/ServerActive=10.0.6.218/ServerActive=10.0.141.142/g' /etc/zabbix/zabbix_agentd.conf\")\n")
   
            
            f.write("    os.system ('service zabbix-agent restart')\n")
            f.write("    time.sleep(2)\n")
            
            if self.app_name != 'web' :
                f.write("os.system ('service tomcat-"+self.app_name+" start > /dev/null 2> /dev/null < /dev/null ')\n")
                f.write('\n')

       

                
    def make_install_dependencies_file(self):
               
        with open(self.install_dependencies_file_path ,'w', newline = '\n') as f:

            f.write('#!/usr/bin/env python\n')
            f.write('\n')
            f.write("import os, time, sys, subprocess \n")
 
            f.write("def make_log_file(_file_name, _file_contents):\n")
            f.write("    f = open('/data/inst/codedeploy/'+_file_name  ,'w')\n")
            f.write("    f.write(_file_contents)\n")
            f.write("    f.close()\n\n\n")            
            f.write("def is_service_running(name):\n")
            f.write("    with open(os.devnull, 'wb') as hide_output:\n")
            f.write("        exit_code = subprocess.Popen(['service', name, 'status'], stdout=hide_output, stderr=hide_output).wait()\n")
            f.write("        return exit_code == 0\n\n\n")
             
            f.write("def is_tomcat_running ( ):\n")
            f.write("    popen = subprocess.Popen('service tomcat-"+self.app_name+" status', stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)\n")
            f.write("    (stdoutdata, stderrdata) = popen.communicate()\n")
            f.write("    return stderrdata\n")
            
            
#             f.write("os.system ('service zabbix-agent stop')\n")
            
            if self.app_name != 'web' :
                
                f.write("os.system ('service tomcat-"+self.app_name+" stop > /dev/null 2> /dev/null < /dev/null ')\n")
#                f.write("make_log_file('server_stop_event11',  is_tomcat_running ( )) \n")
                f.write("time.sleep(1)\n")
#                f.write("make_log_file('server_stop_event22',  is_tomcat_running ( )) \n")

                f.write("os.system ('rm -rf /data/inst/src/"+self.app_name+"/ROOT.war') \n")
                f.write("os.system ('rm -rf /data/inst/tomcat_webapp/"+self.app_name+"/ROOT')  \n")
                f.write("os.system ('rm -rf /data/inst/src_properties/"+self.app_name+"/*') \n")
                f.write("os.system ('aws s3 cp --region ap-northeast-2  s3://midasit-st-s3-deployment/src/"+self.app_name+"/ROOT.war /data/inst/src/"+self.app_name+"/ROOT.war 2> /data/inst/codedeploy/beforeinstall.log') \n")
                f.write("os.system ('aws s3 cp --region ap-northeast-2  s3://midasit-st-s3-deployment/src_properties/"+self.app_name+"  /data/inst/src_properties/"+self.app_name+"/ --recursive') \n")
#                 f.write('[ -f "/data/inst/src/${APP_NAME}/ROOT.war" ] && echo "The file exists" > /data/inst/codedeploy/test1.log || echo "The file does not exist" > /data/inst/codedeploy/test1.log\n')
                f.write("time.sleep(2)\n")
    #                 f.write('[ -f "/data/inst/src/${APP_NAME}/ROOT.war" ] && echo "The file exists" > /data/inst/codedeploy/test2.log || echo "The file does not exist" > /data/inst/codedeploy/test2.log\n')
                

 
 



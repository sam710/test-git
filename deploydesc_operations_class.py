# -*- coding: utf8 -*-

import boto3
import os, sys, time, shutil
import zipfile
import deploydesc_class


class DeployDescOperations(deploydesc_class.DeployDesc):
#variable
    repository_path = ''
    
#initialize
    def __init__(self, _root_dir ,_bucket_name, _platform = 'windows' ):
       
        parent_class = super(DeployDescOperations, self)
        parent_class.__init__( _root_dir , _bucket_name, _platform)
    
#method    
    def set_app_name (self, _app_name):
        
        parent_class = super(DeployDescOperations, self)
        parent_class.set_app_name( _app_name)
   
        ##############  operations 
        self.repository_path = self.root_dir+self.iterator+'repository'+self.iterator+self.app_name #######
                    
        if not os.path.isdir(self.root_dir+self.iterator+'repository'):
            os.mkdir(self.root_dir+self.iterator+'repository') 
        time.sleep(0.1)   
        
        if not os.path.isdir(self.repository_path):
            os.mkdir(self.repository_path)      
      
    def make_desc_zip_file(self, _app_name ):
        self.set_app_name(_app_name)
        
        self.make_yml_file()
        self.make_start_server_file()
        self.make_install_dependencies_file()
 #       self.make_validate_service_file()
        
        print('make desc files')
        
        desc_zip_file = zipfile.ZipFile( self.desc_zip_file_path  , 'w')
        desc_zip_file.write( self.yml_file_path , 'appspec.yml',  compress_type=zipfile.ZIP_DEFLATED )
        desc_zip_file.write( self.start_server_file_path ,'scripts/start_server' ,compress_type=zipfile.ZIP_DEFLATED )
        desc_zip_file.write( self.install_dependencies_file_path , 'scripts/install_dependencies'  ,compress_type=zipfile.ZIP_DEFLATED )
    #    desc_zip_file.write( self.validate_service_file_path , 'scripts/validate_service'  ,compress_type=zipfile.ZIP_DEFLATED )
           
        desc_zip_file.close()
      
        time.sleep(0.2) 
        
        #upload S3
        s3obj = boto3.resource('s3')
        bucket = s3obj.Bucket( self.bucket_name )
        bucket.upload_file( self.desc_zip_file_path, 'deployment-descriptor/'+_app_name+'/'+_app_name+'.zip' )
       
        print ('\nmake '+_app_name+'.zip file to /deployment-descriptor/'+_app_name+'/'+_app_name+'.zip')
        
                        
    def make_repository_file(self, _app_name ):
        self.set_app_name(_app_name)
        
#         self.make_zabbix_agent_file('a')
#         self.make_zabbix_agent_file('c')
        
        self.make_was_healthcheck_file()
        self.make_userparameter_file()
        
        self.make_was_heapdump_file()
        
        self.make_linux_external_file()
        self.make_userparameter_linux_file()
        
        #upload S3
        s3obj = boto3.resource('s3')
        bucket = s3obj.Bucket( self.bucket_name )
        

        
        bucket.upload_file(self.repository_path+self.iterator+'userparameter_tomcat.conf', 'repository/'+_app_name+'/userparameter_tomcat.conf' )
        print ('\nUpload '+self.repository_path+self.iterator+'userparameter_tomcat.conf  file to /repository/'+_app_name+'/userparameter_tomcat.conf' )
        time.sleep(0.1)
        bucket.upload_file(self.repository_path+self.iterator+'was_healthcheck.py', 'repository/'+_app_name+'/was_healthcheck.py')
        print ('\nUpload '+self.repository_path+self.iterator+'was_healthcheck.py  file to /repository/'+_app_name+'/was_healthcheck.py' )

        time.sleep(0.1)
        bucket.upload_file(self.repository_path+self.iterator+'was_heapdump.py', 'repository/'+_app_name+'/was_heapdump.py')
        print ('\nUpload '+self.repository_path+self.iterator+'was_heapdump.py  file to /repository/'+_app_name+'/was_heapdump.py' )
    
        time.sleep(0.1)

        bucket.upload_file(self.repository_path+self.iterator+'userparameter_linux.conf', 'repository/'+_app_name+'/userparameter_linux.conf' )
        print ('\nUpload '+self.repository_path+self.iterator+'userparameter_linux.conf  file to /repository/'+_app_name+'/userparameter_linux.conf' )
        time.sleep(0.1)
         
        bucket.upload_file(self.repository_path+self.iterator+'linux_external.py', 'repository/'+_app_name+'/linux_external.py')
        print ('\nUpload '+self.repository_path+self.iterator+'linux_external.py  file to /repository/'+_app_name+'/linux_external.py' )
         
        
        

        
#         bucket.upload_file(self.repository_path+self.iterator+'zabbix_agentd_a.conf', 'repository/'+_app_name+'/zabbix_agentd_a.conf' )
#         print ('\nUpload '+self.repository_path+self.iterator+'zabbix_agentd_a.conf  file to /repository/'+_app_name+'/zabbix_agentd_a.conf' )
#         time.sleep(0.1)
#         bucket.upload_file(self.repository_path+self.iterator+'zabbix_agentd_c.conf', 'repository/'+_app_name+'/zabbix_agentd_c.conf')
#         print ('\nUpload '+self.repository_path+self.iterator+'zabbix_agentd_c.conf  file to /repository/'+_app_name+'/zabbix_agentd_c.conf' )
 
 
#         if ( self.make_tomcat_config_file() == True):
#             bucket.upload_file(self.repository_path+self.iterator+'setenv-custom.sh', 'repository/'+_app_name+'/setenv-custom.sh')
#             print ('\nUpload '+self.repository_path+self.iterator+'setenv-custom.sh  file to /repository/'+_app_name+'/setenv-custom.sh' )
#         else:
#             print('not make setenv-custom.sh')
 
                  
    def make_yml_file(self):     
               
        with open(self.yml_file_path  ,'w', newline='\n') as f:
            f.write("version: 0.0\n")
            f.write("os: linux\n")
            f.write("files:\n")
            f.write("hooks:\n")
            f.write("  BeforeInstall:\n")
            f.write("    - location: scripts/install_dependencies\n")
            f.write("      timeout: 300\n")
            f.write("      runas: root\n")
            f.write("  ApplicationStart:\n")
            f.write("    - location: scripts/start_server\n")
            f.write("      timeout: 300\n")
            f.write("      runas: root\n")
#             f.write("  ApplicationStop:\n")
#             f.write("    - location: scripts/stop_server\n")
#             f.write("      timeout: 300\n")
#             f.write("      runas: root\n")
    
    def make_start_server_file(self):
      
        with open(self.start_server_file_path  ,'w', newline = '\n') as f:
            f.write('#!/usr/bin/env python\n')
            f.write('\n')
            f.write("import os, time \n")
          
# zabbix agent conf (az)
            f.write("os.system ('service zabbix-agent stop')\n")

            
#             if self.app_name != 'web' :
#                 f.write("os.system ('service tomcat-"+self.app_name+" start > /dev/null 2> /dev/null < /dev/null ')\n")
#                 f.write('\n')

       
              
                
    def make_install_dependencies_file(self):
               
        with open(self.install_dependencies_file_path ,'w', newline = '\n') as f:
    
            f.write('#!/usr/bin/env python\n')
            f.write('\n')
            f.write("import os, time, sys, subprocess \n")
            f.write("os.system('mkdir /etc/zabbix/externalscripts')\n\n")
            f.write("os.system('rm -rf /etc/zabbix/zabbix_agentd.d/was_healthcheck.py')\n\n")
            f.write("os.system ('aws s3 cp --region ap-northeast-2  s3://"+self.bucket_name+"/repository/"+self.app_name+"/userparameter_tomcat.conf  /etc/zabbix/zabbix_agentd.d/userparameter_tomcat.conf') \n")
#             f.write("os.system ('aws s3 cp --region ap-northeast-2  s3://"+self.bucket_name+"/repository/"+self.app_name+"/was_healthcheck.py  /etc/zabbix/externalscripts/was_healthcheck.py') \n")
            f.write("os.system ('aws s3 cp --region ap-northeast-2  s3://"+self.bucket_name+"/repository/"+self.app_name+"/was_heapdump.py  /etc/zabbix/externalscripts/was_heapdump.py') \n")
            
#             f.write("os.system ('chmod 777  /etc/zabbix/externalscripts/was_healthcheck.py') \n")
            f.write("os.system ('chmod 777  /etc/zabbix/externalscripts/was_heapdump.py') \n")
            
#             f.write("os.system ('service zabbix-agent stop')\n")
            
#            if self.app_name != 'web' :

#             f.write("os.system ('aws s3 cp --region ap-northeast-2  s3://"+self.bucket_name+"/repository/"+self.app_name+"/userparameter_linux.conf  /etc/zabbix/zabbix_agentd.d/userparameter_linux.conf') \n")
#             f.write("os.system ('aws s3 cp --region ap-northeast-2  s3://"+self.bucket_name+"/repository/"+self.app_name+"/linux_external.py  /etc/zabbix/externalscripts/linux_external.py') \n")
#             
#             f.write("os.system ('chmod 777  /etc/zabbix/externalscripts/linux_external.py') \n")


#
            
            #/data/inst/tomcat/"+ self.app_name+"/cust/setenv-custom.sh
#             f.write('\n')
#             f.write("cp -rfa /data/inst/tomcat/"+ self.app_name+ "/cust/setenv-custom.sh /data/inst/tomcat/"+ self.app_name+"/cust/setenv-custom.sh_20170613")
#             f.write('\n')
#             #f.write("sed -i 's/tomcat_jdbc_url_prefix=jdbc:mysql:\/\/pr-rds-web-a1.cfrba7dflywv.ap-northeast-2.rds.amazonaws.com:3306/tomcat_jdbc_url_prefix=jdbc:mysql:\/\/st-rds-web-a1.cfrba7dflywv.ap-northeast-2.rds.amazonaws.com:3306/g' /data/inst/tomcat/"+ self.app_name+"/cust/setenv-custom.sh")
#             f.write("sed -i 's/redis_session_host=pr-elc-redis3.iqky1i.0001.apn2.cache.amazonaws.com/redis_session_host=pr-elc-redis.iqky1i.ng.0001.apn2.cache.amazonaws.com/g' /data/inst/tomcat/"+ self.app_name+"/cust/setenv-custom.sh")
#             f.write('\n')
            


    def make_userparameter_file(self):
        with open(self.repository_path+self.iterator+'userparameter_tomcat.conf', 'w', newline = '\n') as f:
            f.write("UserParameter=was.healthcheck[*],/etc/zabbix/externalscripts/was_healthcheck.py $1\n")
            f.write("UserParameter=was.heapdump,/etc/zabbix/externalscripts/was_heapdump.py \n")


    def make_userparameter_linux_file(self):
        with open(self.repository_path+self.iterator+'userparameter_linux.conf', 'w', newline = '\n') as f:
            f.write("UserParameter=linux.tcpcount,/etc/zabbix/externalscripts/linux_external.py\n")


    def make_linux_external_file(self):
        with open(self.repository_path+self.iterator+'linux_external.py', 'w', newline = '\n') as f:
            f.write("#!/usr/bin/env python\n")
            f.write("import os, sys\n\n")
            
            f.write("if __name__ == '__main__':\n")
            f.write("    count = int(os.popen('netstat -ant  |wc -l').read())\n")
            f.write("    print(count)\n")
            


    def make_was_heapdump_file(self):
        with open(self.repository_path+self.iterator+'was_heapdump.py', 'w', newline = '\n') as f:
            f.write("#!/usr/bin/env python\n")
            f.write("import os, sys\n\n")
            
            f.write("if __name__ == '__main__':\n")
            f.write("    count = int(os.popen('find /data/log -name \"java_pid*.hprof\" | wc -l').read())\n")
            f.write("    print(count)\n")
    
    def make_was_healthcheck_file(self):
        with open(self.repository_path+self.iterator+'was_healthcheck.py', 'w', newline = '\n') as f:
            f.write("#!/usr/bin/env python\n")
            f.write("import os, sys\n\n")
            
            f.write("if __name__ == '__main__':\n")
            
            f.write("    port = sys.argv[1]\n")
            
            f.write("    if(os.popen('curl -iksL  127.0.0.1:'+port+'/health.html |grep \"HTTP/1.1 200\" |wc -l').read() == '1\\n' ):\n")
            f.write("        print('1')\n")
            f.write("    else:\n")
            f.write("        print('0')\n") 
            
            
            
    def make_zabbix_agent_file(self,_zone):
        
        HostnameItem = 'HostnameItem=system.run[echo "pr-'+self.app_name+'-"$(wget -qO- http://instance-data/latest/meta-data/local-ipv4)]'
        HostMetadata=''
        ProxyServerIP =''
        if(self.app_name == 'mrs'):
            HostMetadata='HostMetadata=linux-was-mrs-root'
        elif(self.app_name == 'erp'):
            HostMetadata='HostMetadata=linux-was-erp-root'
        elif(self.app_name == 'web'):
            HostMetadata='HostMetadata=linux'
        else:
            HostMetadata='HostMetadata=linux-was'
            
        if(_zone == 'a'):
            ProxyServerIP = '10.0.141.142'
        else:
            ProxyServerIP = '10.0.6.218'
        
        with open(self.repository_path+self.iterator+'zabbix_agentd_'+_zone+'.conf', 'w', newline = '\n') as f:
            print ( 'make ' +self.repository_path+self.iterator+'zabbix_agentd_'+_zone+'.conf')
            f.write("PidFile=/var/run/zabbix/zabbix_agentd.pid\n")
            f.write("LogFile=/var/log/zabbix/zabbix_agentd.log\n")
            f.write("LogFileSize=0\n")
            f.write("EnableRemoteCommands=0\n")
            f.write("LogRemoteCommands=0\n")
            
            f.write("Server="+ProxyServerIP+"\n")
            f.write("ListenPort=10050\n")
            f.write("ServerActive="+ProxyServerIP+"\n")
            
            f.write(HostnameItem)
            f.write("\n")
            f.write(HostMetadata)
            f.write("\n")
            
            f.write("RefreshActiveChecks=60\n")
            f.write("Timeout=30\n")
            f.write("Include=/etc/zabbix/zabbix_agentd.d/\n")
                
        
    def make_tomcat_config_file(self):
        app_list= [
                 {'name':'erp-se',          'jmx':'8348' , 'http':'8342' , 'shutdown':  '8341' },
                 {'name':'mit-api',         'jmx':'8248' , 'http':'8242' , 'shutdown':  '8241' },
                 {'name':'doc-api',         'jmx':'8288' , 'http':'8282' , 'shutdown':  '8281' },
                 {'name':'inseed',          'jmx':'8178' , 'http':'8172' , 'shutdown':  '8171' },
                 {'name':'insolver',        'jmx':'8188' , 'http':'8182' , 'shutdown':  '8181' },
                 {'name':'jain',              'jmx':'8268' , 'http':'8262' , 'shutdown':  '8261' },
                 {'name':'midasinsight', 'jmx':'8228' , 'http':'8222' , 'shutdown':  '8221' },
                 {'name':'mit-job',         'jmx':'8448' , 'http':'8442' , 'shutdown':  '8441' },
                 {'name':'mmsw',          'jmx':'8238' , 'http':'8232' , 'shutdown':  '8231' },
                 {'name':'mrs-app',        'jmx':'8128' , 'http':'8122' , 'shutdown':  '8121' },
                 {'name':'mrs-bigfile',    'jmx':'8168' , 'http':'8162' , 'shutdown':  '8161' },
                 {'name':'mrs-se',          'jmx':'8138' , 'http':'8132' , 'shutdown':  '8131' },
                 {'name':'product-site',   'jmx':'8218' , 'http':'8212' , 'shutdown':  '8211' },
                 {'name':'erp',                'jmx':'8358' , 'http':'8352' , 'shutdown':  '8351' },         
                 {'name':'mrs',               'jmx':'8118' , 'http':'8112' , 'shutdown':  '8111' },        
               ]
        app_info = None
        for app in app_list :
            print('app name = '+app['name'])
            if self.app_name == app['name'] : 
                app_info = app;
                break
        
        print(app_info)
        if app_info == None:
            print ('not find app info')
            return False
        
        
        with open(self.repository_path+self.iterator+'setenv-custom.sh', 'w', newline = '\n') as f: 
            f.write("################################ for instance\n")           
            f.write("INST_GROUP_NAME="+self.app_name+"\n")           
            f.write("TOMCAT_INST_NAME=${INST_GROUP_NAME}\n")           
            f.write("TOMCAT_SHUTDOWN_PORT="+app_info['shutdown']+ "\n")           
            f.write("\n")           
            f.write("\n")           
            f.write("################################ for web\n")           
            f.write("## TOMCAT_SESSION_TIMEOUT=30\n")           
            f.write("## TOMCAT_MAX_POSTSIZE=2097152\n")           
            f.write("## TOMCAT_SESSION_COOKIENAME=JSESSIONID\n")           
            f.write("\n")           
            f.write("\n")           
            f.write("################################ for temp\n")           
            f.write("## DATA_HOME=/data\n")           
            f.write("## JAVA_HOME=${DATA_HOME}inst/java/jdk\n")           
            f.write("## JAVA_Xms=128m\n")           
            f.write("JAVA_Xmx=1024m\n")           
            f.write("\n")           
            f.write("\n")     
            f.write("################################ for datasource\n")           
            f.write("master_jdbc_url=pr-rds-web-a1.cfrba7dflywv.ap-northeast-2.rds.amazonaws.com:3306\n")           
            f.write("master_jdbc_username=jain\n")           
            f.write("## master_jdbc_maxActive=200\n")           
            f.write("## master_jdbc_minIdle=0\n")           
            f.write("\n")           
            f.write("\n")           
            f.write("################################ for monitoring\n")           
            f.write("PINPOINT_AGENT_ENABLE=true\n")           
            f.write("## JMXREMOTE_ADDRESS=125.141.205.101\n")           
            f.write("\n")           
            f.write("\n")           
            f.write("################################ for use gui\n")           
            f.write('## JAVA_OPTS="$JAVA_OPTS -Djava.awt.headless=true"\n')           
            f.write("\n")           
            f.write("\n")           
            f.write("################################ for session\n")           
            f.write("redis_session_host=pr-elc-redis3.iqky1i.0001.apn2.cache.amazonaws.com\n")           
            f.write("redis_session_port=6379\n")           
            f.write("redis_session_database=0\n")           
            f.write("## default: 1800 sec\n")           
            f.write("## redis_session_timeout=1800\n")           
            f.write("\n")           
            f.write("\n")           
            f.write("################################ for app\n")           
            f.write("## attach file root path (bucket name for S3)\n")           
            f.write("APP_ATTACHFILE_DIR=midasit-pr-s3-attachfile\n")           

        return True




























































    
    

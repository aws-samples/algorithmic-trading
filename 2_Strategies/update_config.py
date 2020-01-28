# Update configurations
import json
import sys
import boto3
import sagemaker as sage

sess = sage.Session()

algo_name=sys.argv[1]
conf_file='local/'+algo_name+'/input/config/hyperparameters.json'
with open(conf_file, 'r') as f:
    config = json.load(f)

config["algo_name"]=algo_name    

account=boto3.client('sts').get_caller_identity().get('Account')

if 'user' not in config:
    config['user']='user'
config["account"] = account
config["region"]=sess.boto_session.region_name

#try:
#    s3 = boto3.client('s3')
#    s3.download_file('', 'algo_event.config', 'algo_event.config')
#    with open('algo_event.config', 'r') as f:
#        event_config = json.load(f)
#    config['submitUrl']=event_config['submitUrl']
#except:
#  print("Skipped event config") 
    
with open(conf_file, "w") as text_file:
    text_file.write(json.dumps(config))    

print("config=%s" % json.dumps(config))
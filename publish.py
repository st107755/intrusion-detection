import os
### Build Container ###
os.system('docker build -t ddos-setup ./data/.')
os.system('docker build -t ddos-api ./api/.')
### Find Container ID ###
latest_api_id = os.popen('docker images ddos-api -q').read().strip()
latest_db_setup_id = os.popen('docker images ddos-setup -q').read().strip()
### Tag Container ###
# print('docker tag {} primefactor/ddos-api:latest'.format(latest_api_id))
os.system('docker tag  {} primefactor/ddos-api:latest'.format(latest_api_id))
os.system("docker tag {} primefactor/ddos-setup:latest".format(latest_db_setup_id))
### Push to Dockerhub ###
os.system("docker push primefactor/ddos-api:latest")
os.system("docker push primefactor/ddos-setup:latest")
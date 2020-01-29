###############################
Preparation of Dev environment
###############################

Clone the Git repository

go into the directory W4S/app

Create the Virtual Environment
python -m venv venv

Activate the Virtual Environment

Windows
W4S/app/venv/script/activate.ps1

Linux
source ./W4S/app/venv/bin/activate

Install requirements

pip install -r requirements.txt

########################
Configure the AWS CLI
########################

aws configure --profile w4suser                                                                                                                                                
AWS Access Key ID [None]: dummy
AWS Secret Access Key [None]: dummy
Default region name [None]: eu-west-1
Default output format [None]:

########################################
Create Docker image fro th eapplication
########################################

If you cahnge the code then you will have to create a new Docker image.

run th efollowing command and use the appropriate versioning (in the example you would change v1 with the appropriat everison):

docker build -t w4stest:v1 .

#####################################
Run the contenerised environment
#####################################

Change this section of th edocker-compose.yml to point to th eright version of the app (in th ebelow change v3 with the appropriate version):

w4stest:
      image: w4stest:v3

docker-compose up

Test DynamoDB Local via AWS CLI

aws dynamodb list-tables --endpoint-url http://localhost:8000 --profile w4suser

#############################
Clean up
#############################

stop docker-compose

Run the following command to remove all suspended containers:

docker rm $(docker ps -a -q)

##############################
Other notes
##############################

docker run -e AWS_ACCESS_KEY_ID='dummy' -e AWS_SECRET_ACCESS_KEY='dummy' -e AWS_REGION='eu-west-1' --name testpy -d -p 5000:5000 w4stest:v3

docker run -it --rm \

aws dynamodb list-tables --endpoint-url http://localhost:8000 --profile w4suser

docker run --name dynamodb -d -p 8000:8000 amazon/dynamodb-local:latest

once th econtainer is running, test with th efollowing:

aws dynamodb list-tables --endpoint-url http://localhost:8000

Found this issue on Windows: https://github.com/boto/boto3/issues/1238

Build your application container

docker build -t w4stest:v1 .

run it

docker run --name w4stest1 -d -p 8088:5000 w4stest:v1
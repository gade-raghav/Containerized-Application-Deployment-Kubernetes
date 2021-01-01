# Auto scalable containerized application deployment in kubernetes cluster with backend data base integration

## Project description

This project aims to deploy auto scalable HTML containerized application in kubernetes cluster with backend data base integration. This is demostrated by deploying
django application on kubernetes with mysql database in backend. 


GitHub repo link: https://github.com/gade-raghav/kubernetes-assignment/

### The project has been divided into 6 steps:
#### Step 1 : Creating a Django web-application which adds Employee ID and Employee name in Mysql database
#### Step 2 : Dockering the web-application and pushing it to Docker Hub
#### Step 3 : Installing microk8s on your laptop/desktop (Addition step : Installing Lens which is Kubernetes IDE for DEVOPS) 
#### Step 4 : Creating helm chart to install application (with auto scaling) + database deployed
#### Step 5 : Deploy ingress nginx controller to do loadbalancing between multiple application container pods.
#### Step 6 : Configure nginx ingress controller with SSL certificate (Yet to be configured)

## Pre-requisites
Operating System: Ubuntu 18.04 LTE

### Let's execute the above mentioned steps in sequence :

## 1. Creating a Django web-application which adds Employee ID and Employee name in Mysql database

The application's requriement is to use a form to take Employee ID and Employee Name and store it in Mysql. User Authentication has been added further to ensure 
only authenticated users can add employee details to the database.

This has been achieved using a Django web-application. Code has been pushed to GitHub repository (GitHub Link for repository is mentioned above).

By default Django applications are connected to sqlite database, however, we have made changes in settings.py[https://github.com/gade-raghav/kubernetes-assignment/blob/master/employeedb/settings.py] to connect it to Mysql Database which is deployed directly in kubernetes using helm charts.

Our application :

![](/images/home.png)
![](/images/login.png)
![](/images/form.png)

**Note**: This documentation does not focus on creating the web-application and is more focused on deploying it to Kubernetes. However, detailed explination can be provided during technical discussion.

## 2. Dockering the web-application and pushing it to Docker Hub

Docker is a set of platform as a service products that use OS-level virtualization to deliver software in packages called containers.

Docker Hub is a cloud-based repository in which Docker users and partners create, test, store and distribute container images.

In this step we will dockerize the application.

So let's start our dive into Docker.

**Writing Dockerfile**

Docker works using Dockerfile, a file which specifies how Docker is supposed to build your application.
It contains the steps Docker is supposed to follow to package your app. Once that is done, you can send this packaged app to anyone and they can run it on their system with no problems.


![Dockerfile](/images/Dockerfile.png)

Dockerfile starts with a base image that decides on which image your app should be built upon. Basically "Images" are nothing but apps.

We want to run our application on Python, So we'll use python:3.6 as the base image.

ENV creates an environment variable called PYTHONUNBUFFERED and sets it to 1 (which, remember, is “truthy”). All together, this statement means that Docker won't buffer the output from your application; instead, you will get to see your output in your console the way you're used to.

RUN is a Docker command which instructs to run something on the shell. Here we'll use this several time for the following tasks
- mkdir to make a new directory
- apt-get update to update package list and install vim incase you need to edit files inside the container later.
- pip install -r requirements to install all the necessary python packages for our application to work.


The next thing you will want to do now is to put your application inside the container which can be achieved by ADD/COPY command. 

The EXPOSE instruction informs Docker that the container listens on the specified network ports at runtime. You can specify whether the port listens on TCP or UDP, and the default is TCP if the protocol is not specified. Since all Django application by-default runs on port 8000, we will expose that port.

The last thing remaining now is to run your app. With this, your Dockerfile is complete.
The CMD command specifies the instruction that is to be executed when a Docker container starts. In our case we need to run the application which is achieved by
*python manage.py runserver 0.0.0.0:8000*

**Building the app**

To build the app run the following command.

` docker build -t raghavgade/ems . `

You need to add a dot , which means to use the Dockerfile in the local directory.

**Run the app**

After the build is *successful* you can run the application using the following command.

` docker run raghavgade/ems `

However, our main aim is to deploy the applicaiton on kubernetes and hence we will take it a step further and push the built image to Docker Hub.

**Push Docker image to Docker Hub**

Login from your console using the following command

` docker login `

After login, execute the following command to push (latest tag ensures that the last built version of the image is pushed)

` docker push raghavgade/ems:latest `

**With this step we have successfully dockerized our application and pushed it to Docker Hub**

## 3. Kubernetes Setup using [microk8s](https://microk8s.io/docs)

We need to set up Kubernetes and we are achieving that by using microk8s :

Install microk8s :

`sudo snap install microk8s --classic`

`sudo usermod -a -G microk8s $USER`

`sudo chown -f -R $USER ~/.kube`

This will give us Kubectl command-line tool and Kube config file.

Add an alias in .bashrc as follows to make things simpler:

`alias kubectl="microk8s.kubectl"`


Run `source .bashrc` after making changes to .bashrc file.

Incase the config file doesn't exist in ~/.kube directory follow the steps below

`
microk8s config > ~/.kube/config
`

Extra careful while giving read, write and execute permissions 

`chmod 700 ~/.kube/config`

Now let's run the Kubernetes cluster

`microk8s start`

Check status using the following commands and make sure everything is running.

![microk8s status](/images/microk8sstatus.png)

`kubectl get nodes` (Check if the node is ready. We are using a single node.)

***Additional Step***

#### [Lens](https://k8slens.dev/) Setup:

Lens is an IDE for working Kubernetes clusters. The only system you'll ever need to take control of your Kubernetes clusters. You just need to pass in the kube config file and it takes care of the rest. (Makes visualizing clusters very simple)

[Installing Lens](https://github.com/lensapp/lens/releases/tag/v3.6.7)

I have downloaded the AppImage which is extremely easy to use. After download give executable permissions to file and run using the following command

`./Lens-3.6.6.AppImage`


Provide the path to Kubernetes config file and it gets all the information about the cluster.

## 4. Creating helm chart to install application (with auto scaling) + database deployed

[Helm](https://helm.sh/) Setup:

Helm is the Package Manager for Kubernetes. Helm is the best way to find, share, and use software built for Kubernetes.

[Installing helm](https://helm.sh/docs/intro/install/)

I prefer installing it from the script.

Helm now has an installer script that will automatically grab the latest version of Helm and install it locally.

Run the following commands:

`curl -fsSL -o get_helm.sh https://raw.githubusercontent.com/helm/helm/master/scripts/get-helm-3`

`chmod 700 get_helm.sh`

`./get_helm.sh`

There are couple approaches how to work with Helm. In this documentation we will demonstrate both the approaches.

- One of them is to download publicly available charts from the Helm Hub. They are prepared by community and are free to use.


We are going to set up Mysql database using this approach. [Artifact Hub](https://artifacthub.io/) has a lot of Kubernetes packages.
Search for the required package and it provides us with clear instructions about how to use it. We can also do it using the command line as follows.

Repo used for pulling mysql chart: stable (which is a default repo that is add when helm init is run)

Before deploying mysql to kubernetes we need to manage storage so that the data in pod is not lost.

Kubernetes has a solution for this. We need to create persistent volume and persistent volume claim.

**Persistent volume**

Persistent Volumes are simply a piece of storage in your cluster. Similar to how you have a disk resource in a server, a persistent volume provides storage resources for objects in the cluster. At the most simple terms you can think of a PV as a disk drive. It should be noted that this storage resource exists independently from any pods that may consume it. Meaning, that if the pod dies, the storage should remain intact assuming the claim policies are correct. 

This is our .yaml file that helps us to create a volume for mysql.

Command to create persistent volume:

` kubectl apply -f mysqldb-pv.yaml `

To view information about persistent volume:

` kubectl get pv `

![persistent volume](/images/pv.png)


**Persistent volume claim**

Pods that need access to persistent storage, obtain that access through the use of a Persistent Volume Claim. A PVC, binds a persistent volume to a pod that requested it.

When a pod wants access to a persistent disk, it will request access to the claim which will specify the size , access mode and/or storage classes that it will need from a Persistent Volume. Indirectly the pods get access to the PV, but only through the use of a PVC.

This is our .yaml file that helps us to create a persistent volume claim for the persistent volume we just created.

Command to create persistent volume claim:

` kubectl apply -f mysqldb-pvc.yaml `

To view information about persistent volume:

` kubectl get pvc `

![persistent volume claim](/images/pvc.png)

Now we have to make changes to stable/mysql chart

Use the following command to put the chart in a local file and then make changes.

`helm inspect values bitnami/parse >> mysql.values `

Change the following details in values chart:
- mysqlRootPassword
- mysqlUser
- mysqlPassword
- mysqlDatabase
- existingClaim (Pass pvc name which is mysql-pvc in our case and set persistence enabled value to "true")
- Change service type to nodeport and give a valid nodeport number (range 30000-32767). We are using nodeport as service type since we are running it in a local environment.

Let's deploy mysql db using the following commands

`helm install mysql stable/mysql --values mysql.values `

![mysql install](/images/mysql.png)

Wait for some time until mysql database is deployed. Check the status on Lens .

Now we need to follow the instructions provided on command line i.e to get the port numbers from services deployed.

Run the following commands

` MYSQL_HOST=$(kubectl get nodes --namespace default -o jsonpath='{.items[0].status.addresses[0].address}') `

` MYSQL_PORT=$(kubectl get svc --namespace default mysql -o jsonpath='{.spec.ports[0].nodePort}') `

MYSQL_HOST variable has the ip which we need to provide our web-application so that it can connect to the database.

MYSQL_PORT variable has the port number which we need to pass to our web-application.

To connect to your database directly from outside the K8s cluster use the following command after setting the required variable:

` mysql -h ${MYSQL_HOST} -P${MYSQL_PORT} -u root -p${MYSQL_ROOT_PASSWORD} ` 


***Lens IDE gives detailed view of the deployment and helps in monitoring the status ***

With this our mysql database has been successfully deployed.

We will now by using a different approach to deploy our Django web-application

- Our next approach allows us to create our own charts.

Command to create our own helm chart (django-helm is the name of the chart) :

` helm create django-helm `

This command creates a folder with a basic structure.

Now we will define necessary files to create chart.

Fundamentally there are four files required for our deployment which are placed in django-helm/templates directory
- deployment.yaml file

Scaling has been achieved using replicas. If any specific criteria is mentioned, autosacling can be applied to the deployment.
We have to mention the image name that is being pulled, Container port on which the application is running and all other necessary/required details.

![app deployment file](/images/deployment.png)

- service.yaml file

![service file](/images/service.png)

- ingress.yaml files

Since we are using ingress-nginx controller to do loadbalancing between multiple applications, we must have an ingress file.

![ingress file](/images/ingress.png)


Now use the following command to deploy our web-application using helm:

` helm install django ./django-helm/ `

![django install ](/images/djangoinstall.png)

**NOTE**: We need to set the following variable in settings.py file in the web application container for it to access our mysql database:

- NAME: 'ems', Database name we passed in mysql.values
- HOST: '192.168.43.243', MYSQL_HOST variable value we exported
- PORT: '32000', MYSQL_PORT variable values we exposed
- USER: 'root', user value in mysql.values  
- PASSWORD: 'rootpassword', rootpassword value in mysql.values
        
![Settings.py](/images/settings.png)

***We will discuss about ingress.yaml in next step as we need to enable ingress controller prior to our deployments***


## Step 5 : Deploy ingress nginx controller to do loadbalancing between multiple application container pods

Ingress exposes HTTP and HTTPS routes from outside the cluster to services within the cluster. Traffic routing is controlled by rules defined on the Ingress resource.

You must have an Ingress controller to satisfy an Ingress. Only creating an Ingress resource has no effect.

**Creating Ingress controller**

There are multiple ways to achieve this (helm,.yaml files etc) , however we will be doing it with just a command.

` microk8s enable ingress `

![ingress controller](/images/nginx.png)

**Creating Ingress resource for our web-application** 

The following is our ingress.yaml file:

![ingress file](/images/ingress.png)

Pass host name, path, service name of web application and port number.

This resource has already been created when we deployed our web application.

## Step 6 : Configure nginx ingress controller with SSL certificate 

This step is yet to be configured.































# Deploying the Blogger App in OpenShift

This document outlines the steps to deploy the Blogger App in OpenShift, including setting up the application, database, and initializing the database schema.

---

## Prerequisites
- OpenShift CLI (`oc`) installed and configured.
- Access to an OpenShift cluster.
- A Git repository containing the application code.

---

## Deployment Steps

### 1. Create a New Project
Create a new OpenShift project for the Blogger App:
```bash
oc new-project blogger-app
```

### 2. Deploy the Blogger App
Use the oc new-app command to build and deploy the application:
```bash
oc new-app --name=blogger-app https://github.com/lakshmanarao3/python_projects.git --context-dir=blogger_web
```
* This creates an image stream and builds the application image using the Docker strategy.

### 3.  Create a Service for the Blogger App
Define a service to expose the application internally:
Create a file named blogger_service.yml with the following content:
```yaml
apiVersion: v1
kind: Service
metadata:
  name: blogger-app
spec:
  selector:
    deployment: blogger-app
  ports:
  - protocol: TCP
    port: 8000
    targetPort: 8000
```

Apply the service configuration:
```bash
oc apply -f blogger_service.yml
```

### 4. Deploy the Database
Deploy a PostgreSQL database for the application:
```bash
oc new-app --name=db postgres:13 \
    -e POSTGRES_USER=flaskuser \
    -e POSTGRES_PASSWORD=flaskpassword \
    -e POSTGRES_DB=flaskdb
```

### 5. Grant Permissions
Allow the application to run as anyuid to avoid permission issues:
```bash
oc adm policy add-scc-to-user anyuid -z default -n blogger-app
```

### 6. Restart Deployments
Restart the deployments to ensure that the latest configurations are applied:
```bash
oc rollout restart deployment/blogger-app
oc rollout restart deployment/db
```

### 7. Initialize the Database
Login to the blogger-app pod to initialize the database schema:
  * Start a terminal session inside the pod:
    ```bash
    oc rsh <blogger-app-pod-name>
    ```
  * Run the Flask database migration commands:
    ```bash
    flask db init
    flask db migrate -m "initial"
    flask db upgrade
    ```

### 8. Expose the Application
Expose the service externally using a route:
```bash
oc expose svc/blogger-app
```
Retrieve the route URL:
```bash
oc get route blogger-app
```
Access the application in your browser using the route URL.





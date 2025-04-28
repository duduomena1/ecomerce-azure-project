docker build -t ecommerce:latest .

docker run -d -p 80:5108 --name ecommerce ecommerce:latest

az login

az group create --name containerslabs003 --location eastus

az acr create --resource-group containerslabs003 --name containerslabs003 --sku Basic

az acr login --name containerslabs003

docker tag ecommerce/azure:latest containerslabs003.azurecr.io/ecommerce:latest

docker push containerslabs003.azurecr.io/ecommerce:latest

az acr repository list --name containerslabs003 --output table

az containerapp env create --name ecommerce-env --resource-group containerslabs003 --location eastus

az containerapp create --name ecommerce-app --resource-group containerslabs003 --environment ecommerce-env --image containerslabs003.azurecr.io/ecommerce:latest --target-port 80 --ingress 'external' --registry-server containerslabs003.azurecr.io --registry-username containerslabs003 --registry-password +RQhcgxIwLp7XLQcbT7Ly7XQmrvv4hW3bkMCGE1AbR+ACRANI9zP
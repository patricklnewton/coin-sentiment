To run locally
docker build -t gathersentiment .
docker run -p 9000:8080 gathersentiment:latest
curl -XPOST "http://localhost:9000/2015-03-31/functions/function/invocations" -d '{}'

to push to ECR
docker build -t gathersentiment .
docker tag gathersentiment:latest 708357095774.dkr.ecr.us-east-1.amazonaws.com/gathersentiment:latest
docker push 708357095774.dkr.ecr.us-east-1.amazonaws.com/gathersentiment:latest

to run API locally
uvicorn api:app --reload
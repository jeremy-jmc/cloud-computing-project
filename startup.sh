docker compose -f /home/ubuntu/cloud-computing-project/docker-compose.yaml down || true
docker container prune -af
docker volume prune -af
docker compose -d -f /home/ubuntu/cloud-computing-project/docker-compose.yaml up --build
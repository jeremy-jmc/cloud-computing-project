docker compose -f /home/ubuntu/cloud-computing-project/docker-compose-bd.yaml down || true
docker container prune -af
docker volume prune -af
docker compose -f /home/ubuntu/cloud-computing-project/docker-compose-bd.yaml up -d --build
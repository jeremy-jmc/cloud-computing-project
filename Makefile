up:
	clear && docker compose up --build
api-logs:
	clear && docker compose logs -f api_membresias api_promociones api_clientes api_orquestador
occupied-ports:
# https://www.cyberciti.biz/faq/unix-linux-check-if-port-is-in-use-command/
	clear && sudo lsof -i -P -n | grep LISTEN
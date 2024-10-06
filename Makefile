up:
	clear && docker compose up --build
api-logs:
	clear && docker compose logs -f api_membresias api_promociones api_clientes api_orquestador
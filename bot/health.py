"""Health check endpoint for monitoring and load balancers."""

from __future__ import annotations

import json
import logging
from http.server import BaseHTTPRequestHandler, HTTPServer
from threading import Thread

LOGGER = logging.getLogger(__name__)


class HealthCheckHandler(BaseHTTPRequestHandler):
    """Simple HTTP handler for health check endpoint."""

    def do_GET(self) -> None:
        """Handle GET requests to /health endpoint."""
        if self.path == "/health":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            response = {"status": "ok", "service": "telegram-bot"}
            self.wfile.write(json.dumps(response).encode())
        else:
            self.send_response(404)
            self.end_headers()

    def log_message(self, format: str, *args) -> None:
        """Suppress default request logging."""
        pass


def start_health_server(port: int = 8080) -> None:
    """Start health check server in background thread."""
    server = HTTPServer(("0.0.0.0", port), HealthCheckHandler)
    thread = Thread(target=server.serve_forever, daemon=True)
    thread.start()
    LOGGER.info("Health check server started on port %d", port)

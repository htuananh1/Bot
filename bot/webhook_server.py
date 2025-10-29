"""Flask webhook server for Discord interactions."""

from __future__ import annotations

import asyncio
import logging
from threading import Thread

from flask import Flask, jsonify, request

LOGGER = logging.getLogger(__name__)


class WebhookServer:
    """Flask server for handling Discord webhooks."""

    def __init__(self, port: int = 8080, path: str = "/discord-webhook"):
        self.app = Flask(__name__)
        self.port = port
        self.path = path
        self._setup_routes()

    def _setup_routes(self) -> None:
        """Setup Flask routes."""
        
        @self.app.route("/health", methods=["GET"])
        def health_check():
            """Health check endpoint."""
            return jsonify({"status": "ok", "service": "discord-bot"}), 200

        @self.app.route(self.path, methods=["POST"])
        def discord_webhook():
            """Handle Discord webhook events."""
            try:
                data = request.get_json()
                LOGGER.info("Received webhook: %s", data)
                
                # Process webhook data
                # This can be extended for Discord Interactions
                
                return jsonify({"status": "received"}), 200
            except Exception as error:
                LOGGER.error("Webhook error: %s", error, exc_info=True)
                return jsonify({"error": "Internal error"}), 500

        @self.app.route("/", methods=["GET"])
        def index():
            """Root endpoint."""
            return jsonify({
                "service": "Discord Game Bot",
                "status": "running",
                "health": "/health",
                "webhook": self.path
            }), 200

    def run(self) -> None:
        """Run the Flask server."""
        LOGGER.info("Starting webhook server on port %d", self.port)
        self.app.run(host="0.0.0.0", port=self.port, debug=False)

    def run_threaded(self) -> Thread:
        """Run server in background thread."""
        thread = Thread(target=self.run, daemon=True)
        thread.start()
        LOGGER.info("Webhook server started in background")
        return thread

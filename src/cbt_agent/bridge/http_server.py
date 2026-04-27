from __future__ import annotations

import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Any, Dict, cast

from cbt_agent.agents.cbt_agent import CbtAgent
from cbt_agent.guardrails.policy_engine import load_policy
from cbt_agent.runtime.input_router import parse_input
from cbt_agent.runtime.tool_router import route_tool_call

SESSIONS: Dict[str, CbtAgent] = {}
POLICY = load_policy()


def get_agent(session_id: str) -> CbtAgent:
    if session_id not in SESSIONS:
        SESSIONS[session_id] = CbtAgent()
    return SESSIONS[session_id]


class BridgeHandler(BaseHTTPRequestHandler):
    def _json_response(self, status: int, payload: Dict[str, object]) -> None:
        body = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_POST(self) -> None:  # noqa: N802
        headers_obj = cast(Any, self.headers)
        content_len_raw = headers_obj.get("Content-Length")
        try:
            content_len = int(content_len_raw) if content_len_raw else 0
        except (TypeError, ValueError):
            content_len = 0
        raw = self.rfile.read(content_len).decode("utf-8")

        try:
            data = json.loads(raw or "{}")
        except json.JSONDecodeError:
            self._json_response(400, {"error": "Invalid JSON"})
            return

        session_id = str(data.get("session_id", "default"))
        message = str(data.get("message", "")).strip()

        if self.path != "/chat":
            self._json_response(404, {"error": "Unknown path"})
            return

        routed = parse_input(message)
        agent = get_agent(session_id)

        if routed.route == "command":
            if routed.command == "help":
                self._json_response(200, {"response": "Commands: /cbt <text>, /tool <name> <input>, /reset, /exit"})
                return

            if routed.command == "reset":
                agent.reset()
                self._json_response(200, {"response": "Session history cleared."})
                return

            if routed.command in {"exit", "quit"}:
                self._json_response(200, {"response": "Session can be closed client-side."})
                return

            if routed.command == "tool":
                tool_name = routed.args.get("name", "") if routed.args else ""
                tool_input = routed.args.get("input", "") if routed.args else ""

                if tool_name == "suggest_cbt_exercise":
                    result = route_tool_call(POLICY, tool_name, {"context": tool_input})
                elif tool_name == "reflect_user_text":
                    result = route_tool_call(POLICY, tool_name, {"user_text": tool_input})
                else:
                    result = "Unsupported tool for bridge command."

                self._json_response(200, {"response": result, "mode": "command"})
                return

        response = agent.run_turn(routed.payload)
        self._json_response(
            200,
            {
                "response": response.text,
                "violations": response.violations,
                "meta": response.meta,
            },
        )


def run_server(host: str = "127.0.0.1", port: int = 8080) -> None:
    server = ThreadingHTTPServer((host, port), BridgeHandler)  # type: ignore[arg-type]
    print(f"Bridge server listening at http://{host}:{port}")
    server.serve_forever()


if __name__ == "__main__":
    run_server()






import sys
import json
import time
from client import PersonalRelationshipGraph

prm = PersonalRelationshipGraph()

def handle_request(req):
    method = req.get("method")
    req_id = req.get("id")
    
    if method == "initialize":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "protocolVersion": "2024-11-05",
                "capabilities": {"tools": {}},
                "serverInfo": {"name": "genpark-personal-relationship-network-graph-skill", "version": "1.0.0"}
            }
        }
    elif method == "tools/list":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "tools": [
                    {
                        "name": "add_contact",
                        "description": "Add a new contact with specified cadence target to PRM graph",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "contact_id": {"type": "string"},
                                "name": {"type": "string"},
                                "relationship_tag": {"type": "string"},
                                "cadence_days": {"type": "number"}
                            },
                            "required": ["contact_id", "name"]
                        }
                    },
                    {
                        "name": "log_interaction",
                        "description": "Log an ambient interaction note with a contact",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "contact_id": {"type": "string"},
                                "note": {"type": "string"}
                            },
                            "required": ["contact_id", "note"]
                        }
                    },
                    {
                        "name": "get_stale_contacts",
                        "description": "Retrieve contacts whose last touchpoint exceeds target cadence",
                        "inputSchema": {"type": "object", "properties": {}}
                    }
                ]
            }
        }
    elif method == "tools/call":
        params = req.get("params", {})
        tool_name = params.get("name")
        args = params.get("arguments", {})
        
        if tool_name == "add_contact":
            prm.add_contact(args["contact_id"], args["name"], args.get("relationship_tag", "general"), args.get("cadence_days", 14))
            return {"jsonrpc": "2.0", "id": req_id, "result": {"content": [{"type": "text", "text": "Contact added successfully"}]}}
        elif tool_name == "log_interaction":
            prm.log_interaction(args["contact_id"], args["note"])
            return {"jsonrpc": "2.0", "id": req_id, "result": {"content": [{"type": "text", "text": "Interaction logged"}]}}
        elif tool_name == "get_stale_contacts":
            stale = prm.get_stale_contacts(time.time())
            return {"jsonrpc": "2.0", "id": req_id, "result": {"content": [{"type": "text", "text": json.dumps(stale, indent=2)}]}}

    return {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32601, "message": "Method not found"}}

def main():
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            req = json.loads(line)
            res = handle_request(req)
            sys.stdout.write(json.dumps(res) + "\n")
            sys.stdout.flush()
        except Exception as e:
            err_res = {"jsonrpc": "2.0", "id": None, "error": {"code": -32700, "message": str(e)}}
            sys.stdout.write(json.dumps(err_res) + "\n")
            sys.stdout.flush()

if __name__ == "__main__":
    main()

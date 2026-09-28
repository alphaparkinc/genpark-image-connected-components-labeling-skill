import sys
import json
from client import ConnectedComponentsLabeler

def handle_rpc(line):
    try:
        req = json.loads(line)
    except Exception:
        return
    req_id = req.get("id")
    method = req.get("method")
    params = req.get("params", {})

    if method == "initialize":
        res = {
            "protocolVersion": "2024-11-05",
            "serverInfo": {"name": "genpark-image-connected-components-labeling-skill", "version": "1.0.0"},
            "capabilities": {"tools": {}}
        }
    elif method == "tools/list":
        res = {
            "tools": [
                {
                    "name": "label_components",
                    "description": "Label connected components in binary mask and compute bounding boxes and areas",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "binary_image": {"type": "array", "items": {"type": "array", "items": {"type": "integer"}}},
                            "connectivity": {"type": "integer", "enum": [4, 8], "default": 8}
                        },
                        "required": ["binary_image"]
                    }
                }
            ]
        }
    elif method == "tools/call":
        tool_name = params.get("name")
        args = params.get("arguments", {})
        if tool_name == "label_components":
            ccl = ConnectedComponentsLabeler(connectivity=args.get("connectivity", 8))
            data = ccl.label_components(args.get("binary_image", []))
            res = {"content": [{"type": "text", "text": json.dumps(data)}]}
        else:
            res = {"isError": True, "content": [{"type": "text", "text": f"Unknown tool {tool_name}"}]}
    else:
        res = {"error": {"code": -32601, "message": "Method not found"}}

    resp = {"jsonrpc": "2.0", "id": req_id, "result": res.get("result", res)}
    sys.stdout.write(json.dumps(resp) + "\n")
    sys.stdout.flush()

def main():
    for line in sys.stdin:
        if line.strip():
            handle_rpc(line.strip())

if __name__ == "__main__":
    main()

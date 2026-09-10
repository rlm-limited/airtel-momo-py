import json

def fix_openapi_spec(file_path, output_path):
    with open(file_path, 'r') as f:
        spec = json.load(f)

    # 1. Fix Parameter Ordering (Remove default from accountHolderIdType)
    # This prevents the "Parameter without a default cannot follow a parameter with a default" error.
    for path, methods in spec.get("paths", {}).items():
        for method, details in methods.items():
            if "parameters" in details:
                for param in details["parameters"]:
                    if param.get("name") == "accountHolderIdType" and "default" in param.get("schema", {}):
                        del param["schema"]["default"]

    # 2. Fix Unsupported Content Types
    # Converts keys like "Incorrect target environment" into "application/json"
    def fix_content_objects(obj):
        if isinstance(obj, dict):
            if "content" in obj and isinstance(obj["content"], dict):
                new_content = {}
                for key, value in obj["content"].items():
                    # If the key isn't a standard MIME type, force it to application/json
                    if "/" not in key:
                        new_content["application/json"] = value
                    else:
                        new_content[key] = value
                obj["content"] = new_content
            
            for k, v in obj.items():
                fix_content_objects(v)
        elif isinstance(obj, list):
            for item in obj:
                fix_content_objects(item)

    fix_content_objects(spec)

    # 3. Ensure bc-authorize has a proper schema for form-urlencoded
    # The generator needs properties to create the data classes.
    bc_auth_path = "/v1_0/bc-authorize"
    if bc_auth_path in spec["paths"]:
        post_content = spec["paths"][bc_auth_path]["post"].get("requestBody", {}).get("content", {})
        form_key = "application/x-www-form-urlencoded"
        if form_key in post_content and "schema" not in post_content[form_key]:
            post_content[form_key]["schema"] = {
                "type": "object",
                "properties": {
                    "login_hint": {"type": "string"},
                    "scope": {"type": "string"},
                    "access_type": {"type": "string", "enum": ["online", "offline"]}
                }
            }

    with open(output_path, 'w') as f:
        json.dump(spec, f, indent=4)
    print(f"Cleaned spec saved to {output_path}")

if __name__ == "__main__":
    fix_openapi_spec('./docs/collection.json', './docs/collection_fixed.json')
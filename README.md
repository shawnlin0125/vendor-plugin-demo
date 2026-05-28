# Vendor Plugin Template

GitHub template for creating new vendor plugins.

## Quick Start

```bash
# Create new plugin from this template
gh repo create vendor-plugin-<name> --template shawnlin0125/vendor-plugin-template --private

# Clone and develop
git clone https://github.com/shawnlin0125/vendor-plugin-<name>
cd vendor-plugin-<name>

# Set plugin name
echo "PLUGIN_NAME=vendor-plugin-<name>" >> .env

# Run locally
docker build -t plugin .
docker run -e PORT=8080 -e PLUGIN_NAME=vendor-plugin-<name> -p 8080:8080 plugin
curl http://localhost:8080/health
```

## Required Endpoints (Contract v1)

| Method | Path     | Description    |
|--------|----------|----------------|
| GET    | `/health`| Health check   |
| GET    | `/`      | Plugin info    |

## CI Gates

| Job            | Description                    |
|----------------|--------------------------------|
| contract-lint  | Validate openapi.yaml exists   |
| build-smoke    | Docker build + /health smoke   |
| unit-test      | pytest with coverage           |

## Development

```bash
pip install -e ".[dev]"
pytest tests/ -v
```

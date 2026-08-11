# Azure Deployment

A small FastAPI chatbot can run on Azure App Service or Azure Container Apps.
Static Web Apps are a good fit when the frontend is deployed separately from
the API.

Production deployments should keep provider credentials in Azure Key Vault,
use Managed Identity where supported, send redacted telemetry to Application
Insights, and configure a budget alert for provider usage.

Start with the smallest viable service tier. Add PostgreSQL, Blob Storage, or
Azure AI Search only when persistence, file storage, or retrieval scale
requires them.

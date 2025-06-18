Overview

This architecture outlines how we leverage Istio Service Mesh within our Azure Kubernetes Service (AKS) environment to secure, control, and observe internal microservice traffic.

Key benefits:

Zero-trust security (mTLS)

Full observability with Prometheus + Grafana

Fine-grained traffic routing and policies

Controlled ingress/egress via Azure Application Gateway (AGIC)

Architecture Components

1. External Access
All incoming traffic flows through the Azure Application Gateway.

Managed by AGIC (Azure Gateway Ingress Controller).

Routes external traffic into the Istio mesh.

2. Istio Control Plane
Acts as the brain of the mesh.

Responsible for:

mTLS enforcement (PeerAuthentication)

Traffic routing policies (DestinationRule, VirtualService)

Ingress/Egress control (Gateway, ServiceEntry)

Access control (AuthorizationPolicy)

3. Security Policies
PeerAuthentication: Enables encrypted mTLS between services.

AuthorizationPolicy: Defines who can access what based on rules.

ServiceEntry: Manages external API/service access.

4. Traffic Management
Gateway: Accepts external traffic and forwards it into the mesh.

VirtualService: Defines how traffic is routed to services (e.g., based on paths or versions).

DestinationRule: Applies load balancing, connection pool, or circuit-breaker policies.

5. Namespaces & Services
Two key Kubernetes namespaces:

PLM-ORCHESTRATION: Manages orchestration-related services.

PLM-SERVICES: Hosts business logic services like Configuration and Business Rules.

Each pod runs with an Envoy sidecar, automatically injected by Istio.

6. Telemetry & Monitoring
Prometheus: Collects metrics from services and sidecars.

Grafana: Provides dashboards and visualization.

Summary Table
Component	Purpose
Azure App Gateway	Ingress controller, routes external traffic
Istio Control Plane	Mesh controller; applies routing, security, and access policies
PeerAuthentication	Enables mTLS encryption across services
AuthorizationPolicy	Access control for service-to-service communication
VirtualService	Traffic routing rules for services
DestinationRule	Load balancing and failover strategies
Prometheus & Grafana	Metrics collection and visualization
Envoy Sidecars	Transparent proxies for mTLS, metrics, routing, and telemetry
Final Notes
All services within the mesh communicate securely via mTLS.

The Istio Gateway + AGIC combo ensures secure and scalable ingress.

This architecture supports zero-trust security, fine-grained control, and real-time observability — ideal for modern microservices.
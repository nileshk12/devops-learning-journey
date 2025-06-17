Troubleshooting Istio 403 Forbidden Errors in Multi-Namespace AKS Setup

The Challenge

Recently, I encountered a frustrating issue while implementing Istio service mesh in an Azure Kubernetes Service (AKS) cluster. Everything worked perfectly until I enabled Istio sidecar injection — then suddenly, all API calls started returning 403 Forbidden errors with “RBAC: access denied” messages.

Architecture Overview

AKS Cluster with Istio service mesh
Azure Application Gateway Ingress Controller (AGIC) for external traffic
Two Namespaces with cross-namespace communication:
namespace-a: Orchestration service
namespace-b: Configuration and rule management services
API Flow: External → AGIC → Orchestration Service → Configuration Service
What Went Wrong?

The issue boiled down to three critical misconfigurations in Istio Authorization Policies:

1. HTTP Methods vs URL Paths Confusion

Problem: I was putting URL paths in the methods field instead of HTTP methods.

# INCORRECT

spec:

rules:

- to:

operation:

methods:

- /public/* # This should be HTTP methods, not paths!

- /api/*

Solution: Properly separate HTTP methods and URL paths.

# CORRECT

spec:

rules:

- to:

operation:

methods: [“GET”, “POST”, “PUT”, “DELETE”, “OPTIONS”]

paths: [“/public/*”, “/api/*”]

2. Wrong Service Account Principal

Problem: Authorization policy expected a service account that didn’t exist.

# INCORRECT

principals: [“cluster.local/ns/my-namespace/sa/my-custom-sa”]

Diagnosis: Checked the actual service account being used:

kubectl get pod <pod-name> -o yaml | grep serviceAccount

# Output: serviceAccount: default

Solution: Use the correct service account principal.

# CORRECT

principals: [“cluster.local/ns/my-namespace/sa/default”]

3. Incomplete Path Patterns

Problem: Missing required API path patterns in authorization policies.

For an API call like /public/api/v1/organizations/92, I needed the pattern /public/api/v1/* which was missing from my configuration.

The Solution

Step 1: Fixed Orchestration Namespace Policy

apiVersion: security.istio.io/v1beta1

kind: AuthorizationPolicy

metadata:

name: orchestration-access

namespace: namespace-a

spec:

selector:

matchLabels:

app: orchestration-app

action: ALLOW

rules:

# Allow external traffic from AGIC

- to:

- operation:

methods: [“GET”, “POST”, “PUT”, “DELETE”, “OPTIONS”]

paths: [“/public/*”, “/api/*”]

ports: [“8080”]

# Allow health checks

- to:

- operation:

methods: [“GET”]

paths: [“/actuator/*”]

ports: [“8080”, “8081”]

Step 2: Fixed Cross-Namespace Communication Policy

apiVersion: security.istio.io/v1beta1

kind: AuthorizationPolicy

metadata:

name: config-service-access

namespace: namespace-b

spec:

selector:

matchLabels:

app: config-service

action: ALLOW

rules:

- from:

- source:

namespaces: [“namespace-a”]

principals: [“cluster.local/ns/namespace-a/sa/default”]

to:

- operation:

methods: [“GET”, “POST”, “PUT”, “DELETE”, “OPTIONS”]

paths: [“/api/v1/*”, “/public/*”, “/public/api/v1/*”]

ports: [“8080”]

Step 3: Fixed Malformed DestinationRule

Problem: Invalid YAML with duplicate host entries at the same level.

Solution: Created separate DestinationRule resources for each service.

Key Debugging Commands

# Check authorization policies

kubectl get authorizationpolicy -n <namespace>

kubectl describe authorizationpolicy <policy-name> -n <namespace>

# Verify service accounts

kubectl get pod <pod-name> -n <namespace> -o yaml | grep serviceAccount

# Check pod labels

kubectl get pods -n <namespace> — show-labels

# Monitor Istio proxy logs

kubectl logs <pod-name> -c istio-proxy -n <namespace>

Key Lessons Learned

Istio is Restrictive by Default — Enabling Istio changes from permissive to restrictive security model
YAML Structure Matters — Small configuration errors can break everything
Verify Service Account Reality — Don’t assume — check what service accounts pods actually use
Comprehensive Path Patterns — Include ALL API paths your services need
Explicit Cross-Namespace Policies — Never assume default connectivity works
Don’t Forget Health Checks — Actuator and monitoring endpoints need explicit permission
The Result

After implementing these fixes:

Login API calls return 200 OK
Configuration API calls return 200 OK
Cross-namespace communication working
Bearer token authentication flows properly
Final Thoughts

This experience taught me that Istio’s security-first approach requires careful planning and thorough testing. The key is understanding that Istio Authorization Policies are deny-by-default — you must explicitly allow everything your application needs.

Architecture Overview

Troubleshooting Istio 403 Forbidden Errors in Multi-Namespace AKS Setup

The Challenge

Recently, I encountered a frustrating issue while implementing Istio service mesh in an Azure Kubernetes Service (AKS) cluster. Everything worked perfectly until I enabled Istio sidecar injection — then suddenly, all API calls started returning 403 Forbidden errors with “RBAC: access denied” messages.

Architecture Overview

AKS Cluster with Istio service mesh
Azure Application Gateway Ingress Controller (AGIC) for external traffic
Two Namespaces with cross-namespace communication:
namespace-a: Orchestration service
namespace-b: Configuration and rule management services
API Flow: External → AGIC → Orchestration Service → Configuration Service
What Went Wrong?

The issue boiled down to three critical misconfigurations in Istio Authorization Policies:

1. HTTP Methods vs URL Paths Confusion

Problem: I was putting URL paths in the methods field instead of HTTP methods.

# INCORRECT

spec:

rules:

- to:

operation:

methods:

- /public/* # This should be HTTP methods, not paths!

- /api/*

Solution: Properly separate HTTP methods and URL paths.

# CORRECT

spec:

rules:

- to:

operation:

methods: [“GET”, “POST”, “PUT”, “DELETE”, “OPTIONS”]

paths: [“/public/*”, “/api/*”]

2. Wrong Service Account Principal

Problem: Authorization policy expected a service account that didn’t exist.

# INCORRECT

principals: [“cluster.local/ns/my-namespace/sa/my-custom-sa”]

Diagnosis: Checked the actual service account being used:

kubectl get pod <pod-name> -o yaml | grep serviceAccount

# Output: serviceAccount: default

Solution: Use the correct service account principal.

# CORRECT

principals: [“cluster.local/ns/my-namespace/sa/default”]

3. Incomplete Path Patterns

Problem: Missing required API path patterns in authorization policies.

For an API call like /public/api/v1/organizations/92, I needed the pattern /public/api/v1/* which was missing from my configuration.

The Solution

Step 1: Fixed Orchestration Namespace Policy

apiVersion: security.istio.io/v1beta1

kind: AuthorizationPolicy

metadata:

name: orchestration-access

namespace: namespace-a

spec:

selector:

matchLabels:

app: orchestration-app

action: ALLOW

rules:

# Allow external traffic from AGIC

- to:

- operation:

methods: [“GET”, “POST”, “PUT”, “DELETE”, “OPTIONS”]

paths: [“/public/*”, “/api/*”]

ports: [“8080”]

# Allow health checks

- to:

- operation:

methods: [“GET”]

paths: [“/actuator/*”]

ports: [“8080”, “8081”]

Step 2: Fixed Cross-Namespace Communication Policy

apiVersion: security.istio.io/v1beta1

kind: AuthorizationPolicy

metadata:

name: config-service-access

namespace: namespace-b

spec:

selector:

matchLabels:

app: config-service

action: ALLOW

rules:

- from:

- source:

namespaces: [“namespace-a”]

principals: [“cluster.local/ns/namespace-a/sa/default”]

to:

- operation:

methods: [“GET”, “POST”, “PUT”, “DELETE”, “OPTIONS”]

paths: [“/api/v1/*”, “/public/*”, “/public/api/v1/*”]

ports: [“8080”]

Step 3: Fixed Malformed DestinationRule

Problem: Invalid YAML with duplicate host entries at the same level.

Solution: Created separate DestinationRule resources for each service.

Key Debugging Commands

# Check authorization policies

kubectl get authorizationpolicy -n <namespace>

kubectl describe authorizationpolicy <policy-name> -n <namespace>

# Verify service accounts

kubectl get pod <pod-name> -n <namespace> -o yaml | grep serviceAccount

# Check pod labels

kubectl get pods -n <namespace> — show-labels

# Monitor Istio proxy logs

kubectl logs <pod-name> -c istio-proxy -n <namespace>

Key Lessons Learned

Istio is Restrictive by Default — Enabling Istio changes from permissive to restrictive security model
YAML Structure Matters — Small configuration errors can break everything
Verify Service Account Reality — Don’t assume — check what service accounts pods actually use
Comprehensive Path Patterns — Include ALL API paths your services need
Explicit Cross-Namespace Policies — Never assume default connectivity works
Don’t Forget Health Checks — Actuator and monitoring endpoints need explicit permission
The Result

After implementing these fixes:

Login API calls return 200 OK
Configuration API calls return 200 OK
Cross-namespace communication working
Bearer token authentication flows properly
Final Thoughts

This experience taught me that Istio’s security-first approach requires careful planning and thorough testing. The key is understanding that Istio Authorization Policies are deny-by-default — you must explicitly allow everything your application needs.



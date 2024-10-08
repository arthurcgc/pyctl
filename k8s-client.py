import os
import code
import readline
import rlcompleter
from kubernetes import client, config
from IPython import start_ipython

def configure_k8s_client():
    """Configure the Kubernetes client."""
    try:
        # Load kubeconfig from default location
        config.load_kube_config()
        print("Kubernetes client configured successfully.")
    except Exception as e:
        print(f"Error configuring Kubernetes client: {e}")
        exit(1)

def interactive_shell():
    """Start an IPython shell with Kubernetes client and helper functions."""
    # Set up the Kubernetes client
    global v1, apps_v1  # Declare as global so they are accessible
    v1 = client.CoreV1Api()
    apps_v1 = client.AppsV1Api()
    
    # Create a dictionary for easy access to client methods and helper functions
    local_context = {
        "v1": v1,
        "apps_v1": apps_v1,
        "list_svcs_with_annotations": list_svcs_with_annotations,
    }
    
    # Start the IPython shell with the local context
    print("Entering IPython interactive shell. Use `exit()` to exit.")
    start_ipython(argv=[], user_ns=local_context)

def list_svcs_with_annotations(annotations_filter):
    svcs = v1.list_service_for_all_namespaces().items
    svc_names = []
    for svc in svcs:
        svc_annotations = svc.metadata.annotations or {}
        if all(key in svc_annotations for key in annotations_filter):
            svc_names.append(svc.metadata.name)
    return svc_names

if __name__ == "__main__":
    configure_k8s_client()
    interactive_shell()

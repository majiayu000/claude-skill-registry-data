---
name: go-kubernetes
description: Kubernetes operators and client-go development
sasmp_version: "1.3.0"
bonded_agent: 08-go-devops
bond_type: PRIMARY_BOND
---

# Go Kubernetes Skill

Build Kubernetes operators and controllers with client-go.

## Overview

Develop custom Kubernetes controllers, operators, and CRDs using client-go and controller-runtime.

## Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| type | string | yes | - | Type: "operator", "controller", "crd" |
| framework | string | no | "controller-runtime" | Framework |

## Core Topics

### Client Setup
```go
import (
    "k8s.io/client-go/kubernetes"
    "k8s.io/client-go/rest"
    "k8s.io/client-go/tools/clientcmd"
)

func NewClient() (*kubernetes.Clientset, error) {
    config, err := rest.InClusterConfig()
    if err != nil {
        // Fallback to kubeconfig
        kubeconfig := filepath.Join(os.Getenv("HOME"), ".kube", "config")
        config, err = clientcmd.BuildConfigFromFlags("", kubeconfig)
        if err != nil {
            return nil, err
        }
    }

    return kubernetes.NewForConfig(config)
}
```

### Watch Resources
```go
func WatchPods(ctx context.Context, client *kubernetes.Clientset, namespace string) error {
    watcher, err := client.CoreV1().Pods(namespace).Watch(ctx, metav1.ListOptions{})
    if err != nil {
        return err
    }
    defer watcher.Stop()

    for event := range watcher.ResultChan() {
        pod := event.Object.(*corev1.Pod)
        switch event.Type {
        case watch.Added:
            fmt.Printf("Pod added: %s\n", pod.Name)
        case watch.Modified:
            fmt.Printf("Pod modified: %s (phase: %s)\n", pod.Name, pod.Status.Phase)
        case watch.Deleted:
            fmt.Printf("Pod deleted: %s\n", pod.Name)
        }
    }
    return nil
}
```

### Controller-Runtime Reconciler
```go
type MyReconciler struct {
    client.Client
    Scheme *runtime.Scheme
    Log    logr.Logger
}

func (r *MyReconciler) Reconcile(ctx context.Context, req ctrl.Request) (ctrl.Result, error) {
    log := r.Log.WithValues("resource", req.NamespacedName)

    var myResource myv1.MyResource
    if err := r.Get(ctx, req.NamespacedName, &myResource); err != nil {
        if apierrors.IsNotFound(err) {
            return ctrl.Result{}, nil
        }
        return ctrl.Result{}, err
    }

    // Reconciliation logic
    if myResource.Status.Phase == "" {
        myResource.Status.Phase = "Pending"
        if err := r.Status().Update(ctx, &myResource); err != nil {
            return ctrl.Result{}, err
        }
    }

    return ctrl.Result{RequeueAfter: time.Minute}, nil
}
```

### Custom Resource Definition
```yaml
apiVersion: apiextensions.k8s.io/v1
kind: CustomResourceDefinition
metadata:
  name: myresources.example.com
spec:
  group: example.com
  versions:
    - name: v1
      served: true
      storage: true
      schema:
        openAPIV3Schema:
          type: object
          properties:
            spec:
              type: object
              properties:
                replicas:
                  type: integer
            status:
              type: object
              properties:
                phase:
                  type: string
  scope: Namespaced
  names:
    plural: myresources
    singular: myresource
    kind: MyResource
```

## Troubleshooting

### Failure Modes
| Symptom | Cause | Fix |
|---------|-------|-----|
| RBAC denied | Missing permissions | Check ServiceAccount |
| CRD not found | Not installed | kubectl apply CRD |
| Leader election fail | Lease conflict | Check replicas |

## Usage

```
Skill("go-kubernetes")
```

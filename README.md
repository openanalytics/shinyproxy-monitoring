# ShinyProxy Monitoring

## Summary

This repository provides all resources required for setting up comprehensive
monitoring of ShinyProxy on Kubernetes. The setup uses Loki (together with
Alloy) for collecting logs of ShinyProxy, the ShinyProxy Operator and any app
running in ShinyProxy. Prometheus is used for gathering metrics of ShinyProxy
and the apps (i.e. the resources used by the apps). The setup also includes
Grafana, together with **nine** dashboards for visualizing all logs and metrics.

The retention of both Loki and Prometheus is set to 90 days.

## Overview of dashboards

Starting with version 3.2.0 of the stack, all documentation has been added to
the dashboards. See the `Description` panel at the top of every dashboard and
the info icons of every panel for detailed information.

### ShinyProxy Usage

[**Screenshot**](https://raw.githubusercontent.com/openanalytics/shinyproxy-monitoring/master/.github/screenshots/shinyproxy-usage.png)
[**Screenshot (continued)**](https://raw.githubusercontent.com/openanalytics/shinyproxy-monitoring/master/.github/screenshots/shinyproxy-usage2.png)

- **Datasource:** Prometheus
- **Goal:** provide inside in the *current* usage and performance of ShinyProxy.

**Note**: the last three panels of this dashboard can somtimes show a too high
value, e.g. the app crashes dashboard could list two app crashes while in
reality only a single app crashed. This is caused by a limitation
in [Prometheus](https://www.doit.com/making-peace-with-prometheus-rate/).

### ShinyProxy Aggregated Usage

[**Screenshot**](https://raw.githubusercontent.com/openanalytics/shinyproxy-monitoring/master/.github/screenshots/shinyproxy-aggregated-usage.png)

- **Datasource:** Prometheus
- **Goal:** provide inside in the *long-term* usage and performance of
  ShinyProxy.

### ShinyProxy logs

[**Screenshot**](https://raw.githubusercontent.com/openanalytics/shinyproxy-monitoring/master/.github/screenshots/shinyproxy-logs.png)

- **Datasource:** Loki
- **Goal:** show the logs of the ShinyProxy server

**Note:** This requires ShinyProxy to log using
the [JSON format](https://shinyproxy.io/documentation/configuration/#json-logstash-logging).

### ShinyProxy Operator Logs

[**Screenshot**](https://raw.githubusercontent.com/openanalytics/shinyproxy-monitoring/master/.github/screenshots/shinyproxy-operator-logs.png)

- **Datasource:** Loki
- **Goal:** show the logs of the ShinyProxy Operator

**Note:** promtail is configured such that it recognizes when Java outputs a stack
trace and therefore collects this as a single log message. We could improve and
optimize this by adding an option to the ShinyProxy Operator to log to JSON.

### ShinyProxy App Logs

[**Screenshot**](https://raw.githubusercontent.com/openanalytics/shinyproxy-monitoring/master/.github/screenshots/shinyproxy-app-logs.png)
[**Screenshot (error)**](https://raw.githubusercontent.com/openanalytics/shinyproxy-monitoring/master/.github/screenshots/shinyproxy-app-logs2.png)

- **Datasource:** Loki
- **Goal:** show the logs of any app started by ShinyProxy.

**Note:** this dashboard also works when apps are run in different namespaces
than the namespace of the ShinyProxy server. As an example, the Dash application
in ShinyProxy 1 runs in a different namespace.

**Note:** this dashboard also shows parts of the ShinyProxy log that are
relevant for this app.

### ShinyProxy App Resources

[**Screenshot**](https://raw.githubusercontent.com/openanalytics/shinyproxy-monitoring/master/.github/screenshots/shinyproxy-app-resources.png)

- **Datasource:** Prometheus
- **Goal:** show the resources (CPU, Memory, Network) used by any app started by
  ShinyProxy.

**Note:** this dashboard also works when apps are run in different namespaces
than the namespace of the ShinyProxy server. As an example, the Dash application
in ShinyProxy 1 runs in a different namespace.

### ShinyProxy Delegate App Logs

[**Screenshot**](https://raw.githubusercontent.com/openanalytics/shinyproxy-monitoring/master/.github/screenshots/shinyproxy-delegate-app-logs.png)

- **Datasource:** Loki
- **Goal:** show the logs of *delegate* apps started by ShinyProxy. This are the
  underlying container/apps when using
  the [pre-initialization and container sharing feature](https://shinyproxy.io/documentation/configuration/#container-pre-initialization-and-sharing).

### ShinyProxy Delegate App Resources

[**Screenshot**](https://raw.githubusercontent.com/openanalytics/shinyproxy-monitoring/master/.github/screenshots/shinyproxy-delegate-app-resources.png)

- **Datasource:** Prometheus
- **Goal:** show the resources (CPU, Memory, Network) used by *delegate* apps. This are the
  underlying container/apps when using
  the [pre-initialization and container sharing feature](https://shinyproxy.io/documentation/configuration/#container-pre-initialization-and-sharing).

### ShinyProxy Seats

[**Screenshot**](https://raw.githubusercontent.com/openanalytics/shinyproxy-monitoring/master/.github/screenshots/shinyproxy-seats.png)

- **Datasource:** Prometheus
- **Goal:** show the number of seats (and wait time) for apps that
  use [pre-initialization and container sharing](https://shinyproxy.io/documentation/configuration/#container-pre-initialization-and-sharing).

## How it works

### Loki + Alloy

Both Loki and Alloy are used to collect the logs for all relevant dashboards.
The upstream Loki helm chart is used. No tweaks are needed to make it work with
ShinyProxy. In contrast, the configuration of Alloy must be changed such that it
collects the correct metadata. See the [`overlays/alloy/configs/config.alloy`](overlays/alloy/configs/config.alloy)
file.

### Prometheus

The Prometheus setup is based on
the [kube-prometheus](https://github.com/prometheus-operator/kube-prometheus)
stack.

#### Grafana

The following changes are made to the configuration of Grafana:

* [`overlays/monitoring/configs/dashboards`](overlays/monitoring/configs/dashboards)
  contains the Grafana dashboards.
* [`overlays/monitoring/configs/datasources.yaml`](overlays/monitoring/configs/datasources.yaml)
  configures Prometheus and Loki as a datasource for Grafana.
* [`overlays/monitoring/configs/grafana-dashboardSources.json`](overlays/monitoring/configs/grafana-dashboardSources.json)
  creates a folder for the ShinyProxy dashboards.
* [`overlays/monitoring/patches/grafana.deployment.yaml`](overlays/monitoring/patches/grafana.deployment.yaml)
  adapts the Grafana deployment to use the ShinyProxy dashboards. It als adds a
  PVC for storage.
* [`overlays/monitoring/resources/grafana-storage.pvc.yaml`](overlays/monitoring/resources/grafana-storage.pvc.yaml)
  creates a PVC for Grafana.
* all dashboards are displayed in the timezone of the browser, show the data for
  the last 30 minutes and refresh every 10 seconds.

#### Prometheus

The changes to the Prometheus config are:

- [`overlays/monitoring/patches/prometheus-k8s.clusterrole.yaml`](overlays/monitoring/patches/prometheus-k8s.clusterrole.yaml)
  gives Prometheus additional permissions, to view `ServiceMonitor`, `Pod`
  and `Service` resources on cluster level.
- [`overlays/monitoring/resources/shinyproxy.servicemonitor.yaml`](overlays/monitoring/resources/shinyproxy.servicemonitor.yaml)
  setups a `ServiceMonitor` such that Prometheus collects the metrics of
  ShinyProxy. **Note**: this only collects the metrics of ShinyProxy servers
  running in the `shinyproxy-operator` namespace.

## Getting started

This section demonstrates how to set up this stack in minikube.

1. Start minikube

    ```bash
   minikube start --addons=metrics-server,ingress
    ```

2. Configure web access to the cluster. First get the IP of minikube using:

   ```bash
   minikube ip
   ```

   Next, add the following entries to `/etc/hosts`, replacing `MINIKUBE_IP` by
   the output of the previous command;

   ```text
   MINIKUBE_IP       grafana.shinyproxy-demo.local
   MINIKUBE_IP       shinyproxy-demo.local
   ``` 

3. Set up Loki

    ```bash
    cd overlays/loki
    kustomize build | kubectl apply --server-side -f - 
    cd ../..
    ```

   **Note:** re-run the command if it fails when it cannot find some CRDs.

4. Set up Alloy 

    ```bash
    cd overlays/alloy
    kustomize build | kubectl apply --server-side -f - 
    cd ../..
    ```

5. Set up Prometheus and Grafana

    ```bash
    cd overlays/monitoring
    kustomize build | kubectl apply --server-side -f - 
    cd ../..
    ```
   
   **Note:** re-run the command if it fails because it cannot find some CRDs.

6. Set up the demo ShinyProxy Operator deployment:

    ```bash
    cd overlays/shinyproxy
    kustomize build | kubectl apply --server-side -f - 
    cd ../shinyproxy1-app
    kustomize build | kubectl apply --server-side -f - 
     ```

   **Note:** re-run the command if it fails because it cannot find some CRDs.

You can now log in into shinyproxy on <http://shinyproxy-demo.local/shinyproxy1>
and <http://shinyproxy-demo.local/shinyproxy2> with the users `jack` and `jeff` (both
have as password `password`). You can log into grafana
on <http://grafana.shinyproxy-demo.local>, with the username and password `admin`.

## Upgrading

This repository uses the same version numbers as ShinyProxy. Always use the same
version of ShinyProxy and this repository.

### Upgrade to 3.1.0

In release 3.1.0 of this repository, all components were upgraded. In order to
maintain your logs and metrics, it's important to take the following steps when
updating:

- edit line 50
  of [`overlays/loki/configs/config.yaml`](overlays/loki/configs/config.yaml):
  change the day to be one day after you upgrade Loki. E.g. if you update this
  on `2024-03-25` (25 March 2024), change the date to `2024-03-26`. If you do
  not modify this line, you will no longer be able to access logs from before
  the upgrade. See
  the [Loki docs](https://grafana.com/docs/loki/latest/operations/storage/schema/)
  for more information.
  
### Upgrade to 3.2.0

This release contains the following improvements:

- replace Promtail by Alloy (for collecting logs). Alloy uses only a single pod
  instead of a daemonset, this reduces the overall resource consumption of the
  monitoring stack.
- include documentation in all dashboards
- allow selecting multiple apps/instances in app logs and resources dashboards
- allow to search in log dashboards
- make it easier to use the app resources dashboard
- show user, app id and instance in dashboards (only when a single `id` is selected)
- show app state in dashboards
- remove dependency on `kube-state-metrics`
- update all components

In order to upgrade an existing stack:

- edit line 105
  of [`overlays/loki/configs/config.yaml`](overlays/loki/configs/config.yaml#L105):
  change the day to be one day after you upgrade Loki. E.g. if you update this
  on `2025-07-03` (3 July 2025), change the date to `2025-07-04`. If you do
  not modify this line, you will no longer be able to access logs from before
  the upgrade. See
  the [Loki docs](https://grafana.com/docs/loki/latest/operations/storage/schema/)
  for more information.
- apply the manifests of all components:

    ```bash
    cd overlays/loki
    kustomize build | kubectl apply --server-side -f -
    cd ../..
    cd overlays/alloy
    kustomize build | kubectl apply --server-side -f -
    cd ../..
    cd overlays/monitoring
    kustomize build | kubectl apply --server-side -f -
    cd ../..
    ```
  
- once everything is running, remove Promtail:
  
    ```bash
    kubectl delete -n loki ds promtail
    kubectl delete -n loki sa promtail
    kubectl delete -n loki secret promtail
    ```

Following these steps both the old and new logs are available throuh Grafana.

## Docker support

The resources in this repository can only be used on Kubernetes. However, a very
similar stack can be deployed on pure docker hosts by using
the [ShinyProxy Operator](https://shinyproxy.io/documentation/shinyproxy-operator/docker/#enabling-monitoring).

**(c) Copyright Open Analytics NV, 2022-2025.**

manifest_version=5.44.1
component=loki

outfile=../base.yaml
helm_dir=helm/

all: update

update:
	$(info Updating to version $(manifest_version))
	rm -rf $(helm_dir) $(outfile)
	helm repo add grafana https://grafana.github.io/helm-charts
	helm repo update
	helm fetch grafana/loki --untar --untardir $(helm_dir) --version $(manifest_version)
	# use namespace loki here, because the namespace is hard coded in the configuration of nginx in the loki-gateway component
	helm template --include-crds --namespace loki --release-name dummy-release \
			--set singleBinary.replicas=1 --set monitoring.selfMonitoring.enabled=false \
			--set monitoring.selfMonitoring.grafanaAgent.installOperator=false \
			--set monitoring.lokiCanary.enabled=false --set test.enabled=false \
			--set loki.storage.type=filesystem \
			--set loki.commonConfig.replication_factor=1 \
			--set loki.auth_enabled=false \
			--set gateway.enabled=false \
            $(helm_dir)/$(component) | sed -e s/dummy-release-//g|grep -v dummy-release > $(outfile)

	rm -rf $(helm_dir)

clean:
	rm -rf $(helm_dir) $(outfile)

uninstall:
	kubectl delete -f $(outfile)

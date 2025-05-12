manifest_version=6.29.0
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
			--set deploymentMode=SingleBinary \
			--set backend.replicas=0 \
			--set read.replicas=0 \
			--set write.replicas=0 \
			--set ingester.replicas=0 \
			--set querier.replicas=0 \
			--set queryFrontend.replicas=0 \
			--set queryScheduler.replicas=0 \
			--set distributor.replicas=0 \
			--set compactor.replicas=0 \
			--set indexGateway.replicas=0 \
			--set bloomCompactor.replicas=0 \
			--set bloomGateway.replicas=0 \
			--set singleBinary.replicas=1 --set monitoring.selfMonitoring.enabled=false \
			--set monitoring.selfMonitoring.grafanaAgent.installOperator=false \
			--set monitoring.lokiCanary.enabled=false --set test.enabled=false \
			--set loki.storage.type=filesystem \
			--set loki.commonConfig.replication_factor=1 \
			--set lokiCanary.enabled=false \
			--set loki.auth_enabled=false \
			--set gateway.enabled=false \
			--set loki.useTestSchema=true \
			$(helm_dir)/$(component) | sed -e s/dummy-release-//g|grep -v dummy-release > $(outfile)

	rm -rf $(helm_dir)

clean:
	rm -rf $(helm_dir) $(outfile)

uninstall:
	kubectl delete -f $(outfile)

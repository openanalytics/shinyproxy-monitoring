manifest_version=1.0.3
outfile=../base.yaml
helm_dir=helm/
component=alloy

all:
	$(info Updating to version $(manifest_version))
	rm -rf $(helm_dir) $(outfile)
	helm repo add grafana https://grafana.github.io/helm-charts
	helm repo update
	helm fetch grafana/$(component) --untar --untardir $(helm_dir) --version $(manifest_version)
	helm template --namespace loki \
		--release-name dummy-release \
		--set controller.type=deployment \
		$(helm_dir)/$(component) | sed -e s/dummy-release-//g|grep -v dummy-release > $(outfile)
	rm -rf $(helm_dir)

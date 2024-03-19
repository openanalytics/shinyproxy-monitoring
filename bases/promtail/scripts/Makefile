manifest_version=6.15.5
component=promtail

outfile=../base.yaml
helm_dir=helm/

all: update

update:
	$(info Updating to version $(manifest_version))
	rm -rf $(helm_dir) $(outfile)
	helm repo add grafana https://grafana.github.io/helm-charts
	helm repo update
	helm fetch grafana/promtail --untar --untardir $(helm_dir) --version $(manifest_version)
	helm template --namespace default --release-name dummy-release \
            $(helm_dir)/$(component) | sed -e s/dummy-release-//g|grep -v dummy-release > $(outfile)

	rm -rf $(helm_dir)

clean:
	rm -rf $(helm_dir) $(outfile)

uninstall:
	kubectl delete -f $(outfile)

manifest_version=4.0.2
component=minio

outfile=../base.yaml
helm_dir=helm/

all: update

update:
	$(info Updating to version $(manifest_version))
	rm -rf $(helm_dir) $(outfile)
	helm repo add minio https://charts.min.io/
	helm repo update
	helm fetch minio/minio --untar --untardir $(helm_dir) --version $(manifest_version)
	helm template --namespace default --release-name dummy-release --set mode=standalone \
            $(helm_dir)/$(component) | sed -e s/dummy-release-//g|grep -v dummy-release > $(outfile)

	rm -rf $(helm_dir)

clean:
	rm -rf $(helm_dir) $(outfile)

uninstall:
	kubectl delete -f $(outfile)

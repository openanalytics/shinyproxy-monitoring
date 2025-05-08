manifest_version=release-0.14

git_dir=kube-prometheus-repo
out_dir=../

all: update

update:
	$(info Updating to version $(manifest_version))
	rm -rf $(git_dir) $(out_dir)/manifests $(out_dir)/kustomization.yaml
	git clone https://github.com/prometheus-operator/kube-prometheus/ -b ${manifest_version} --depth 1 $(git_dir)
	cp -r $(git_dir)/manifests/ $(out_dir)/manifests

	echo "apiVersion: kustomize.config.k8s.io/v1beta1" > $(out_dir)/kustomization.yaml
	echo "kind: Kustomization" >> $(out_dir)/kustomization.yaml
	echo "" >> $(out_dir)/kustomization.yaml
	echo "resources:" >> $(out_dir)/kustomization.yaml

	cd ../ ; \
 	find "manifests/setup" -maxdepth 1 -type f -print0 | while read  -d $$'\0' -r file; do \
		printf " - %s\n" "$$file" >> kustomization.yaml ; \
	done ; \
 	find "manifests" -maxdepth 1 -type f -print0 | while read  -d $$'\0' -r file; do \
		printf " - %s\n" "$$file" >> kustomization.yaml ; \
	done

	rm -rf $(git_dir)

clean:
	rm -rf $(git_dir) $(out_dir)/manifests $(out_dir)/kustomization.yaml

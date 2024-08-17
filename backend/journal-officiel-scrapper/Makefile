.PHONY: deploy build

build:
	sam build

deploy: build
	sam deploy --stack-name journal-officiel-scrapper --resolve-image-repos --region eu-west-3
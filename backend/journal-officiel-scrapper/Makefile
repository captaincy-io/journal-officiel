.PHONY: deploy build

build:
	sam build

deploy: build
	AWS_PROFILE=acme sam deploy --stack-name journal-officiel-scrapper --resolve-image-repos --region eu-west-3

test: build
	sam local invoke JournalOfficielScrapperFunction --profile acme
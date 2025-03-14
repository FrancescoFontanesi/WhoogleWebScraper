# WhoogleWebScraper
WebScraper based on the open source alternative of Google 


Need to install docker and pull the whoogle image that will run on localhost:5000
Run this command to run the container 

docker pull benbusby/whoogle-search:latest

docker run --publish 5000:5000 --detach --name whoogle-search `
--env WHOOGLE_RESULTS_PER_PAGE=100 `
benbusby/whoogle-search:latest
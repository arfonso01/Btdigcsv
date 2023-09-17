# Btdigcsv 

A simple script that exports the results of [btdig ](https://btdig.com/) to csv file. \
Works for trackers that use a naming structure like 'movie [trackerName]'

## Dependencies

- [python3](https://www.python.org/downloads/)
- [BeautifulSoup](https://pypi.org/project/beautifulsoup4/)
- [FlareSolverr](https://github.com/FlareSolverr/FlareSolverr) (Solver version)

## How to use it

There are two versions of the script: btdigscv.py (normal version) and solverr_version.py. The \
first uses a tor2web version and the second uses the original website whose requests are resolved \using FlareSolverr.

### Normal version

- Step 1: Edit the keyword variable (line 9) to 'trackerName'
- Step 2: Run the python script
- Step 3: You can now use your csv in [flexget](https://flexget.com/) or others

### Solver version

- Step 1: Install and run [Flaresolverr](https://github.com/FlareSolverr/FlareSolverr). \
I recommend using the docker image and its daemon so that it is always available.

    docker run -d \
      --name=flaresolverr \
      -p 8191:8191 \
      -e LOG_LEVEL=info \
      --restart unless-stopped \
      ghcr.io/flaresolverr/flaresolverr:latest

- Step 2: Edit the keyword variable (line 9) to 'trackerName'
- Step 3: Run the python script
- Step 4: You can now use your csv in [flexget](https://flexget.com/) or others


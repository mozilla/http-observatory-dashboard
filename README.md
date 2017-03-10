# HTTP Observatory Dashboard

This dashboard provides a metrics dashboard to see the status of the [Observatory](https://observatory.mozilla.org/) for each link.

## Prerequisites

This site requires:

- Python >3.4
- Make
  - **Linux:** most package managers have *build-essential* which provide make
  - **MacOS:** installing Xcode provides make

## Install

```
pip install -r requirements.txt
```

**Note:** Some linux setups may require *pip3* instead of *pip* in the above command.

## Running

Running `make devserver` will make a live dev environment that can be loaded in the browser and refreshes every time you change templates or run `make generate`.

Running `make generate` fetches the reports from the Observatory.

```
cd httpobsdashboard;
make generate;
make devserver;
```

## Configuring

Configuring the dashboard is simple, edit the JSON files `httpobsdashboard/conf/` the main files is `sites.json`.

To modify the meaning of scores for websites edit `deviations.json`. 

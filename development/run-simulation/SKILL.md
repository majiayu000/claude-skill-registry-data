---
name: Analyze PDE Simulation
description: Run and analyze one or multiple PDE simulations. Use for every simulation.
---

Before running simulations, ensure that you are using the correct python environment with the necessary dependencies installed.

## Simulation

Run a single PDE simulation by invoking the ``single_job.sh`` script with the required parameters or use the Python module directly, e.g.,

```bash
python -m pde_sim run configs/physics/gray_scott/default.yaml --log-file logs/physics/gray_scott.log --overwrite
```

To run multiple parameter combinations of the same PDE in parallel, use the ``batch_job.sh`` script, specifying the configuration file and the number of parallel jobs, e.g.,

```bash
sbatch batch_job.sh <base_config.yaml> <parameters.csv> [log_file] [start_row]
```

In all cases, make sure you specify a log file to capture the output of the simulation. Place the log file in the logs directory.
The output directory will contain the results of the simulation, including images and metadata.

## Analysis

After running simulations, analyze the results FOR EACH simulation and each parameter combination. Do not skip a simulation. In general, we are (1) checking for errors / warnings, (2) inspect the resulting images and see if the simulation produces interesting results/patterns. The changes per image should be visible but not too fast. For example, in a Gray-Scott simulation, you should see the emergence of patterns over time, not just a uniform color or an instantly occuring pattern.

1. Look at the generated log file to check for errors. Check if the simulation took too much time to run, perhaps indicating wrong parameter combinations.
2. Look at the metadata.json file in the output directory to see the parameters used for the simulation. Check the adaptive timestep information to see if the simulation was stable.
3. Look at the start image and some intermediate images in the output directory of **each simulation dir** to see if the simulation produced expected patterns.
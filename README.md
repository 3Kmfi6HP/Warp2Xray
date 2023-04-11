# Warp2Xray
Usage Guide:

- Ensure that you have the necessary dependencies installed before running the code, including Python 3 and the required modules (csv and json).

- Place the CSV file with the IP addresses in the same directory as the Python script.

- Modify the script variables to suit your needs, such as the maximum number of IP addresses to use, the load balancer strategy to employ, and the configuration file and output file names.

- Run the Python script. It will read the IP addresses from the CSV file, generate outbound configurations for each IP, generate a balancer configuration, and generate a complete configuration. Finally, the complete configuration will be written to a JSON file specified by the CONFIG_FILE variable.

- Copy the generated configuration file to the directory where your proxy application is installed, and use it as the configuration file for your proxy application.


# Check_GPIO_TE
Script used to read gpio states on units and sends info to QChub over MQTT

1)Open the TE unit you want to test in Balena and access the backend container

2)To send the file from computer to TE unit on the local network use SCP command:

scp juanquintana@10.0.0.157:/Users/juanquintana/Downloads/read_gpio_database1/read_gpio.py .

3)Once the file has been transferred we need to run it on the backend terminal of balena:

python read_gpio.py

4)Follow the instructions on the terminal and the data will be saved in the QChub:

At the moment its saved as a JSON format txt file and will be updated to do SQlite

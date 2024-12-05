import paramiko
import time

# Define variables for SSH connection
ssh_ip_address = '192.168.56.101'  # Example IP address of your network device
ssh_username = 'prne'              # SSH username
ssh_password = 'cisco123!'         # SSH password for login
ssh_password_enable = 'class123!'  # Enable password for privileged mode
ssh_new_hostname = 'R1'            # New hostname to set for the device

ssh_client = None  # Define globally to maintain the SSH client session

# Task 1: Establish SSH connection and modify the hostname
def ssh_connection():
    """
    This function establishes an SSH connection to the device,
    modifies the device hostname, and compares running and startup configurations.
    """
    global ssh_client  # Use the global variable for SSH client session
    try:
        # Initialize the SSH client and set policy to accept unknown host keys
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())  
        print("Establishing SSH connection...")

        # Attempt to connect to the device
        ssh_client.connect(ssh_ip_address, username=ssh_username, password=ssh_password, timeout=10)
        print("SSH connection established.")

        # Open an interactive shell session
        shell = ssh_client.invoke_shell()

        # Enter enable mode using the enable password
        shell.send('enable\n')
        time.sleep(1)
        shell.send(ssh_password_enable + '\n')
        time.sleep(1)

        # Enter configuration mode to change the hostname
        shell.send('configure terminal\n')
        time.sleep(1)

        # Change the hostname of the device
        shell.send(f'hostname {ssh_new_hostname}\n')
        time.sleep(1)

        # Save the configuration to memory
        shell.send('write memory\n')
        time.sleep(1)

        # Exit configuration mode
        shell.send('exit\n')
        time.sleep(1)
        shell.send('exit\n')  # Exit the interactive shell

        print(f"Device hostname changed to {ssh_new_hostname}.")

        # Task 2: Capture and compare Running and Startup Configurations
        stdin, stdout, stderr = ssh_client.exec_command('show running-config')
        running_config = stdout.read().decode('utf-8').splitlines()

        stdin, stdout, stderr = ssh_client.exec_command('show startup-config')
        startup_config = stdout.read().decode('utf-8').splitlines()

        # Display the differences between the Running and Startup Configurations
        print("\n-- Displaying Differences Between Running and Startup Configurations --")
        diff = difflib.unified_diff(startup_config, running_config, fromfile='Startup Config', tofile='Running Config', lineterm='')

        # Print the differences
        for line in diff:
            print(line)

        print("\n--  Comparison Completed  --")

    except Exception as e:
        print(f"Error: {e}")
        ssh_client = None  # Reset the SSH client if connection fails

# Task 3: Configure Loopback Interface and Routing Protocol (OSPF/EIGRP/RIP)
def configure_network_device():
    """
    This function configures a loopback interface and a routing protocol (e.g., OSPF).
    """
    if not ssh_client:
        print("Error: SSH client is not initialized. Please establish a connection first.")
        return  # Exit if the SSH connection is not established

    try:
        # Open an interactive shell session
        shell = ssh_client.invoke_shell()

        # Enter enable mode using the enable password
        shell.send('enable\n')
        time.sleep(1)
        shell.send(ssh_password_enable + '\n')
        time.sleep(1)

        # Enter configuration mode to set up the loopback interface
        shell.send('configure terminal\n')
        time.sleep(1)

        # Configure a loopback interface with IP address
        shell.send('interface loopback 0\n')
        shell.send('ip address 10.0.0.1 255.255.255.0\n')  # Example IP address for loopback interface
        shell.send('no shutdown\n')
        time.sleep(1)

        # Configure OSPF routing protocol (you can change to EIGRP/RIP if needed)
        shell.send('router ospf 1\n')
        shell.send('network 10.0.0.0 0.0.0.255 area 0\n')  # Example OSPF configuration
        time.sleep(1)

        # Save the configuration to memory
        shell.send('write memory\n')
        time.sleep(1)

        # Exit configuration mode
        shell.send('exit\n')
        time.sleep(1)
        shell.send('exit\n')  # Exit the interactive shell

        print("Loopback interface configured and OSPF routing protocol enabled.")

    except Exception as e:
        print(f"Error: {e}")
        ssh_client = None  # Reset the SSH client if any error occurs

# Main Menu to guide the user through available tasks
def main_menu():
    """
    This function presents a menu to the user to either establish an SSH connection,
    configure network devices, or exit the program.
    """
    while True:
        print("\n== Main Menu ====")
        print("1. Establish SSH connection and modify hostname")
        print("2. Configure loopback interface and routing protocol")
        print("3. Exit")
        choice = input("Enter your choice (1/2/3): ")

        # Task 1: Establish SSH connection and modify hostname
        if choice == '1':
            ssh_connection()
        
        # Task 2: Configure Loopback interface and routing protocol
        elif choice == '2':
            if ssh_client and ssh_client.get_transport() and ssh_client.get_transport().is_active():
                configure_network_device()
            else:
                print("Error: No existing SSH session. Please establish a connection first.")
        
        # Task 3: Exit the program
        elif choice == '3':
            print("Exiting...")
            break  # Exit the program

        # Invalid option
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")

# Run the main menu
main_menu()

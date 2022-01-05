#!/usr/bin/env bash

# This script installs and sets up mininet and ONOS as well as their dependencies on an Ubuntu machine

set -o errexit   # abort on nonzero exitstatus
set -o nounset   # abort on unbound variable
set -o pipefail  # don't hide errors within pipes

# Print script usage message
function_print_usage() {
  
  cat << EOF

Welcome to the GANSO dependency installer. Script usage:

    $> sudo ./ganso_dependency_installer.sh [OPTIONS]

Available options:
    -o              - Install ONOS
    -v ONOS_VERSION - Installs specified ONOS version (requires option "-o"!) e.g. -o 2.0.0
    -m              - Install mininet latest
    -t CUSTOM_TOPO  - Use custom mininet topology (requires option "-n"!) e.g. -t ./custom_topo.py -n customTopo
    -n TOPO_NAME    - Set name of the custom topo (requires option "-t"!) e.g. -t ./custom_topo.py -n customTopo
    -p              - Install packages bridge-utils, jq, openvswitch-switch, wget and curl if not found
    -h              - Shows this help message

Example:

    $> sudo ./ganso_dependency_installer.sh -o -v 2.4.0 # Install ONOS version 2.4.0
    $> sudo ./ganso_dependency_installer.sh -m -p # Install mininet and required packages
    $> sudo ./ganso_dependency_installer.sh -t ./custom_topo.py -n mytopo # Run mininet with topology customTopo in file custom_topo.py

EOF

  exit 0
}

# Clean and exit script
function_exit_script() {

    printf "\\n>>> Exiting GANSO environment.\\n"

    # Stop ONOS service
    printf "\\n>>> Stopping ONOS..."
    sudo /opt/onos/bin/onos-service stop > /dev/null 2>&1
    printf "Done!\\n"

    # Stop Open vSwitch and clean mininet
    printf "\\n>>> Cleaning mininet...\\n\\n"
    sudo systemctl stop openvswitch-switch
    sudo mn -c
    printf "\\n>>> Done!\\n\\n"

    exit 0
}

# Install environment's necessary dependencies
function_install_packages() {

    packages_to_install=("bridge-utils" "jq" "openvswitch-switch" "wget" "curl")

    printf "\\n>>> Checking necessary packages:\\n"

    # Check if a package is installed, install if not present
    for package in "${packages_to_install[@]}"; do

        printf "\\n\\t- Package ${package}: "

        if [[ $(apt -qq list --installed "${package}" 2> /dev/null) == *"installed"* ]]; then
            printf "Already installed!\\n"
        else
            printf "Not found! Installing...\\n\\n"
            sudo apt install "${package}" -y
        fi
    done
}


# Install and run ONOS and activate necessary apps
function function_onos_install_setup_and_run(){

    onos_apps=("drivers" "hostprovider" "lldpprovider" "gui2" "openflow-base" "openflow" "optical-model" "proxyarp" "fwd")
    onos_domain="127.0.0.1:8181/onos/v1"
    onos_running="false"

    onos_install="${1}"
    onos_version="${2}"

    # Stop ONOS if already running
    onos_pid=$(ps aux | grep 'onos' | grep '/usr/lib/jvm/java-11-openjdk-amd64/bin/java' | awk '{print $2}' || true)
    if [[ "${onos_pid}" != "" ]]; then sudo kill -9 "${onos_pid}"; fi

    if [ "${onos_install}" == "true" ]; then

        printf "\\n>>> Installing ONOS..."

        # Install specific ONOS version
        sudo rm -rf /opt/onos/
        sudo rm -rf /opt/onos*
        printf "\\n>>> Downloading ONOS version ${onos_version}, this might take a couple of minutes...\\n\\n"
        sudo wget -O /opt/onos.tar.gz -c "https://repo1.maven.org/maven2/org/onosproject/onos-releases/${onos_version}/onos-${onos_version}.tar.gz"

        if [ "$?" == "0" ]; then printf "\\n>>> ONOS downloaded! Unpacking...\\n"; else function_exit_script; fi
        
        sudo tar xzf /opt/onos.tar.gz -C /opt/
        sudo mv /opt/onos-"${onos_version}" /opt/onos
        sudo rm /opt/onos.tar.gz

        printf " Done!\\n\\n"
    fi

    printf "\\n>>> Starting ONOS, this might take a couple of minutes...\\n\\n"
    sudo /opt/onos/bin/onos-service start > /dev/null 2>&1 &

    # Wait until ONOS has been started
    while [ "${onos_running}" == "false" ]; do

        sleep 5

        printf "\\tChecking ONOS' status..."
        onos_status=$(curl -su "onos":"rocks" -X GET --header 'Accept: application/json' "http://${onos_domain}/docs/index.html" || true)

        if [[ "${onos_status}" == *"<title>ONOS API Docs</title>"* ]]; then
        
            printf "\\n\\n>>> ONOS running! Setting things up...\\n"
            sleep 10
            onos_running="true"
        else
            printf " Still starting, waiting 5 seconds...\\n"
        fi
    done

    # Check and activate necessary ONOS apps
    printf "\\n>>> Checking necessary ONOS apps:\\n"
    for app in "${onos_apps[@]}"; do
        app_id="org.onosproject.${app}"
        printf "\\t- App ${app_id}: "
        app_state=$(curl -u "onos":"rocks" -sX GET --header 'Accept: application/json' "http://${onos_domain}/applications/${app_id}" | jq .state | sed 's/"//g')

        if [ "${app_state}" != "ACTIVE" ]; then
            printf "Not active, activating...\\n"
            curl -u "onos":"rocks" -sX POST --header 'Accept: application/json' "http://${onos_domain}/applications/${app_id}/active" > /dev/null
            app_activated=$(curl -u "onos":"rocks" -sX GET --header 'Accept: application/json' "http://${onos_domain}/applications/${app_id}" | jq .state | sed 's/"//g')

            if [ "${app_activated}" != "ACTIVE" ]; then
                printf "\\t  >> App could not be activated, might need to be installed. \\n\\n>>> Stopping ONOS and exiting...\\n\\n"
                onos_pid=$(ps aux | grep 'onos' | grep '/usr/lib/jvm/java-11-openjdk-amd64/bin/java' | awk '{print $2}')
                sudo kill -9 "${onos_pid}"
                exit 99
            else
                printf "\\t Successful app activation!\\n"
            fi
        else
            printf "Already active!\\n"
        fi
    done
}


# Install, setup and run mininet
function_mininet_install_setup_and_run() {

    mn_install="${1}"
    mn_custom_topo_file="${2}"
    mn_custom_topo_name="${3}"

    if [ "${mn_install}" == "true" ]; then
        printf "\\n>>> Installing and setting up mininet... "

        # Check if a package is installed, install if not present
        if [[ $(apt -qq list --installed mininet 2> /dev/null) == *"installed"* ]]; then
            printf "Already installed!\\n\\n"
        else
            printf "Not found! Installing...\\n\\n"
            sudo apt install mininet -y
        fi
    fi

    printf "\\n>>> Starting mininet...\\n"

    # Start Open vSwitch and mininet
    sudo systemctl start openvswitch-switch

    if [ "${mn_custom_topo_file}" == "false" ] || [ "${mn_custom_topo_name}" == "false" ]; then
            
        printf "\\nsudo mn --controller remote,ip=127.0.0.1 --switch=ovs,protocols=OpenFlow13 --nat\\n\\n"
        sudo mn --controller remote,ip=127.0.0.1 --switch=ovs,protocols=OpenFlow13 --nat
        
    else
        printf "\\nsudo mn --custom "${mn_custom_topo_file}" --controller remote,ip=127.0.0.1 --switch=ovs,protocols=OpenFlow13 --nat --topo "${mn_custom_topo_name}"\\n\\n"
        sudo mn --custom "${mn_custom_topo_file}" --controller remote,ip=127.0.0.1 --switch=ovs,protocols=OpenFlow13 --nat --topo "${mn_custom_topo_name}"
    fi
}


main () {

    if [ "$(whoami)" != "root" ]; then 
        printf "\\n>>> You need root priviledges to run this script, please run with \'sudo\'\\n\\n>>> Exiting...\\n\\n"
        exit 1
    fi

    # Set variables
    onos_install="false"
    onos_version="2.3.0"
    mn_install="false"
    mn_custom_topo_file="false"
    mn_custom_topo_name="false"
    packages_install="false"

    # Get script set options
    while getopts 'ov:mt:n:p' flag; do
        case "${flag}" in
            o) onos_install="true" ;;
            v) onos_version="${OPTARG}" ;;
            m) mn_install="true" ;;
            t) mn_custom_topo_file="${OPTARG}" ;;
            n) mn_custom_topo_name="${OPTARG}" ;;
            p) packages_install="true" ;;
            *) function_print_usage
            exit 1 ;;
        esac
    done

    if [ "${mn_custom_topo_file}" != "false" ] || [ "${mn_custom_topo_name}" != "false" ]; then
        if [ "${mn_custom_topo_file}" == "false" ] || [ "${mn_custom_topo_name}" == "false" ]; then
            printf "\\n>>> Please use -t CUSTOM_TOPO and -n TOPO_NAME simultaneously\\n\\n>>> Exiting...\\n\\n"
            exit 1
        fi
    fi

    # Install environment's required packages
    if [ "${packages_install}" == "true" ]; then function_install_packages; fi

    # Install and set up ONOS
    function_onos_install_setup_and_run "${onos_install}" "${onos_version}"

    # Install and set up mininet
    function_mininet_install_setup_and_run "${mn_install}" "${mn_custom_topo_file}" "${mn_custom_topo_name}"

    # Exit script gracefully
    function_exit_script

}

main "$@"
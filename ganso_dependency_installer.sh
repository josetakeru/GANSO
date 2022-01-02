#!/usr/bin/env bash

# This script installs and sets up mininet and ONOS as well as their dependencies on an Ubuntu machine

# Print script usage message
function_print_usage() {
  
  cat << EOF

Welcome to the GANSO dependency installer. Script usage:

    $> sudo ./ganso_dependency_installer.sh [OPTIONS]

Available options:
    -o ONOS_VERSION - Installs specified ONOS version e.g. -o 2.0.0
    -s              - Stop ONOS upon exit
    -h              - Shows this help message

Example:

    $> sudo ./ganso_dependency_installer.sh -o 2.4.0 # Install dependencies, with ONOS version 2.4.0

EOF

  exit 0
}


# Clean and exit script
function_exit_script() {

    # Stop ONOS service
    if [ "${1}" == "true" ]; then
        sudo /opt/onos/bin/onos-service stop > /dev/null 2>&1
        printf "\\nONOS has been stopped.\\n"
    fi

    printf "\\nExiting...\\n\\n"
    exit 0
}


# Install mininet and GANSO necessary dependencies
function_install_packages() {

    packages_to_install=("mininet" "bridge-utils" "jq" "openvswitch-switch" "wget" "curl")

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

    # Start Open vSwitch
    sudo systemctl start openvswitch-switch

}

# Install ONOS and activate necessary apps
function function_onos_install_and_setup(){

    apps_to_install=("drivers" "hostprovider" "lldpprovider" "gui2" "openflow-base" "openflow" "optical-model" "proxyarp" "fwd")
    onos_domain="127.0.0.1:8181/onos/v1"
    onos_version="${1}"
    onos_running="false"

    # Install specific ONOS version
    sudo rm -rf /opt/onos/
    sudo rm -rf /opt/onos*
    printf "\\n>>> Downloading ONOS version ${onos_version}, this might take a couple of minutes...\\n\\n"
    sudo wget -O /opt/onos.tar.gz -c "https://repo1.maven.org/maven2/org/onosproject/onos-releases/${onos_version}/onos-${onos_version}.tar.gz"

    if [ "$?" == "0" ]; then printf "\\n>>> ONOS downloaded! Unpacking...\\n"; else function_exit_script; fi
    
    sudo tar xzf /opt/onos.tar.gz -C /opt/
    sudo mv /opt/onos-"${onos_version}" /opt/onos
    sudo rm /opt/onos.tar.gz

    printf "\\n>>> Starting ONOS, this might take a couple of minutes...\\n\\n"
    sudo /opt/onos/bin/onos-service start > /dev/null 2>&1 &

    # Wait until ONOS has been started
    while [ "${onos_running}" == "false" ]; do

        sleep 10

        printf "\\tChecking ONOS' status..."
        onos_status=$(curl -su "onos":"rocks" -X GET --header 'Accept: application/json' "http://${onos_domain}/docs/index.html")

        if [[ "${onos_status}" == *"<title>ONOS API Docs</title>"* ]]; then
        
            printf "\\n\\n>>> ONOS running! Setting things up...\\n"
            sleep 10
            onos_running="true"
        else
            printf " Still starting, waiting 10 seconds...\\n"
        fi
    done

    # Check and activate necessary ONOS apps
    printf "\\n>>> Checking necessary ONOS apps:\\n"
    for app in "${apps_to_install[@]}"; do
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


main () {

    # Set variables
    onos_version="2.3.0"
    stop_onos="false"

    # Get script set options
    while getopts 'hso:' flag; do
        case "${flag}" in
            o) onos_version="${OPTARG}" ;;
            s) stop_onos="true" ;;
            *) function_print_usage
            exit 1 ;;
        esac
    done

    # Install mininet and ONOS required packages
    function_install_packages

    # Install and set up ONOS
    function_onos_install_and_setup "${onos_version}"

    # Exit script gracefully
    function_exit_script "${stop_onos}"

}

main "$@"
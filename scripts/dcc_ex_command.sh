#!/bin/bash

usage() {
    echo "Usage: $0 -c <command_type> -v <command_value> -a <ip_address> -p <port>"
    exit 1
}

while getopts "c:v:a:p:" opt; do
    case "$opt" in
        c) COMMAND_TYPE="$OPTARG" ;;
        v) COMMAND_VALUE="$OPTARG" ;;
        a) DCC_EX_SERVER_IP="$OPTARG" ;;
        p) DCC_EX_SERVER_PORT="$OPTARG" ;;
        *) usage ;;
    esac
done

if [ -z "$COMMAND_TYPE" ] || [ -z "$DCC_EX_SERVER_IP" ] || [ -z "$DCC_EX_SERVER_PORT" ]; then
    usage
fi

case "$COMMAND_TYPE" in
    "volume")
        if [ -z "$COMMAND_VALUE" ]; then
            echo "Volume command requires a volume level (0.0 to 1.0)."
            exit 1
        fi
        if (( $(echo "$COMMAND_VALUE < 0.0" | bc -l) || $(echo "$COMMAND_VALUE > 1.0" | bc -l) )); then
            echo "Volume level must be between 0.0 and 1.0."
            exit 1
        fi

        # Calculate the volume value 0-64
        VOLUME_VAL_64=$(printf "%.0f" "$(echo "$COMMAND_VALUE * 64" | bc -l)")
        COMMAND="<w 4 63 $VOLUME_VAL_64>"   # Vossloh volume set (CV63)
        ;;
    "power")
        if [ "$COMMAND_VALUE" = "on" ]; then
            COMMAND="<1>"
        elif [ "$COMMAND_VALUE" = "off" ]; then
            COMMAND="<0>"
        else
            echo "Invalid power command. Use 'on' or 'off'."
            exit 1
        fi
        ;;
    *)
        echo "Invalid command type."
        exit 1
        ;;
esac

echo "Command: $COMMAND"
echo "$COMMAND" | nc "$DCC_EX_SERVER_IP" "$DCC_EX_SERVER_PORT"
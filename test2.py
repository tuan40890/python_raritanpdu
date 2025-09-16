        # retrieve outlet data and display output using pandas
        outlet_data = [
        {
            "Watts": int(outlet.getSensors().activePower.getReading().value),
            "Outlet": outlet.getMetaData().label,
            "Type": outlet.getMetaData().receptacleType[-3:],
            "Status": str(outlet.getState().powerState).split("_")[-1],
            "Name": outlet.getSettings().name
        }
        for outlet in pdu.getOutlets()]

        if outlet_data:
            # Create DataFrame directly from the list of dictionaries
            df = pd.DataFrame(outlet_data)
            display_output.append("[OUTLET INFO]")
            display_output.append(df.to_string(index=False, justify="left"))

            inlet_power = pdu.getInlets()[-1].getSensors().activePower.getReading().value
            display_output.append(f"----------------------------\nTotal Active Power: {inlet_power:.2f} W\n")
            display_output.append("-------------------------------------------------------------------------------\n")
            ip_with_underscore = ip.replace(".", "_")
            output_file_name = f"pdu_{retrieve_hostname}_{ip_with_underscore}.txt"
            display_output.append(f"PDU output for {retrieve_hostname} is saved to '{output_file_name}'\n")
        else:
            display_output.append("\tNo outlets found.")

import pandas as pd

display_output = []

def test():
    all_outlets_data = []


    # loop over each outlet to obtain settings
    for outlet in range(5):

        # set variables to retrieve outlet data
        retrieve_outlet_watts = outlet
        retrieve_outlet_label = outlet
        retrieve_outlet_receptacletype = outlet
        retrieve_outlet_status = outlet
        retrieve_outlet_description = outlet

        # add data to the existing empty all_outlets_data list
        current_outlet_data_to_be_added = {
                "Watts": retrieve_outlet_watts,
                "Outlet": retrieve_outlet_label,
                "Type": retrieve_outlet_receptacletype,
                "Status": retrieve_outlet_status,
                "Description": retrieve_outlet_description
                }
        
        # add all outputs to all_outlets_data
        all_outlets_data.append(current_outlet_data_to_be_added)

    # create DataFrame directly from the dictionaries
    # tell Pandas not to print the DataFrame's index (the row numbers) in the output
    # also align the column headers in the center
    df = pd.DataFrame(all_outlets_data)
    display_output.append(df.to_string(index=False, justify="left"))
    print("\n".join(display_output))

if __name__ == "__main__":
    test()

import math
import argparse
import json

def calculate_attenuation(tx_power, rx_power):
    # Calculate the ratio
    ratio = tx_power / rx_power

    # Calculate the loss in dB
    rx_attenuation_dBm = 10 * math.log10(ratio)

    # Calculate the loss in mW
    rx_attenuation_mW =  rx_power - tx_power

    return rx_attenuation_dBm, rx_attenuation_mW

def calculate_loss_budget(fiber_type, wavelength, fiber_length, num_connectors, num_splices):
    # Define loss values
    connector_loss = 0.75  # dB per mated connector pair
    splice_loss = 0.3  # dB per splice

    # Define fiber loss values based on type and wavelength
    if fiber_type == "multimode":
        if wavelength == 850:
            fiber_loss = 3.5  # dB per km
        elif wavelength == 1300:
            fiber_loss = 1.5  # dB per km
    elif fiber_type == "singlemode":
        if wavelength == 1310 or wavelength == 1550:
            fiber_loss = 1.0  # dB per km

    # Calculate total loss budget
    total_loss_budget = (fiber_loss * (fiber_length / 1000)) + (connector_loss * num_connectors) + (splice_loss * num_splices)

    return total_loss_budget

def main():
 
    parser = argparse.ArgumentParser(description="Calculate optical loss and evaluate against loss budget.")
    parser.add_argument("--tx", type=float, required=False, help="TX power in mW") # valid decimal positive number
    parser.add_argument("--rx", type=float, required=False, help="RX power in mW") # valid decimal positive number
    parser.add_argument("--tx_dbm", type=float, required=False, help="TX power in dBm") # valid decimal positive or positive dBm value
    parser.add_argument("--rx_dbm", type=float, required=False, help="RX power in dBm") # valid decimal positive or positive dBm value
    parser.add_argument("--min_rx_dbm", type=float, required=False, help="Target minimum RX dBm. Default -5dBm") # valid decimal positive or positive dBm value
    parser.add_argument("--max_rx_dbm", type=float, required=False, help="Target maximum RX dBm. Default +5dBm") # valid decimal positive or positive dBm value
    parser.add_argument("--fiber_type", choices=["s", "m"], help="Fiber type: 's' for singlemode, 'm' for multimode") # Valid s or m only, s = singlemode, m = multimode
    parser.add_argument("--wavelength", type=int, choices=[850, 1300, 1310, 1550], help="Wavelength in nm") # Valid 850 or 1300 for multimode, 1310 or 1550 for singlemode
    parser.add_argument("--fiber_length", type=float, help="Total length of the fiber in meters") # Valid 1 or more
    parser.add_argument("--num_connectors", type=int, help="Number of mated connectors") # Valid 0 or more
    parser.add_argument("--num_splices", type=int, help="Number of splices") # Valid 0 or more
    parser.add_argument("--json", action="store_true", help="Output as JSON")

    args = parser.parse_args()
    
    # If tx_dbm is not provided, calculate it from tx
    if args.tx_dbm is None and args.tx is not None:
        args.tx_dbm = 10 * math.log10(args.tx)
    elif args.tx_dbm is not None and args.tx is None:
    # If tx is not provided, calculate it from tx_dbm
        args.tx = 10 ** (args.tx_dbm / 10)
    else:
        # Else if both tx and tx_dbm are not provided, quit
        print("Please provide either tx or tx_dbm")
        quit(1)
    
    # If rx_dbm is not provided, calculate it from rx
    if args.rx_dbm is None and args.rx is not None:
        args.rx_dbm = 10 * math.log10(args.rx)
    elif args.rx_dbm is not None and args.rx is None:
    # If rx is not provided, calculate it from rx_dbm
        args.rx = 10 ** (args.rx_dbm / 10)
    else:
        # Else if both rx and rx_dbm are not provided, quit
        print("Please provide either rx or rx_dbm")
        quit(1)
        
    # If min_rx_dbm is not provided, set it to -5dBm
    if args.min_rx_dbm is None:
        args.min_rx_dbm = -5
    # If max_rx_dbm is not provided, set it to +5dBm
    if args.max_rx_dbm is None:
        args.max_rx_dbm = 5
            
    # Calculate the loss
    rx_attenuation_dBm, rx_attenuation_mW = calculate_attenuation(args.tx, args.rx)

    attenuation_combined = f"{abs(rx_attenuation_mW):.4f} mW / -{abs(rx_attenuation_dBm):.2f} dBm"

    # Validate against loss budget if all required arguments are provided
    if args.fiber_type and args.wavelength and args.fiber_length is not None:
        num_connectors = 0 if args.num_connectors is None else args.num_connectors
        num_splices = 0 if args.num_splices is None else args.num_splices
        fiber_type = "singlemode" if args.fiber_type == 's' else "multimode"
        loss_budget = calculate_loss_budget(fiber_type, args.wavelength, args.fiber_length, num_connectors, num_splices)

        if abs(rx_attenuation_dBm) <= loss_budget:
            evaluation = "PASS"
            evaluation_detail = f"Attenuation of {attenuation_combined} is within the calculated TIA-568 maximum loss budget of {loss_budget:.2f} dBm."
        else:
            excess_percentage = ((abs(rx_attenuation_dBm) - loss_budget) / loss_budget) * 100
            evaluation = "FAIL"
            evaluation_detail = f"Attenuation of {attenuation_combined} exceeds the calculated TIA-568 maximum loss budget of {loss_budget:.2f} dBm by {excess_percentage:.2f}%."

        summary = {
            "TX Power mW": f"{abs(args.tx):.4f}",
            "TX Power dBm": f"{(args.tx_dbm):.2f}",
            "RX Power mW": f"{abs(args.rx):.4f}",
            "RX Power dBm": f"{(args.rx_dbm):.2f}",
            "RX Attenuation mW": f"{(rx_attenuation_mW):.4f}",
            "RX Attenuation dBm": f"{abs(rx_attenuation_dBm):.2f}",
            "Fiber Type": fiber_type,
            "Fiber Wavelength": f"{args.wavelength}",
            "Fiber Length Meters": f"{args.fiber_length}",
            "Number of Mated Connectors": num_connectors,
            "Number of Splices": num_splices,
            "TIA-568 dBm Max Loss Budget": f"{loss_budget:.2f}",
            "TIA-568 Evaluation": evaluation,
            "TIA-568 Detail": evaluation_detail
        }
    else:
        summary = {
            "TX Power mW": f"{abs(args.tx):.4f}",
            "TX Power dBm": f"{(args.tx_dbm):.2f}",
            "RX Power mW": f"{abs(args.rx):.4f}",
            "RX Power dBm": f"{(args.rx_dbm):.2f}",
            "RX Attenuation mW": f"{(rx_attenuation_mW):.4f}",
            "RX Attenuation dBm": f"{abs(rx_attenuation_dBm):.2f}",
            }

    if args.json:
        summary = {key.replace(" ", "_"): str(value).replace(" ", "") if key != "TIA-568 Detail" else str(value) for key, value in summary.items()}
        print(json.dumps(summary, indent=4))
        quit(0)
    else:
        print("\nSummary of Inputs and Attenuation:")
        for key, value in summary.items():
            print(f"    {key}: {value}")
        print("\n")
        quit(0)

if __name__ == "__main__":
    main()

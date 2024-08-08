import math
import argparse
import json

def calculate_loss(transmit_power, receive_power):
    # Calculate the ratio
    ratio = transmit_power / receive_power

    # Calculate the loss in dB
    loss_dB = 10 * math.log10(ratio)

    # Calculate the loss in mW
    loss_mW = transmit_power - receive_power

    return loss_dB, loss_mW

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
    """
    Calculate optical loss and validate against loss budget.

    Args:
        --tx_power (float): Transmission power in mW (valid decimal positive number).
        --rx_power (float): Received power in mW (valid decimal positive number).
        --fiber_type (str): Fiber type: 's' for singlemode, 'm' for multimode (valid 's' or 'm' only).
        --wavelength (int): Wavelength in nm (valid 850 or 1300 for multimode, 1310 or 1550 for singlemode).
        --fiber_length (float): Total length of the fiber in meters (valid 1 or more).
        --num_connectors (int): Number of mated connectors (valid 0 or more).
        --num_splices (int): Number of splices (valid 0 or more).
        --json (bool): Output results as JSON.

    Returns:
        None

    Prints:
        Summary of Inputs and Results if --json is not provided.
        JSON representation of the summary if --json is provided.
    """
    parser = argparse.ArgumentParser(description="Calculate optical loss and validate against loss budget.")
    parser.add_argument("--tx_power", type=float, required=True, help="Transmission power in mW") #valid decimal positive number
    parser.add_argument("--rx_power", type=float, required=True, help="Received power in mW") # valid decimal positive number
    parser.add_argument("--fiber_type", choices=["s", "m"], help="Fiber type: 's' for singlemode, 'm' for multimode") # Valid s or m only, s = singlemode, m = multimode
    parser.add_argument("--wavelength", type=int, choices=[850, 1300, 1310, 1550], help="Wavelength in nm") # Valid 850 or 1300 for multimode, 1310 or 1550 for singlemode
    parser.add_argument("--fiber_length", type=float, help="Total length of the fiber in meters") # Valid 1 or more
    parser.add_argument("--num_connectors", type=int, help="Number of mated connectors") # Valid 0 or more
    parser.add_argument("--num_splices", type=int, help="Number of splices") # Valid 0 or more
    parser.add_argument("--json", action="store_true", help="Output results as JSON")

    args = parser.parse_args()

    # Calculate the loss
    loss_dB, loss_mW = calculate_loss(args.tx_power, args.rx_power)

    # Determine if it's a loss or gain
    if loss_mW > 0:
        result = f"-{abs(loss_mW):.4f} mW / +{abs(loss_dB):.2f} dBm loss"
    else:
        if loss_mW == 0:
            result = f"0.0000 mW / 0.00 dBm"
        else:
            result = f"{abs(loss_mW):.4f} mW / -{abs(loss_dB):.2f} dBm gain"

    # Validate against loss budget if all required arguments are provided
    if args.fiber_type and args.wavelength and args.fiber_length is not None and args.num_connectors is not None and args.num_splices is not None:
        fiber_type = "singlemode" if args.fiber_type == 's' else "multimode"
        loss_budget = calculate_loss_budget(fiber_type, args.wavelength, args.fiber_length, args.num_connectors, args.num_splices)

        if abs(loss_dB) <= loss_budget:
            validation_result = f"The observed loss of {result} is within the acceptable loss budget of {loss_budget:.2f}."
        else:
            excess_percentage = ((abs(loss_dB) - loss_budget) / loss_budget) * 100
            validation_result = f"The observed loss of {result} exceeds the acceptable loss budget of {loss_budget:.2f} dB by {excess_percentage:.2f}%."

        summary = {
            "Transmission Power": f"{args.tx_power} mW",
            "Received Power": f"{args.rx_power} mW",
            "Observed Loss": result,
            "Fiber Type": fiber_type,
            "Wavelength": f"{args.wavelength} nm",
            "Fiber Length": f"{args.fiber_length} meters",
            "Number of Mated Connectors": args.num_connectors,
            "Number of Splices": args.num_splices,
            "Calculated Loss Budget": f"{loss_budget:.2f} dB",
            "Validation Result": validation_result
        }
    else:
        summary = {
            "Transmission Power": f"{args.tx_power} mW",
            "Received Power": f"{args.rx_power} mW",
            "Observed Loss": result
        }

    if args.json:
        print(json.dumps(summary, indent=4))
    else:
        print("\nSummary of Inputs and Results:")
        for key, value in summary.items():
            print(f"    {key}: {value}")
        print("\n")

if __name__ == "__main__":
    main()

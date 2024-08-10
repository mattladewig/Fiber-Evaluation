import math
import argparse
import json
import math

# MIT License
# Copyright (c) [2024] [Matt Ladewig]


def calculate_attenuation(tx_power, rx_power):
    # Calculate the ratio
    ratio = tx_power / rx_power

    # Calculate the loss in dB
    rx_attenuation_dBm = 10 * math.log10(ratio)

    # Calculate the loss in mW
    rx_attenuation_mW = rx_power - tx_power

    return rx_attenuation_dBm, rx_attenuation_mW


def calculate_loss_budget_max_dbm(
    fiber_type, wavelength, fiber_length, num_connectors, num_splices
):
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
    total_loss_budget_max_dbm = (
        (fiber_loss * (fiber_length / 1000))
        + (connector_loss * num_connectors)
        + (splice_loss * num_splices)
    )

    return total_loss_budget_max_dbm


def calculate_loss_budget_typical_dbm(
    fiber_type, wavelength, fiber_length, num_connectors, num_splices
):
    # Define loss values
    connector_loss = 0.3  # dB per mated connector pair
    splice_loss = 0.3  # dB per splice

    # Define fiber loss values based on type and wavelength
    if fiber_type == "multimode":
        if wavelength == 850:
            fiber_loss = 3  # dB per km
        elif wavelength == 1300:
            fiber_loss = 1  # dB per km
    elif fiber_type == "singlemode":
        if wavelength == 1310 or wavelength == 1550:
            fiber_loss = 0.5  # dB per km

    # Calculate total loss budget
    total_loss_budget_typical_dbm = (
        (fiber_loss * (fiber_length / 1000))
        + (connector_loss * num_connectors)
        + (splice_loss * num_splices)
    )

    return total_loss_budget_typical_dbm


def validate_inputs(args):
    error = {}
    missing_input = []
    invalid_input = []
    """
    Validates the input arguments for the fiber evaluation program.

    Args:
        args (object): The input arguments object.

    Returns:
        error (str): The error message if any.

    Notes:
        - This function checks if the required input arguments are provided.
        - It checks for specific conditions and raises an error if they are violated.
    """
    # Else if both tx and tx_dbm are not provided, quit
    if args.tx_dbm is None and args.tx is None:
        missing_input.append("--tx or --tx_dbm")
    # Else if both rx and rx_dbm are not provided, quit
    if args.rx_dbm is None and args.rx is None:
        missing_input.append("--rx or --rx_dbm")
    if (
        args.wavelength is None or args.fiber_length is None or args.fiber_type is None
    ) and (
        args.wavelength is not None
        or args.fiber_length is not None
        or args.fiber_type is not None
    ):
        if args.fiber_type is None:
            missing_input.append("--fiber_type")
        if args.wavelength is None:
            missing_input.append("--wavelength")
        if args.fiber_length is None:
            missing_input.append("--fiber_length")
        if args.fiber_type == "s" and args.wavelength == 850:
            invalid_input.append("Singlemode fiber does not support 850nm wavelength.")
        if args.fiber_type == "s" and args.wavelength == 1300:
            invalid_input.append("Singlemode fiber does not support 1300nm wavelength.")
        if args.fiber_type == "m" and args.wavelength == 1310:
            invalid_input.append("Multimode fiber does not support 1310nm wavelength.")
        if args.fiber_type == "m" and args.wavelength == 1550:
            invalid_input.append("Multimode fiber does not support 1550nm wavelength.")
        if missing_input:
            error["missing_input"] = missing_input
        if invalid_input:
            error["invalid_input"] = invalid_input
        if error != {}:
            return error


def format_results(power_eval, loss_eval):
    """
    Prints the evaluation results in a formatted manner.

    Args:
        power_eval (dict): Dictionary containing power evaluation results.
        loss_eval (dict): Dictionary containing loss evaluation results.
    """
    power_eval = {
        key.replace(" ", "_"): (
            str(value).replace(" ", "") if key != "Findings" else str(value)
        )
        for key, value in power_eval.items()
    }
    if loss_eval is not None:
        loss_eval = {
            key.replace(" ", "_"): (
                str(value).replace(" ", "") if key != "Findings" else str(value)
            )
            for key, value in loss_eval.items()
        }
        print(json.dumps({"power_eval": power_eval, "loss_eval": loss_eval}, indent=4))
    else:
        print(json.dumps({"power_eval": power_eval}, indent=4))
    quit(0)


def main():
    loss_eval = None
    power_eval = None
    parser = argparse.ArgumentParser(
        description="Calculate optical loss and evaluate against loss budget."
    )
    parser.add_argument(
        "--tx", type=float, required=False, help="TX power in mW"
    )  # valid decimal positive number
    parser.add_argument(
        "--rx", type=float, required=False, help="RX power in mW"
    )  # valid decimal positive number
    parser.add_argument(
        "--tx_dbm", type=float, required=False, help="TX power in dBm"
    )  # valid decimal positive or positive dBm value
    parser.add_argument(
        "--rx_dbm", type=float, required=False, help="RX power in dBm"
    )  # valid decimal positive or positive dBm value
    parser.add_argument(
        "--rx_target_min_dbm",
        type=float,
        required=False,
        help="Target minimum RX dBm. Default -5dBm",
    )  # valid decimal positive or positive dBm value
    parser.add_argument(
        "--rx_target_max_dbm",
        type=float,
        required=False,
        help="Target maximum RX dBm. Default +1dBm",
    )  # valid decimal positive or positive dBm value
    parser.add_argument(
        "--fiber_type",
        choices=["s", "m"],
        help="Fiber type: 's' for singlemode, 'm' for multimode",
    )  # Valid s or m only, s = singlemode, m = multimode
    parser.add_argument(
        "--wavelength",
        type=int,
        choices=[850, 1300, 1310, 1550],
        help="Wavelength in nm",
    )  # Valid 850 or 1300 for multimode, 1310 or 1550 for singlemode
    parser.add_argument(
        "--fiber_length", type=float, help="Total length of the fiber in meters"
    )  # Valid 1 or more
    parser.add_argument(
        "--num_connectors", type=int, help="Number of mated connectors"
    )  # Valid empty or more
    parser.add_argument(
        "--num_splices", type=int, help="Number of splices"
    )  # Valid empty or more
    parser.add_argument("--json", action="store_true", help="Output as JSON")

    args = parser.parse_args()

    error = validate_inputs(args)

    if error:
        print(json.dumps({"error": error}, indent=4))
        quit(1)

    # setup var for further work
    # If tx_dbm is not provided, calculate it from tx
    if args.tx_dbm is None and args.tx is not None:
        args.tx_dbm = 10 * math.log10(args.tx)

    # If tx is not provided, calculate it from tx_dbm
    elif args.tx_dbm is not None and args.tx is None:
        args.tx = 10 ** (args.tx_dbm / 10)

    # If rx_dbm is not provided, calculate it from rx
    if args.rx_dbm is None and args.rx is not None:
        args.rx_dbm = 10 * math.log10(args.rx)

    # If rx is not provided, calculate it from rx_dbm
    elif args.rx_dbm is not None and args.rx is None:
        args.rx = 10 ** (args.rx_dbm / 10)

    fiber_type = "singlemode" if args.fiber_type == "s" else "multimode"

    num_connectors = 0 if args.num_connectors is None else args.num_connectors

    num_splices = 0 if args.num_splices is None else args.num_splices

    # If rx_target_min_dbm is not provided, set it to -5dBm
    if args.rx_target_min_dbm is None:
        args.rx_target_min_dbm = -5

    # If rx_target_max_dbm is not provided, set it to +1dBm
    if args.rx_target_max_dbm is None:
        args.rx_target_max_dbm = 1

    # Calculate the RX attenuation
    rx_attenuation_dBm, rx_attenuation_mW = calculate_attenuation(args.tx, args.rx)

    attenuation_combined = (
        f"{(rx_attenuation_mW):.4f} mW / {(rx_attenuation_dBm):.2f} dBm"
    )
    # Create power evaluation report
    power_eval = {
        "TX mW": f"{abs(args.tx):.4f}",
        "TX dBm": f"{(args.tx_dbm):.2f}",
        "RX mW": f"{abs(args.rx):.4f}",
        "RX dBm": f"{(args.rx_dbm):.2f}",
        "RX Attenuation mW": f"{(rx_attenuation_mW):.4f}",
        "RX Attenuation dBm": f"{abs(rx_attenuation_dBm):.2f}",
        "RX Min dBm": f"{args.rx_target_min_dbm:.2f}",
        "RX Max dBm": f"{args.rx_target_max_dbm:.2f}",
    }
    # Begin loss evaluation
    if (
        args.fiber_type is not None
        and args.wavelength is not None
        and args.fiber_length is not None
    ):
        loss_budget_max_dbm = calculate_loss_budget_max_dbm(
            fiber_type,
            args.wavelength,
            args.fiber_length,
            num_connectors,
            num_splices,
        )
        loss_budget_typical_dbm = calculate_loss_budget_typical_dbm(
            fiber_type,
            args.wavelength,
            args.fiber_length,
            num_connectors,
            num_splices,
        )

        if rx_attenuation_dBm <= loss_budget_typical_dbm:
            evaluation = "PASS"
            evaluation_detail = f"Attenuation of {attenuation_combined} is less then both the calculated typical loss budget of {loss_budget_typical_dbm:.2f} dBm and the TIA-568 maximum of {loss_budget_max_dbm:.2f} dBm."

        elif (
            rx_attenuation_dBm > loss_budget_typical_dbm
            and rx_attenuation_dBm <= loss_budget_max_dbm
        ):
            evaluation = "WARN"
            evaluation_detail = f"Attenuation of {attenuation_combined} is higher then the calculated typical loss budget of {loss_budget_typical_dbm:.2f} dBm but less then the TIA-568 maximum of {loss_budget_max_dbm:.2f} dBm."
        else:
            excess_percentage = (
                (abs(rx_attenuation_dBm) - loss_budget_max_dbm) / loss_budget_max_dbm
            ) * 100
            evaluation = "FAIL"
            evaluation_detail = f"Attenuation of {attenuation_combined} exceeds the calculated TIA-568 maximum loss budget of {loss_budget_max_dbm:.2f} dBm by {excess_percentage:.2f}%."

        loss_eval = {
            "Fiber Type": fiber_type,
            "Fiber Wavelength": f"{args.wavelength}",
            "Fiber Length Meters": f"{args.fiber_length}",
            "Number of Mated Connectors": num_connectors,
            "Number of Splices": num_splices,
            "RX Attenuation mW": f"{(rx_attenuation_mW):.4f}",
            "RX Attenuation dBm": f"{abs(rx_attenuation_dBm):.2f}",
            "Typical Loss Budget dBm": f"{loss_budget_typical_dbm:.2f}",
            "TIA-568 Max Loss Budget dBm": f"{loss_budget_max_dbm:.2f}",
            "Result": evaluation,
            "Findings": evaluation_detail,
        }

    format_results(power_eval, loss_eval)


if __name__ == "__main__":
    main()

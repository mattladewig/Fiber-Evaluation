import unittest
from unittest.mock import patch
from io import StringIO
import json
import db_loss_calc

class TestMain(unittest.TestCase):

    def test_main_with_valid_arguments(self):
        args = ["--tx", "1.5", "--rx", "0.5", "--fiber_type", "s", "--wavelength", "1310", "--fiber_length", "1000", "--num_connectors", "2", "--num_splices", "1"]
        expected_output = "\nSummary of Inputs and Attenuation:\n    TX Power mW: 1.5000\n    TX Power dBm: 1.76\n    RX Power mW: 0.5000\n    RX Power dBm: -3.01\n    RX Attenuation mW: 1.0000\n    RX Attenuation dBm: 4.77\n    Fiber Type: singlemode\n    Fiber Wavelength: 1310\n    Fiber Length Meters: 1000\n    Number of Mated Connectors: 2\n    Number of Splices: 1\n    TIA-568 dBm Max Loss Budget: 4.20\n    TIA-568 Evaluation: FAIL\n    TIA-568 Detail: Attenuation of 1.0000 mW / -4.77 dBm exceeds the calculated TIA-568 maximum loss budget of 4.20 dBm by 13.57%.\n\n"

        with patch("sys.stdout", new=StringIO()) as fake_out:
            with patch("sys.argv", ["db_loss_calc.py"] + args):
                db_loss_calc.main()
                self.assertEqual(fake_out.getvalue(), expected_output)

    def test_main_with_missing_arguments(self):
        args = ["--tx", "1.5", "--rx", "0.5", "--fiber_type", "s", "--wavelength", "1310"]
        expected_output = "Please provide either tx or tx_dbm\n"

        with patch("sys.stdout", new=StringIO()) as fake_out:
            with patch("sys.argv", ["db_loss_calc.py"] + args):
                db_loss_calc.main()
                self.assertEqual(fake_out.getvalue(), expected_output)

    def test_main_with_json_output(self):
        args = ["--tx", "1.5", "--rx", "0.5", "--fiber_type", "s", "--wavelength", "1310", "--fiber_length", "1000", "--num_connectors", "2", "--num_splices", "1", "--json"]
        expected_output = {
            "TX_Power_mW": "1.5000",
            "TX_Power_dBm": "1.76",
            "RX_Power_mW": "0.5000",
            "RX_Power_dBm": "-3.01",
            "RX_Attenuation_mW": "1.0000",
            "RX_Attenuation_dBm": "4.77",
            "Fiber_Type": "singlemode",
            "Fiber_Wavelength": "1310",
            "Fiber_Length_Meters": "1000",
            "Number_of_Mated_Connectors": "2",
            "Number_of_Splices": "1",
            "TIA-568_dBm_Max_Loss_Budget": "4.20",
            "TIA-568_Evaluation": "FAIL",
            "TIA-568_Detail": "Attenuation of 1.0000 mW / -4.77 dBm exceeds the calculated TIA-568 maximum loss budget of 4.20 dBm by 13.57%."
        }

        with patch("sys.stdout", new=StringIO()) as fake_out:
            with patch("sys.argv", ["db_loss_calc.py"] + args):
                db_loss_calc.main()
                self.assertEqual(json.loads(fake_out.getvalue()), expected_output)

if __name__ == "__main__":
    unittest.main()
from unittest import TestCase
from processor import process_nem12_file

class TestProcessor(TestCase):

    def test_process_valid_nem12_file(self):
        input_file = 'test_nem_valid/valid_test.csv'
        sql_output = process_nem12_file(input_file)
        assert sql_output == ["INSERT INTO meter_readings (nmi, timestamp, consumption) VALUES ('NEM1201002', '2005-03-15 00:00:00', 300.000), ('NEM1201002', '2005-03-15 00:30:00', 266.100), ('NEM1201002', '2005-03-15 01:00:00', 191.550), ('NEM1201002', '2005-03-15 01:30:00', 247.800), ('NEM1201002', '2005-03-15 02:00:00', 288.600), ('NEM1201002', '2005-03-15 02:30:00', 280.800), ('NEM1201002', '2005-03-15 03:00:00', 282.450), ('NEM1201002', '2005-03-15 03:30:00', 206.100), ('NEM1201002', '2005-03-15 04:00:00', 204.750), ('NEM1201002', '2005-03-15 04:30:00', 289.500), ('NEM1201002', '2005-03-15 05:00:00', 390.600), ('NEM1201002', '2005-03-15 05:30:00', 360.150), ('NEM1201002', '2005-03-15 06:00:00', 407.700), ('NEM1201002', '2005-03-15 06:30:00', 432.600), ('NEM1201002', '2005-03-15 07:00:00', 435.000), ('NEM1201002', '2005-03-15 07:30:00', 491.850), ('NEM1201002', '2005-03-15 08:00:00', 600.900), ('NEM1201002', '2005-03-15 08:30:00', 541.950), ('NEM1201002', '2005-03-15 09:00:00', 474.600), ('NEM1201002', '2005-03-15 09:30:00', 565.350), ('NEM1201002', '2005-03-15 10:00:00', 548.550), ('NEM1201002', '2005-03-15 10:30:00', 491.850), ('NEM1201002', '2005-03-15 11:00:00', 593.250), ('NEM1201002', '2005-03-15 11:30:00', 602.400), ('NEM1201002', '2005-03-15 12:00:00', 571.350), ('NEM1201002', '2005-03-15 12:30:00', 450.150), ('NEM1201002', '2005-03-15 13:00:00', 509.400), ('NEM1201002', '2005-03-15 13:30:00', 559.950), ('NEM1201002', '2005-03-15 14:00:00', 522.000), ('NEM1201002', '2005-03-15 14:30:00', 520.950), ('NEM1201002', '2005-03-15 15:00:00', 541.200), ('NEM1201002', '2005-03-15 15:30:00', 538.050), ('NEM1201002', '2005-03-15 16:00:00', 484.800), ('NEM1201002', '2005-03-15 16:30:00', 330.900), ('NEM1201002', '2005-03-15 17:00:00', 329.250), ('NEM1201002', '2005-03-15 17:30:00', 331.650), ('NEM1201002', '2005-03-15 18:00:00', 330.750), ('NEM1201002', '2005-03-15 18:30:00', 333.750), ('NEM1201002', '2005-03-15 19:00:00', 335.250), ('NEM1201002', '2005-03-15 19:30:00', 294.150), ('NEM1201002', '2005-03-15 20:00:00', 185.250), ('NEM1201002', '2005-03-15 20:30:00', 184.800), ('NEM1201002', '2005-03-15 21:00:00', 186.450), ('NEM1201002', '2005-03-15 21:30:00', 256.800), ('NEM1201002', '2005-03-15 22:00:00', 329.700), ('NEM1201002', '2005-03-15 22:30:00', 320.100), ('NEM1201002', '2005-03-15 23:00:00', 316.500), ('NEM1201002', '2005-03-15 23:30:00', 321.150);"]

    def test_error_missing_100(self):
        input_file = 'test_nem_invalid/test_missing_100.csv'
        with self.assertRaises(ValueError) as context:
            process_nem12_file(input_file)
        self.assertEqual(str(context.exception), "Unexpected row type on line 1: Actual row: 200. Expected: 100")
                         

    def test_error_missing_200(self):
        input_file = 'test_nem_invalid/NEM12#000000000000021#CNRGYMDP#NEMMCO'
        with self.assertRaises(ValueError) as context:
            process_nem12_file(input_file)
        self.assertEqual(str(context.exception), "Unexpected row type on line 2: Actual row: 300. Expected: 200")

    def test_error_missing_300(self):
        input_file = 'test_nem_invalid/test_missing_300.csv'
        with self.assertRaises(ValueError) as context:
            process_nem12_file(input_file)
        self.assertEqual(str(context.exception), "Unexpected row type on line 3: Actual row: 900. Expected: 300")

    def test_error_missing_900(self):
        input_file = 'test_nem_invalid/NEM12#000000000000025#CNRGYMDP#NEMMCO'
        with self.assertRaises(ValueError) as context:
            process_nem12_file(input_file)
        self.assertEqual(str(context.exception), "Malformed file. Final row should be: 900. Actual row type: 300")

    def test_unexpected_row_number(self):
        input_file = 'test_nem_invalid/test_unexpected_row_type.csv'
        with self.assertRaises(ValueError) as context:
            process_nem12_file(input_file)
        self.assertEqual(str(context.exception), "Unexpected row type on line 4: Actual row: 600. Expected: 200, 300, 400, 500, or 900")

    def test_multiple_900(self):
        input_file = 'test_nem_invalid/test_multiple_900.csv'
        with self.assertRaises(ValueError) as context:
            process_nem12_file(input_file)
        self.assertEqual(str(context.exception), "Malformed file. There is data present after expected end of file on line 7")
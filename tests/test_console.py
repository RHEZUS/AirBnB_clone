import unittest
from unittest.mock import patch
from io import StringIO
from console import HBNBCommand

class TestHBNBCommand(unittest.TestCase):

    @patch('sys.stdout', new_callable=StringIO)
    def assert_stdout(self, cmd_instance, expected_output, mock_stdout):
        with patch('builtins.input', return_value=cmd_instance) as mock_input:
            HBNBCommand().cmdloop()
            self.assertEqual(mock_stdout.getvalue(), expected_output)

    def test_do_quit(self):
        self.assert_stdout('quit', '')
    
    def test_do_EOF(self):
        self.assert_stdout('EOF', '')
    
    def test_emptyline(self):
        self.assert_stdout('\n', '')
    
    def test_do_create(self):
        self.assert_stdout('create BaseModel', '')

    def test_do_show(self):
        self.assert_stdout('show BaseModel 123', '')

    def test_do_destroy(self):
        self.assert_stdout('destroy BaseModel 123', '')

    def test_do_all(self):
        self.assert_stdout('all BaseModel', '')

    def test_do_update(self):
        self.assert_stdout('update BaseModel 123 attr "value"', '')

    def test_do_count(self):
        self.assert_stdout('count BaseModel', '')

    def test_precmd(self):
        self.assert_stdout('BaseModel.show("123")', 'show BaseModel 123\n')



if __name__ == '__main__':
    unittest.main()

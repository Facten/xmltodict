from xmltodict import parse, ParsingInterrupted
import collections
import unittest

class XMLToDictFactenTestCase(unittest.TestCase):

    def test_force_flatten_callable(self):
        xml = """
        <config>
            <flatten>
                <server>
                    <name>server1</name>
                    <os>os1</os>
                </server>
            </flatten>
            <noflatten>
              <server>
                <name>server1</name>
                <os>os1</os>
              </server>
            </noflatten>
        </config>
        """

        def flatten(path, key):
            return key == 'flatten'

        expectedResult = {
            'config': {
                'flatten': 'server1os1',
                'noflatten': {
                    'server': {
                        'name': 'server1',
                        'os': 'os1',
                    },
                },
            }
        }

        self.assertEqual(parse(xml,
                               flatten=flatten,
                               dict_constructor=dict), expectedResult)

